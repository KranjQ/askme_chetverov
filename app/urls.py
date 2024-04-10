from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('questions/<int:question_id>', views.question, name='question'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
    path('tag/<int:tag_id>', views.tag, name='tag'),
    path('settings/', views.settings, name='settings'),
    path('not_auth/', views.not_auth, name='not_auth')
]


