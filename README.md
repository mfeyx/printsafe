# printsafe

A Python library that prevents accidental exposure of sensitive data in logs, debug output, and string representations.

## Overview

`printsafe` provides a `Secret` class that wraps sensitive values (passwords, API keys, tokens, etc.) and prevents them from being accidentally exposed through:
- String representation (`str()`, `print()`)
- Debug output (`repr()`)
- Logging statements
- Iteration (prevents character-by-character exposure)

The wrapped value remains fully accessible when explicitly requested, but is protected from accidental disclosure.

## Installation

```bash
pip install printsafe
```

## Quick Start

```python
from printsafe import Secret

# Wrap a sensitive value
api_key = Secret("sk-1234567890abcdef")

# Safe operations - won't expose the secret
print(api_key)                    # Output: [REDACTED]
print(f"API Key: {api_key}")      # Output: API Key: [REDACTED]
str(api_key)                      # Returns: "[REDACTED]"
repr(api_key)                     # Returns: "[REDACTED]"

# Access the actual value when needed
actual_key = api_key.value        # Returns: "sk-1234567890abcdef"
```

## Usage Examples

### Basic Usage

```python
from printsafe import Secret

# Create a secret with default placeholder
password = Secret("my_super_secret_password")
print(password)  # [REDACTED]

# Create a secret with custom placeholder
token = Secret("abc123xyz", placeholder="<HIDDEN>")
print(token)     # <HIDDEN>
```

### Working with Different Data Types

```python
# String secrets
api_key = Secret("sk-1234567890")

# Numeric secrets
secret_number = Secret(42)
print(secret_number)        # [REDACTED]
print(secret_number.value)  # 42

# Dictionary secrets
config = Secret({"database_url": "postgresql://user:pass@host/db"})
print(config)               # [REDACTED]
print(config.value["database_url"])  # Access nested values
```

### Method Delegation

The `Secret` class delegates method calls to the wrapped value:

```python
secret_text = Secret("hello world")

# These methods are delegated to the wrapped string
print(secret_text.upper())    # Raises AttributeError or returns delegated result
print(secret_text.value.upper())  # "HELLO WORLD" - safe explicit access
```

### Callable Secrets

If the wrapped value is callable, the Secret can be called directly:

```python
def secret_function(x):
    return x * 2

secret_func = Secret(secret_function)
result = secret_func(5)  # Calls the wrapped function, returns 10
```

### Comparison and Hashing

```python
secret1 = Secret("password123")
secret2 = Secret("password123")
secret3 = Secret("different")

# Equality comparison
print(secret1 == secret2)     # True
print(secret1 == secret3)     # False
print(secret1 == "password123")  # True

# Can be used in sets and as dict keys
secrets = {secret1, secret2}  # Set with one unique secret
secret_dict = {secret1: "user1"}
```

### Prevented Operations

```python
secret = Secret("sensitive")

# These operations are blocked to prevent exposure:
try:
    for char in secret:  # Iteration blocked
        print(char)
except TypeError as e:
    print(e)  # 'Secret' object is not iterable
```

## API Reference

### `Secret(value, placeholder="[REDACTED]")`

#### Parameters
- `value`: The sensitive value to wrap (any type)
- `placeholder` (str, optional): Text to display instead of the actual value. Defaults to `"[REDACTED]"`

#### Attributes
- `value`: Access the wrapped sensitive value
- `placeholder`: The placeholder text used for string representation

#### Methods
- `__str__()`: Returns the placeholder string
- `__repr__()`: Returns the placeholder string
- `__eq__(other)`: Compare with another Secret or value
- `__hash__()`: Returns hash of the wrapped value
- `__call__(*args, **kwargs)`: Call the wrapped value if it's callable
- `__getattr__(name)`: Delegate attribute access to wrapped value

#### Blocked Operations
- `__iter__()`: Raises `TypeError` to prevent iteration

## Security Considerations

- The actual value is stored in memory and can be accessed via the `value` attribute
- This library protects against accidental exposure, not malicious access
- Memory dumps or debugging tools may still reveal the sensitive data
- Consider additional security measures for highly sensitive applications

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
