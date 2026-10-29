# Учебный проект на Django
## Быстрый старт (Windows)
```powershell
python -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

***
## Команды для работы с проектом

### Содержание

- [Создание и активация виртуального окружения](#создание-и-активация-виртуального-окружения)
- [Установка зависимостей](#установка-зависимостей)
- [Создание проекта Django](#создание-проекта-django)
- [Создание приложения](#создание-приложения)
- [Запуск сервера](#запуск-сервера)
- [Работа с миграциями](#работа-с-миграциями)
- [Создание суперпользователя](#создание-суперпользователя)
- [Создания файла зависимостей](#создания-файла-зависимостей)


### Создание и активация виртуального окружения:
#### Windows
```powershell
python -m venv .venv # создание
.venv\Scripts\activate # активация
```

***Если не сработала активация на Windows:***
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```
#### Mac/Linux
```sh
python3 -m venv .venv # создание
source .venv/bin/activate # активация
```

### Установка зависимостей (из файла):
```sh
pip install -r requirements.txt
```
#### Если нужно установить зависимости самостоятельно:
```sh
pip install django pillow
```

### Создание проекта 
```sh
django-admin startproject myshop .
```

`django-admin` - обращение к фреймворку
`startproject` - создать проект
`myshop` - название проекта
`.` - текущая директория (чтобы создалось прям тут, а не в отдельной подпапке)

### Создание приложения
```sh
python manage.py startapp products
```

`manage.py` - утилита управления
`startapp` - создание приложения
`products` - название приложения

### Запуск сервера
```sh
python manage.py runserver
```

Сервер доступен по адресу http://127.0.0.1:8000

### Создание файлов миграций и их применение к базе данных
```sh
python manage.py makemigrations # создание
python manage.py migrate # применение
```

### Создание суперпользователя
```sh
python manage.py createsuperuser
```
**Внимание**: при вводе пароля он **НЕ** отображается в строке ввода, это нормальное поведение

### Создания файла зависимостей
```sh
pip freeze > requirements.txt 
```

После этого можно удалять виртуальное окружение
Это нужно делать **ОБЯЗАТЕЛЬНО** перед отправкой работы!