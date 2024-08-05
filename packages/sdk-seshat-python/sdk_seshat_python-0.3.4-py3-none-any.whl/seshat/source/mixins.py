from typing import Optional, Callable

from sqlalchemy import Engine, create_engine

from seshat.transformer.schema import Schema


class SQLMixin:
    filters: Optional[dict]
    table_name: str
    query: Optional[str]
    query_fn: Optional[Callable]
    schema: Schema
    url: str
    limit: Optional[int] = None

    def get_query(self, filters=None, *args, **kwargs):
        query = f"SELECT {self._get_query_columns()} FROM {self.table_name}"
        if getattr(self, "query", None):
            query = self.query
        if getattr(self, "query_fn", None):
            query = self.query_fn(*args, **kwargs)
        return query + self.generate_sql_from_filter(
            {**self.filters, **(filters or {})}
        )

    def _get_query_columns(self):
        columns = "*"
        if self.schema and self.schema.exclusive:
            columns = self.schema.selected_cols_str
        return columns

    @classmethod
    def generate_sql_from_filter(cls, filters):
        sql = ""
        for key, value in filters.items():
            prefix = "AND"
            if not sql:
                prefix = "WHERE"
            if isinstance(value, dict):
                val = value["val"]
                if "type" in value:
                    val = cls.get_converted_value(value["val"], value["type"])
                sql += f" {prefix} {key} {value['op']} {val}"
            else:
                sql += f" {prefix} {key}={value}"
        return sql

    @staticmethod
    def get_converted_value(value, type_):
        if type_ == "str":
            return f"'{value}'"
        return value

    def get_engine(self) -> Engine:
        return create_engine(self.url)

    def get_from_db(self, query):
        with self.get_engine().connect() as conn:
            result = conn.execute(query)
            result = result.fetchmany(self.limit) if self.limit else result.fetchall()
            conn.close()
            return result

    def write_on_db(self, *args, **kwargs):
        with self.get_engine().connect() as conn:
            trans = conn.begin()
            conn.execute(*args, **kwargs)
            trans.commit()
            conn.close()
