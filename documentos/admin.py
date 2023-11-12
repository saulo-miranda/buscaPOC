from django.contrib import admin

from .models import Documento, Token


class DocumentoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "instituicao")

admin.site.register(Documento, DocumentoAdmin)

class TokenAdmin(admin.ModelAdmin):
    list_display = ("id_token", "termo", "quantidade", "documento")

admin.site.register(Token, TokenAdmin)
