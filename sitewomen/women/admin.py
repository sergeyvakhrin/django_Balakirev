from django.contrib import admin, messages

from women.models import Women, Category


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info') # вывод в таблицу
    list_display_links = ('title', 'time_create', ) # сделать кликабельным
    ordering = ['-time_create', 'title', ] # добавить сортировку
    list_editable = ['is_published'] # добавить возможность редактирования
    list_per_page = 4 # кол-во записей на страницу
    actions = ['set_published', 'set_draft'] # дополнительные действия с записями
    search_fields = ['title', 'cat__name'] # добавляем поиск по записям
    list_filter = ['cat__name', 'is_published'] # добавляем фильтрацию

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
