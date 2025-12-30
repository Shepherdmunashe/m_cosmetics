from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.http import JsonResponse # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib import messages # type: ignore
from django.core.paginator import Paginator # type: ignore
from functools import wraps # type: ignore
from .models import Product
from .forms import UserRegistrationForm, UserLoginForm, ProductForm


def admin_only(view_func):
    """Decorator to ensure only admin/superuser can access the view"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You need to be logged in to access the admin panel.')
            return redirect('login')
        if not request.user.is_superuser and not request.user.is_staff:
            messages.error(request, 'You do not have permission to access the admin panel.')
            return redirect('product_list')
        return view_func(request, *args, **kwargs)
    return wrapper


def product_list(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'paginator': paginator,
        'page_obj': products,
    }
    return render(request, 'store/index.html', context)


@login_required(login_url='login')
def get_cart(request):
    """API endpoint to get cart info (currently unused - cart is client-side)"""
    return JsonResponse({'status': 'success'})


def register(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to M Cosmetics.')
            return redirect('product_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                next_page = request.GET.get('next', 'product_list')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'store/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('product_list')


def contact(request):
    """Display contact information page"""
    context = {
        'contact_info': {
            'whatsapp': '+263715297108',  # Update with your WhatsApp number
            'cell': '+263781156422',  # Update with your cell number
            'email': 'shepherdmunashe6@gmail.com',  # Update with your email
            'facebook': 'https://facebook.com/mcosmetics',  # Update with your Facebook URL
            'tiktok': 'https://tiktok.com/@mcosmetics',  # Update with your TikTok URL
        }
    }
    return render(request, 'store/contact.html', context)


def about(request):
    """Display about page"""
    return render(request, 'store/about.html')


@admin_only
def admin_dashboard(request):
    """Admin dashboard with overview statistics"""
    total_products = Product.objects.count()
    total_users = User.objects.count()
    in_stock_products = Product.objects.filter(in_stock=True).count()
    out_of_stock_products = Product.objects.filter(in_stock=False).count()
    recent_products = Product.objects.all()[:5]
    
    context = {
        'total_products': total_products,
        'total_users': total_users,
        'in_stock_products': in_stock_products,
        'out_of_stock_products': out_of_stock_products,
        'recent_products': recent_products,
    }
    return render(request, 'store/admin/dashboard.html', context)


@admin_only
def manage_products(request):
    """View all products with admin options"""
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 10)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'paginator': paginator,
        'page_obj': products,
    }
    return render(request, 'store/admin/manage_products.html', context)


@admin_only
def add_product(request):
    """Add a new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('manage_products')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ProductForm()
    
    context = {'form': form, 'title': 'Add New Product'}
    return render(request, 'store/admin/product_form.html', context)


@admin_only
def edit_product(request, product_id):
    """Edit an existing product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('manage_products')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ProductForm(instance=product)
    
    context = {'form': form, 'product': product, 'title': f'Edit {product.name}'}
    return render(request, 'store/admin/product_form.html', context)


@admin_only
def delete_product(request, product_id):
    """Delete a product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('manage_products')
    
    context = {'product': product}
    return render(request, 'store/admin/delete_product.html', context)


@admin_only
def manage_users(request):
    """View all users"""
    from django.contrib.auth.models import User # type: ignore
    users_list = User.objects.all()
    paginator = Paginator(users_list, 10)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    context = {
        'users': users,
        'paginator': paginator,
        'page_obj': users,
    }
    return render(request, 'store/admin/manage_users.html', context)
