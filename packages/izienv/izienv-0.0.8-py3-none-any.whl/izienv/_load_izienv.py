from pathlib import Path
from dotenv import load_dotenv

def get_path_env(path_envs: Path, name: str) -> Path:
    return path_envs / f"{name}.env"

def __load_env_base(path_envs: Path, override: bool = True) -> None:
    path_base = get_path_env(path_envs=path_envs, name="base")
    if path_base.exists():
        load_dotenv(path_base, override=override)
    else:
        print(f"base.env dont exists into {path_envs}")

def __load_env_etc(path_envs: Path, override: bool = True) -> None:
    path_etc = get_path_env(path_envs=path_envs, name="etc")
    if path_etc.exists():
        load_dotenv(path_etc, override=override)


def load_izienv(name: str, path_envs: Path = Path(".envs"), override: bool = True) -> None:
    path_env = get_path_env(path_envs=path_envs, name=name)
    if not path_env.exists():
        raise ValueError(f"{path_env} dont exists.")
    
    # Load `base.env` if exists.
    __load_env_base(path_envs=path_envs, override=override)

    # Load `{name}.env`.
    load_dotenv(path_env, override=override)

    # Load `etc.env` if exists.
    __load_env_etc(path_envs=path_envs, override=override)
