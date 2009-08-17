from django import forms

from localtv import models


class FeedNameForm(forms.ModelForm):
    class Meta:
        model = models.Feed
        fields = ('name')


class FeedAutoCategoriesForm(forms.ModelForm):
    class Meta:
        model = models.Feed
        fields = ('auto_categories')

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['auto_categories'].queryset = \
            self.fields['auto_categories'].queryset.filter(
            site=self.instance.site)


class FeedAutoAuthorsForm(forms.ModelForm):
    class Meta:
        model = models.Feed
        fields = ('auto_authors')

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['auto_authors'].queryset = \
            self.fields['auto_authors'].queryset.filter(
            site=self.instance.site)
