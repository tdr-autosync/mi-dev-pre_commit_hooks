# pre-commit-hooks

### check-const-translations

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
