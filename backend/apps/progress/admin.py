from django.contrib import admin

from .models import StudentProgress, TopicProgress

admin.site.register(TopicProgress)
admin.site.register(StudentProgress)
