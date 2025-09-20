from os import getenv

from .secret import Secret


class EnvVar(Secret):
    """A Secret that automatically loads its value from an environment variable.

    The Env class extends Secret to automatically retrieve sensitive values from
    environment variables, providing the same protection against accidental exposure
    while simplifying the process of working with environment-based secrets.

    Args:
        name (str): The name of the environment variable to read
        default: Default value if environment variable is not set (default: None)
        placeholder (str): The text to display instead of the actual value.
                          If None (default), uses "[{name}]" where {name} is the env var name.
                          Can be explicitly set to any string.

    Examples:
        >>> # Assuming API_KEY environment variable is set to "sk-12345"
        >>> api_key = EnvVar("API_KEY")
        >>> print(api_key)
        [API_KEY]
        >>> api_key.value
        'sk-12345'

        >>> # With default value
        >>> debug_mode = EnvVar("DEBUG_MODE", default="false")
        >>> print(debug_mode.value)  # "false" if DEBUG_MODE not set

        >>> # With custom placeholder
        >>> secret_token = EnvVar("SECRET_TOKEN", placeholder="<ENV_SECRET>")
        >>> print(secret_token)
        <ENV_SECRET>
    """

    def __init__(self, name: str, default=None, placeholder=None):
        """Initialize an Env secret from an environment variable.

        Args:
            name (str): The name of the environment variable to read
            default: Default value if environment variable is not set
            placeholder (str): Text to show instead of the actual value.
                             If None, defaults to "[{name}]". Can be set to any string.
        """
        value = getenv(name, default)
        if placeholder is None:
            placeholder = f"[{name}]"
        super().__init__(value, placeholder)
        self.name = name
