# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Asr(models.Model):
    filename = models.FileField(upload_to='./audio/')
    text1 = models.TextField()
    text2 = models.TextField()
    text3 = models.TextField()
    text4 = models.TextField()
    text5 = models.TextField()
    text6 = models.TextField()
    text7 = models.TextField()

    def __unicode__(self):
        return self.filename
