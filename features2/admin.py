from django.contrib import admin
from .models import MyFormModel
from .forms import MyForm

class MyFormAdmin(admin.ModelAdmin):
    form = MyForm

admin.site.register(MyFormModel, MyFormAdmin)

