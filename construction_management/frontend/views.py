from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from vendors.models import Vendor  # Importing the Vendor model

@login_required
def dashboard(request):
    context = {
        'active_projects_count': 0,
        'active_labourers_count': 0,
        'total_transactions': 0,
        'vendors_count': 0,
    }
    return render(request, 'dashboard.html', context)

@login_required
def vendors_list(request):
    if request.method == 'POST':
        # Logic for adding a new vendor
        name = request.POST.get('name')
        contact_person = request.POST.get('contact_person')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        Vendor.objects.create(name=name, contact_person=contact_person, phone=phone, email=email)
        return redirect('vendors')

    vendors = Vendor.objects.all()
    return render(request, 'vendors/list.html', {'vendors': vendors})

@login_required
def labour_list(request):
    return render(request, 'labour/list.html', {'labourers': []})

@login_required
def transactions_list(request):
    return render(request, 'transactions/list.html', {'transactions': []})

@login_required
def reports_list(request):
    return render(request, 'reports/list.html')
