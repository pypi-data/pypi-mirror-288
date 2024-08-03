import streamlit as st
from confidentialmindserver.config_manager import ConfigManager, ConnectorSchema
import os


# Note: ConfigManager must be initialized before it can be used
@st.cache_resource
def get_config_manager():
    """
    Retrieve a cached instance of the ConfigManager.

    This function leverages Streamlit's caching mechanism to ensure that only one instance of ConfigManager is created
    per session, optimizing resource usage and performance.

    Returns:
        ConfigManager: An initialized and cached ConfigManager instance.
    """
    return ConfigManager()


# This non-caching function exists to make sure the id is used in the cache key
# and to make the parameter names nicer (no underscores)
def init_config_manager(
    config_model,
    connectors: list[ConnectorSchema] = None,
    id=None,
    use_local_configs=False,
):
    """
    Initialize a ConfigManager instance with the given parameters.

    This function is designed to ensure that certain parameters, such as 'id', are included in the cache key for
    Streamlit's caching mechanism. It also provides a more user-friendly interface than the private `_init_config_manager`
    function.

    Args:
        config_model (type): The model class used by ConfigManager.
        connectors (list[ConnectorSchema], optional): List of ConnectorSchema instances to initialize with.
        id (str, optional): Identifier for the configuration manager. Defaults to SERVICE_NAME environment variable or None.
        use_local_configs (bool, optional): Flag indicating whether to use local configurations.

    Returns:
        ConfigManager: An initialized and potentially cached ConfigManager instance.
    """
    id = os.environ.get("SERVICE_NAME") or id
    config_manager = _init_config_manager(
        _config_model=config_model,
        _connectors=connectors,
        id=id,
        use_local_configs=use_local_configs,
    )
    return config_manager


# Underscored parameters are not used in cache key
# TODO: implement hash function for custom objects if needed
@st.cache_resource
def _init_config_manager(
    _config_model,
    _connectors: list[ConnectorSchema] = None,
    id=None,
    use_local_configs=False,
):
    """
    Initialize a ConfigManager instance, intended for internal use.

    This function is similar to `init_config_manager`, but with parameters prefixed by an underscore. These parameters
    are not included in the cache key since they may be complex objects like classes or lists of custom objects, which
    could complicate caching logic.

    Args:
        _config_model (type): The app config model class used by ConfigManager.
        _connectors (list[ConnectorSchema], optional): List of connectors the app may use.
        id (str, optional): Identifier for the service. Defaults to None. Can be an arbitrary string for local dev. Set automatically
            when running inside the stack.
        use_local_configs (bool, optional): If True, configs will not be fetched from or sent to the server. Used for local development.

    Returns:
        ConfigManager: An initialized ConfigManager instance.
    """
    config_manager = ConfigManager()

    config_manager.init_manager(
        config_model=_config_model,
        id=id,
        connectors=_connectors,
        use_local_configs=use_local_configs,
    )
    return config_manager
