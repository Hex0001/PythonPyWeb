from django.shortcuts import render
from django.views import View
from django.db.models import Q, Max, Min, Avg, Count
from .models import Author, AuthorProfile, Entry, Tag


class TrainView(View):
    def get(self, request):
        # Какие авторы имеют самую высокую уровень самооценки(self_esteem)?
        max_self_esteem = Author.objects.aggregate(max_self_esteem=Max('self_esteem'))
        self.answer1 = Author.objects.filter(self_esteem=max_self_esteem['max_self_esteem'])

        # Какой автор имеет наибольшее количество опубликованных статей?
        self.answer2 = Author.objects.annotate(num_entries=Count('entries')).order_by('-num_entries')[0]

        # Какие статьи содержат тег 'Кино' или 'Музыка' ?
        self.answer3 = Entry.objects.filter(tags__name__in=['Кино', 'Музыка']).distinct()

        # Сколько авторов женского пола зарегистрировано в системе?
        self.answer4 = Author.objects.filter(gender='ж').count()

        # Какой процент авторов согласился с правилами при регистрации?
        self.answer5 = round((Author.objects.filter(status_rule=True).count() / Author.objects.count()) * 100, 2)

        # Какие авторы имеют стаж от 1 до 5 лет?
        self.answer6 = Author.objects.filter(profiles__stage__range=[1, 5])  # В моделях дополнительно
        # добавлен related_name='profiles'

        # Какой автор имеет наибольший возраст?
        self.answer7 = Author.objects.order_by('-age')[0]  # Дополнительно внесены изменения в training_db
        # для правильного отображения

        # Сколько авторов указали свой номер телефона?
        self.answer8 = Author.objects.filter(phone_number__isnull=False).count()

        # Какие авторы имеют возраст младше 25 лет?
        self.answer9 = Author.objects.filter(age__lt=25)

        # Сколько статей написано каждым автором?
        self.answer10 = Author.objects.annotate(count=Count('entries'))

        context = {f'answer{index}': self.__dict__[f'answer{index}'] for index in range(1, 11)}

        return render(request, 'train_db/training_db.html', context=context)
