from typing import Type, TypeVar, Callable
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
        name_pre: bool = False,
        is_path: bool = False,
        raise_none_error: bool = True
    ):
    """
    - `name_pre (bool):` Add the `upper_name` to the left of the variable. Separated by "_".
    - `is_path: (bool):` Returns the path instead of the string.
    - `raise_none_error (bool):` Raise error if the `env_var` is None when load.
    """
    def decorator(func: Callable[[Type[T_BaseEnv]], str]):
        """ Raise error if result is None."""
        def wrapper(self: Type[T_BaseEnv]) -> str | Path:
            env_name = func(self)
            if not isinstance(env_name, str):
                raise ValueError("Expected string for `env_name`.")

            if name_pre:
                env_name = f"{self.name_upper}_{env_name}"
            
            env_var = os.getenv(env_name)
            if raise_none_error and env_var is None:
                raise ValueError(f"`{func.__name__}` for `{self.name_upper}` is None")
            
            if is_path:
                return Path(env_var)
            return env_var
        return wrapper
    return decorator
