from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(max_length=200,
                             widget=forms.Textarea(
                                 attrs={'class': 'form-control form-control-sm', 'rows': 1}))