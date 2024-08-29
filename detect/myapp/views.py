from django.http import JsonResponse
from rest_framework.decorators import api_view

from django.shortcuts import render, redirect
from . forms import RegisterUserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from . models import Stick, StickInfo
from rest_framework import status
from . forms import StickInfoForm
from rest_framework.response import Response



@api_view(['GET'])
def get_product_info(request, pk):
    try:
        stick = Stick.objects.get(stick_id=pk)
    except Stick.DoesNotExist:
        return Response({'error': 'Stick not found'}, status=status.HTTP_404_NOT_FOUND)

    stick_info = StickInfo.objects.filter(stick=stick)
    
    if not stick_info.exists():
        return Response({'error': 'Stick information not found'}, status=status.HTTP_404_NOT_FOUND)

    info = stick_info[0]
    location_field = info.final_destinations
    location_list = [item.strip() for item in location_field.split(',')]
    
    # Assuming you want to return all StickInfo data as JSON
    stick_info_data = {
        'owner_name': info.owner_name,  # Replace with actual fields
        'emergency_contact': info.emergency_contact,  # Replace with actual fields
        'starting_location': info.starting_location,  # Replace with actual fields
        'final_destinations': location_list,  # Replace with actual fields
        # Add more fields as needed
    }
    return Response(stick_info_data, status=status.HTTP_200_OK)


def register(request):
    form = RegisterUserForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            form.save()
            
            return redirect("login")
        
    context = {
        'form' : form
    }
    return render(request, "register.html", context)


def login_(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            
            messages.warning(request, "Username or Password is incorrect")
            return redirect("login")
        
        messages.warning(request, "User does not exist")
        return redirect('login')

    return render(request, "login.html")


@login_required(login_url="login")
def dashboard(request):
    if request.method == "POST":
        device_id = request.POST.get("device_number")
        print(device_id)
        sticks = Stick.objects.filter(stick_id=device_id)
        
        if sticks.exists():
            stick = sticks[0]
            return redirect("product_setup", pk=stick.stick_id)
        else:
            messages.warning(request, "No stick with that number exist")
        
    return render(request, "index.html")


@login_required(login_url="login")
def product_setup(request, pk):
    stick = Stick.objects.get(stick_id=pk)
    stickInfo = StickInfo.objects.filter(stick=stick)
    
    if stickInfo.exists():
        form = StickInfoForm(request.POST or None, instance=stickInfo[0])
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Information saved successfully")
                return redirect("dashboard")
            else:
                messages.warning(request, "Something went wrong, Please try again")
                return redirect("product_setup", pk=pk)
    else:
        form = StickInfoForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                curr = form.save(commit=False)
                curr.stick = stick
                curr.save()
            
                messages.success(request, "Information saved successfully")
                return redirect("dashboard")
            else:
                messages.warning(request, "Something went wrong, Please try again")
                return redirect("product_setup", pk=pk)
    
    context = {
        'form' : form,
    }
    return render(request, 'forms.html', context)


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect("login")