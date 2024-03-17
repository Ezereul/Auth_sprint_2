from django.contrib import admin

from movies.models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork, User


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    extra = 1
    autocomplete_fields = ["person"]
    fields = ("person", "role")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "modified")


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = ("title", "type", "creation_date", "rating", "created", "modified")
    list_filter = ("type", "genres")
    search_fields = ("title", "description", "id")
    empty_value_display = "-empty-"


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "created", "modified")
    search_fields = ("full_name",)
