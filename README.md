# pre-commit-hooks

Some extra pre-commit hooks for Motoinsight.


### Using pre-commit-hooks with pre-commit

Add this to your .pre-commit-config.yaml


```
- repo: https://github.com/unhaggle/pre-commit-hooks
  rev: master
  hooks:
  - id: check-const-translations
    language_version: python3
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
