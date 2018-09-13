from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from app1.models import CoepHostel
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from coep.utils import render_to_pdf 

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        print("Hello c")
        form = SignupForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            # print(username)
            try:
                # print("username =", username)
                go = CoepHostel.objects.get(c_id=username)
                print(go.email)
                global email
                email = go.email
                #form.first_name = go.name
                year = go.year
                category = go.category
                gender = go.gender
                cet = go.cet
                branch = go.branch
                cgpa = go.cgpa
                name = go.name
                
            except CoepHostel.DoesNotExist:
                print("anya Exception")
                con = "***College Id Does Not Exist***"
                return render(request,"signup.html",{'form':form,'con':con})
            else:
                user=User( email=email ,year=year, name=name ,category=category ,gender=gender ,cet=cet ,cgpa=cgpa,username=username ,status=0 , branch=branch)
                #user.save(commit=False)
                print(user.category)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token':account_activation_token.make_token(user),
                })
                to_email = email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
        print("sory")
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def catgy(yr , gen , br ):  
    go1 = User.objects.all().filter(year=yr , gender=gen)
    go = go1.filter(branch=br).order_by('-cet') 
    gom1 = go[:10]
    gom =  go.filter(category='MINORITY' ).exclude(id__in=[o.id for o in gom1])[:6]
    gobc = go.filter(category='OBC' ).exclude(id__in=[o.id for o in gom1])[:4]
    context = {
       "go" :gom1, "gom" : gom , "gobc" : gobc ,# "go2" : go2 , "go3" : go3 , "go4" : go4 , "types" : 'FIRST YEAR GIRLS'
    }
    return context
 

def fe_pdf_boys(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy('FE' ,'MALE' ,'MECH' )
    con2 = catgy('FE' ,'MALE' ,'COMP' )
    con3 = catgy('FE' ,'MALE' ,'IT' )
    con4 = catgy('FE' ,'MALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'FE BOYS'
    }

    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


    


    

    




def fe_pdf_girls(request, *args, **kwargs):
    
    template = get_template('pdf/invoice.html')
    con1 = catgy('FE' ,'FEMALE' ,'MECH' )
    con2 = catgy('FE' ,'FEMALE' ,'COMP' )
    con3 = catgy('FE' ,'FEMALE' ,'IT' )
    con4 = catgy('FE' ,'FEMALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'FE GIRLS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

def se_pdf_boys(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy('SE' ,'MALE' ,'MECH' )
    con2 = catgy('SE' ,'MALE' ,'COMP' )
    con3 = catgy('SE' ,'MALE' ,'IT' )
    con4 = catgy('SE' ,'MALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'SE BOYS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

def se_pdf_girls(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy('SE' ,'FEMALE' ,'MECH' )
    con2 = catgy('SE' ,'FEMALE' ,'COMP' )
    con3 = catgy('SE' ,'FEMALE' ,'IT' )
    con4 = catgy('SE' ,'FEMALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'SE GIRLS'
    }

    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

def te_pdf_boys(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy('TE' ,'MALE' ,'MECH' )
    con2 = catgy('TE' ,'MALE' ,'COMP' )
    con3 = catgy('TE' ,'MALE' ,'IT' )
    con4 = catgy('TE' ,'MALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'TE BOYS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

def te_pdf_girls(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy('TE' ,'FEMALE' ,'MECH' )
    con2 = catgy('TE' ,'FEMALE' ,'COMP' )
    con3 = catgy('TE' ,'FEMALE' ,'IT' )
    con4 = catgy('TE' ,'FEMALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'TE GIRLS'
    }

    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

def be_pdf_boys(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy('BE' ,'MALE' ,'MECH' )
    con2 = catgy('BE' ,'MALE' ,'COMP' )
    con3 = catgy('BE' ,'MALE' ,'IT' )
    con4 = catgy('BE' ,'MALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "type" : 'BE BOYS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

def be_pdf_girls(request, *args, **kwargs):
    template = get_template('pdf/invoice.html')
    con1 = catgy('BE' ,'FEMALE' ,'MECH' )
    con2 = catgy('BE' ,'FEMALE' ,'COMP' )
    con3 = catgy('BE' ,'FEMALE' ,'IT' )
    con4 = catgy('BE' ,'FEMALE' ,'PLANNING')
    context = {
        "con1" : con1 , "con2" : con2 , "con3" : con3 , "con4" : con4 , "types" : 'BE GIRLS'
    }
    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Hostel_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

