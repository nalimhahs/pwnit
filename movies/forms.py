from django import forms


class AddMovieURLForm(forms.Form):
    url = forms.URLField(max_length=256)


class MovieSearchForm(forms.Form):
    query = forms.CharField(max_length=50)
