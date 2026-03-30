from django.shortcuts import render,redirect

# Create your views here.
from django.views import View

from .models import Cake,Wishlist

from .forms import AddCakeForm

from django.db.models import Q

from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from authentication.permissions import allowed_permission_roles


class HomeView(View):

    template="cakes/home.html"

    def get(self,request,*args,**kwargs):

        query=request.GET.get('query')

        # cakes=Cake.objects.all()

        cakes=Cake.objects.filter(active_status=True)

        wedding_cakes=cakes.filter(category__name='Wedding Cakes')

        birthday_cakes=cakes.filter(category__name='Birthday Cakes')

        plum_cakes=cakes.filter(category__name='Plum Cakes')

        cup_cakes=cakes.filter(category__name="Cup Cakes")

        data={'wedding_cakes':wedding_cakes,'birthday_cakes':birthday_cakes,'plum_cakes':plum_cakes,'cup_cakes':cup_cakes}

        if query:

            search_results=cakes.filter(Q(name__icontains=query)|
                                        Q(description__icontains=query)|
                                        Q(category__name__icontains=query)|
                                        Q(shape__name__icontains=query)|
                                        Q(weight__name__icontains=query)|
                                        Q(flavour__name__icontains=query)
                                        )
            
            data["search_results"]=search_results

            data['query'] = query

            print(search_results)
        
        return render(request,self.template,context=data)
    
# @method_decorator(login_required(login_url='login'),name='dispatch')

@method_decorator(allowed_permission_roles(['Admin']),name='dispatch') 
class AddCakeView(View):

    template='cakes/add-cake.html'

    form_class=AddCakeForm

    def get(self,request,*args,**kwargs):

        form=self.form_class()
        
        
        # data = {'categories':CategoryChoices,'flavours':FlavourChoices,'weights':WeightChoices,'shapes':ShapeChoices}

        data={'form':form}
        
        return render(request,self.template,context=data)
    
    def post(self,request,*args,**kwargs):

       

        # name=request.POST.get('name')

        # description=request.POST.get('description')
        
        # photo=request.FILES.get('photo')

        # category=request.POST.get('category')

        # flavour=request.POST.get('flavour')

        # shape=request.POST.get('shape')

        # weight=request.POST.get('weight')

        # egg_added=request.POST.get('egg_added')

        # price=request.POST.get('price')

        # is_available=request.POST.get('is_available')

        # cake=Cake.objects.create(name=name,description=description,photo=photo,category=category,
        #                          flavour=flavour,shape=shape,weight=weight,egg_added=egg_added,is_available=is_available,price=price)

        
        form=self.form_class(request.POST,request.FILES)

        if form.is_valid():
            
            form.save()
            
            return redirect('home')
        
        data={'form':form}

        return render(request,self.template,context=data)
    
class CakeDetailsView(View):

    template= 'cakes/cake-details.html'

  

    def get(self,request,*args,**kwargs):

        uuid=kwargs.get('uuid')

        cake=Cake.objects.get(uuid=uuid)

   

        data={'cake':cake}

        return render(request,self.template,context=data)
    
@method_decorator(allowed_permission_roles('Admin'),name='dispatch')

    
class CakeEditView(View):

    template='cakes/cake-edit.html'
    
    form_class= AddCakeForm

    def get(self,request,*args,**kwargs):

        
        uuid=kwargs.get('uuid')

        cake=Cake.objects.get(uuid=uuid)

        form=self.form_class(instance=cake)

        data={'form':form}
        
        return render(request,self.template,context=data)

    def post(self,request,*args,**kwargs):

        uuid=kwargs.get('uuid')

        cake=Cake.objects.get(uuid=uuid)

        form=self.form_class(request.POST,request.FILES,instance=cake)

        if form.is_valid():

            form.save()

            return redirect('cake-details',uuid=cake.uuid)
        
        data= {'form':form}

        return render(request,self.template,context=data)
    
@method_decorator(allowed_permission_roles(['Admin']),name='dispatch')

    
class CakeDeleteView(View):
    
    def get(self,request,*args,**kwargs):

        uuid=kwargs.get('uuid')

        cake=Cake.objects.get(uuid=uuid)

        # cake.delete()--for noraml delete

        cake.active_status=False

        cake.save()
        
        return redirect("home")
    
@method_decorator(allowed_permission_roles(['User']),name='dispatch')

    
class AddtoWishlist(View):

    def get(self,request,*args,**kwargs):
        
        uuid = self.kwargs.get('uuid')

        user = request.user

        cake=Cake.objects.get(uuid=uuid)

        wishlist,_ =Wishlist.objects.get_or_create(user=user)

        wishlist.cakes.add(cake)

        return redirect('home')
    
@method_decorator(allowed_permission_roles(['User']),name='dispatch')


class RemovefromWishlist(View):

    def get(self,request,*args,**kwargs):

        uuid = self.kwargs.get('uuid')

        user = request.user

        cake=Cake.objects.get(uuid=uuid)

        wishlist = Wishlist.objects.get(user=user)

        wishlist.cakes.remove(cake)

        return redirect('home')
        







