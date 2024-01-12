from django.contrib import admin
from django.urls import path, include
from app1 import views
from app1.views import PostModelAPIView, PostModelAPIViewID
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from app1.views import UserRatingAPIView
# from app1.views import FilteredPostAPIView

from app1.Password import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.indexPage,name='index'),
    path('signup/',views.signupPage,name='signup'),
    path('login/',views.loginPage,name='login'),
    path('get-post/',views.getpostPage,name='get-post'),
    path('help/',views.helpPage,name='help'),
    path('post/',views.postPage,name='post'),
    path('base/',views.basePage,name='base'),
    path('submit/', views.submit_form, name='submit_form'),
    # path('logout/',views.logoutPage,name='logout'),
    path('logout/', views.logout_view, name='logout'),
    path('post/',views.Post,name='post'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('postAPI/',PostModelAPIView.as_view()),
    path('postAPI/<int:id>/',PostModelAPIViewID.as_view()),
    path('chat/messages/<int:user_id>/', views.user_chat_list, name='user_chat_list'),
    path('chat/messages/<int:user_id>/<int:other_user_id>/', views.chat_messages, name='chat_messages'),
    # path('help/filtered_posts/', FilteredPostAPIView.as_view(), name='filter_post'),
    path('chat/user_rating/', UserRatingAPIView.as_view(), name='user_rating'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
