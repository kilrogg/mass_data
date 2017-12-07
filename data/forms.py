# coding: utf-8

from django.forms import ModelForm

from data.models import TestData


class TestDataForm(ModelForm):

    class Meta:
        model = TestData
        exclude = []

    def clean(self):
        return self.cleaned_data
