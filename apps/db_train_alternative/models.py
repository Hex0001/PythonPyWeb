from django.db import models
from datetime import date, datetime
from django.core.validators import RegexValidator

"""
Рассматриваются 4 таблицы условно обобщающие функционал блога
"""


class Blog(models.Model):
    """
    Таблица Блог, содержащая в себе
    name - название блога
    tagline - используется для хранения краткого описания или слогана блога
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    tagline = models.TextField(verbose_name="Слоган")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"


class Author(models.Model):
    """
    Таблица Автор, содержащая в себе
    name - username автора
    email - адрес электронной почты автора
    """

    name = models.CharField(max_length=200, verbose_name="Имя")
    email = models.EmailField(unique=True, verbose_name="Почта")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class AuthorProfile(models.Model):
    """
    Дополнительная информация к профилю, было создано, чтобы показать, как можно
    расширить какую-то модель за счёт использования отношения
    один к одному(OneToOneField).
    author - связь с таблицей автор (один к одному(у автора может быть только один профиль,
    соответственно профиль принадлежит определенному автору))
    bio - текст о себе
    phone_number - номер телефона с валидацией при внесении
    """
    author = models.OneToOneField(Author, on_delete=models.CASCADE)
    bio = models.TextField(blank=True,
                           null=True,
                           help_text="Короткая биография",
                           )

    phone_regex = RegexValidator(
        regex=r'^\+79\d{9}$',
        message="Телефонный номер должен быть следующего формата: '+79123456789'."
    )
    phone_number = models.CharField(validators=[phone_regex],
                                    max_length=12,
                                    blank=True,
                                    null=True,
                                    unique=True,
                                    help_text="Формат +79123456789",
                                    )  # максимальная длина 12 символов
    city = models.CharField(max_length=120,
                            blank=True,
                            null=True,
                            help_text="Город проживания",
                            )

    def __str__(self):
        return self.author.name


class Entry(models.Model):
    """
    Статья блога
    blog - связь с конкретным блогом (отношением "один ко многим" (one-to-many).
        Одна запись блога (Entry) может быть связана с одним конкретным блогом (Blog),
        но блог (Blog) может иметь множество связанных записей блога (Entry))
    headline - заголовок
    body_text - текст статьи
    pub_date - дата и время публикации записи
    mod_date - дата редактирования записи
    author - автор написавший данную статью (отношение "один ко многим")
    number_of_comments - число комментариев к статье
    number_of_pingbacks -  число отзывов/комментариев на других блогах или сайтах,
        связанных с определенной записью блога (Entry)
    rating - оценка статьи
    tags - теги статьи (отношение многие-ко-многим)

    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='entries')
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateTimeField(default=datetime.now)
    mod_date = models.DateField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='entries')
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    tags = models.ManyToManyField('Tag', related_name='entries')

    def __str__(self):
        return self.headline


class Tag(models.Model):
    """
    Тег для статьи
    name - название тега
    slug_name - название в виде slug
    """
    name = models.CharField(max_length=50, verbose_name="Название", unique=True)
    slug_name = models.SlugField(verbose_name="Slug название", unique=True)

    def __str__(self):
        return self.name
