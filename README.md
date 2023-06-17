## Практика

Наша задача написать полностью типизированное консольное приложение с проверкой кода при помощи `mypy`.

В качестве основы - берем приложение из домашнее задание из занятия 8 (про список дел).

1. Используем следующие настройки `mypy`

```ini
[mypy]
# mypy configurations: http://bit.ly/2zEl9WI
allow_redefinition = False
check_untyped_defs = True
disallow_any_explicit = True
disallow_any_generics = True
disallow_untyped_calls = True
disallow_incomplete_defs = True
ignore_errors = False
ignore_missing_imports = True
implicit_reexport = False
local_partial_types = True
strict_optional = True
strict_equality = True
no_implicit_optional = True
warn_no_return = True
warn_unused_ignores = True
warn_redundant_casts = True
warn_unused_configs = True
warn_unreachable = True
```

2. Покрываем все функции и методы: параметры и возвращаемые значения
3. Все константы и классы отмечаем как `Final` и `@final` (что допустимо)

Дополнительные задания (необязательные, но можно попробовать):

1. Воспользуйтесь https://github.com/wemake-services/wemake-python-package для генерации пакета
2. Воспользуйтесь https://github.com/dry-python/returns для работы с исключениями и нечистыми операциями
