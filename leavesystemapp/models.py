from django.db import models 
from django.core.exceptions import ValidationError 

# Create your models here.
class StudentLeave(models.Model):
    roll_number = models.CharField(max_length=6,unique= True) 
    full_name = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    semester = models.PositiveBigIntegerField()
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=100)
    guardian_contact = models.CharField(max_length=20)
    student_contact = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)
    delete_time = models.DateTimeField(null=True, blank=True)
    student_mail = models.EmailField() 
    leave_request_date = models.DateTimeField(auto_now_add=True) 
    
    def clean_end_date(self):
        if self.end_date < self.start_date:
            raise ValidationError("End Date cannot be before Start Date.")
        
    def leave_days_no(self):
        leave_days = self.end_date - self.start_date     
        return (leave_days.days + 1)
     
    
    def __str__(self):
        return self.full_name