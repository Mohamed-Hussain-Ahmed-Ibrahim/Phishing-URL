from django.contrib import admin
from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'rate')
  

   

admin.site.register(Feedback, FeedbackAdmin)

