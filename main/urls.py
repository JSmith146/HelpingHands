from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index),                              #
    path('register', views.register),                   
    path('login', views.login),                         
    path('dashboard', views.job_dashboard),
    path('addJob', views.new_job_form),
    path('create_job',views.create_job),
    path('view/<int:id>', views.show_job),
    path('edit/<int:id>', views.edit_job_form),
    path('edit_job/<int:id>', views.edit_job),
    path('add_job/<int:id>',views.add_job),
    path('destroy/<int:id>', views.delete),
    path('remove/<int:id>', views.remove),
    path('logout', views.logout)
]