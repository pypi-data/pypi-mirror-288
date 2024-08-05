from typing import Dict, Callable, List

import pandas as pd
from pandas import DataFrame
from pyspark.sql import DataFrame as PySparkDataFrame, Window
from pyspark.sql import functions as F
from pyspark.sql.functions import array_distinct, array_union, coalesce, array
from pyspark.sql.types import IntegerType, StructType, StructField

from seshat.data_class import SFrame, SPFrame
from seshat.data_class.base import GroupSFrame
from seshat.data_class.pandas import DFrame
from seshat.general import configs
from seshat.transformer import Transformer
from seshat.transformer.schema import Schema, Col
from seshat.utils import pandas_func
from seshat.utils import pyspark_func
from seshat.utils.validation import NumericColumnValidator, TimeStampColumnValidator

SYMBOLS_RECEIVED_COL = "symbols_received"
SYMBOLS_SENT_COL = "symbols_sent"


class SFrameDeriver(Transformer):
    """
    Interface for deriver, specially set handler name to `derive` for all other derivers.
    """

    ONLY_GROUP = False
    HANDLER_NAME = "derive"
    DEFAULT_FRAME = DFrame


class SFrameFromColsDeriver(SFrameDeriver):
    """
    This class is used to create new sframe from specific columns of default sframes.
    If input is contained only one sframe the result is group sframe with two children.

    Parameters
    ----------
    cols : list of str
        List of columns in the default sframe to transformation must apply of them.
    result_col : str
        Column name of result values in address sframe
    """

    ONLY_GROUP = False
    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "address": configs.ADDRESS_SF_KEY,
    }

    def __init__(
        self,
        group_keys=None,
        cols=(configs.FROM_ADDRESS_COL, configs.TO_ADDRESS_COL),
        result_col="extracted_value",
    ):
        super().__init__(group_keys)
        self.cols = cols
        self.result_col = result_col

    def validate(self, sf: SFrame):
        super().validate(sf)
        self._validate_columns(sf, self.default_sf_key, *self.cols)

    def derive_df(self, default: DataFrame, *args, **kwargs) -> Dict[str, DataFrame]:
        new_df = DataFrame()

        new_df[self.result_col] = pd.unique(default[[*self.cols]].values.ravel())
        new_df[self.result_col] = new_df[self.result_col].astype(
            default[self.cols[0]].dtype
        )
        new_df.dropna(subset=[self.result_col], inplace=True)
        return {"default": default, "address": new_df}

    def derive_spf(
        self, default: PySparkDataFrame, *args, **kwargs
    ) -> Dict[str, PySparkDataFrame]:
        temp_spf = default.withColumn(
            self.result_col, F.explode(F.array(*[F.col(c) for c in self.cols]))
        )
        address = temp_spf.select(self.result_col).distinct()
        return {"default": default, "address": address}


class FeatureForAddressDeriver(SFrameDeriver):
    """
    This class is responsible for adding a new column as a new feature to address the sframe
    based on the default sframe.

    Parameters
    ----------
    default_index_col : str
        Columns that group by default will be applied based on this column.
    address_index_col: str
        Column in the address that must be matched to address_col in default sframe.
        Joining default and address sframe using this column and address_col to
        join new column to address.
    result_col : str
        Column name for a new column in address sframe
    agg_func: str
        Function name that aggregation operates based on it. For example count, sum, mean, etc.
    """

    ONLY_GROUP = True
    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "address": configs.ADDRESS_SF_KEY,
    }

    def __init__(
        self,
        value_col,
        group_keys=None,
        default_index_col: str | List[str] = configs.FROM_ADDRESS_COL,
        address_index_col: str | List[str] = configs.ADDRESS_COL,
        result_col="result_col",
        agg_func="mean",
        is_numeric=True,
    ):
        super().__init__(group_keys)

        self.value_col = value_col
        self.default_index_col = default_index_col
        self.address_index_col = address_index_col
        self.result_col = result_col
        self.agg_func = agg_func
        self.is_numeric = is_numeric

    def validate(self, sf: SFrame):
        super().validate(sf)
        self._validate_columns(sf, self.group_keys["default"], self.value_col)
        if isinstance(self.address_index_col, list):
            self._validate_columns(
                sf, self.group_keys["address"], *self.address_index_col
            )
        else:
            self._validate_columns(
                sf, self.group_keys["address"], self.address_index_col
            )

    def derive_df(
        self, default: DataFrame, address: DataFrame, *args, **kwargs
    ) -> Dict[str, DataFrame]:
        if self.is_numeric:
            NumericColumnValidator().validate(default, self.value_col)

        zero_value = pandas_func.get_zero_value(default[self.value_col])
        default.fillna({self.value_col: zero_value}, inplace=True)

        df_agg = (
            default.groupby(self.default_index_col)[self.value_col]
            .agg(self.agg_func)
            .reset_index(name=self.result_col)
        )

        if isinstance(self.default_index_col, str):
            should_dropped = [self.default_index_col]
        else:
            should_dropped = set(self.default_index_col) - set(self.address_index_col)

        address = address.merge(
            df_agg,
            right_on=self.default_index_col,
            left_on=self.address_index_col,
            how="left",
        ).drop(should_dropped, axis=1)

        result_zero_value = pandas_func.get_zero_value(address[self.result_col])
        address.fillna({self.result_col: result_zero_value}, inplace=True)
        return {"default": default, "address": address}

    def derive_spf(
        self, default: PySparkDataFrame, address: PySparkDataFrame, *args, **kwargs
    ) -> Dict[str, PySparkDataFrame]:
        try:
            func = getattr(F, self.agg_func)
        except AttributeError:
            raise AttributeError(
                "agg func %s not available for pyspark dataframe" % self.agg_func
            )
        if self.is_numeric:
            default = NumericColumnValidator().validate(default, self.value_col)

        zero_value = pyspark_func.get_zero_value(default, self.value_col)
        default = default.fillna({self.value_col: zero_value})

        agg_value = (
            default.groupBy(self.default_index_col)
            .agg(func(F.col(self.value_col)).alias(self.result_col))
            .withColumnRenamed(self.default_index_col, self.address_index_col)
        )
        address = address.join(agg_value, on=self.address_index_col, how="left")
        zero_value = pyspark_func.get_zero_value(address, self.result_col)
        address = address.fillna(zero_value, subset=[self.result_col])

        return {"default": default, "address": address}


class OperationOnColsDeriver(SFrameDeriver):
    """
    This deriver does some operation on two different columns of default sframe


    Parameters
    ----------
    cols: list of str
        List of column names that operation must be applied on them
    result_col: str
        Column name of result column
    agg_func: str
        Aggregation function name that operates on specified columns.

    """

    ONLY_GROUP = False
    DEFAULT_GROUP_KEYS = {"default": configs.DEFAULT_SF_KEY}

    def __init__(
        self,
        group_keys=None,
        cols=(configs.AMOUNT_COL,),
        result_col="interacted_value",
        agg_func: str | Callable = "mean",
        is_numeric=False,
    ):
        super().__init__(group_keys)
        self.cols = cols
        self.result_col = result_col
        self.agg_func = agg_func
        self.is_numeric = is_numeric

    def validate(self, sf: SFrame):
        super().validate(sf)
        self._validate_columns(sf, self.default_sf_key, *self.cols)

    def derive_df(self, default: DataFrame, *args, **kwargs):
        if self.is_numeric:
            for col in self.cols:
                default = NumericColumnValidator().validate(default, col)
        if isinstance(self.agg_func, str):
            default[self.result_col] = default[[col for col in self.cols]].agg(
                self.agg_func, axis=1
            )
        else:
            default[self.result_col] = default.apply(self.agg_func, axis=1)

        return {"default": default}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        if self.is_numeric:
            for col in self.cols:
                default = NumericColumnValidator().validate(default, col)
        try:
            func = pyspark_func.func_maps[self.agg_func]
        except KeyError:
            raise KeyError(
                "func %s not available for pyspark dataframe" % self.agg_func
            )
        func_udf = F.udf(func)
        default = default.withColumn(self.result_col, func_udf(*self.cols))
        if self.is_numeric:
            default = NumericColumnValidator().validate(default, self.result_col)
        return {"default": default}


class PercentileTransactionValueDeriver(SFrameDeriver):
    """
    Used to compute percentile of the specific column and insert result as a new column.

    Parameters
    ----------
    value_col: str
        The column that computing percentile will execute on it.
    quantile_probabilities: list of float
        List of quantile probabilities
    result_col: str
        Column name of result column
    """

    def __init__(
        self,
        group_keys=None,
        value_col=configs.AMOUNT_COL,
        result_col="percentile",
        quantile_probabilities=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9),
    ):
        super().__init__(group_keys)

        self.value_col = value_col
        self.result_col = result_col
        self.quantile_probabilities = quantile_probabilities

    def validate(self, sf: SFrame):
        super().validate(sf)
        self._validate_columns(sf, self.default_sf_key, self.value_col)

    def derive_df(self, default: DataFrame, *args, **kwargs) -> Dict[str, DataFrame]:
        default = NumericColumnValidator().validate(default, self.value_col)

        quantiles = default[self.value_col].quantile(
            self.quantile_probabilities, interpolation="linear"
        )
        percentile = pandas_func.PandasPercentile(quantiles)
        default[self.result_col] = default[self.value_col].apply(percentile)
        return {"default": default}

    def derive_spf(
        self, default: PySparkDataFrame, *args, **kwargs
    ) -> Dict[str, PySparkDataFrame]:
        default = NumericColumnValidator().validate(default, self.value_col)

        quantiles = default.approxQuantile(
            self.value_col, self.quantile_probabilities, 0.05
        )

        def get_percentile(value):
            for i, quantile in enumerate(quantiles):
                if value <= quantile:
                    return (i + 1) * 10

            return 100

        get_percentile_udf = F.udf(get_percentile, IntegerType())
        default = default.withColumn(
            self.result_col, get_percentile_udf(F.col(self.value_col))
        )
        return {"default": default}


class InteractedSymbolsToSentenceDeriver(SFrameDeriver):
    """
    This deriver joins symbols that each user in address sframe
    be interacted with it into a new column in string type.
    If already sent symbols or received symbols are calculated as an array of symbol strings
    deriver use them otherwise compute these columns.

    Parameters
    ----------
    symbol_col: str
        Column name of a symbol column in default sframe
    from_address_col: str
        Column name of from address column in default sframe
    to_address_col: str
        Column name of to address column in default sframe
    address_address_col: str
        Column name of address column in address sframe. This column
        consider as a joining condition between default and address sframe
    sent_symbols_col : str
        Column name for the result of sent symbols column in address sframe. If this parameter is set to None
        sent symbols are computed and this value as a new column name.
    received_symbols_col : str
        Column name for the result of received symbols column in address sframe. If this parameter is set to None
        received symbols are computed and this value is a new column name.
    total_symbols_col : str
        Column name for merged two columns sent_symbols and received_symbols.
    result_col: str
        Column name of interacted symbols column
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "address": configs.ADDRESS_SF_KEY,
    }

    def __init__(
        self,
        group_keys=None,
        symbol_col=configs.SYMBOL_COL,
        from_address_col=configs.FROM_ADDRESS_COL,
        to_address_col=configs.TO_ADDRESS_COL,
        address_address_col=configs.ADDRESS_COL,
        sent_symbols_col=None,
        received_symbols_col=None,
        total_symbols_col=None,
        result_col=None,
    ):
        super().__init__(group_keys)

        self.symbol_col = symbol_col
        self.from_address_col = from_address_col
        self.to_address_col = to_address_col
        self.address_address_col = address_address_col
        self.sent_symbols_col = sent_symbols_col
        self.received_symbols_col = received_symbols_col
        self.total_symbols_col = total_symbols_col
        self.result_col = result_col

    def validate(self, sf: SFrame):
        super().validate(sf)
        if self.sent_symbols_col is None:
            self._validate_columns(sf, self.default_sf_key, self.from_address_col)
        if self.received_symbols_col is None:
            self._validate_columns(sf, self.default_sf_key, self.to_address_col)

    def derive_df(
        self, address: DataFrame, default: DataFrame = None, *args, **kwargs
    ) -> Dict[str, DataFrame]:
        if self.sent_symbols_col is None:
            group_sf = GroupSFrame(
                children={
                    "default": DFrame.from_raw(default),
                    "address": DFrame.from_raw(address),
                }
            )

            address = (
                FeatureForAddressDeriver(
                    self.symbol_col,
                    self.group_keys,
                    self.from_address_col,
                    self.address_address_col,
                    SYMBOLS_SENT_COL,
                    "unique",
                    is_numeric=False,
                )(group_sf)
                .get(self.group_keys["address"])
                .to_raw()
            )

        if self.received_symbols_col is None:
            group_sf = GroupSFrame(
                children={
                    "default": DFrame.from_raw(default),
                    "address": DFrame.from_raw(address),
                }
            )
            address = (
                FeatureForAddressDeriver(
                    self.symbol_col,
                    self.group_keys,
                    self.to_address_col,
                    self.address_address_col,
                    SYMBOLS_RECEIVED_COL,
                    "unique",
                    is_numeric=False,
                )(group_sf)
                .get(self.group_keys["address"])
                .to_raw()
            )

        final_sent_col = self.sent_symbols_col or SYMBOLS_SENT_COL
        final_received_col = self.received_symbols_col or SYMBOLS_RECEIVED_COL

        address[final_sent_col] = address[final_sent_col].fillna("").apply(list)
        address[final_received_col] = address[final_received_col].fillna("").apply(list)

        address[self.result_col] = address.apply(
            lambda row: ", ".join(set(row[final_sent_col] + row[final_received_col])),
            axis=1,
        )
        return {"default": default, "address": address}

    def derive_spf(
        self,
        address: PySparkDataFrame,
        default: PySparkDataFrame = None,
        *args,
        **kwargs,
    ) -> Dict[str, PySparkDataFrame]:
        if self.sent_symbols_col is None:
            group_sframe = GroupSFrame(
                children={
                    "default": SPFrame.from_raw(default),
                    "address": SPFrame.from_raw(address),
                }
            )

            address = (
                FeatureForAddressDeriver(
                    self.symbol_col,
                    self.group_keys,
                    self.from_address_col,
                    self.address_address_col,
                    SYMBOLS_SENT_COL,
                    "collect_set",
                    is_numeric=False,
                )(group_sframe)
                .get(self.group_keys["address"])
                .to_raw()
            )

        if self.received_symbols_col is None:
            group_sframe = GroupSFrame(
                children={
                    "default": SPFrame.from_raw(default),
                    "address": SPFrame.from_raw(address),
                }
            )
            address = (
                FeatureForAddressDeriver(
                    self.symbol_col,
                    self.group_keys,
                    self.to_address_col,
                    self.address_address_col,
                    SYMBOLS_RECEIVED_COL,
                    "collect_set",
                    is_numeric=False,
                )(group_sframe)
                .get(self.group_keys["address"])
                .to_raw()
            )
        final_sent_col = self.sent_symbols_col or SYMBOLS_SENT_COL
        final_received_col = self.received_symbols_col or SYMBOLS_RECEIVED_COL

        address = address.withColumn(
            final_sent_col, coalesce(final_received_col, array())
        )

        address = address.withColumn(
            self.result_col,
            F.concat_ws(
                ", ",
                array_distinct(array_union(final_received_col, final_sent_col)),
            ),
        )

        return {"default": default, "address": address}


class SenderReceiverTokensDeriver(SFrameDeriver):
    """
    This will find tokens that in at least one record be from_address or to_address.
    The result will save in another sf.
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "other": configs.OTHER_SF_KEY,
    }

    def __init__(
        self,
        group_keys=None,
        address_cols=(configs.FROM_ADDRESS_COL, configs.TO_ADDRESS_COL),
        contract_address_col=configs.CONTRACT_ADDRESS_COL,
        result_col=configs.CONTRACT_ADDRESS_COL,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.address_cols = address_cols
        self.contract_address = contract_address_col
        self.result_col = result_col

    def derive_df(self, default: DataFrame, *args, **kwargs):
        all_tokens = set(default[self.contract_address].tolist())
        addresses = set()
        for address_col in self.address_cols:
            addresses |= set(default[address_col].tolist())

        sender_receiver_tokens = list(addresses & all_tokens)
        other = pd.DataFrame(data={self.result_col: sender_receiver_tokens})
        return {"default": default, "other": other}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        all_tokens = set(
            default.select(self.contract_address).rdd.flatMap(lambda x: x).collect()
        )
        addresses = set()
        for address_col in self.address_cols:
            addresses |= set(
                default.select(address_col).rdd.flatMap(lambda x: x).collect()
            )

        sender_receiver_tokens = list(addresses & all_tokens)
        schema = StructType(
            [
                StructField(
                    self.result_col, default.schema[self.contract_address].dataType
                )
            ]
        )

        data = [{self.result_col: addr} for addr in sender_receiver_tokens]
        other = SPFrame.get_spark().createDataFrame(schema=schema, data=data)
        return {"default": default, "other": other}


class TokenLastPriceDeriver(SFrameDeriver):
    """
    This deriver finds the last usd unit price for every token if there is not zero and no null amount USD.
    To find the last price deriver needs to sort values based on the timestamp column. If dtype of this column is something
    except for valid datetime type, the column values will be converted to the proper type.
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "result": configs.TOKEN_PRICE_SF_KEY,
    }

    def __init__(
        self,
        contract_address_col=configs.CONTRACT_ADDRESS_COL,
        timestamp_col=configs.BLOCK_TIMESTAMP_COL,
        amount_col=configs.AMOUNT_COL,
        amount_usd_col=configs.AMOUNT_USD_COL,
        result_unit_price_col=configs.TOKEN_PRICE_COL,
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.contract_address_col = contract_address_col
        self.timestamp_col = timestamp_col
        self.amount_col = amount_col
        self.amount_usd_col = amount_usd_col
        self.result_unit_price_col = result_unit_price_col

    def derive_df(self, default: pd.DataFrame, *args, **kwargs):
        default = TimeStampColumnValidator().validate(default, self.timestamp_col)
        price = default[default[self.amount_usd_col] != 0]
        price = price.sort_values(self.timestamp_col, ascending=False)
        price = price.dropna(subset=[self.amount_usd_col])
        last_price = (
            price.groupby([self.contract_address_col]).head(1).reset_index(drop=True)
        ).reset_index(drop=True)

        last_price[self.result_unit_price_col] = (
            last_price["amount_usd"] / last_price["amount"]
        )
        last_price = last_price[[self.contract_address_col, self.result_unit_price_col]]
        return {"default": default, "result": last_price}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        default = TimeStampColumnValidator().validate(default, self.timestamp_col)
        price: PySparkDataFrame = default.filter(
            F.col(self.amount_usd_col) != 0
        ).select(
            self.timestamp_col,
            self.contract_address_col,
            self.amount_usd_col,
            self.amount_col,
        )
        price = price.dropna(subset=[self.amount_usd_col])
        window = Window.partitionBy(self.contract_address_col).orderBy(
            F.col(self.timestamp_col).desc()
        )
        last_price = (
            price.withColumn("_row_number", F.row_number().over(window))
            .filter(F.col("_row_number") == 1)
            .drop("_row_number")
        )
        last_price = last_price.withColumn(
            self.result_unit_price_col,
            last_price[self.amount_usd_col] / last_price[self.amount_col],
        )
        last_price = last_price.select(
            self.contract_address_col, self.result_unit_price_col
        )
        return {"default": default, "result": last_price}


class ProfitLossDeriver(SFrameDeriver):
    """
    Find the profit and loss of addresses with this logic:
    Sum over all buying and selling amount & amount USD, then find the difference between
    buy & sell amount for each address & token. By using the token price sframe the current amount
    of address property will be calculated. The difference between USD that address paid and
    the current amount is the PL for that address & token.

    Parameters
    ----------
    from_address_col : str
        The name of from address column in default sf.
    to_address_col : str
        The name of to address column in default sf.
    contract_address_col : str
        The name of contract address column in default sf.
    timestamp_col : str
        The name of block_timestamp column in default sf.
    amount_col : str
        The name of amount column in default sf.
    amount_usd_col : str
        The name of USD amount column of transactions in default sf.
    token_price_col : str
        The name of price column in price sf.
    address_col : str
        The name of address column in result sf.
    net_amount_col : str
        The name of net amount column in result sf.
    net_amount_usd_col : str
        The name of USD net amount column in result sf.
    current_amount_usd_col : str
        The name of USD amount column in result sf.
    pl_col : str
        The name of profit & loss column in result sf.
    group_keys
        Group keys for the parent Transformer class.
    *args
        Additional positional arguments.
    **kwargs
        Additional keyword arguments.
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.DEFAULT_SF_KEY,
        "price": configs.TOKEN_PRICE_SF_KEY,
        "result": configs.PROFIT_LOSS_SF_KEY,
    }

    def __init__(
        self,
        from_address_col=configs.FROM_ADDRESS_COL,
        to_address_col=configs.TO_ADDRESS_COL,
        contract_address_col=configs.CONTRACT_ADDRESS_COL,
        timestamp_col=configs.BLOCK_TIMESTAMP_COL,
        amount_col=configs.AMOUNT_COL,
        amount_usd_col=configs.AMOUNT_USD_COL,
        token_price_col=configs.TOKEN_PRICE_COL,
        address_col=configs.ADDRESS_COL,
        net_amount_col="net_amount",
        net_amount_usd_col="net_amount_usd",
        current_amount_usd_col="current_amount_usd",
        pl_col="pl",
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.from_address_col = from_address_col
        self.to_address_col = to_address_col
        self.contract_address_col = contract_address_col
        self.timestamp_col = timestamp_col
        self.amount_col = amount_col
        self.amount_usd_col = amount_usd_col
        self.token_price_col = token_price_col
        self.address_col = address_col
        self.net_amount_col = net_amount_col
        self.net_amount_usd_col = net_amount_usd_col
        self.current_amount_usd_col = current_amount_usd_col
        self.pl_col = pl_col

    def validate(self, sf: SFrame):
        super().validate(sf)
        self._validate_columns(
            sf,
            "default",
            self.from_address_col,
            self.to_address_col,
            self.contract_address_col,
            self.timestamp_col,
            self.amount_col,
            self.amount_usd_col,
        )

    def derive_df(self, default: pd.DataFrame, price: pd.DataFrame, *args, **kwargs):
        clean_default = default[default[self.amount_col] != 0]
        selling = (
            clean_default.groupby([self.from_address_col, self.contract_address_col])
            .agg({self.amount_col: "sum", self.amount_usd_col: "sum"})
            .reset_index()
            .rename(
                columns={
                    self.from_address_col: self.address_col,
                    self.amount_col: "sell_amount",
                    self.amount_usd_col: "sell_amount_usd",
                }
            )
        )
        buying = (
            clean_default.groupby([self.to_address_col, self.contract_address_col])
            .agg({self.amount_col: "sum", self.amount_usd_col: "sum"})
            .reset_index()
            .rename(
                columns={
                    self.to_address_col: self.address_col,
                    self.amount_col: "buy_amount",
                    self.amount_usd_col: "buy_amount_usd",
                }
            )
        )
        investing = pd.merge(
            selling, buying, on=[self.address_col, self.contract_address_col]
        )
        del selling
        del buying
        investing[self.net_amount_col] = (
            investing["buy_amount"] - investing["sell_amount"]
        )
        investing[self.net_amount_usd_col] = (
            investing["buy_amount_usd"] - investing["sell_amount_usd"]
        )
        investing = investing[
            [
                self.address_col,
                self.contract_address_col,
                self.net_amount_col,
                self.net_amount_usd_col,
            ]
        ]
        investing = investing[investing[self.net_amount_col] >= 0]

        investing = investing.merge(price, on=self.contract_address_col)
        investing[self.current_amount_usd_col] = (
            investing[self.net_amount_col] * investing[self.token_price_col]
        )

        investing[self.pl_col] = (
            investing[self.current_amount_usd_col] - investing[self.net_amount_usd_col]
        )
        investing = investing.drop(columns=[self.token_price_col])

        return {"default": default, "price": price, "result": investing}

    def derive_spf(
        self, default: PySparkDataFrame, price: PySparkDataFrame, *args, **kwargs
    ):
        clean_default = default.filter(F.col(self.amount_col) != 0)
        selling = (
            clean_default.groupBy([self.from_address_col, self.contract_address_col])
            .agg({self.amount_col: "sum", self.amount_usd_col: "sum"})
            .withColumnRenamed(self.from_address_col, self.address_col)
            .withColumnRenamed(f"sum({self.amount_col})", "sell_amount")
            .withColumnRenamed(f"sum({self.amount_usd_col})", "sell_amount_usd")
        )

        buying = (
            clean_default.groupBy([self.to_address_col, self.contract_address_col])
            .agg({self.amount_col: "sum", self.amount_usd_col: "sum"})
            .withColumnRenamed(self.to_address_col, self.address_col)
            .withColumnRenamed(f"sum({self.amount_col})", "buy_amount")
            .withColumnRenamed(f"sum({self.amount_usd_col})", "buy_amount_usd")
        )

        investing = selling.join(
            buying, on=[self.address_col, self.contract_address_col]
        )

        investing = investing.withColumn(
            self.net_amount_col, investing["buy_amount"] - investing["sell_amount"]
        ).withColumn(
            self.net_amount_usd_col,
            investing["buy_amount_usd"] - investing["sell_amount_usd"],
        )

        investing = investing.select(
            self.address_col,
            self.contract_address_col,
            self.net_amount_col,
            self.net_amount_usd_col,
        )
        investing = investing.filter(F.col(self.net_amount_col) >= 0)
        investing = investing.join(price, on=self.contract_address_col)

        investing = Schema(
            exclusive=False,
            cols=[
                Col(self.net_amount_col, dtype="double"),
                Col(self.net_amount_usd_col, dtype="double"),
                Col(self.token_price_col, dtype="double"),
            ],
        )(SPFrame.from_raw(investing)).to_raw()

        investing = investing.withColumn(
            self.current_amount_usd_col,
            investing[self.net_amount_col] * investing[self.token_price_col],
        )
        investing = investing.withColumn(
            self.pl_col,
            investing[self.current_amount_usd_col] - investing[self.net_amount_usd_col],
        )
        investing = investing.drop(self.token_price_col)
        return {"default": default, "price": price, "result": investing}


class FractionDeriver(SFrameDeriver):
    """
    Find fraction that each rows have from sum of all calculation columns values.

    Parameters
    ----------
    calculation_col : str
        The column that every value of it divide by sum of it over all rows
    result_fraction_col : str
        The column name for result fraction values
    group_keys
        Group keys for the parent Transformer class.
    *args
        Additional positional arguments.
    **kwargs
        Additional keyword arguments.
    """

    DEFAULT_GROUP_KEYS = {
        "default": configs.TOKEN_SF_KEY,
    }

    def __init__(
        self,
        calculation_col: str,
        result_fraction_col: str = "weight",
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.calculation_col = calculation_col
        self.result_fraction_col = result_fraction_col

    def validate(self, sf: SFrame):
        super().validate(sf)
        self._validate_columns(sf, self.default_sf_key, self.calculation_col)

    def derive_df(self, default: pd.DataFrame, *args, **kwargs):
        default = NumericColumnValidator().validate(default, self.calculation_col)
        default[self.calculation_col] = default[self.calculation_col].fillna(0)
        total_value = default[self.calculation_col].sum()

        default[self.result_fraction_col] = default[self.calculation_col] / total_value
        return {"default": default}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        default = NumericColumnValidator().validate(default, self.calculation_col)
        default = default.fillna(0, subset=[self.calculation_col])
        total_value = default.agg(F.sum(self.calculation_col)).collect()[0][0]
        default = default.withColumn(
            self.result_fraction_col, F.col(self.calculation_col) / F.lit(total_value)
        )
        return {"default": default}


class ChangingOverTimeDeriver(SFrameDeriver):
    DEFAULT_GROUP_KEYS = {"default": configs.DEFAULT_SF_KEY, "result": "result"}

    def __init__(
        self,
        index_col: str,
        value_col: str,
        result_changing_col: str,
        timestamp_col: str = configs.BLOCK_TIMESTAMP_COL,
        group_keys=None,
        *args,
        **kwargs,
    ):
        super().__init__(group_keys, *args, **kwargs)
        self.index_col = index_col
        self.value_col = value_col
        self.result_changing_col = result_changing_col
        self.timestamp_col = timestamp_col

    def derive_df(self, default: pd.DataFrame, *args, **kwargs):
        default = TimeStampColumnValidator().validate(default, self.timestamp_col)

        sorted_default = default.sort_values(self.timestamp_col, ascending=False)
        sorted_default = sorted_default[
            [self.index_col, self.value_col, self.timestamp_col]
        ]
        top = (
            sorted_default.groupby(self.index_col)
            .first()
            .reset_index()
            .rename(columns={self.value_col: "top"})
        )
        sorted_default = sorted_default.sort_values(self.timestamp_col)
        bottom = (
            sorted_default.groupby(self.index_col)
            .first()
            .reset_index()
            .rename(columns={self.value_col: "bottom"})
        )

        result = pd.merge(top, bottom, on=self.index_col)
        result[self.result_changing_col] = (result["top"] + result["bottom"]) / result[
            "bottom"
        ]

        result = result[[self.index_col, self.result_changing_col]]

        result = result.dropna(subset=[self.result_changing_col])

        return {"default": default, "result": result}

    def derive_spf(self, default: PySparkDataFrame, *args, **kwargs):
        default = TimeStampColumnValidator().validate(default, self.timestamp_col)
        sorted_default = default.sort(F.desc(self.timestamp_col)).select(
            self.index_col, self.value_col, self.timestamp_col
        )
        top = sorted_default.groupBy(self.index_col).agg(
            F.first(self.value_col).alias("top")
        )
        sorted_default = default.orderBy(self.timestamp_col).select(
            self.index_col, self.value_col, self.timestamp_col
        )
        bottom = sorted_default.groupBy(self.index_col).agg(
            F.first(self.value_col).alias("bottom")
        )

        result = top.join(bottom, on=self.index_col)
        result = result.withColumn(
            self.result_changing_col, (F.col("top") + F.col("bottom")) / F.col("bottom")
        )
        result = result.select(self.index_col, self.result_changing_col)

        result = result.dropna(subset=[self.result_changing_col])
        return {"default": default, "result": result}
