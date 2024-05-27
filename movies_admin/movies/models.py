import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField('id', primary_key=True,
                          default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:  # type: ignore
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('full_name'))

    class Meta:  # type: ignore
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class Type(models.TextChoices):
        MOVIE = 'movie', _('type_movie')
        TV_SHOW = 'tv_show', _('type_tv_show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation_date'), blank=True, null=True)
    rating = models.FloatField(_('rating'), blank=True, validators=[
                               MinValueValidator(0), MaxValueValidator(100)])
    type = models.TextField(_('type'), choices=Type.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:  # type: ignore
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', verbose_name=_(
        'Filmwork'), on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', verbose_name=_(
        'Genre'), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:  # type: ignore
        db_table = "content\".\"genre_film_work"
        verbose_name = _("genre_film_work")
        verbose_name_plural = _("genre_film_works")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "genre"],
                name="film_work_genre_idx",
            )
        ]


class PersonFilmwork(UUIDMixin):
    class Role(models.TextChoices):
        ACTOR = 'actor', _('role_actor')
        DIRECTOR = 'director', _('role_director')
        WRITER = 'writer', _('role_writer')

    film_work = models.ForeignKey('Filmwork', verbose_name=_(
        'Filmwork'), on_delete=models.CASCADE)
    person = models.ForeignKey('Person', verbose_name=_(
        'Person'), on_delete=models.CASCADE)
    role = models.TextField(_('role'), choices=Role.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:  # type: ignore
        db_table = "content\".\"person_film_work"
        verbose_name = _("person_film_work")
        verbose_name_plural = _("person_film_works")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "person", "role"],
                name="film_work_person_role_idx",
            )
        ]
