from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ask', views.ask, name='ask'),
    path('hot', views.hot, name='hot'),
    path('login', views.login, name='login'),
    path('question/<int:question_id>', views.question, name='question'),
    path('settings', views.settings, name='settings'),
    path('signup', views.signup, name='signup'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
]
