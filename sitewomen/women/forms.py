from django import forms
from django.forms import ModelForm
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError

from women.models import Category, Husband, Women


# @deconstructible
# class RussianValidator:
#     """ Делаем кастомный валидатор для часто используемых проверок """
#     ALLOWED_CHARS = 'йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ0123456789- '
#     code = 'russian'
#
#     def __init__(self, message=None):
#         self.message = message if message else "Должны быть только русские буквы, дефис или продел"
#
#     def __call__(self, value, *args, **kwargs):
#         if not (set(value) <= set(self.ALLOWED_CHARS)):
#             raise ValidationError(self.message, code=self.code)



class AddPostForm(ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Не выбрано", label="Категория")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label="Муж", empty_label="Не замужем")

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']
        widget = {
            'title': forms.TextInput(attrs={"class": 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {'slug': 'URL'}

    def clean_title(self):
        """ Второй способ валидации данных для частных проверок"""
        title = self.cleaned_data['title']
        ALLOWED_CHARS = 'йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ0123456789- '

        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны быть только русские буквы, дефис или пробел")
        return title

# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, min_length=5, label='Заголовок',
#                             widget=forms.TextInput(attrs={'class': 'form-input'}),
#                             # validators=[
#                             #     RussianValidator(),
#                             # ],
#                             error_messages={
#                                 'min_length': "Слишком короткий заголовок",
#                                 'required': "Без заголовка ни как",
#                             })
#     # widget=forms.TextInput(attrs={'class': 'form-input'}) для изменения этого поля ввода
#     slug = forms.SlugField(max_length=255, label='URL',
#                            validators=[
#                                MinLengthValidator(5, message="Минимум 5 символов"),
#                                MaxLengthValidator(100, message="Максимум 100 символов")
#                            ])
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Контент')
#     # widget=forms.Textarea() для построчного ввода с заданным размером, required=False не обязательное для заполнения
#     is_published = forms.BooleanField(required=False, initial=True, label="Статус")
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Не выбрано", label="Категория")
#     husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label="Муж", empty_label="Не замужем")
#
#     def clean_title(self):
#         """ Второй способ валидации данных для частных проверок"""
#         title = self.cleaned_data['title']
#         ALLOWED_CHARS = 'йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ0123456789- '
#
#         if not (set(title) <= set(ALLOWED_CHARS)):
#             raise ValidationError("Должны быть только русские буквы, дефис или продел")
#         return title


class UploadFileForm(forms.Form):
    """ Форма для загрузки файлов на сервер. Нужна, что бы пустой запрос не падал в ошибку """
    file = forms.FileField(label="Файл")
