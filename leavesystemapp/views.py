from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_date
from .models import StudentLeave 
from datetime import timedelta, datetime  
from django.core.exceptions import ValidationError  
from django.contrib import messages 


# Dashboard
from django.db.models import Q
from django.shortcuts import render
from .models import StudentLeave

def home(request):
    searched = request.GET.get('searched')
    category = request.GET.get('category')

    if searched:
        if category == 'full_name':
            students = StudentLeave.objects.filter(full_name__icontains=searched)
        elif category == 'roll_number':
            students = StudentLeave.objects.filter(roll_number__icontains=searched)
        else:
            students = StudentLeave.objects.filter(
                Q(full_name__icontains=searched) |
                Q(faculty__icontains=searched),
                is_delete=False
            )
    else:
        students = StudentLeave.objects.filter(is_delete=False)

    return render(request, 'main/home.html', {'students': students})


# Add student leave
def student_leave(request):
    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        full_name = request.POST.get('full_name')
        faculty = request.POST.get('faculty')
        semester = request.POST.get('semester')
        reason = request.POST.get('reason')

        # Safely parse dates (convert '' to None)
        start_date_raw = request.POST.get('start_date')
        end_date_raw = request.POST.get('end_date')
        start_date = parse_date(start_date_raw) if start_date_raw else None
        end_date = parse_date(end_date_raw) if end_date_raw else None

        leave_type = request.POST.get('leave_type')
        guardian_contact = request.POST.get('guardian_contact')
        student_contact = request.POST.get('student_contact')
        student_mail = request.POST.get('student_mail')

        # Save the data to the model
        StudentLeave.objects.create(
            roll_number=roll_number,
            full_name=full_name,
            faculty=faculty,
            semester=semester,
            reason=reason,
            start_date=start_date,
            end_date=end_date,
            leave_type=leave_type,
            guardian_contact=guardian_contact,
            student_contact=student_contact,
            student_mail=student_mail,
        )
        messages.success(request, "Your leave application is submitted.")

        return redirect('home')

    return render(request, 'main/leave_form.html')


# Soft-delete a record
def delete_data(request, id):
    data = get_object_or_404(StudentLeave, id=id)
    data.is_delete = True
    data.delete_time = timezone.now()  # use timezone-aware datetime
    data.save()
    return redirect('home')


# Recycle bin – permanently remove soft-deleted items older than 30 days
def recycle(request):
    # Show soft-deleted data
    data = StudentLeave.objects.filter(is_delete=True)

    # Determine threshold for permanent deletion
    threshold = datetime.now() - timedelta(days=20)

    # Records that are soft-deleted and older than 30 days
    expired = StudentLeave.objects.filter(
        is_delete=True,
        delete_time__lt = threshold  # use __lt (less than)
    )

    deleted_count = expired.count()

    if deleted_count > 0:
        expired.delete()  # hard delete permanently
    else:
        print("No expired soft-deleted records.")

    return render(request, 'main/recycle.html', {'data': data})

#Restore the Students 
def restore(request, id): 
    to_restore_data = StudentLeave.objects.get(id = id) 
    to_restore_data.is_delete = False 
    to_restore_data.save() 
    return redirect('home')

##Restore All
def restore_all(request):
    StudentLeave.objects.filter(is_delete= True).update(is_delete = False) 
    return redirect('home')   

##Edit 
def edit_leave(request, id):
    student = get_object_or_404(StudentLeave, id=id)
    
    if request.method == 'POST':
        # Get all the form data
            full_name = request.POST.get('full_name')
            roll_number = request.POST.get('roll_number')
            faculty = request.POST.get('faculty')
            semester = request.POST.get('semester')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            reason = request.POST.get('reason')
            student_contact = request.POST.get('student_contact')
            
            if start_date > end_date:
                raise ValidationError("End date must be after start date")
            
            # Update the student object
            student.full_name = full_name
            student.roll_number = roll_number
            student.faculty = faculty
            student.semester = semester
            student.start_date = start_date
            student.end_date = end_date
            student.reason = reason
            student.student_contact = student_contact
            
            #save the data
            student.save() 
            messages.success(request, 'Leave Request updated Successfully!!!')
            return redirect('home') 
    return render(request, 'main/edit_student_leave.html', {'student':student})    

#Delete All 
def delete_all(request): 
    StudentLeave.objects.filter(is_delete= False).update(is_delete = True) 
    return redirect('home')
            
            
            
        
        
        
    
