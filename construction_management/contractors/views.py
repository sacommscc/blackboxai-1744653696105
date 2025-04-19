from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.http import require_http_methods
import json
from .models import Contractor, ContractorPayment
from transactions.models import Project

@login_required
@require_http_methods(["GET", "POST"])
def contractor_list_create(request):
    if request.method == "GET":
        contractors = Contractor.objects.all()
        data = []
        for contractor in contractors:
            data.append({
                'id': contractor.id,
                'name': contractor.name,
                'company_name': contractor.company_name,
                'contact_person': contractor.contact_person,
                'phone': contractor.phone,
                'email': contractor.email,
                'specialization': contractor.specialization,
                'rate_per_day': str(contractor.rate_per_day),
                'is_active': contractor.is_active,
                'projects': [{'id': p.id, 'name': p.name} for p in contractor.projects.all()]
            })
        return JsonResponse(data, safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            contractor = Contractor.objects.create(
                name=data['name'],
                company_name=data.get('company_name', ''),
                contact_person=data['contact_person'],
                phone=data['phone'],
                email=data.get('email', ''),
                address=data['address'],
                specialization=data['specialization'],
                rate_per_day=data['rate_per_day'],
                is_active=data.get('is_active', True)
            )
            
            # Add projects if provided
            if 'projects' in data:
                project_ids = data['projects']
                projects = Project.objects.filter(id__in=project_ids)
                contractor.projects.set(projects)
            
            return JsonResponse({
                'id': contractor.id,
                'name': contractor.name,
                'message': 'Contractor created successfully'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_http_methods(["GET", "PUT", "DELETE"])
def contractor_detail(request, pk):
    contractor = get_object_or_404(Contractor, pk=pk)
    
    if request.method == "GET":
        data = {
            'id': contractor.id,
            'name': contractor.name,
            'company_name': contractor.company_name,
            'contact_person': contractor.contact_person,
            'phone': contractor.phone,
            'email': contractor.email,
            'address': contractor.address,
            'specialization': contractor.specialization,
            'rate_per_day': str(contractor.rate_per_day),
            'is_active': contractor.is_active,
            'projects': [{'id': p.id, 'name': p.name} for p in contractor.projects.all()]
        }
        return JsonResponse(data)
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            contractor.name = data.get('name', contractor.name)
            contractor.company_name = data.get('company_name', contractor.company_name)
            contractor.contact_person = data.get('contact_person', contractor.contact_person)
            contractor.phone = data.get('phone', contractor.phone)
            contractor.email = data.get('email', contractor.email)
            contractor.address = data.get('address', contractor.address)
            contractor.specialization = data.get('specialization', contractor.specialization)
            contractor.rate_per_day = data.get('rate_per_day', contractor.rate_per_day)
            contractor.is_active = data.get('is_active', contractor.is_active)
            
            if 'projects' in data:
                project_ids = data['projects']
                projects = Project.objects.filter(id__in=project_ids)
                contractor.projects.set(projects)
            
            contractor.save()
            return JsonResponse({'message': 'Contractor updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == "DELETE":
        try:
            contractor.delete()
            return JsonResponse({'message': 'Contractor deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_http_methods(["GET", "POST"])
def contractor_payments(request, contractor_id):
    contractor = get_object_or_404(Contractor, pk=contractor_id)
    
    if request.method == "GET":
        payments = contractor.payments.all()
        data = []
        for payment in payments:
            data.append({
                'id': payment.id,
                'amount': str(payment.amount),
                'payment_date': payment.payment_date.strftime('%Y-%m-%d'),
                'payment_method': payment.payment_method,
                'transaction_id': payment.transaction_id,
                'project': {'id': payment.project.id, 'name': payment.project.name},
                'description': payment.description
            })
        return JsonResponse(data, safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            project = get_object_or_404(Project, pk=data['project_id'])
            
            payment = ContractorPayment.objects.create(
                contractor=contractor,
                project=project,
                amount=data['amount'],
                payment_date=data['payment_date'],
                payment_method=data['payment_method'],
                transaction_id=data.get('transaction_id'),
                description=data.get('description', '')
            )
            
            return JsonResponse({
                'id': payment.id,
                'message': 'Payment recorded successfully'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
