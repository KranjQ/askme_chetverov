from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('questions/<int:question_id>', views.question, name='question'),
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
    path('tag/<int:tag_id>', views.tag, name='tag'),
    path('profile/edit', views.settings, name='settings'),
    path('not_auth/', views.not_auth, name='not_auth'),
    path('<int:question_id>/like_async', views.like_async, name='like_async'),
    path('hot/<int:question_id>/like_async', views.like_async_hot, name='like_async'),
    path('questions/<int:answer_id>/like_async_answer', views.like_async_answer, name='like_async_answer'),
    path('questions/<int:answer_id>/checkbox_async_answer', views.checkbox_async_answer, name='check_async_answer'),
    path('logout', views.logout_user, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
