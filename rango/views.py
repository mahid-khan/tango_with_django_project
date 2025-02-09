from django.shortcuts import render, redirect
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from django.urls import reverse


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    # Spoiler: you don't need to pass a context dictionary here.
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    
    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    # Create a form instance
    form = CategoryForm()

    # Check if the request method is POST
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # Save the new category to the database
            form.save(commit=True)

            # Redirect the user back to the index view
            return redirect('/rango/')
        else:
            # Print form errors to the terminal for debugging
            print(form.errors)

    # Render the form with error messages (if any)
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        # Try to fetch the category by its slug
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        # If the category does not exist, set it to None
        category = None

    # You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('/rango/')

    # Create a form instance
    form = PageForm()

    # Check if the request method is POST
    if request.method == 'POST':
        form = PageForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            if category:
                # Save the form but don't commit to the database yet
                page = form.save(commit=False)
                page.category = category  # Set the category for the page
                page.views = 0  # Initialize views to 0
                page.save()  # Save the page to the database

                # Redirect to the category page after successfully adding the page
                return redirect(
                    reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug})
                )
        else:
            # Print form errors to the terminal for debugging
            print(form.errors)

    # Prepare the context dictionary for rendering the template
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)