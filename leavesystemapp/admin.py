from django.contrib import admin 
from .models import StudentLeave

# Register your models here.  
class StudentFormAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'roll_number','faculty')
    list_filter = ('roll_number',) 
    
admin.site.register(StudentLeave, StudentFormAdmin)    


