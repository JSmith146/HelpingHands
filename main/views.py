from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
# from django.db.models import Count
# Create your views here.

def index(request):
    context={}
    return render(request,"index.html", context)


def register(request):
    if request.method=="GET":
        return redirect("/")
    errors = User.objects.registration_validator(request.POST)
    #check errors for messages
    if len(errors):
        for key, value in errors.items():
            messages.error(request,value)
        return redirect("/")
    else:
        user = User.objects.create(
            first_name = request.POST["fname"],
            last_name = request.POST['lname'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        request.session['user_id'] = user.id
        request.session['greeting'] = (f"{user.first_name}")
    return redirect("/dashboard")

def login(request):
    if request.method=="GET":
        return redirect("/")
    errors = User.objects.login_validator(request.POST)
    #check errors for messages
    if len(errors):
        for key, value in errors.items():
            messages.error(request,value)
        return redirect("/")
    else:
        user = User.objects.get(email = request.POST['login_email'])
        request.session['user_id'] = user.id 
        request.session['greeting'] = (f"{user.first_name}")
    return redirect("/dashboard")

def job_dashboard(request):
    if "user_id" not in request.session:
        return redirect("/")
    else:
        context = {
            'user':User.objects.get(id = request.session['user_id']),
            'all_jobs': Job.objects.all(),
        }
    return render(request,"dashboard.html",context)

def new_job_form(request):
    if "user_id" not in request.session:
        return redirect('/')
    return render(request, 'new_job_form.html')
    

def create_job(request):
    if "user_id" not in request.session:
        return redirect('/')
    if request.method =="GET":
        return redirect('/')

    errors = Job.objects.create_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/addJob')
    else:
        user = User.objects.get(id = request.session['user_id'])
        job = Job.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            location = request.POST['location'],
            creator = user
        )
        # print("Job created")
    return redirect("/dashboard")

def show_job(request,id):
    if "user_id" not in request.session:
        return redirect("/")
    
    job_exists = Job.objects.filter(id=id)

    if len(job_exists) > 0:
        context={
            'job': Job.objects.get(id=id),
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request,"show_job.html",context)
    return redirect("/dashboard")

def edit_job_form(request,id):
    if "user_id" not in request.session:
            return redirect("/")
    # check that job exists in the database        
    job_exists = Job.objects.filter(id=id)

    if len(job_exists) > 0:
        context={
            'job': Job.objects.get(id=id),
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request,"edit_form.html",context)
    return redirect("/dashboard")

def add_job(request,id):
    if "user_id" not in request.session:
            return redirect("/")
    # check that job exists in the database        
    job_exists = Job.objects.filter(id=id)

    if len(job_exists) > 0:
        user = User.objects.get(id = request.session['user_id'])
        Job.objects.filter(id=id).update(job_owners=user)
    return redirect('/dashboard')
    
def edit_job(request,id):
    if "user_id" not in request.session:
        return redirect('/')
    if request.method =="GET":
        return redirect('/')
    job_exists = Job.objects.filter(id=id)
    if len(job_exists) > 0:
        job = Job.objects.get(id=id)
        if job.creator.id != request.session['user_id']:
            return redirect("/dashboard")
        errors = Job.objects.create_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/edit/{id}')
        else:
            user = User.objects.get(id = request.session['user_id'])
            # job = Job.objects.get(id=id)
            job.title = request.POST['title']
            job.description = request.POST['description']
            job.location = request.POST['location']
            job.save()
            print("Job edited")
    return redirect(f"/dashboard")

def remove(request,id):
    if "user_id" not in request.session:
        return redirect("/")
    
    job_exists = Job.objects.filter(id=id)

    if len(job_exists) > 0:
        Job.objects.filter(id=id).update(job_owners=None)
    return redirect("/dashboard")

def delete(request,id):
    if "user_id" not in request.session:
        return redirect("/")
    # check to see that job exists
    job_exists = Job.objects.filter(id=id)
    # compare job creator
    if len(job_exists) > 0:
        job = Job.objects.get(id=id)
        if (job.creator.id == request.session['user_id']) or (job.job_owners.id == request.session['user_id']):
            job.delete()
    return redirect("/dashboard")

def logout(request):
    request.session.flush()
    return redirect('/')

