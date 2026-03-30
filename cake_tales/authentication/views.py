from django.shortcuts import render,redirect

from django.views import View

from .forms import LoginForm,RegisterForm

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.hashers import make_password

from cake_tales.utils import generate_passwords,send_email

import threading

# Create your views here.

class LoginView(View):

    template='authentication/login.html'

    form_class=LoginForm

    def get(self,request,*args,**kwargs):

        form=self.form_class()

        data={'form':form}

        return render(request,self.template,context=data)
    
    def post(self,request,*args,**kwargs):

        form=self.form_class(request.POST)
        
        data={'form':form}


        if form. is_valid():

            user=authenticate(**form.cleaned_data)

            if user :

                login(request,user)

                return redirect('home')
            

            data['msg']='invalid username or password'
        

        return render(request,self.template,context=data)
    

class LogoutView(View):

    def get(self,request,*args,**kwargs):


        logout(request)

        return redirect("home")
    
class RegisterView(View):

    template= 'authentication/register.html'

    form_class=RegisterForm

    def get(self,request,*args,**kwargs):

        form= self.form_class()

        data={'form':form}

        return render(request,self.template,context=data)
    
    def post(self,request,*args,**kwargs):

        form=self.form_class(request.POST)

        if form.is_valid():
            
            user=form.save(commit=False)

            email=form.cleaned_data.get('email')

            password=generate_passwords()
            print(password)

            user.username=email

            user.password=make_password(password)

            user.role='User'

            user.save()

            subject ='Cake Tales | Login Credentials'

            recepient = email

            template = 'emails/login-credentials.html'

            context = {'name':user.first_name,'username':user.username,'password':password}

            thread = threading.Thread(target=send_email,args=(subject,recepient,template,context))

            thread.start()
            
            # send_email(subject,recepient,template,context)---this make the server slow

            return redirect('login')

            

        data={'form':form}

        return render(request,self.template,context=data)



    

    



