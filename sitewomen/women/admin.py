from django.contrib import admin, messages

from women.models import Women, Category


class MarriedFilter(admin.SimpleListFilter):
    """ Клас для кастомных фильтров """
    title = "Статус женщины" # название фильтра
    parameter_name = "status" # название переменной для строки ввода

    def lookups(self, request, model_admin):
        """ Для отображения в админке """
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
        ]

    def queryset(self, request, queryset):
        """ Логика работы кастомного фильтра """
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        if self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'slug', 'cat', 'husband', 'tags'] # для ограничения выводимых полей карточки
    # exclude = ['tag', 'is_published'] # исключает поля для вывода
    readonly_fields = ['slug'] # для отображения, но запрета редактирования

    # prepopulated_fields = {'slug': ('title', )} # второй способ автоматического формирования slug
    # без изменения save(). Работает только если поле slug редактируемое.
    # Либо для авто заполнения других полей на основе других оплей

    filter_horizontal = ['tags'] # более удобное отображение множественного выбора
    # filter_vertical = ['tags'] # более удобное отображение множественного выбора

    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info') # вывод в таблицу
    list_display_links = ('title', 'time_create', ) # сделать кликабельным
    ordering = ['-time_create', 'title', ] # добавить сортировку
    list_editable = ['is_published'] # добавить возможность редактирования
    list_per_page = 10 # кол-во записей на страницу
    actions = ['set_published', 'set_draft'] # дополнительные действия с записями
    search_fields = ['title', 'cat__name'] # добавляем поиск по записям
    list_filter = [MarriedFilter, 'cat__name', 'is_published'] # добавляем фильтрацию кастомную и встроенную

    @admin.display(description='Краткое описание', ordering='content')
    def brief_info(self, women: Women):
        """ Вывод дополнительного поля """
        return f'Описание {len(women.content)} символов.'

    @admin.action(description='Сделать опубликованными')
    def set_published(self, request, queryset):
        """ Логика дополнительного действия """
        count = queryset.update(is_published=True)
        self.message_user(request, f'Изменено {count} записей')

    @admin.action(description='Снять с публикации')
    def set_draft(self, request, queryset):
        """ Логика дополнительного действия """
        count = queryset.update(is_published=False)
        self.message_user(request,f'Изменено {count} записей', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ['name']

# admin.site.register(Women, WomenAdmin)
