from django.urls import path, re_path 
from .views import *
urlpatterns = [
    path('',index,name='todo'),
    path('task/add/', task_add),
    path('task/done/',task_done),
    path('task/undone/',task_undone),
    path('task/delete/',task_del),
    path('project/add/', project_add),
    path('project/delete/', project_del),
    path('project/change_type/', project_chg_type),
]