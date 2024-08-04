### Python package to handle multiple files with environment variables.

- TODO: Ver si puedo instalarlo en global para manejar las variables dentro de arch.

### Quickstart
- Crear folder `.envs/` en la raiz del proyecto.
```bash
cd /path/to/project
mkdir -p .envs
touch .envs/name_env.env
```

- Editar las variables de entorno, deberán llamarse `{NAME_ENV}_{VAR}`.
```bash
SIMPLE_VAR=my_cats_are_beautiful
NAME_ENV_SOME_STRING=my_var_1
NAME_ENV_SOME_PATH=/path/to/data
```


```python
from izienv import BaseEnv, load_env_var, load_izienv

class MyEnv(BaseEnv):
    @property
    @load_env_var_str()
    def SIMPLE_VAR(self) -> str:
        return "SIMPLE_VAR"
    
    @property
    @load_env_var_str(name_left=True)        # Set name_left to add the `NAME_ENV` to the variable.
    def SOME_STRING(self) -> str:
        return "SOME_STRING"
    
    @property
    @load_env_var_path(name_left=True)        # Set name_left to add the `NAME_ENV` to the variable.
    def SOME_PATH(self) -> str:
        return "SOME_PATH"

NAME = 'name_env'
load_izienv(name=NAME, path_envs=Path(".envs"))

# You need .envs/ folder with envs. Or set `path_envs`.
env = MyEnv(name=NAME)
print(env.SIMPLE_VAR)
print(env.SOME_STRING)
print(env.SOME_PATH)
```
