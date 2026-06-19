from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('workout/', views.workout, name='workout'),
    path('diet/', views.diet, name='diet'),
    path('weight/', views.weight, name='weight'),
    path('photos/', views.photos, name='photos'),
    path('delete-workout/<int:id>/', views.delete_workout, name='delete_workout'),
    path('delete-diet/<int:id>/', views.delete_diet, name='delete_diet'),
    path('delete-weight/<int:id>/', views.delete_weight, name='delete_weight'),
    path('delete-photo/<int:id>/', views.delete_photo, name='delete_photo'),
    path('bmi/', views.bmi, name='bmi'),
    path('report/', views.download_report, name='report'),
    path('report/', views.report, name='report'),
]