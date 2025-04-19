from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_POST
import logging
import json

logger = logging.getLogger(__name__)

@ensure_csrf_cookie
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Debug logging
        logger.info("=== Login Attempt Debug Info ===")
        logger.info(f"Email: {email}")
        logger.info(f"Password length: {len(password) if password else 0}")
        logger.info(f"POST data: {json.dumps(dict(request.POST))}")
        logger.info(f"CSRF Cookie: {request.COOKIES.get('csrftoken')}")
        logger.info(f"CSRF Header: {request.META.get('HTTP_X_CSRFTOKEN')}")
        
        # Try both username and email fields for authentication
        user = authenticate(request, username=email, password=password)
        if user is None:
            user = authenticate(request, email=email, password=password)
            
        logger.info(f"Authentication result: {user}")
        if user:
            logger.info(f"User details - Active: {user.is_active}, Staff: {user.is_staff}, Superuser: {user.is_superuser}")
        
        if user is not None:
            if user.is_active:
                login(request, user)
                logger.info(f"Successful login for user: {user.email}")
                
                next_url = request.GET.get('next', '/')
                logger.info(f"Redirecting to: {next_url}")
                
                return redirect(next_url)
            else:
                logger.warning(f"Inactive user attempted login: {email}")
                messages.error(request, 'Your account is inactive.')
        else:
            logger.warning(f"Failed login attempt for email: {email}")
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'registration/login.html')

from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["POST", "GET"])
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/login/?logged_out=1')
    elif request.method == "GET":
        # Redirect GET logout requests to login with message
        return redirect('/login/?message=Please use the logout button to log out properly.')
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])
