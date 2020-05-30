from django import forms


class AddMovieURLForm(forms.Form):
    url = forms.URLField(max_length=256)
