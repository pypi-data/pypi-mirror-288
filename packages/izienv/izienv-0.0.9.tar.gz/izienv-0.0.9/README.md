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
NAME_ENV_VAR_1=my_var_1
NAME_ENV_VAR_2=my_var_2
```


```python
from izienv import BaseEnv, load_env_var, load_izienv

class MyEnv(BaseEnv):
    @property
    @load_env_var()
    def SIMPLE_VAR(self) -> str:
        return "SIMPLE_VAR"
    
    @property
    @load_env_var(name_pre=True)        # Set name_pre to add the `NAME_ENV` to the variable.
    def VAR_1(self) -> str:
        return "VAR_1"
    
    @property
    @load_env_var(name_pre=True)        # Set name_pre to add the `NAME_ENV` to the variable.
    def VAR_2(self) -> str:
        return "VAR_2"

NAME = 'name_env'
load_izienv(name=NAME, path_envs=Path(".envs"))

# You need .envs/ folder with envs. Or set `path_envs`.
env = MyEnv(name=NAME)
print(env.SIMPLE_VAR)
print(env.VAR_1)
print(env.VAR_2)
```
