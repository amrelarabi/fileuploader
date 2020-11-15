from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('my_files', views.Myfiles.as_view(), name='my_files'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('download_file/<int:file_id>', views.download_file, name='download_file'),
    path('delete_file/<int:file_id>', views.delete_file, name='delete_file'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('login', views.login_view, name='login'),
    path('edit_account', views.edit_account, name='edit_account'),
    path('logout', views.logout_view, name='logout'),
    path('social-auth/', include('social_django.urls', namespace="social")),
]