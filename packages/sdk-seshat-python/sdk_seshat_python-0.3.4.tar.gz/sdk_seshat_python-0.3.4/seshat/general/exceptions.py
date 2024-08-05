import typing


class ColDoesNotExistError(Exception):
    def __init__(self, cols: typing.Iterable):
        message = f"columns {' - '.join(cols)} does not exist in dataframe"
        super().__init__(message)


class OnlyGroupRequiredError(Exception):
    def __init__(self):
        messages = "Group SFrame is required for data"
        super().__init__(messages)


class ColIdNotSpecifiedError(Exception):
    def __init__(self):
        message = "Column ID must be specified in schema"
        super().__init__(message)


class SFrameDoesNotExistError(Exception):
    def __init__(self, group_name, key):
        message = "key %s not exists in %s" % (key, group_name)
        super().__init__(message)


class UnknownDataClassError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidModeError(Exception):
    def __init__(self):
        from seshat.data_class import SF_MAP

        message = "Invalid mode. Mode can only be of these items: %s" % " - ".join(
            SF_MAP
        )
        super().__init__(message)


class InvalidArgumentsError(Exception):
    def __init__(self, message):
        super().__init__(message)


class EmptyDataError(Exception):
    def __init__(self, message=None):
        message = message or "Empty data cannot be processed"
        super().__init__(message)


class SchemaNeededForTableCreationError(Exception):
    def __init__(self):
        message = "Schema needed for table creation"
        super().__init__(message)


class DataBaseNotSupportedError(Exception):
    def __init__(self, message):
        super().__init__(message)
