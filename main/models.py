from django.db import models
import re
import bcrypt
# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        check_email = User.objects.filter(email = postData["email"])
        #Validate user first and last name
        if len(postData["fname"]) < 2:
            errors['fname'] = "First name must have at least 2 characters"
        if len(postData["lname"]) < 2:
            errors['lname'] = "Last name must have at least 2 characters"
        #Validate email address
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) < 1:
            errors['reg_email'] = "Email address cannot be blank."
        elif not EMAIL_REGEX.match(postData['email']):
            errors['reg_email'] = "Please enter a valid email address."
        elif check_email:
            errors['reg_email'] = "Email address is already registered."
        #Check password
        if len(postData['password']) < 8:
            errors['password'] = "Password cannot be less than 8 characters."
        elif postData['password'] != postData['confirm-password']:
            errors['password'] = "Passwords do not match."
        return errors

    def login_validator(self, postData):
        errors = {}
        check_email = User.objects.filter(email = postData["login_email"])
        if not check_email:
            errors['login_email'] = "Email has not been registered"
        else:
            if not bcrypt.checkpw(postData['login_password'].encode(), check_email[0].password.encode()):
                errors['login_email'] = "Email and password do not match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class JobManager(models.Manager):
    def create_validator(self,postData):
        errors = {}
        if len(postData['title']) < 3:
            errors['title'] = "Job title must be at least 3 characters"
        if len(postData['description']) < 10:
            errors['description'] = "Job description must be at least 10 characters"
        if len(postData['location']) ==0:
            errors['location'] = 'Job must have a location'
        return errors



class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length = 40)
    creator = models.ForeignKey(User,related_name="has_created_jobs", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    job_owners = models.ForeignKey(User, related_name="owns_jobs", on_delete=models.CASCADE, null=True, blank = True)
    objects = JobManager()
    
