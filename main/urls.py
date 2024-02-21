from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.handlesignup, name='signup'),
    path('home/', views.index, name='home'),
    path('newSheet/', views.subjects_adder, name='add_subjects'),
    path('log_attendance/<int:subject_id>/', views.log_attendance, name='log_attendance'),
    path('support/', views.support_page, name='support_page'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('new/', views.create_new_table, name='create_new_table'),
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
]