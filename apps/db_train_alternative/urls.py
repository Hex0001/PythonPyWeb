from django.urls import path
from .views import AuthorREST


urlpatterns = [
    path('author/', AuthorREST.as_view()),
    path('author/<int:id>/', AuthorREST.as_view()),
]