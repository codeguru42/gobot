import dataclasses
import json
import pathlib


class DataclassJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for dataclasses.
    """

    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        return super().default(obj)


class PathJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for pathlib.Path objects.
    """

    def default(self, obj):
        if isinstance(obj, pathlib.Path):
            return obj.absolute().as_posix()
        return super().default(obj)


class CustomJSONEncoder(PathJSONEncoder, DataclassJSONEncoder):
    pass
