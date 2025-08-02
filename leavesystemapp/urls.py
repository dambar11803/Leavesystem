from django.urls import path 
from . views import *

urlpatterns = [
    path('', home, name='home'),
    path('student-leave/', student_leave, name='student_leave'),
    path('recycle/', recycle, name='recycle'),
    path('delete/<int:id>', delete_data, name='delete_data'), 
    path('restore/<int:id>', restore, name='restore'),
    path('restore-all/', restore_all, name='restore_all'),
    path('edit-leave/<int:id>', edit_leave, name='edit_leave'),
    path('delete-all/', delete_all, name='delete_all'),
]
