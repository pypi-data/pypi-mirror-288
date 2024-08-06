# Jsify Library

Jsify is a Python library designed to bridge the gap between Python's data structures and JSON-like objects, offering seamless integration and manipulation of data in a JavaScript-like manner. With Jsify, you can effortlessly convert Python dictionaries, lists, and tuples into JSON-like objects that support attribute-style access, automatic handling of undefined properties, and easy serialization.

## Features

- **Jsified Objects**: Convert Python dictionaries, lists, and tuples into `JsonObject`, `JsonDict`, `JsonList`, and `JsonTuple` objects that allow attribute-style access.
- **Custom JSON Serialization**: Seamlessly serialize jsified objects to JSON format, with options to handle undefined values.
- **Flexible Data Manipulation**: Access and manipulate data using JavaScript-like syntax in Python.
- **Assertion Utilities**: Validate the structure and contents of JSON-like objects using built-in assertions.
- **Custom Function Decorators**: Automatically convert function arguments to jsified objects and handle results with custom decorators.

## Installation

Install Jsify using pip:

```bash
pip install jsify
```

## Getting Started

Here’s a quick overview of how to use Jsify with some simple examples.

### 1. Creating Jsified Objects

You can easily convert Python data structures into jsified objects using the `jsify` function:

```python
from jsify import jsify

data = {
    'name': 'Alice',
    'details': {
        'age': 30,
        'city': 'Wonderland'
    }
}

# Convert to a jsified object
json_obj = jsify(data)

# Accessing properties using attribute-style access
print(json_obj.name)  # Outputs: Alice
print(json_obj.details.age)  # Outputs: 30
```

### 2. Handling Undefined Properties

Jsify allows you to safely access properties that may not exist, returning an `Undefined` object instead of raising an error:

```python
from jsify import Undefined

# Accessing a non-existent property
print(json_obj.details.country)  # Outputs: Undefined

# Checking if a property is undefined
if json_obj.details.country is Undefined:
    print("Country is not defined.")
```

### 3. Custom JSON Serialization

Jsify provides custom JSON serialization that handles jsified objects and offers the ability to omit undefined values:

```python
import json
from jsify import jsify

data = {
    'name': 'Alice',
    'details': {
        'age': 30,
        'nickname': Undefined
    }
}

json_obj = jsify(data)

# Serialize with omitting Undefined fields
json_string = json.dumps(json_obj, omit_undefined=True)
print(json_string)  # Outputs: {"name": "Alice", "details": {"age": 30}}

# Serialize without omitting Undefined fields
json_string = json.dumps(json_obj, omit_undefined=False)
print(json_string)  # Outputs: {"name": "Alice", "details": {"age": 30, "nickname": null}}
```

### 4. Using Assertions to Validate Data

Jsify includes an `assertions` module to help you validate the structure and contents of JSON-like objects:

```python
from jsify import jsify, JsonAssert

data = {
    'name': 'Alice',
    'details': {
        'age': 30,
        'city': 'Wonderland'
    }
}

json_obj = jsify(data)

# Assert that a key exists
assert_key_present = JsonAssert.IsIn()
assert_key_present.assertion(json_obj, 'name', 'root')  # No error

# Assert that a key does not exist
assert_key_absent = JsonAssert.NotIn()
assert_key_absent.assertion(json_obj, 'nonexistent', 'root')  # No error
```

### 5. Creating Jsified Functions

You can create functions that automatically handle jsified objects using decorators:

```python
from jsify import jsified_function

@jsified_function(result_original=True)
def process_data(data):
    # Accessing properties with attribute-style access
    return data.details.age + 10

data = {
    'details': {
        'age': 30
    }
}

# Call the decorated function
result = process_data(data)
print(result)  # Outputs: 40
```

## Documentation

For detailed documentation and more advanced usage, please refer to the [official documentation](https://citsystems.github.io/jsify/).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Conclusion

Jsify simplifies the process of working with JSON-like data in Python by providing a set of tools that emulate JavaScript's flexibility while maintaining Pythonic design principles. Whether you're building APIs, working with configuration files, or manipulating complex data structures, Jsify offers a clean and intuitive approach.

Feel free to explore the library further and see how it can fit into your projects!
