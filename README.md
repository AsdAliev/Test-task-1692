# Test-task-1692
Выполнение тестового задания в проект #1692
## Инструкция
1. В файле **.env** введите все необходимые данные для авторизации в Taiga и Вашей базе данных:
```
DB_HOST = ""
DB_DATABASE = ""
DB_PASSWORD = ""
DB_USERNAME = ""
TAIGA_TOKEN = "" _Необязательно_
TAIGA_USERNAME = "" _Необязательно_
TAIGA_PASSWORD = "" _Необязательно_
```
2. Затем запустите следующий код в терминале для запуска:
```
python -m venv venv
pip install -r requirements.txt
python main.py
```

## Вы можете изменить кол-во (x) записей для каждой таблицы в 12-15 строках файла main.py:
```
req.get("users", True, x)
```
