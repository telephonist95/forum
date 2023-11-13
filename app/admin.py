from django.contrib import admin
from .models import Profile, Tag, Reaction, Question, Answer

# Register your models here.

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Reaction)
admin.site.register(Question)
admin.site.register(Answer)

