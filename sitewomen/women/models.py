from django.urls import reverse
from django.db import models
# from django.template.defaultfilters import slugify
from pytils.translit import slugify # для корректного создания слаг
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, validators=[
                               MinLengthValidator(5, message="Минимум 5 символов"),
                               MaxLengthValidator(100, message="Максимум 100 символов")
                           ])
    content = models.TextField(blank=True, verbose_name='Статья')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    cat = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Тэг')
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='women')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Известная женщина"
        verbose_name_plural = "Известные женщини"
        ordering = ['-time_create'] # сортировка по убыванию по умолчанию дял проекта
        indexes = [                 # индексирование записей для ускорения выполнения запросов
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        """ Для передачи в форме и перехода на сайт с админки """
        return reverse('post', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        """ Для авто заполнения поля slug """
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name='Тэг')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name
