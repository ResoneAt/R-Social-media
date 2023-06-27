from django import forms
from .models import PostModel, ImagePostModel, CommentModel
from django.forms.models import inlineformset_factory, BaseInlineFormSet


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = PostModel
        fields = ['body', 'location']


class MultipleFileInput(forms.ClearableFileInput):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs['multiple'] = True


class ImagePostForm(forms.ModelForm):
    class Meta:
        model = ImagePostModel
        fields = ['image', 'alt']
        widgets = {
            'image': MultipleFileInput()
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control form-control-sm ', 'rows': 1,
                                          'style': 'margin:16px; width:80%;'})
        }
