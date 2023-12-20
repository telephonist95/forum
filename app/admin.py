from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(AnswerReaction)
admin.site.register(QuestionReaction)
