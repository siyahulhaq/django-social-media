from django.contrib import admin
from . import models

# Register your models here.

models = (models.Like, models.Comment, models.Tweet,)
for m in models:
   admin.site.register(m)