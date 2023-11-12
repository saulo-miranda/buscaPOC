from django.urls import path
from .views import TesteView, popular_banco, teste_regis

urlpatterns = [
    path("", TesteView.as_view(), name="teste"),
    path("popular-banco/", popular_banco, name="popular_banco"),
    path("teste-busca/", teste_regis, name="teste_busca")  
]