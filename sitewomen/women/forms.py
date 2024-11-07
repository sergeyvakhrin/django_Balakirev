from django import forms

from women.models import Category, Husband


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # widget=forms.TextInput(attrs={'class': 'form-input'}) для изменения этого поля ввода
    slug = forms.SlugField(max_length=255, label='URL')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Контент')
    # widget=forms.Textarea() для построчного ввода с заданным размером, required=False не обязательное для заполнения
    is_published = forms.BooleanField(required=False, initial=True, label="Статус")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Не выбрано", label="Категория")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label="Муж", empty_label="Не замужем")


