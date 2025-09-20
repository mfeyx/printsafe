class Secret:
    """A wrapper class that prevents accidental exposure of sensitive values.

    The Secret class wraps sensitive data (like passwords, API keys, tokens) and
    prevents them from being accidentally exposed through string representation,
    logging, or debugging. The actual value is only accessible through the 'value'
    attribute.

    Args:
        value: The sensitive value to be wrapped
        placeholder (str): The text to display instead of the actual value
                          (default: "[REDACTED]")

    Examples:
        >>> secret_password = Secret("my_password123")
        >>> print(secret_password)
        [REDACTED]
        >>> secret_password.value
        'my_password123'

        >>> api_key = Secret("abc123", placeholder="<hidden>")
        >>> str(api_key)
        '<hidden>'
    """

    def __init__(self, value, placeholder="[REDACTED]"):
        """Initialize a Secret with a value and optional placeholder.

        Args:
            value: The sensitive value to wrap
            placeholder (str): Text to show instead of the actual value
        """
        self.placeholder = placeholder
        object.__setattr__(self, "value", value)

    def __str__(self):
        """Return the placeholder string instead of the actual value.

        Returns:
            str: The placeholder text
        """
        return self.placeholder

    def __repr__(self):
        """Return the placeholder string for object representation.

        Returns:
            str: The placeholder text
        """
        return self.placeholder

    def __getattribute__(self, name):
        """Control access to object attributes.

        Args:
            name (str): The attribute name being accessed

        Returns:
            The attribute value
        """
        if name == "value":
            return object.__getattribute__(self, name)
        return object.__getattribute__(self, name)

    def __eq__(self, other):
        """Compare Secret objects or Secret with other values.

        Args:
            other: Another Secret object or value to compare against

        Returns:
            bool: True if the wrapped values are equal
        """
        if isinstance(other, Secret):
            return self.value == other.value
        return self.value == other

    def __hash__(self):
        """Return hash of the wrapped value for use in sets/dicts.

        Returns:
            int: Hash of the wrapped value
        """
        return hash(self.value)

    def __getattr__(self, name):
        """Delegate attribute access to the wrapped value.

        This allows the Secret to behave like the wrapped object for
        attributes not explicitly defined on the Secret class.

        Args:
            name (str): The attribute name

        Returns:
            The attribute from the wrapped value
        """
        return getattr(self.value, name)

    def __call__(self, *args, **kwargs):
        """Allow the secret to be called if the wrapped value is callable.

        Args:
            *args: Positional arguments to pass to the wrapped value
            **kwargs: Keyword arguments to pass to the wrapped value

        Returns:
            The result of calling the wrapped value
        """
        return self.value(*args, **kwargs)

    def __iter__(self):
        """Prevent iteration to avoid exposing secret value character by character.

        Raises:
            TypeError: Always raised to prevent iteration
        """
        msg = f"'{self.__class__.__name__}' object is not iterable"
        raise TypeError(msg)
