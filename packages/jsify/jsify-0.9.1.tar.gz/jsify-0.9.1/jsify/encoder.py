"""
The `encoder` module provides custom JSON serialization functionality specifically designed to handle `JsonObject`
instances. This module extends Python's built-in `json` module to ensure that `JsonObject` instances are correctly
converted into their original dictionary representation during the serialization process.

The module features the `JsonObjectEncoder` class, which overrides the default JSON encoding behavior to accommodate
`JsonObject` instances. Additionally, it provides custom `dump` and `dumps` functions that leverage this encoder,
allowing seamless integration with standard JSON serialization workflows.

You must import this module if you want to use serialization done by the `json` module.
"""

import json
from typing import Any

from .jsify import Undefined, unjsify
from .jsify import JsonObject


class JsonObjectEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for `JsonObject` instances.

    This encoder converts `JsonObject` instances to their original dictionary representation
    for JSON serialization. It also provides an option to omit fields with the `Undefined` value
    during serialization.

    Parameters
    ----------
    omit_undefined : bool
        If True, fields with the `Undefined` value are omitted from the serialized output.
    *args : tuple
        Additional positional arguments passed to `JSONEncoder`.
    **kwargs : dict
        Additional keyword arguments passed to `JSONEncoder`.

    Methods
    -------
    iterencode(o: Any, _one_shot: bool = False) -> Iterator[str]
        Encodes the object into a JSON string, applying custom logic to handle `JsonObject`
        instances and optionally omitting `Undefined` values.
    default(o: Any) -> Any
        Overrides the default method of `JSONEncoder` to handle `JsonObject` instances and
        `Undefined` values.
    """

    def __init__(self, omit_undefined, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.omit_undefined = omit_undefined

    def iterencode(self, o, _one_shot=False):
        if isinstance(o, JsonObject):
            o = unjsify(o)
        if self.omit_undefined:
            if isinstance(o, tuple):
                o = o.__class__(value for value in o if value is not Undefined)
            elif isinstance(o, list):
                o = o.__class__(value for value in o if value is not Undefined)
            elif isinstance(o, dict):
                o = o.__class__({key: value for key, value in o.items() if value is not Undefined})
        return super().iterencode(o, _one_shot)

    def default(self, o: Any) -> Any:
        if o is Undefined:
            return None
        elif isinstance(o, JsonObject):
            return o.__orig__
        else:
            return super().default(o)


_orig_dump = json.dump
_orig_dumps = json.dumps


def dumps(o, omit_undefined=True, **kwargs):
    """
    Serialize `o` to a JSON formatted `str` using `JsonObjectEncoder`.

    This function wraps `json.dumps`, providing custom serialization for `JsonObject` instances
    and optionally omitting fields with the `Undefined` value.

    Parameters
    ----------
    o : Any
        The object to serialize.
    omit_undefined : bool, optional
        If True, fields with the `Undefined` value are omitted from the serialized output. Default is True.
    **kwargs : dict
        Additional keyword arguments passed to `json.dumps`.

    Returns
    -------
    str
        The JSON formatted string.
    """
    return _orig_dumps(o, cls=JsonObjectEncoder, omit_undefined=omit_undefined, **kwargs)


def dump(o, fp, omit_undefined=True, **kwargs):
    """
    Serialize `o` as a JSON formatted stream to `fp` using `JsonObjectEncoder`.

    This function wraps `json.dump`, providing custom serialization for `JsonObject` instances
    and optionally omitting fields with the `Undefined` value.

    Parameters
    ----------
    o : Any
        The object to serialize.
    fp : file-like object
        The file-like object to which the JSON formatted stream is written.
    omit_undefined : bool, optional
        If True, fields with the `Undefined` value are omitted from the serialized output. Default is True.
    **kwargs : dict
        Additional keyword arguments passed to `json.dump`.

    Returns
    -------
    None
    """
    return _orig_dump(o, fp, cls=JsonObjectEncoder, omit_undefined=omit_undefined, **kwargs)


# Override the default json.dump and json.dumps with the custom implementations
json.dump = dump
json.dumps = dumps

# Set the default method of JSONEncoder to handle JsonObject instances
json.JSONEncoder.default = JsonObjectEncoder.default
