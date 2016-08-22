#!/usr/bin/python
# -*- coding=utf-8 -*-

from django import forms
from assets import models
class Assetmoelsform(forms.ModelForm):
    class Meta:
        model = models.Asset
        exclude = ()

class servermoelsform(forms.ModelForm):
    class Meta:
        model = models.Server
        exclude = ()
