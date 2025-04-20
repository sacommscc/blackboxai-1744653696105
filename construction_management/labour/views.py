from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from django.http import JsonResponse
from .models import Labourer, WorkLog, LabourPayment, LabourType, Skill

@login_required
def labour_list(request):
    """View to list all labourers"""
    labourers = Labourer.objects.all()
    return render(request, 'labour/list.html', {'labourers': labourers})

@login_required
def labour_types_api(request):
    """API view to return labour types as JSON"""
    labour_types = LabourType.objects.all().values('id', 'name', 'description', 'base_daily_wage')
    return JsonResponse(list(labour_types), safe=False)

@login_required
def labour_add(request):
    """View to add a new labourer"""
    if request.method == 'POST':
        try:
            labourer = Labourer(
                name=request.POST['name'],
                cnic=request.POST['cnic'],
                phone=request.POST['phone'],
                address=request.POST['address'],
                labour_type_id=request.POST['labour_type'],
                daily_wage=request.POST['daily_wage'],
                emergency_contact=request.POST['emergency_contact'],
                emergency_phone=request.POST['emergency_phone'],
                joining_date=request.POST['joining_date'],
                is_active=request.POST.get('is_active', False) == 'on',
                notes=request.POST['notes']
            )
            labourer.save()
            
            # Handle skills (many-to-many field)
            skills = request.POST.getlist('skills')
            labourer.skills.set(skills)
            
            messages.success(request, 'Labourer added successfully.')
            return redirect('labour:labour_list')
        except Exception as e:
            messages.error(request, f'Error adding labourer: {str(e)}')
    
    labour_types = LabourType.objects.all()
    skills = Skill.objects.all()
    return render(request, 'labour/form.html', {
        'labour_types': labour_types,
        'skills': skills,
        'action': 'Add'
    })

@login_required
def labour_edit(request, pk):
    """View to edit an existing labourer"""
    labourer = get_object_or_404(Labourer, pk=pk)
    
    if request.method == 'POST':
        try:
            labourer.name = request.POST['name']
            labourer.cnic = request.POST['cnic']
            labourer.phone = request.POST['phone']
            labourer.address = request.POST['address']
            labourer.labour_type_id = request.POST['labour_type']
            labourer.daily_wage = request.POST['daily_wage']
            labourer.emergency_contact = request.POST['emergency_contact']
            labourer.emergency_phone = request.POST['emergency_phone']
            labourer.joining_date = request.POST['joining_date']
            labourer.is_active = request.POST.get('is_active', False) == 'on'
            labourer.notes = request.POST['notes']
            labourer.save()
            
            # Handle skills (many-to-many field)
            skills = request.POST.getlist('skills')
            labourer.skills.set(skills)
            
            messages.success(request, 'Labourer updated successfully.')
            return redirect('labour:labour_list')
        except Exception as e:
            messages.error(request, f'Error updating labourer: {str(e)}')
    
    labour_types = LabourType.objects.all()
    skills = Skill.objects.all()
    return render(request, 'labour/form.html', {
        'labourer': labourer,
        'labour_types': labour_types,
        'skills': skills,
        'action': 'Edit'
    })

@login_required
def labour_delete(request, pk):
    """View to delete a labourer"""
    labourer = get_object_or_404(Labourer, pk=pk)
    
    if request.method == 'POST':
        labourer.delete()
        messages.success(request, 'Labourer deleted successfully.')
        return redirect('labour_list')
    
    return render(request, 'labour/delete.html', {'labourer': labourer})

@login_required
def worklog_list(request):
    """View to list all work logs"""
    work_logs = WorkLog.objects.all()
    return render(request, 'labour/worklog_list.html', {'work_logs': work_logs})

@login_required
def worklog_add(request):
    """View to add a new work log"""
    if request.method == 'POST':
        try:
            work_log = WorkLog(
                labourer_id=request.POST['labourer'],
                work_date=request.POST['work_date'],
                hours_worked=request.POST['hours_worked'],
                description=request.POST['description']
            )
            work_log.save()
            
            # Handle tasks performed (many-to-many field)
            tasks = request.POST.getlist('tasks_performed')
            work_log.tasks_performed.set(tasks)
            
            messages.success(request, 'Work log added successfully.')
            return redirect('labour:worklog_list')
        except Exception as e:
            messages.error(request, f'Error adding work log: {str(e)}')
    
    labourers = Labourer.objects.filter(is_active=True)
    skills = Skill.objects.all()
    return render(request, 'labour/worklog_form.html', {
        'labourers': labourers,
        'skills': skills,
        'action': 'Add'
    })

@login_required
def worklog_edit(request, pk):
    """View to edit an existing work log"""
    work_log = get_object_or_404(WorkLog, pk=pk)
    
    if request.method == 'POST':
        try:
            work_log.labourer_id = request.POST['labourer']
            work_log.work_date = request.POST['work_date']
            work_log.hours_worked = request.POST['hours_worked']
            work_log.description = request.POST['description']
            work_log.save()
            
            # Handle tasks performed (many-to-many field)
            tasks = request.POST.getlist('tasks_performed')
            work_log.tasks_performed.set(tasks)
            
            messages.success(request, 'Work log updated successfully.')
            return redirect('labour:worklog_list')
        except Exception as e:
            messages.error(request, f'Error updating work log: {str(e)}')
    
    labourers = Labourer.objects.filter(is_active=True)
    skills = Skill.objects.all()
    return render(request, 'labour/worklog_form.html', {
        'work_log': work_log,
        'labourers': labourers,
        'skills': skills,
        'action': 'Edit'
    })
