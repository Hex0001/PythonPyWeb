"""
Заполнение данных в БД через скрипт python.
Для заполнения, достаточно просто запустить скрипт.

Так же приведенные команды в блоке (if __name__ == "__main__":)
можно аналогично выполнить в окружении запускаемом командой
python manage.py shell

В случае вызова консоли (python manage.py shell), то так же как и в
приведенном блоке (if __name__ == "__main__":) необходимо
импортировать модели с которыми будете работать и далее выполнять команды с БД.
"""

import django
import os
from time import time
from json import load
from django.core.exceptions import ValidationError
from datetime import date, datetime
import re
from django.utils import timezone

# Для загрузки данных через script - обязательно нужно прописать эти 2 строки, подгружающие настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Чтение данных с json
with open("data/alter/blogs.json", encoding="utf-8") as f:
    data_blog = load(f)
with open("data/alter/authors.json", encoding="utf-8") as f:
    data_author = load(f)
with open("data/alter/authors_profile.json", encoding="utf-8") as f:
    data_author_profile = load(f)
with open("data/alter/entrys.json", encoding="utf-8") as f:
    data_entry = load(f)
with open("data/alter/tags.json", encoding="utf-8") as f:
    data_tag = load(f)


if __name__ == "__main__":
    from apps.db_train_alternative.models import Blog, Author, AuthorProfile, Entry, Tag

    # ______Работа с объектами таблицы Blog__________
    """Пример записи в БД с последующим сохранением через цикл"""

    t1 = time()
    for data in data_blog:
        Blog.objects.create(**data)
    t2 = time()
    print(f"Записи таблицы 'Blog' успешно созданы. Время создания {len(data_blog)} строк {t2 - t1:.4f} с")


    # ______Работа с объектами таблицы Author__________
    """Если необходимо записать объекты пакетом, то для этих целей существует bulk_create,
    Однако он записывает данные в БД, если это контейнер подготовленных объектов
    к записи, а не сырые данные."""

    t1 = time()
    data_for_write = [Author(**data) for data in data_author]  # Здесь просто создались объекты, записи в БД не было
    Author.objects.bulk_create(data_for_write)  # А здесь произошла пакетная запись в БД
    t2 = time()
    print(f"Записи таблицы 'Author' успешно созданы. Время создания {len(data_for_write)} строк {t2 - t1:.4f} с")

    """
    При использовании Django ORM в Python - скрипте или через оболочку shell,
    встроенные проверки полей моделей автоматически НЕ ВЫПОЛНЯЮТСЯ при сохранении
    объектов в базу данных(Это сделано, чтобы разработчик мог сам выбрать, когда и на что тратить ресурсы при работе с БД). 
    Однако возможно явно вызвать эти проверки и обработать возможные исключения, чтобы убедиться, что данные соответствуют заданным
    ограничениям полей для этого у объекта, который создали для записи необходимо вызвать метод full_clean(). 
    
    Как пример 
    
    obj = Author(**data)
    obj.full_clean()
    
    К сожалению full_clean применяется только к объекту, а не группе объектов, поэтому если объекты в списке, по нужно 
    применить метод к каждому.
    
    """
    # ______ Работа с объектами таблицы AuthorProfile __________
    t1 = time()

    for data in data_author_profile:
        author = Author.objects.get(name=data["author"])
        obj = AuthorProfile(author=author,
                            bio=data["bio"],
                            phone_number=data["phone_number"],
                            city=data["city"])

        obj.full_clean()
        obj.save()

    t2 = time()
    print(f"Записи таблицы 'AuthorProfile' успешно созданы. Время создания {len(data_author_profile)} строк {t2 - t1:.4f} с")

    ## ______ Работа с объектами таблицы Tag __________
    t1 = time()

    for data in data_tag:
        obj = Tag(**data)
        obj.full_clean()
        obj.save()

    t2 = time()
    print(f"Записи таблицы 'Tag' успешно созданы. Время создания {len(data_tag)} строк {t2 - t1:.4f} с")

    ## ______ Работа с объектами таблицы Entry __________
    t1 = time()

    blogs = Blog.objects.all()
    authors = Author.objects.all()
    tags = Tag.objects.all()

    re_split = re.compile(r'[ :-]')  # Паттерн для разделения строк в формате времени
    for entry in data_entry:
        blog = blogs.get(name=entry["blog"])  # Получение объекта Блог
        author = authors.get(name=entry["author"])  # Получение объекта Автор
        tag = tags.filter(id__in=entry["tags"])  # Получение объектов Тэг
        # pub_date в моделях объявлен как DateTimeField, поэтому на вход необходимо подавать объект datetime
        pub_date = datetime(*map(int, re_split.split(entry["pub_date"]))) if \
            entry["pub_date"] is not None else datetime.now()
        pub_date = timezone.make_aware(pub_date)  # добавляем данных о часовом поясе, так как могут быть проблемы с БД и Django
        obj = Entry(blog=blog,
                    headline=entry["headline"],
                    body_text=entry["body_text"],
                    pub_date=pub_date,
                    author=author,
                    number_of_comments=entry["number_of_comments"],
                    number_of_pingbacks=entry["number_of_pingbacks"],
                    rating=entry["rating"] if entry["rating"] is not None else 0.0)

        obj.full_clean()
        obj.save()
        obj.tags.set(tag)  # Запись отношение многое ко многому немного специфичная
        # необходимо сначала сохранить в БД, а затем установить значения отношений

    t2 = time()
    print(f"Записи таблицы 'Entry' успешно созданы. Время создания {len(data_entry)} строк {t2 - t1:.4f} с")