from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class StudentUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=15,null=True)
    image=models.FileField(null=True)
    gender=models.CharField(max_length=20,null=True)
    type=models.CharField(max_length=20,null=True)
    def _str_(self):
        return self.user.username
    
class Recruiter(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=15,null=True)
    image=models.FileField(null=True)
    gender=models.CharField(max_length=20,null=True)
    company=models.CharField(max_length=200,null=True)
    type=models.CharField(max_length=20,null=True)
    status=models.CharField(max_length=20,null=True)
    def _str_(self):
        return self.user.username
    
class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    jobtitle = models.CharField(max_length=100)
    startdate = models.DateField()
    enddate = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='company_logos/')
    description = models.TextField()
    experience = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    skills = models.CharField(max_length=255)
    creationdate = models.DateField()
    def _str_(self):
        return self.title
    
class Apply(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    resume = models.FileField(null=True)
    applydate=models.DateField()
    def __str__(self):
        return self.id