from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm

from django.http import HttpResponse
def index(request):
    # Query the database for a list of ALL categories currently stored.
# Order the categories by no. likes in descending order.
# Retrieve the top 5 only - or all if less than 5.
# Place the list in our context_dict dictionary
# that will be passed to the template engine.

    category_list= Category.objects.order_by('-likes')[:5]
    page_list=Page.objects.order_by('-views')[:5]
    context_dict = {'categories':category_list, 'pages':page_list}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    #create a context dict which can pass to the template rendering engine
    context_dict={}

    try:
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve all of the associated pages.
        pages = Page.objects.filter(category=category)
        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
# We also add the category object from the database to the context dictionary.
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
    # Save the new category to the database.
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


    
    
