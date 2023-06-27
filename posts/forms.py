from django import forms
from .models import PostModel, ImagePostModel
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


ImageFormSet = inlineformset_factory(PostModel, ImagePostModel, form=ImagePostForm,
                                         formset=BaseInlineFormSet, extra=3, max_num=10,
                                         validate_max=True, can_delete=True)
