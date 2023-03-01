from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Category
from .forms import NewItemForm, EditItemForm
from django.db.models import Q
# from core.models import 
# Create your views here.

def items(request):
    query=request.GET.get('query', '')
    items=Item.objects.filter(isSold=False)
    category_id=request.GET.get('category', 0)
    categories=Category.objects.all()

    if category_id:
        items=items.filter(category_id=category_id)
    if query:
        items=items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    context={
        'items':items,
        'query':query,
        'categories':categories,
        'category_id':int(category_id),
    }
    return render(request, 'item/items.html', context)


def detail(request, pk):
    item=get_object_or_404(Item, pk=pk)
    related_items=Item.objects.filter(category=item.category, isSold=False).exclude(pk=pk)[0:3]
    categories=Category.objects.all()
    context={
        'item':item,
        'related_items':related_items,
        'categories': categories
    }
    return render(request, 'item/detail.html', context)

@login_required
def new(requeset):
    if requeset.method=="POST":
        form=NewItemForm(requeset.POST, requeset.FILES)
        if form.is_valid():
            item=form.save(commit=False)
            item.created_by=requeset.user
            item.save()

            return redirect('item:detail', pk=item.id)
    form=NewItemForm()
    context={
        'form':form,
        'item':"New Item"
    }
    return render(requeset, 'item/form.html', context)


@login_required
def edit(requeset, pk):
    item=get_object_or_404(Item, pk=pk, created_by=requeset.user)
    if requeset.method=="POST":
        form=EditItemForm(requeset.POST, requeset.FILES, instance=item)
        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form=EditItemForm(instance=item)
    context={
        'form':form,
        'item':"Edit Item"
    }
    return render(requeset, 'item/form.html', context)

@login_required
def delete(request, pk):
    item=get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')