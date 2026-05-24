from django.contrib import admin

from .models import LearningPath, LearningPathStep, Recommendation

admin.site.register(Recommendation)
admin.site.register(LearningPath)
admin.site.register(LearningPathStep)
