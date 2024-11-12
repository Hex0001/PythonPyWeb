from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.db_train_alternative.models import Author
from .serializers import AuthorModelSerializer


class AuthorViewSetTestCase(APITestCase):
    fixtures = ['testdata.json']

    def setUp(self):
        print("Создаём данные в БД")
        self.author1 = Author.objects.create(name='John', email='john@example.com')
        self.author2 = Author.objects.create(name='Alice', email='alice@example.com')

    def test_list_authors(self):
        print("Запуск теста test_list_authors")
        print("______________________________")
        print(f'В таблице автор {Author.objects.count()} значения')
        url = reverse('authors-viewset-list')  # Получаем URL ссылку
        print(f"Проверяемы маршрут: {url}")
        response = self.client.get(url)
        print(f"Ответ от сервера: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        authors = Author.objects.all()
        serializer = AuthorModelSerializer(authors, many=True)
        print(f"Сериализатор вернул из БД: {serializer.data}")
        self.assertEqual(response.data['results'], serializer.data)


    def test_retrieve_author(self):
        print("Запуск теста test_retrieve_author")
        print("______________________________")
        url = reverse('authors-viewset-detail', kwargs={'pk': self.author1.pk})  # Укажите имя URL-шаблона и параметры
        print(f"Проверяемы маршрут: {url}")
        response = self.client.get(url)
        print(f"Ответ от сервера: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        author = Author.objects.get(pk=self.author1.pk)
        serializer = AuthorModelSerializer(author)
        print(f"Сериализатор вернул из БД: {serializer.data}")
        self.assertEqual(response.data, serializer.data)

    def test_create_author(self):
        print("Запуск теста test_create_author")
        print("______________________________")
        url = reverse('authors-viewset-list')  # Получаем URL ссылку
        print(f"Проверяемы маршрут: {url}")
        data = {'name': 'Bob', 'email': 'bob@example.com'}
        response = self.client.post(url, data)
        print(f"Ответ от сервера: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        author = Author.objects.get(name='Bob')
        serializer = AuthorModelSerializer(author)
        print(f"Сериализатор вернул из БД: {serializer.data}")
        self.assertEqual(response.data, serializer.data)

    def test_update_author(self):
        print("Запуск теста test_update_author")
        print("______________________________")
        url = reverse('authors-viewset-detail', kwargs={'pk': self.author1.pk})
        print(f"Проверяемы маршрут: {url}")
        data = {'name': 'John Doe', 'email': 'john.doe@example.com'}
        response = self.client.put(url, data)
        print(f"Ответ от сервера: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        author = Author.objects.get(pk=self.author1.pk)
        serializer = AuthorModelSerializer(author)
        print(f"Сериализатор вернул из БД: {serializer.data}")
        self.assertEqual(response.data, serializer.data)

    def test_partial_update_author(self):
        print("Запуск теста test_partial_update_author")
        print("______________________________")
        url = reverse('authors-viewset-detail', kwargs={'pk': self.author1.pk})
        print(f"Проверяемы маршрут: {url}")
        data = {'name': 'John Doe'}
        response = self.client.patch(url, data)
        print(f"Ответ от сервера: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        author = Author.objects.get(pk=self.author1.pk)
        serializer = AuthorModelSerializer(author)
        print(f"Сериализатор вернул из БД: {serializer.data}")
        self.assertEqual(response.data, serializer.data)

    def test_delete_author(self):
        print("Запуск теста test_delete_author")
        print("______________________________")
        url = reverse('authors-viewset-detail', kwargs={'pk': self.author1.pk})
        print(f"Проверяемы маршрут: {url}")
        response = self.client.delete(url)
        print(f"Ответ от сервера: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Author.objects.filter(pk=self.author1.pk).exists())  # Проверка, что теперь этого автора не существует
