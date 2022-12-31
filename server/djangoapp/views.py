from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .models import CarModel
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return redirect('djangoapp:index')

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username,first_name=firstname, last_name=lastname, password=password)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/registration.html', context)

def get_aboutus(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

def get_contactus(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/80dba8ac-9699-4879-a3ff-49b1c42351e5/dealership-package/get-dealership.json"
        # Get dealers from the URL
        context['dealers'] = get_dealers_from_cf(url)
        return render(request,'djangoapp/index.html', context)

def get_dealer_details(request, dealer_id, dealer_name):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/80dba8ac-9699-4879-a3ff-49b1c42351e5/review-package/get-review.json"
        # Get dealers from the URL
        context['reviews'] = get_dealer_reviews_from_cf(url,dealer_id=dealer_id)
        context['dealer'] = dealer_name
        return render(request,'djangoapp/dealer_details.html', context)

def add_review(request, dealer_id, dealer_name):
    if request.method == "GET":
        context = {}
        context['dealer'] = dealer_name
        cars = CarModel.objects.filter(id=int(dealer_id)).all()
        context['cars'] = cars
        return render(request, 'djangoapp/add_review.html',context)
    if request.method == "POST" and request.user.is_authenticated:
        car = CarModel.objects.get(pk=int(request.POST['car']))
        json_payload = {
            'dealership':dealer_id,
            'name': request.user.username,
            'review': request.POST['review'],
            'purchase': bool(request.POST.get('purchase',False)),
            'car_make': car.car_make.name,
            'car_model': car.name,
            'car_year': car.year.strftime("%Y"),
            'purchase_date': datetime.strptime(request.POST['date'], "%m/%d/%Y").isoformat()
        }
        url= "https://us-south.functions.appdomain.cloud/api/v1/web/80dba8ac-9699-4879-a3ff-49b1c42351e5/review-package/create-review"
        post_request(url=url, json_payload=json_payload)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id, dealer_name=dealer_name)
    else:
        return HttpResponse({"message":"Forbidden"})

