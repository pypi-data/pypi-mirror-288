from typing import Type, TypeVar, Callable, Any
from pathlib import Path
import os

T_BaseEnv = TypeVar("T_BaseEnv", bound="BaseEnv")

class BaseEnv:
    def __init__(self, *, name: str):
        self._name = name
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def name_upper(self) -> str:
        return self.name.upper()


def load_env_var(
        *,
        name_left: bool = False,
        raise_none_error: bool = True,
        cast_to: Type[Any]
    ):
    """
    Generic decorator to load environment variables and cast to a specific type.
    
    - `name_left (bool):` Add the `upper_name` to the left of the variable. Separated by "_".
    - `raise_none_error (bool):` Raise error if the `env_var` is None when load.
    - `cast_to (Type[Any]):` Type to cast the env var to a specific type.
    """
    def decorator(func: Callable[[Type[T_BaseEnv]], str]):
        """ Raise error if result is None."""
        def wrapper(self: Type[T_BaseEnv]) -> Any:
            env_name = func(self)
            if not isinstance(env_name, str):
                raise ValueError("Expected string for `env_name`.")

            if name_left:
                env_name = f"{self.name_upper}_{env_name}"
            
            env_var = os.getenv(env_name)
            if raise_none_error and env_var is None:
                raise ValueError(f"`{func.__name__}` for `{self.name_upper}` is None")
            
            return cast_to(env_var)
        return wrapper
    return decorator

def load_env_var_str(
        *,
        name_left: bool = False,
        raise_none_error: bool = True
    ):
    """ Specific decorator for `str`. See `load_env_var` doc for understanding."""
    return load_env_var(name_left=name_left, raise_none_error=raise_none_error, cast_to=str)

def load_env_var_path(
        *,
        name_left: bool = False,
        raise_none_error: bool = True
    ):
    """ Specific decorator for `path`. See `load_env_var` doc for understanding."""
    return load_env_var(name_left=name_left, raise_none_error=raise_none_error, cast_to=Path)

def load_env_var_float(
        *,
        name_left: bool = False,
        raise_none_error: bool = True
    ):
    """ Specific decorator for `float`. See `load_env_var` doc for understanding."""
    return load_env_var(name_left=name_left, raise_none_error=raise_none_error, cast_to=float)

def load_env_var_int(
        *,
        name_left: bool = False,
        raise_none_error: bool = True
    ):
    """ Specific decorator for `int`. See `load_env_var` doc for understanding."""
    return load_env_var(name_left=name_left, raise_none_error=raise_none_error, cast_to=int)
