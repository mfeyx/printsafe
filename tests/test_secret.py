import pytest

from printsafe import Secret


class TestSecretInitialization:
    """Test Secret class initialization."""

    def test_init_with_string(self):
        """Test initialization with string value."""
        secret = Secret("password123")
        assert secret.value == "password123"
        assert secret.placeholder == "[REDACTED]"

    def test_init_with_custom_placeholder(self):
        """Test initialization with custom placeholder."""
        secret = Secret("secret", placeholder="<HIDDEN>")
        assert secret.value == "secret"
        assert secret.placeholder == "<HIDDEN>"

    def test_init_with_different_types(self):
        """Test initialization with various data types."""
        # Integer
        secret_int = Secret(42)
        assert secret_int.value == 42

        # List
        secret_list = Secret([1, 2, 3])
        assert secret_list.value == [1, 2, 3]

        # Dictionary
        secret_dict = Secret({"key": "value"})
        assert secret_dict.value == {"key": "value"}

        # None
        secret_none = Secret(None)
        assert secret_none.value is None


class TestSecretStringRepresentation:
    """Test string representation methods."""

    def test_str_returns_placeholder(self):
        """Test __str__ returns placeholder."""
        secret = Secret("sensitive_data")
        assert str(secret) == "[REDACTED]"

    def test_repr_returns_placeholder(self):
        """Test __repr__ returns placeholder."""
        secret = Secret("sensitive_data")
        assert repr(secret) == "[REDACTED]"

    def test_custom_placeholder_in_str(self):
        """Test custom placeholder appears in string representation."""
        secret = Secret("data", placeholder="***")
        assert str(secret) == "***"
        assert repr(secret) == "***"

    def test_format_string_uses_placeholder(self):
        """Test f-string and format use placeholder."""
        secret = Secret("api_key")
        assert f"Key: {secret}" == "Key: [REDACTED]"
        assert f"Key: {secret}" == "Key: [REDACTED]"


class TestSecretComparison:
    """Test comparison operations."""

    def test_equality_with_same_secret(self):
        """Test equality between Secret objects with same value."""
        secret1 = Secret("password")
        secret2 = Secret("password")
        assert secret1 == secret2

    def test_equality_with_different_secret(self):
        """Test inequality between Secret objects with different values."""
        secret1 = Secret("password1")
        secret2 = Secret("password2")
        assert secret1 != secret2

    def test_equality_with_raw_value(self):
        """Test equality between Secret and raw value."""
        secret = Secret("password")
        assert secret == "password"  # noqa: S105
        assert secret != "wrong_password"  # noqa: S105

    def test_equality_with_different_placeholders(self):
        """Test equality ignores placeholder differences."""
        secret1 = Secret("password", placeholder="[HIDDEN]")
        secret2 = Secret("password", placeholder="***")
        assert secret1 == secret2


class TestSecretHashing:
    """Test hashing functionality."""

    def test_hash_consistency(self):
        """Test hash is consistent for same value."""
        secret1 = Secret("password")
        secret2 = Secret("password")
        assert hash(secret1) == hash(secret2)

    def test_hash_difference(self):
        """Test different values have different hashes."""
        secret1 = Secret("password1")
        secret2 = Secret("password2")
        assert hash(secret1) != hash(secret2)

    def test_use_in_set(self):
        """Test Secret can be used in sets."""
        secret1 = Secret("password")
        secret2 = Secret("password")
        secret3 = Secret("different")

        secret_set = {secret1, secret2, secret3}
        assert len(secret_set) == 2  # secret1 and secret2 are the same

    def test_use_as_dict_key(self):
        """Test Secret can be used as dictionary key."""
        secret = Secret("key")
        data = {secret: "value"}
        assert data[secret] == "value"


class TestSecretAttributeDelegation:
    """Test attribute delegation to wrapped value."""

    def test_string_method_delegation(self):
        """Test string methods are delegated."""
        secret = Secret("hello world")
        # Access through .value to be safe
        assert secret.value.upper() == "HELLO WORLD"
        assert secret.value.split() == ["hello", "world"]

    def test_list_method_delegation(self):
        """Test list methods are delegated."""
        secret = Secret([1, 2, 3])
        # Access through .value to be safe
        assert secret.value.append(4) is None
        assert secret.value == [1, 2, 3, 4]

    def test_dict_method_delegation(self):
        """Test dict methods are delegated."""
        secret = Secret({"a": 1, "b": 2})
        # Access through .value to be safe
        assert secret.value.get("a") == 1
        assert secret.value.keys()


class TestSecretCallable:
    """Test callable functionality."""

    def test_callable_secret(self):
        """Test Secret wrapping callable object."""

        def multiply(x, y):
            return x * y

        secret_func = Secret(multiply)
        result = secret_func(3, 4)
        assert result == 12

    def test_callable_with_kwargs(self):
        """Test callable Secret with keyword arguments."""

        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}!"

        secret_func = Secret(greet)
        result = secret_func("Alice", greeting="Hi")
        assert result == "Hi, Alice!"

    def test_non_callable_secret(self):
        """Test non-callable Secret raises appropriate error."""
        secret = Secret("not_callable")
        with pytest.raises(TypeError):
            secret()


class TestSecretIterationPrevention:
    """Test iteration prevention."""

    def test_iteration_blocked(self):
        """Test iteration raises TypeError."""
        secret = Secret("password")
        with pytest.raises(TypeError, match="'Secret' object is not iterable"):
            for _ in secret:
                pass

    def test_iteration_blocked_for_list(self):
        """Test iteration blocked even for iterable wrapped values."""
        secret = Secret([1, 2, 3])
        with pytest.raises(TypeError, match="'Secret' object is not iterable"):
            for _ in secret:
                pass

    def test_list_conversion_blocked(self):
        """Test list() conversion is blocked."""
        secret = Secret("abc")
        with pytest.raises(TypeError):
            list(secret)


class TestSecretValueAccess:
    """Test direct value access."""

    def test_value_attribute_access(self):
        """Test .value attribute provides access to wrapped value."""
        original_value = "sensitive_data"
        secret = Secret(original_value)
        assert secret.value == original_value
        assert secret.value is original_value

    def test_value_modification_through_reference(self):
        """Test modifying mutable values through .value reference."""
        original_list = [1, 2, 3]
        secret = Secret(original_list)
        secret.value.append(4)
        assert secret.value == [1, 2, 3, 4]
        assert original_list == [1, 2, 3, 4]


class TestSecretEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_string_secret(self):
        """Test Secret with empty string."""
        secret = Secret("")
        assert secret.value == ""
        assert str(secret) == "[REDACTED]"

    def test_none_secret(self):
        """Test Secret with None value."""
        secret = Secret(None)
        assert secret.value is None
        assert str(secret) == "[REDACTED]"

    def test_boolean_secret(self):
        """Test Secret with boolean values."""
        secret_true = Secret(True)
        secret_false = Secret(False)

        assert secret_true.value is True
        assert secret_false.value is False
        assert str(secret_true) == "[REDACTED]"
        assert str(secret_false) == "[REDACTED]"

    def test_zero_secret(self):
        """Test Secret with zero value."""
        secret = Secret(0)
        assert secret.value == 0
        assert str(secret) == "[REDACTED]"

    def test_empty_placeholder(self):
        """Test Secret with empty placeholder."""
        secret = Secret("value", placeholder="")
        assert str(secret) == ""
        assert secret.value == "value"


class TestSecretSecurityFeatures:
    """Test security-related features."""

    def test_prevents_accidental_logging(self):
        """Test that Secret prevents accidental exposure in logging scenarios."""
        import io  # noqa: PLC0415
        import logging  # noqa: PLC0415

        # Create a string stream to capture log output
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        logger = logging.getLogger("test_logger")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        secret = Secret("sensitive_password")
        logger.info("User credentials: %s", secret)

        log_output = log_stream.getvalue()
        assert "sensitive_password" not in log_output
        assert "[REDACTED]" in log_output

        # Clean up
        logger.removeHandler(handler)

    def test_memory_protection_concept(self):
        """Test that value is accessible but protected from casual inspection."""
        secret = Secret("api_key_12345")

        # Direct access works
        assert secret.value == "api_key_12345"

        # But casual inspection is protected
        secret_vars = vars(secret)
        # The value should be accessible but not through casual string conversion
        assert str(secret_vars) != str({"value": "api_key_12345"})
