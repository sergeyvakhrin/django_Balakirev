from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from women.models import Category, Husband


@deconstructible
class RussianValidator:
    """ Делаем кастомный валидатор """
    ALLOWED_CHARS = 'ФЫВФЫВПАЫВАРВАПОПАРОЛРОЛД '
    code = 'russian'


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=5, label='Заголовок',
                            widget=forms.TextInput(attrs={'class': 'form-input'}),
                            error_messages={
                                'min_length': "Слишком короткий заголовок",
                                'required': "Без заголовка ни как",
                            })
    # widget=forms.TextInput(attrs={'class': 'form-input'}) для изменения этого поля ввода
    slug = forms.SlugField(max_length=255, label='URL',
                           validators=[
                               MinLengthValidator(5, message="Минимум 5 символов"),
                               MaxLengthValidator(100, message="Максимум 100 символов")
                           ])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Контент')
    # widget=forms.Textarea() для построчного ввода с заданным размером, required=False не обязательное для заполнения
    is_published = forms.BooleanField(required=False, initial=True, label="Статус")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Не выбрано", label="Категория")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label="Муж", empty_label="Не замужем")


