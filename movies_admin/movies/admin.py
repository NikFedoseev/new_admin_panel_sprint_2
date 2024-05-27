from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'modified')
    search_fields = ('name', 'id')


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 1


class PersonFilmworkAdmin(admin.TabularInline):
    model = PersonFilmwork
    extra = 1


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkAdmin)

    list_display = ('title', 'type', 'creation_date',
                    'rating', 'created', 'modified')
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',  'created', 'modified')
    search_fields = ('full_name', 'id')
