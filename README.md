# pre-commit-hooks

Some extra pre-commit hooks for Motoinsight.


### Using pre-commit-hooks with pre-commit

Add this to your .pre-commit-config.yaml


```
- repo: git@gitlab.com:motoinsight/infra/pre-commit-hooks.git
  rev: master
  hooks:
  - id: check-const-translations
```


### Hooks available

#### check-const-translations

Checks if all translation function calls have a constant parameter.

Example:

```python
# Contant parameter: Valid

_("This is valid")

# Variable parameter: INVALID

var = "This is invalid"
_(var)

# Function call parameter: INVALID

def func():
    return "This is invalid"

_(func())
```
