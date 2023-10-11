from django import forms
from .models import PostModel, CommentModel
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from ckeditor.widgets import CKEditorWidget


class CreatePostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget(config_name='awesome_ckeditor'))

    class Meta:
        model = PostModel
        fields = ['image', 'body', 'location']


class MultipleFileInput(forms.ClearableFileInput):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs['multiple'] = True


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control form-control-sm ', 'rows': 1,
                                          'style': 'margin:16px; width:80%;'})
        }
