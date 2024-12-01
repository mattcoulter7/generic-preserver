# generic-preserver

<img src="assets/logo.webp" alt="logo" width="500">

**Extracting Generic Type References in Python**

## Introduction

In Python, generic types are a powerful feature for writing reusable and type-safe code. However, one limitation is that generic type arguments are typically not preserved at runtime, making it challenging to access or utilize these types dynamically. **`generic-preserver`** is a Python package that overcomes this limitation by capturing and preserving generic type arguments, allowing you to access them at runtime.

This package is particularly useful when you need to perform operations based on the specific types used in your generic classes, such as serialization, deserialization, or dynamic type checking.

## Features

- **Preserve Generic Types at Runtime**: Capture and retain generic type arguments for classes and instances.
- **Runtime Access to Type Parameters**: Easily access the type parameters passed to generic classes from their instances.
- **Supports Inheritance and Nested Generics**: Works seamlessly with class hierarchies and nested generic types.
- **Simple and Intuitive API**: Use either a metaclass or a decorator to enable functionality with minimal code changes.
- **Python 3.9+ Support**: Leverages modern Python features for type hinting and annotations.

## Installation

Install `generic-preserver` via pip:

```bash
pip install generic-preserver
```

Or install using Poetry:

```bash
poetry add generic-preserver
```

## Requirements

- Python 3.9 or higher

## Usage

### Using the `GenericMeta` Metaclass

To enable capturing generic type arguments, use the `GenericMeta` metaclass in your base class definition.

```python
from typing import TypeVar, Generic
from generic_preserver.metaclass import GenericMeta

# Define type variables
A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

# Example classes to use as type arguments
class ExampleA:
    pass

class ExampleB:
    pass

class ExampleC:
    pass

# Base class with GenericMeta metaclass
class Parent(Generic[A, B], metaclass=GenericMeta):
    pass

# Child classes specifying some generic type arguments
class Child(Parent[ExampleA, B], Generic[B, C]):
    pass

class GrandChild(Child[ExampleB, C], Generic[C]):
    pass

# Create an instance of the generic class with type arguments
instance = GrandChild[ExampleC]()

# Access the preserved generic type arguments
print(instance[A])  # Output: <class '__main__.ExampleA'>
print(instance[B])  # Output: <class '__main__.ExampleB'>
print(instance[C])  # Output: <class '__main__.ExampleC'>

# View the internal generic map
print(instance.__generic_map__)
# Output:
# {
#     ~A: <class '__main__.ExampleA'>,
#     ~B: <class '__main__.ExampleB'>,
#     ~C: <class '__main__.ExampleC'>,
# }
```

### Using the `@generic_preserver` Decorator

Alternatively, use the `@generic_preserver` decorator to enable capturing generic arguments without explicitly specifying the metaclass.

```python
from typing import TypeVar, Generic
from generic_preserver.wrapper import generic_preserver

# Define type variables
A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

# Example classes to use as type arguments
class ExampleA:
    pass

class ExampleB:
    pass

class ExampleC:
    pass

# Use the decorator to enable generic preservation
@generic_preserver
class Parent(Generic[A, B]):
    pass

# Child classes specifying some generic type arguments
class Child(Parent[ExampleA, B], Generic[B, C]):
    pass

class GrandChild(Child[ExampleB, C], Generic[C]):
    pass

# Create an instance of the generic class with type arguments
instance = GrandChild[ExampleC]()

# Access the preserved generic type arguments
print(instance[A])  # Output: <class '__main__.ExampleA'>
print(instance[B])  # Output: <class '__main__.ExampleB'>
print(instance[C])  # Output: <class '__main__.ExampleC'>

# View the internal generic map
print(instance.__generic_map__)
# Output:
# {
#     ~A: <class '__main__.ExampleA'>,
#     ~B: <class '__main__.ExampleB'>,
#     ~C: <class '__main__.ExampleC'>,
# }
```

### Accessing Type Variables

You can access the type arguments by indexing the instance with the corresponding `TypeVar`.

```python
print(instance[A])  # Output: <class '__main__.ExampleA'>
```

If you attempt to access a type variable that was not defined or is not in the generic map, a `KeyError` will be raised.

```python
D = TypeVar("D")
try:
    print(instance[D])
except KeyError as e:
    print(e)  # Output: No generic type found for generic arg ~D
```

### Accessing Multiple Type Variables

You can retrieve multiple type variables at once by passing an iterable of `TypeVar` instances.

```python
types = instance[A, B, C]
print(types)
# Output: (<class '__main__.ExampleA'>, <class '__main__.ExampleB'>, <class '__main__.ExampleC'>)
```

## How It Works

The `generic-preserver` package uses a custom metaclass `GenericMeta` to intercept class creation and capture generic type arguments when a generic class is subscripted (e.g., `MyClass[int, str]`). Here's a brief overview:

- **Metaclass (`GenericMeta`)**: Overrides the `__getitem__` method to capture the type arguments and store them in a `__generic_map__`.
- **Class Wrapper**: Creates a wrapper class that inherits from the original class and includes the `__generic_map__`.
- **Instance Access**: Allows instances to access the type arguments via the `__getitem__` method.
- **Decorator (`@generic_preserver`)**: Provides a convenient way to apply `GenericMeta` without altering the class definition directly.

By preserving the generic type arguments in `__generic_map__`, you can access them at runtime, enabling more dynamic and type-aware programming patterns.

## Testing

The package includes a test suite to verify its functionality. To run the tests, first install the development dependencies:

```bash
poetry install --with dev
```

Then, run the tests using `pytest`:

```bash
pytest
```

An example test case is provided in `tests/test_wrapper.py`:

```python
def test_template():
    A = TypeVar("A")
    B = TypeVar("B")
    C = TypeVar("C")

    class ExampleA: pass
    class ExampleB: pass
    class ExampleC: pass

    @generic_preserver
    class Parent(Generic[A, B]): pass

    class Child(Parent[ExampleA, B], Generic[B, C]): pass

    class GrandChild(Child[ExampleB, C], Generic[C]): pass

    instance = GrandChild[ExampleC]()

    assert instance[A] is ExampleA
    assert instance[B] is ExampleB
    assert instance[C] is ExampleC

    D = TypeVar("D")
    with pytest.raises(KeyError):
        instance[D]
```

## Limitations

- **Python Version**: Requires Python 3.9 or higher due to the use of internal structures from the `typing` module.
- **Compatibility**: May not be compatible with other metaclass-based libraries or complex metaclass hierarchies.
- **TypeVar Constraints**: Does not enforce `TypeVar` constraints or bounds at runtime; it only captures the types provided.

## Contributing

Contributions are welcome! If you find a bug or have an idea for a new feature, please open an issue or submit a pull request.

To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/my-feature`).
3. Commit your changes (`git commit -am 'Add my feature'`).
4. Push to your branch (`git push origin feature/my-feature`).
5. Open a Pull Request.

Please ensure that your code passes all tests and follows the existing coding style.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Inspired by the need to access and utilize generic type parameters at runtime in Python applications.
- Special thanks to the Python community for their contributions and support.

To learn more about how I came up with this solution, please read my blog post: [Extracting Generic Type References in Python](https://mica-twig-c4c.notion.site/Extracting-Generic-Type-References-in-Python-14c04289061f802b851ae564e80c251e)

## Contact

For questions, suggestions, or feedback, please contact:

Matthew Coulter  
Email: [mattcoul7@gmail.com](mailto:mattcoul7@gmail.com)

---

Thank you for using `generic-preserver`! If you find this package helpful, consider giving it a star on GitHub.
