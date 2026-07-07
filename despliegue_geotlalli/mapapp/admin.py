from django.contrib.gis import admin
from .models import PuntoCosta, FotoPunto

class FotoPuntoInline(admin.TabularInline):
    model = FotoPunto
    extra = 1

@admin.register(PuntoCosta)
class PuntoCostaAdmin(admin.GISModelAdmin):
    list_display = ('nombre', 'creado')
    search_fields = ('nombre',)
    inlines = [FotoPuntoInline]

@admin.register(FotoPunto)
class FotoPuntoAdmin(admin.ModelAdmin):
    list_display = ('punto', 'leyenda')
