"""
The `exceptions` module defines custom exception handling mechanisms tailored for use within the broader library.
Currently, it includes the `AnyError` exception, which is a tuple containing `BaseException`, and serves as a
general-purpose base for catching any exception that may occur.
By using `AnyError`, developers can create more flexible and generalized exception handling patterns that are capable
of catching all types of exceptions in a single construct. This can be particularly useful in situations where a
broad catch-all exception is needed.
"""

AnyError = (BaseException,)
