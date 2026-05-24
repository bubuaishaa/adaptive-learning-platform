from django.contrib import admin

from .models import AnswerOption, Question, StudentAnswer, Test, TestAttempt

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(AnswerOption)
admin.site.register(TestAttempt)
admin.site.register(StudentAnswer)
