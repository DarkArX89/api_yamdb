**Проект "Api для проекта Yatube"**

В данном проекте создано API для взаимодействия с сайтом Yatube - социальной сетью для публикации и чтения дневников пользователей.

В проекте применены технологии для реализации следующих задач:
1. Просмотр контента сайта открыт любому пользователю, доступ к контенту предоставляется только авторизованным пользователям. Регистрация новых пользователей и их последующая аутентификация выполняется с использованием токена, проверка прав доступа выполняется как на уровне проекта так и на уровне отдельных классов и функций. Изменение или удаление контента других пользователей запрещено. 

2. При создании запроса о подписках к API возможен поиск по имени автора.

3. Доступна пагинация - выдача результатов запроса настраивается по количеству объектов и с какого по счету объекта ее начать.



**Как запустить проект:**

Клонировать репозиторий и перейти в него в командной строке: 

```
git clone git@github.com:Shubarina/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

    python3 manage.py migrate

Запустить проект:

    python3 manage.py runserver