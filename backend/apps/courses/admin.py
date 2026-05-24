from django.contrib import admin

from .models import Course, Lesson, Topic

admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(Lesson)
