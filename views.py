from django.shortcuts import render,redirect 
from .models import *
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
from datetime import date

# Create your views here.
def index(request):
    return render(request,'index.html')

def admin_login(request):
    error=""
    if request.method == "POST":
        u=request.POST['uname']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d={'error':error}
    return render(request,'admin_login.html',d)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('uname')
        password = request.POST.get('pwd')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login Successful!")
            return redirect('user_home')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'user_login.html')


def recruiter_login(request):
    if request.method == "POST":
        email = request.POST.get('Email')
        password = request.POST.get('pwd')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login Successful!")
            return redirect('recruiter_home')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'recruiter_login.html')

from django.contrib import messages
from django.core.exceptions import ValidationError

def recruiter_signup(request):
    error = ""
    if request.method == 'POST':
        try:
            f = request.POST.get('fname', '').strip()
            l = request.POST.get('lname', '').strip()
            e = request.POST.get('email', '').strip()
            p = request.POST.get('pwd', '').strip()
            con = request.POST.get('contact', '').strip()
            gen = request.POST.get('gender', '').strip()
            com = request.POST.get('company', '').strip()
            i = request.FILES.get('image')
            if not all([f, l, e, p, con, gen, com]):
                raise ValueError("All fields are required.")
            if not i:
                raise ValueError("Image is required.")
            if User.objects.filter(username=e).exists():
                raise ValidationError("A user with this email already exists.")
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            Recruiter.objects.create(
                user=user, 
                mobile=con, 
                image=i, 
                gender=gen, 
                type="recruiter", 
                company=com, 
                status="pending"
            )
            error = "no"
        except KeyError as key_error:
            error = f"Missing field: {str(key_error)}"
        except ValidationError as val_error:
            error = f"Validation error: {str(val_error)}"
        except ValueError as val_err:
            error = str(val_err)
        except Exception as ex:
            error = f"An unexpected error occurred: {str(ex)}"
    return render(request, 'recruiter_signup.html', {'error': error})

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    rcount=Recruiter.objects.all().count()
    scount=StudentUser.objects.all().count()
    d={'rcount':rcount,'scount':scount}
    return render(request,'admin_home.html',d)

def Logout(request):
    logout(request)
    return redirect('index')

from django.shortcuts import render
from django.contrib.auth.models import User
from .models import StudentUser 

def user_signup(request):
    error = ""
    if request.method == "POST":
        try:
            f = request.POST['fname']
            l = request.POST['lname']
            i = request.FILES.get('image')
            p = request.POST['pwd']
            e = request.POST['Email']
            con = request.POST['Contact'] 
            gen = request.POST['gender']
            if p != request.POST['cpwd']:
                error = "Passwords do not match"
            else:
                user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
                StudentUser.objects.create(user=user, mobile=con, image=i, gender=gen, type="student")
                error = "no" 
        except KeyError as e:
            error = f"Missing field: {str(e)}"
        except Exception as e:
            error = f"An error occurred: {str(e)}"
    return render(request, 'user_signup.html', {'error': error})

def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    recruiter, created = Recruiter.objects.get_or_create(user=request.user)
    error = ""
    if request.method == "POST":
        try:
            f = request.POST.get('fname', recruiter.user.first_name)
            l = request.POST.get('lname', recruiter.user.last_name)
            con = request.POST.get('contact', recruiter.mobile)
            comp = request.POST.get('company', recruiter.company)
            email = request.POST.get('email', recruiter.user.email)
            gen = request.POST.get('gender', recruiter.gender)
            i = request.FILES.get('image')

            recruiter.user.first_name = f
            recruiter.user.last_name = l
            recruiter.mobile = con
            recruiter.company = comp
            recruiter.user.email = email
            recruiter.gender = gen
            if i:
                recruiter.image = i
            recruiter.save()
            recruiter.user.save()
            error = "no"
        except Exception as e:
            print(f"Error: {e}")
            error = "yes"
    d = {'recruiter': recruiter, 'error': error}
    return render(request, 'recruiter_home.html', d)

def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=StudentUser.objects.all()
    d={'data':data}
    return render(request,'view_users.html',d)

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student=User.objects.get(id=pid)
    student.delete()
    return redirect('view_users')

def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='pending')
    d={'data':data}
    return render(request,'recruiter_pending.html',d)

def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    recruiter=Recruiter.objects.get(id=pid)
    if request.method=="POST":
        s=request.POST['status']
        recruiter.status=s
        try:
            recruiter.save()
            error="no"
        except:
            error="yes"
    d={'recruiter':recruiter,'error':error}
    return render(request,'change_status.html',d)

def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='Accept')
    d={'data':data}
    return render(request,'recruiter_accepted.html',d)

def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='Reject')
    d={'data':data}
    return render(request,'recruiter_rejected.html',d)

def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.all()
    d={'data':data}
    return render(request,'recruiter_all.html',d)

def delete_recruiter(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    recruiter=User.objects.get(id=pid)
    recruiter.delete()
    return redirect('recruiter_all')

def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    if request.method=="POST":
        c=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'change_passwordadmin.html',d)

def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method=="POST":
        c=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'change_passworduser.html',d)

def change_passwordrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('reeuriter_login')
    error=""
    if request.method=="POST":
        c=request.POST['currentpassword']
        n=request.POST['newpassword']
        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'change_passwordrecruiter.html',d)

from django.shortcuts import render, redirect
from datetime import date
from django.http import HttpResponseBadRequest
from .models import Recruiter, Job

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    if request.method == "POST":
        j = request.POST.get('jobtitle')
        sd = request.POST.get('startdate')
        ed = request.POST.get('enddate')
        s = request.POST.get('salary')
        lo = request.FILES.get('logo') 
        exp = request.POST.get('experience')
        loc = request.POST.get('location')
        sk = request.POST.get('skills')
        d = request.POST.get('description')
        if not all([j, sd, ed, s, lo, exp, loc, sk, d]):
            error = "yes"
        else:
            user = request.user
            recruiter = Recruiter.objects.get(user=user)
            try:
                Job.objects.create(recruiter=recruiter,jobtitle=j,startdate=sd,enddate=ed,salary=s,image=lo,experience=exp,location=loc,skills=sk,description=d,creationdate=date.today())
                error = "no"
            except Exception as e:
                print(f"Error: {e}")
                error = "yes"
    d = {'error': error}
    return render(request, 'add_job.html', d)

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter = Recruiter.objects.get(user=request.user)
    job=Job.objects.filter(recruiter=recruiter)
    d={'job':job}
    return render(request,'job_list.html',d)

def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job=Job.objects.get(id=pid)
    if request.method == "POST":
        j = request.POST.get('jobtitle')
        sd = request.POST.get('startdate')
        ed = request.POST.get('enddate')
        s = request.POST.get('salary') 
        exp = request.POST.get('experience')
        loc = request.POST.get('location')
        sk = request.POST.get('skills')
        d = request.POST.get('description')
        job.jobtitle=j
        job.salary=s
        job.experience=exp
        job.location=loc
        job.skills=sk
        job.description=d
        try:
            job.save()
            error = "no"
        except:
            error = "yes"
        if sd:
            try:
                job.startdate=sd
                job.save()
            except:
                pass
        else:
            pass
        if ed:
            try:
                job.enddate=ed
                job.save()
            except:
                pass
        else:
            pass
    d = {'error': error,'job':job}
    return render(request, 'edit_jobdetail.html', d)

def change_companylogo(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job=Job.objects.get(id=pid)
    if request.method == "POST":
        cl=request.FILES['logo']
        job.image=cl
        try:
            job.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'job':job}
    return render(request, 'change_companylogo.html', d)

def latest_job(request):
    job=Job.objects.all().order_by('-startdate')
    d={'job':job}
    return render(request,'latest_job.html',d)

def user_latestjob(request):
    job=Job.objects.all().order_by('-startdate')
    user=request.user
    student=StudentUser.objects.get(user=user)
    data=Apply.objects.filter(student=student)
    li=[]
    for i in data:
        li.append(i.job.id)
    d={'job':job,'li':li}
    return render(request,'user_latestjob.html',d)

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user=request.user
    student=StudentUser.objects.get(user=user)
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        con=request.POST['contact']
        gen=request.POST['gender']
        student.user.first_name=f
        student.user.last_name=l
        student.mobile=con
        student.gender=gen
        try:
            student.save()
            student.user.save()
            error="no"
        except:
            error="yes"
        try:
            i=request.FILES['image']
            student.image=i
            student.save()
            error="no"
        except:
            pass
    d = {'student': student, 'error': error}
    return render(request, 'user_home.html',d)

def job_detail(request,pid):
    job=Job.objects.get(id=pid)
    d={'job':job}
    return render(request,'job_detail.html',d)

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from datetime import date

def applyforjob(request, pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error = ""
    user = request.user
    try:
        student = StudentUser.objects.get(user=user)
    except StudentUser.DoesNotExist:
        error = "nostudent" 
        return render(request, 'applyforjob.html', {'error': error})
    try:
        job = Job.objects.get(id=pid)
    except Job.DoesNotExist:
        error = "nojob"
        return render(request, 'applyforjob.html', {'error': error})
    date1 = date.today()
    if job.enddate < date1:
        error = "close"
    elif job.startdate > date1:
        error = "notopen"
    else:
        if request.method == 'POST':
            try:
                r = request.FILES['resume']
                Apply.objects.create(job=job, student=student, resume=r, applydate=date.today())
                error = "done"
            except Exception as e:
                error = "uploaderror" 

    context = {'error': error}
    return render(request, 'applyforjob.html', context)

def applied_candidatelist(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    data=Apply.objects.all()
    d = {'data': data}
    return render(request, 'applied_candidatelist.html', d)

def contact(request):
    return render(request,'contact.html')
