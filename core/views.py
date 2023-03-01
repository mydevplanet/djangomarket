from django.shortcuts import render, redirect
from item.models import Category, Item
from .forms import SignUpForm
# Create your views here.

def index(request):
    items=Item.objects.filter(isSold=False)[0:6]
    categories=Category.objects.all()
    context={
        'categories':categories,
        'items':items,
    }
    return render(request, 'core/index.html', context)

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:   
        form=SignUpForm()
    context={
         'form':form,
        }
    return render(request, 'core/signup.html', context)