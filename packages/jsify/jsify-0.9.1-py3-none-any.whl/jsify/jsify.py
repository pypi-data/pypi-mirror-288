"""
The `jsify` module provides a set of classes and functions designed to wrap standard Python data structures
(such as dictionaries, lists, and tuples) with JSON-like behavior. These wrapped objects, known as `JsonObject`,
`JsonDict`, `JsonList`, and `JsonTuple`, allow for attribute-style access, dynamic nesting, and additional
functionality that is commonly required when working with JSON data.
The core component of this module is the `JsonObject` class, which provides a flexible and dynamic interface for
accessing and manipulating underlying data. The `JsonDict`, `JsonList`, and `JsonTuple` classes extend `JsonObject`
to offer more specific behaviors for dictionaries, lists, and tuples, respectively.
Additionally, the module offers a series of utility functions such as `jsify` for converting standard Python objects
into their JSON-like counterparts, and `unjsify` for reversing this transformation.
"""
from copy import copy, deepcopy
from typing import Iterable, Iterator

from .exceptions import AnyError
from .undefined import Undefined


class JsonObject:
    """
    The `JsonObject` class is designed to provide convenient access to object properties using dot notation instead of
    square brackets, enhancing code readability and ease of use. It acts as a wrapper around original objects,
    preserving their data without duplication or alteration. This wrapper supports nested access to properties,
    allowing deeper navigation into the original data using dot notation. Essentially, `JsonObject` facilitates
    intuitive and simplified interaction with JSON-like objects, while maintaining the integrity and structure of the
    original data.
    """

    def __init__(self, o):
        """
        Initialize the JsonObject with the given original object.

        :param o: The original dictionary or object to wrap.
        :type o: tuple or dict or list or object
        """
        object.__setattr__(self, "__orig__", o)

    def __getitem__(self, item):
        """
        Get an item from the original object, returning Undefined if the item does not exist.

        :param item: The item key to retrieve.
        :type item: Any
        :return: The value associated with the item key or Undefined if not present.
        :rtype: Any or Undefined
        """
        try:
            return jsify(self.__orig__.__getitem__(item))
        except (Exception,):
            return Undefined

    def __setitem__(self, item, value):
        """
        Set an item in the original object.

        :param item: The item key to set.
        :type item: str
        :param value: The value to set.
        :type value: Any
        """
        self.__orig__.__setitem__(item, value)

    def __delitem__(self, item):
        """
        Delete an item from the original object.

        :param item: The item key to delete.
        :type item: str
        """
        self.__orig__.__delitem__(item)

    __getattr__ = __getitem__  # Set similar behaviour to following methods
    __setattr__ = __setitem__
    __delattr__ = __delitem__

    def __repr__(self):
        """
        Return the string representation of the original object.

        :return: The string representation of the original object.
        :rtype: str
        """
        return self.__orig__.__repr__()

    def __contains__(self, item):
        """
        Check if the original object contains the given item.

        :param item: The item key to check.
        :type item: str
        :return: True if the item is in the original object, False otherwise.
        :rtype: bool
        """
        return self.__orig__.__contains__(unjsify(item))

    def __len__(self):
        """
        Return the length of the original object.

        :return: The length of the original object.
        :rtype: int
        """
        return self.__orig__.__len__()

    def __int__(self):
        """
        Return the integer representation of the original object.

        :return: The integer representation of the original object.
        :rtype: int
        """
        return self.__orig__.__int__()

    def __float__(self):
        """
        Return the float representation of the original object.

        :return: The float representation of the original object.
        :rtype: float
        """
        return self.__orig__.__float__()

    def __complex__(self):
        """
        Return the complex number representation of the original object.

        :return: The complex number representation of the original object.
        :rtype: complex
        """
        return self.__orig__.__complex__()

    def __oct__(self):
        """
        Return the octal string representation of the original object.

        :return: The octal string representation of the original object.
        :rtype: str
        """
        return self.__orig__.__oct__()

    def __hex__(self):
        """
        Return the hexadecimal string representation of the original object.

        :return: The hexadecimal string representation of the original object.
        :rtype: str
        """
        return self.__orig__.__hex__()

    def __index__(self):
        """
        Return the index representation of the original object.

        :return: The index representation of the original object.
        :rtype: int
        """
        return self.__orig__.__index__()

    def __trunc__(self):
        """
        Return the truncated value of the original object.

        :return: The truncated value of the original object.
        :rtype: int
        """
        return self.__orig__.__trunc__()

    def __str__(self):
        """
        Return the string representation of the original object.

        :return: The string representation of the original object.
        :rtype: str
        """
        return self.__orig__.__str__()

    def __unicode__(self):
        """
        Return the Unicode string representation of the original object.

        :return: The Unicode string representation of the original object.
        :rtype: str
        """
        return self.__orig__.__unicode__()

    def __format__(self, format_string):
        """
        Return the formatted string representation of the original object.

        :param format_string: The format string.
        :type format_string: str
        :return: The formatted string representation of the original object.
        :rtype: str
        """
        return self.__orig__.__format__(format_string)

    def __hash__(self):
        """
        Return the hash value of the original object.

        :return: The hash value of the original object.
        :rtype: int
        """
        return self.__orig__.__hash__()

    def __nonzero__(self):
        """
        Return the boolean value of the original object.

        :return: True if the original object is considered True, False otherwise.
        :rtype: bool
        """
        return self.__orig__.__nonzero__()

    def __sizeof__(self):
        """
        Return the size of the original object in memory.

        :return: The size of the original object in memory.
        :rtype: int
        """
        return self.__orig__.__sizeof__()

    def __pos__(self):
        """
        Return the positive value of the original object.

        :return: The positive value of the original object.
        :rtype: Any
        """
        return self.__orig__.__pos__()

    def __neg__(self):
        """
        Return the negative value of the original object.

        :return: The negative value of the original object.
        :rtype: Any
        """
        return self.__orig__.__neg__()

    def __abs__(self):
        """
        Return the absolute value of the original object.

        :return: The absolute value of the original object.
        :rtype: Any
        """
        return self.__orig__.__abs__()

    def __invert__(self):
        """
        Return the inverted value of the original object.

        :return: The inverted value of the original object.
        :rtype: Any
        """
        return self.__orig__.__invert__()

    def __round__(self):
        """
        Return the rounded value of the original object.

        :return: The rounded value of the original object.
        :rtype: int
        """
        return self.__orig__.__round__()

    def __floor__(self):
        """
        Return the floored value of the original object.

        :return: The floored value of the original object.
        :rtype: int
        """
        return self.__orig__.__floor__()

    def __ceil__(self):
        """
        Return the ceiling value of the original object.

        :return: The ceiling value of the original object.
        :rtype: int
        """
        return self.__orig__.__ceil__()

    def __or__(self, other):
        """
        Perform a bitwise OR operation with the original object and another value.

        :param other: The other value to perform the operation with.
        :type other: Any
        :return: The result of the bitwise OR operation.
        :rtype: Any
        """
        return self.__orig__.__or__(unjsify(other))

    def __and__(self, other):
        """
        Perform a bitwise AND operation with the original object and another value.

        :param other: The other value to perform the operation with.
        :type other: Any
        :return: The result of the bitwise AND operation.
        :rtype: Any
        """
        return self.__orig__.__and__(unjsify(other))

    def __add__(self, other):
        """
        Perform an addition operation with the original object and another value.

        :param other: The other value to perform the operation with.
        :type other: Any
        :return: The result of the addition operation.
        :rtype: Any
        """
        return self.__orig__.__add__(unjsify(other))

    def __sub__(self, other):
        """
        Perform a subtraction operation with the original object and another value.

        :param other: The other value to perform the operation with.
        :type other: Any
        :return: The result of the subtraction operation.
        :rtype: Any
        """
        return self.__orig__.__sub__(unjsify(other))

    def __mul__(self, other):
        """
        Perform a multiplication operation with the original object and another value.

        :param other: The other value to perform the operation with.
        :type other: Any
        :return: The result of the multiplication operation.
        :rtype: Any
        """
        return self.__orig__.__mul__(unjsify(other))

    def __floordiv__(self, other):
        """
        Perform a floor division operation with the original object and another value.

        :param other: The other value to perform the operation with.
        :type other: Any
        :return: The result of the floor division operation.
        :rtype: Any
        """
        return self.__orig__.__floordiv__(unjsify(other))

    def __truediv__(self, other):
        """
        Perform a true division operation with the original object and another value.

        :param other: The other value to perform the operation with.
        :type other: Any
        :return: The result of the true division operation.
        :rtype: Any
        """
        return self.__orig__.__truediv__(unjsify(other))

    def __mod__(self, other):
        """
        Perform a modulus operation with the original object and another value.

        :param other: The other value to perform the operation with.
        :type other: Any
        :return: The result of the modulus operation.
        :rtype: Any
        """
        return self.__orig__.__mod__(unjsify(other))

    def __pow__(self, other):
        """
        Perform a power operation with the original object and another value.

        :param other: The other value to perform the operation with.
        :type other: Any
        :return: The result of the power operation.
        :rtype: Any
        """
        return self.__orig__.__pow__(unjsify(other))

    def __lt__(self, other):
        """
        Perform a less-than comparison with the original object and another value.

        :param other: The other value to compare with.
        :type other: Any
        :return: The result of the less-than comparison.
        :rtype: bool
        """
        return self.__orig__.__lt__(unjsify(other))

    def __le__(self, other):
        """
        Perform a less-than-or-equal-to comparison with the original object and another value.

        :param other: The other value to compare with.
        :type other: Any
        :return: The result of the less-than-or-equal-to comparison.
        :rtype: bool
        """
        return self.__orig__.__le__(unjsify(other))

    def __eq__(self, other):
        """
        Perform an equality comparison with the original object and another value.

        :param other: The other value to compare with.
        :type other: Any
        :return: The result of the equality comparison.
        :rtype: bool
        """
        return self.__orig__.__eq__(unjsify(other))

    def __ne__(self, other):
        """
        Perform an inequality comparison with the original object and another value.

        :param other: The other value to compare with.
        :type other: Any
        :return: The result of the inequality comparison.
        :rtype: bool
        """
        return self.__orig__.__ne__(unjsify(other))

    def __ge__(self, other):
        """
        Perform a greater-than-or-equal-to comparison with the original object and another value.

        :param other: The other value to compare with.
        :type other: Any
        :return: The result of the greater-than-or-equal-to comparison.
        :rtype: bool
        """
        return self.__orig__.__ge__(unjsify(other))

    def __gt__(self, other):
        """
        Perform a greater-than comparison with the original object and another value.

        :param other: The other value to compare with.
        :type other: Any
        :return: The result of the greater-than comparison.
        :rtype: bool
        """
        return self.__orig__.__gt__(unjsify(other))

    def __getstate__(self):
        """
        Get the state of the JsonObject for serialization.

        :return: The state of the JsonObject.
        :rtype: dict
        """
        return dict(__orig__=self.__orig__)

    def __setstate__(self, state):
        """
        Set the state of the JsonObject during deserialization.

        :param state: The state to set.
        :type state: dict
        """
        object.__setattr__(self, "__orig__", state["__orig__"])

    def __dir__(self):
        """
        Return the list of attributes of the original object.

        :return: The list of attributes of the original object.
        :rtype: list
        """
        return self.__orig__

    @property
    def __dict__(self):
        """
        Return the dictionary representation of the original object.

        :return: The dictionary representation of the original object.
        :rtype: dict
        """
        return {key: jsify(value) for key, value in self.__orig__.items()}

    def __iter__(self):
        """
        Return an iterator for the JsonObject.

        :return: An iterator for the JsonObject.
        :rtype: iterator
        """
        return JsonIterator(self)

    def __deepcopy__(self, memo):
        return deepcopy(self.__orig__, memo=memo)


class JsonTuple(JsonObject):
    """
    A JSON-like tuple object that extends JsonObject and provides tuple-specific methods.

    :param o: The original tuple or object to wrap.
    :type o: tuple or object
    :param args: Additional elements to include in the tuple.
    """

    def __init__(self, o, *args):
        """
        Initialize the JsonTuple with the given original object and additional elements.

        :param o: The original tuple or object to wrap.
        :type o: tuple or object
        :param args: Additional elements to include in the tuple.
        :type args: Any
        """
        super().__init__(o)
        for arg in args:
            self.append(arg)

    def count(self, value):
        """
        Return the number of occurrences of value in the tuple.

        :param value: The value to count in the tuple.
        :type value: Any
        :return: The number of occurrences of value.
        :rtype: int
        """
        return self.__orig__.count(unjsify(value))

    def __getitem__(self, item, *args, **kwargs):
        """
        Get an item from the tuple by index or slice, returning Undefined if the item does not exist.

        :param item: The index or slice to retrieve.
        :type item: int or slice
        :return: The value at the specified index or slice, or Undefined if not present.
        :rtype: Any or Undefined
        """
        try:
            return jsify(
                self.__orig__.__getitem__(
                    int(item) if not isinstance(item, slice) else item, *args, **kwargs
                )
            )
        except (Exception, TypeError):
            return Undefined

    __getattr__ = __getitem__

    def index(self, value):
        """
        Return the first index of value in the tuple.

        Raises ValueError if the value is not present.

        :param value: The value to find in the tuple.
        :type value: Any
        :return: The first index of the value.
        :rtype: int
        :raises ValueError: If the value is not present.
        """
        return self.__orig__.index(unjsify(value))

    def copy(self, deep=False):
        """
        Create a shallow or deep copy of the tuple.

        :param deep: True if the object should be deep copied, False otherwise.
        :type deep: bool
        :return: A copy of the tuple.
        :rtype: JsonTuple
        """
        return jsify(copy(self.__orig__) if not deep else deepcopy(self.__orig__))

    @property
    def __dict__(self):
        """
        Return the dictionary representation of the tuple.

        :return: The dictionary representation of the tuple.
        :rtype: dict
        """
        return {f"{key}": jsify(value) for key, value in enumerate(self.__orig__)}

    def __contains__(self, item):
        """
        Check if an index is within the bounds of the tuple.

        :param item: The index to check.
        :type item: int
        :return: True if the index is within the bounds of the tuple, False otherwise.
        :rtype: bool
        """
        return int(item) < len(self.__orig__)


class JsonList(JsonObject):
    """
    A JSON-like list object that extends JsonObject and provides list-specific methods.

    :param o: The original list or object to wrap.
    :type o: list or object
    :param args: Additional elements to include in the list.
    """

    def __init__(self, o, *args):
        """
        Initialize the JsonList with the given original object and additional elements.

        :param o: The original list or object to wrap.
        :type o: list or object
        :param args: Additional elements to include in the list.
        :type args: Any
        """
        super().__init__(o)
        for arg in args:
            self.append(arg)

    def append(self, obj):
        """
        Append an object to the list.

        :param obj: The object to append.
        :type obj: Any
        """
        self.__orig__.append(unjsify(obj))

    def clear(self):
        """
        Clear all elements from the list.
        """
        self.__orig__.clear()

    def __getitem__(self, item, *args, **kwargs):
        """
        Get an item from the list by index or slice, returning Undefined if the item does not exist.

        :param item: The index or slice to retrieve.
        :type item: int or slice
        :return: The value at the specified index or slice, or Undefined if not present.
        :rtype: Any or Undefined
        """
        try:
            return jsify(
                self.__orig__.__getitem__(
                    int(item) if not isinstance(item, slice) else item, *args, **kwargs
                )
            )
        except (Exception, BaseException):
            return Undefined

    __getattr__ = __getitem__

    def copy(self, deep=False):
        """
        Create a shallow or deep copy of the list.

        :param deep: True if the object should be deep copied, False otherwise.
        :type deep: bool
        :return: A copy of the list.
        :rtype: JsonList
        """
        return jsify(copy(self.__orig__) if not deep else deepcopy(self.__orig__))

    def count(self, value):
        """
        Return the number of occurrences of a value in the list.

        :param value: The value to count.
        :type value: Any
        :return: The number of occurrences of the value.
        :rtype: int
        """
        return self.__orig__.count(unjsify(value))

    def extend(self, obj: Iterable):
        """
        Extend the list by appending elements from the iterable.

        :param obj: The iterable to extend the list with.
        :type obj: Iterable
        """
        self.__orig__.extend(unjsify(obj))

    def index(self, value):
        """
        Return the first index of a value in the list.

        :param value: The value to find.
        :type value: Any
        :return: The first index of the value.
        :rtype: int
        :raises ValueError: If the value is not present.
        """
        return self.__orig__.index(unjsify(value))

    def insert(self, index, obj):
        """
        Insert an object at a specified index in the list.

        :param index: The index to insert the object at.
        :type index: int
        :param obj: The object to insert.
        :type obj: Any
        """
        self.__orig__.insert(index, unjsify(obj))

    def pop(self, index=-1):
        """
        Remove and return the item at the specified index in the list.

        :param index: The index to remove the item from. Defaults to -1 (the last item).
        :type index: int, optional
        :return: The removed item.
        :rtype: Any
        """
        return jsify(self.__orig__.pop(index))

    def remove(self, value):
        """
        Remove the first occurrence of a value from the list.

        :param value: The value to remove.
        :type value: Any
        """
        self.__orig__.remove(unjsify(value))

    def reverse(self, *args, **kwargs):
        """
        Reverse the elements of the list in place.

        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        """
        self.__orig__.reverse(*args, **kwargs)

    def sort(self, *args, **kwargs):
        """
        Sort the elements of the list in place.

        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        """
        return self.__orig__.sort(*args, **kwargs)

    def __dir__(self):
        """
        Return a list of attributes of the object.

        :return: A list of attributes of the object.
        :rtype: list
        """
        keys_list = [str(value) for value in self.__dict__.keys()]
        return keys_list

    @property
    def __dict__(self):
        """
        Return the dictionary representation of the list.

        :return: The dictionary representation of the list.
        :rtype: dict
        """
        digits = len(str(len(self.__orig__)))
        return {
            f"{key:0{digits}}": jsify(value) for key, value in enumerate(self.__orig__)
        }

    def __contains__(self, item):
        """
        Check if an index is within the bounds of the list.

        :param item: The index to check.
        :type item: int
        :return: True if the index is within the bounds of the list, False otherwise.
        :rtype: bool
        """
        return int(item) < len(self.__orig__)


class JsonDict(JsonObject):
    """
    A JSON-like dictionary object that extends JsonObject and provides dictionary-specific methods.

    :param o: The original dictionary or object to wrap.
    :type o: dict or object
    :param kwargs: Additional key-value pairs to include in the dictionary.
    """

    def __init__(self, o, **kwargs):
        """
        Initialize the JsonDict with the given original object and additional key-value pairs.

        :param o: The original dictionary or object to wrap.
        :type o: dict or object
        :param kwargs: Additional key-value pairs to include in the dictionary.
        :type kwargs: Any
        """
        super().__init__(o)
        for key, value in kwargs.items():
            self.__orig__[key] = value

    def __contains__(self, item):
        """
        Check if a key is in the dictionary.

        :param item: The key to check.
        :type item: str
        :return: True if the key is in the dictionary, False otherwise.
        :rtype: bool
        """
        return item in self.__orig__

    def __call__(self, item_name, default_class, *args, **kwargs):
        """
        Call the dictionary to get an item, creating it if it does not exist.

        :param item_name: The key to retrieve or create.
        :type item_name: str
        :param default_class: The class to instantiate if the key does not exist.
        :type default_class: type
        :param args: Additional arguments to pass to the class constructor.
        :type args: Any
        :param kwargs: Additional keyword arguments to pass to the class constructor.
        :type kwargs: Any
        :return: The value associated with the key, or a new instance of the default class.
        :rtype: Any
        """
        if item_name in self:
            return self.__getitem__(item_name)
        self.__setattr__(item_name, default_class(*args, **kwargs))
        return self.__getattr__(item_name)


class JsonIterator(Iterator):
    """
    An iterator for JSON-like objects that supports conversion to and from JSON.

    :param json_object: The JSON object to iterate over.
    :type json_object: JsonObject
    """

    def __init__(self, json_object):
        """
        Initialize the JsonIterator with the given JSON object.

        :param json_object: The JSON object to iterate over.
        :type json_object: JsonObject or Any
        """
        self.iterator = iter(unjsify(json_object))

    def __iter__(self):
        """
        Return the iterator itself.

        :return: The iterator itself.
        :rtype: JsonIterator
        """
        return self

    def __next__(self):
        """
        Return the next item from the iterator.

        :return: The next item from the iterator.
        :rtype: Any
        :raises StopIteration: If there are no more items.
        """
        return jsify(next(self.iterator))


def unjsify(obj):
    """
    Convert a JsonObject to its original representation.

    :param obj: The object to convert.
    :type obj: JsonObject or Any
    :return: The original object if obj is a JsonObject, otherwise returns obj.
    :rtype: Any
    """
    if isinstance(obj, JsonObject):
        return obj.__orig__
    else:
        return obj


def deep_unjsify(obj):
    """
    Convert a JsonObject to its original representation, performing a deep conversion.

    :param obj: The object to convert.
    :type obj: JsonObject or Any
    :return: The original object if obj is a JsonObject, otherwise returns obj.
    :rtype: Any
    """
    return unjsify(json_copy(obj, deep=True))


def json_copy(obj, deep=True):
    """
    Create a shallow or deep copy of the object.

    :param obj: The object to copy.
    :type obj: JsonObject or Any
    :param deep: True if the object should be deep copied, False otherwise.
    :type deep: bool
    :return: A copy of the object.
    :rtype: JsonObject or Any
    """
    return jsify(copy(obj) if not deep else deepcopy(obj))


def json_get(obj, item, *args, **kwargs):
    """
    Get an item from the object, returning a default value if the item does not exist.

    :param obj: The object to get the item from.
    :type obj: JsonObject or Any
    :param item: The item to get.
    :type item: Any
    :param args: Additional arguments.
    :param kwargs: Additional keyword arguments.
    :return: The value of the item.
    :rtype: JsonObject or Any
    """
    return jsify(
        super(JsonObject, obj).__getattribute__("__orig__").get(item, *args, **kwargs)
        if isinstance(obj, JsonObject)
        else obj.get(item, *args, **kwargs)
    )


def json_pop(obj, item, *args, **kwargs):
    """
    Remove the specified item from the object and return its value.

    :param obj: The object to pop the item from.
    :type obj: JsonObject or Any
    :param item: The item to pop.
    :type item: Any
    :param args: Additional arguments.
    :param kwargs: Additional keyword arguments.
    :return: The value of the popped item.
    :rtype: JsonObject or Any
    """
    return jsify(
        super(JsonObject, obj).__getattribute__("__orig__").pop(item, *args, **kwargs)
        if isinstance(obj, JsonObject)
        else obj.pop(item, *args, **kwargs)
    )


def json_popitem(obj, *args, **kwargs):
    """
    Remove and return a (key, value) pair from the object.

    :param obj: The object to pop the item from.
    :type obj: JsonObject or Any
    :param args: Additional arguments.
    :param kwargs: Additional keyword arguments.
    :return: The popped (key, value) pair.
    :rtype: tuple
    """
    return jsify(
        super(JsonObject, obj).__getattribute__("__orig__").popitem(*args, **kwargs)
        if isinstance(obj, JsonObject)
        else obj.popitem(*args, **kwargs)
    )


def json_setdefault(obj, value, default, *args, **kwargs):
    """
    Insert a key with a default value if the key is not in the dictionary.

    :param obj: The object to set the default value in.
    :type obj: JsonObject or Any
    :param value: The key to set the default value for.
    :type value: Any
    :param default: The default value to set.
    :type default: Any
    :param args: Additional arguments.
    :param kwargs: Additional keyword arguments.
    :return: The value of the key.
    :rtype: JsonObject or Any
    """
    return jsify(
        super(JsonObject, obj)
        .__getattribute__("__orig__")
        .setdefault(value, default, *args, **kwargs)
        if isinstance(obj, JsonObject)
        else obj.setdefault(value, default, *args, **kwargs)
    )


def json_update(obj, value, *args, **kwargs):
    """
    Update the dictionary with the key-value pairs from another dictionary.

    :param obj: The object to update.
    :type obj: JsonObject or Any
    :param value: The dictionary to update from.
    :type value: dict
    :param args: Additional arguments.
    :param kwargs: Additional keyword arguments.
    :return: The updated object.
    :rtype: JsonObject or Any
    """
    return jsify(
        super(JsonObject, obj)
        .__getattribute__("__orig__")
        .update(value, *args, **kwargs)
        if isinstance(obj, JsonObject)
        else obj.update(value, *args, **kwargs)
    )


def json_values(obj):
    """
    Return a new view of the dictionary's values.

    :param obj: The object to get the values from.
    :type obj: JsonObject or Any
    :return: A view object displaying a list of the dictionary's values.
    :rtype: JsonIterator
    """
    return JsonIterator(
        super(JsonObject, obj).__getattribute__("__orig__").values()
        if isinstance(obj, JsonObject)
        else obj.values()
    )


def json_keys(obj):
    """
    Return a new view of the dictionary's keys.

    :param obj: The object to get the keys from.
    :type obj: JsonObject, JsonList, JsonTuple or Any
    :return: A view object displaying a list of the object's keys (in case of list or tuple these would be the indexes
    in string format).
    :rtype: JsonIterator
    """
    return JsonIterator(
        obj.__dict__.keys()
        if isinstance(obj, (JsonList, JsonTuple))
        else super(JsonObject, obj).__getattribute__("__orig__").keys()
        if isinstance(obj, JsonObject)
        else obj.keys()
    )


def json_items(obj):
    """
    Return a new view of the dictionary's items (key, value pairs).

    :param obj: The object to get the items from.
    :type obj: JsonObject, JsonList, JsonTuple or Any
    :return: A view object displaying a list of the objects's items (in case of list or tuple these would be values with
     keys being their indexes in string format).
    :rtype: JsonIterator
    """
    return JsonIterator(
        obj.__dict__.items()
        if isinstance(obj, (JsonList, JsonTuple))
        else super(JsonObject, obj).__getattribute__("__orig__").items()
        if isinstance(obj, JsonObject)
        else obj.items()
    )


class PropertiesExistResult:
    def __init__(self, value=None):
        """
        Initialize the result with an optional value.

        :param value: The value to store.
        :type value: Any
        """
        self.jsified = jsify(value)
        self.unjsified = unjsify(value)

    def __bool__(self):
        return True


def properties_exist(obj, *path):
    """
    Check if a series of properties exist in the JSON object.

    :param obj: The JSON object to check.
    :type obj: JsonObject or Any
    :param path: The sequence of properties to check.
    :type path: str
    :return: True if the properties exist, False otherwise.
    :rtype: bool or PropertiesExistResult
    """

    obj = JsonObject(obj)
    try:
        for node in path:
            obj = obj[node]
            if obj is Undefined:
                return False
    except AnyError:
        return False
    return PropertiesExistResult(obj)


def jsify(o, **kwargs):
    """
    Convert a dictionary, list, or tuple to its corresponding JsonObject.

    :param o: The object to convert.
    :type o: dict, list, tuple or Any
    :param kwargs: Additional keyword arguments.
    :return: The converted JsonObject.
    :rtype: JsonObject, JsonDict, JsonList, or JsonTuple
    """
    if isinstance(o, dict):
        return JsonDict(o, **kwargs)
    elif isinstance(o, list):
        return JsonList(o)
    elif isinstance(o, tuple):
        return JsonTuple(o)
    else:
        return o
