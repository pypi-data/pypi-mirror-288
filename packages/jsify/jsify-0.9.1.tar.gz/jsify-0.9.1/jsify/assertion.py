"""
The `assertion` module provides a suite of tools for performing assertions on JSON-like objects, ensuring that their
structure and content conform to expected criteria. This module is particularly useful in testing scenarios where you
need to validate the presence or absence of specific keys, as well as the correctness of values within nested JSON
structures.
At the heart of this module is the `JsonAssert` class, which offers a range of assertion methods designed to work with
instances of `JsonObject`. These assertions enable you to verify that certain keys are either present or absent within
a JSON object and that the values associated with those keys are as expected.
"""

from .jsify import JsonObject


class JsonAssert:
    """
    A class providing assertions to verify the contents of JSON-like objects.
    """

    class Assertion:
        """
        Base class for assertions on JSON objects.
        """

        def assertion(self, json_object, key, path):
            """
            Perform an assertion on a JSON object.

            :param json_object: The JSON object to perform the assertion on.
            :type json_object: JsonObject
            :param key: The key to check in the JSON object.
            :type key: str or int
            :param path: The current path in the JSON object.
            :type path: str
            """
            pass

    class NotIn(Assertion):
        """
        Assertion to check that a key is not in the JSON object.
        """

        def __init__(self):
            """
            Initialize the NotIn assertion.
            """
            pass

        def assertion(self, json_object, key, path):
            """
            Assert that a key is not in the JSON object.

            :param json_object: The JSON object to perform the assertion on.
            :type json_object: JsonObject
            :param key: The key to check in the JSON object.
            :type key: str
            :param path: The current path in the JSON object.
            :type path: str
            :raises AssertionError: If the key is found in the JSON object.
            """
            if key in json_object:
                raise AssertionError(
                    "{0}.{1} shouldn't be in JTO object.".format(path, key)
                )

    class IsIn(Assertion):
        """
        Assertion to check that a key is in the JSON object.
        """

        def __init__(self):
            """
            Initialize the IsIn assertion.
            """
            pass

        def assertion(self, json_object, key, path):
            """
            Assert that a key is in the JSON object.

            :param json_object: The JSON object to perform the assertion on.
            :type json_object: JsonObject
            :param key: The key to check in the JSON object.
            :type key: str
            :param path: The current path in the JSON object.
            :type path: str
            :raises AssertionError: If the key is not found in the JSON object.
            """
            if key not in json_object:
                raise AssertionError(
                    "{0}.{1} should be in JTO object.".format(path, key)
                )

    @staticmethod
    def values_equal(json_object, values: dict, path=""):
        """
        Assert that the values in a JSON object match the expected values.

        :param json_object: The JSON object to check.
        :type json_object: JsonObject
        :param values: The expected values to match against the JSON object.
        :type values: dict or list
        :param path: The current path in the JSON object (used for error messages).
        :type path: str
        :raises AssertionError: If the values do not match the expected values.
        """
        if not isinstance(values, dict) and not isinstance(values, list):
            raise AssertionError("{0} is an object not a value".format(path))
        if isinstance(values, dict):
            iteration = values.items()
        else:
            iteration = enumerate(values)
        for key, attribute in iteration:
            if isinstance(attribute, JsonAssert.Assertion):
                attribute.assertion(json_object, key, path)
            else:
                if key not in json_object:
                    raise AssertionError("{0}.{1} not in JTO object.".format(path, key))
                jto_attribute_value = json_object[key]
                if isinstance(jto_attribute_value, JsonObject):
                    JsonAssert.values_equal(
                        jto_attribute_value, attribute, path + "." + str(key)
                    )
                elif jto_attribute_value != attribute:
                    raise AssertionError(
                        "{0}.{1} not equal to {2}".format(path, key, json_object[key])
                    )
