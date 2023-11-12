from django.urls import path
from .views import (
    DocumentoListView,
    DocumentoDetailView,
    DocumentoUpdateView,
    DocumentoDeleteView,
    DocumentoCreateView,
    buscar
)

urlpatterns = [
    path("", DocumentoListView.as_view(), name="documento_list"),
    path("<int:pk>/", DocumentoDetailView.as_view(), name="documento_detail"), # new
    path("<int:pk>/edit/", DocumentoUpdateView.as_view(), name="documento_edit"), # new
    path("<int:pk>/delete/", DocumentoDeleteView.as_view(), name="documento_delete"),
    path("new/", DocumentoCreateView.as_view(), name="documento_new"),
    path("buscar/", buscar, name="buscar"),
]