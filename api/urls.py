from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.ApiOverview, name='api_home'),
    path('create/', views.add_documentos, name='add-items'),
    path('all/', views.view_documentos, name='view_items'),
    path('update/<int:pk>/', views.update_documentos, name='update-items'),
    path('documento/<int:pk>/delete/', views.delete_documents, name='delete-items'),
]