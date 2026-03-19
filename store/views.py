from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.http import JsonResponse # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.views.decorators.http import require_POST # type: ignore
from django.contrib import messages # type: ignore
from django.core.paginator import Paginator # type: ignore
from django.db.models import Q # type: ignore
from django.utils.http import url_has_allowed_host_and_scheme # type: ignore
from django.conf import settings # type: ignore
from functools import wraps # type: ignore
from .models import Product, Category
from .forms import UserRegistrationForm, UserLoginForm, ProductForm, CategoryForm


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
    categories = Category.objects.all()
    paginator = Paginator(products_list, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'paginator': paginator,
        'page_obj': products,
        'categories': categories,
    }
    return render(request, 'store/index.html', context)

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products_list = Product.objects.filter(category=category)
    categories = Category.objects.all()
    paginator = Paginator(products_list, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'paginator': paginator,
        'page_obj': products,
        'category': category,
        'categories': categories,
    }
    return render(request, 'store/index.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'store/product_detail.html', context)


def search_results(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        products = Product.objects.none()

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'paginator': paginator,
        'page_obj': page_obj,
        'query': query,
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
                next_page = request.GET.get('next', '')
                if next_page and url_has_allowed_host_and_scheme(
                    next_page,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure(),
                ):
                    return redirect(next_page)
                return redirect('product_list')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'store/login.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('product_list')


def contact(request):
    """Display contact information page"""
    context = {
        'contact_info': settings.CONTACT_INFO,
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
    total_categories = Category.objects.count()
    in_stock_products = Product.objects.filter(in_stock=True).count()
    out_of_stock_products = Product.objects.filter(in_stock=False).count()
    recent_products = Product.objects.order_by('-created_at')[:5]
    
    context = {
        'total_products': total_products,
        'total_users': total_users,
        'total_categories': total_categories,
        'in_stock_products': in_stock_products,
        'out_of_stock_products': out_of_stock_products,
        'recent_products': recent_products,
    }
    return render(request, 'store/admin/dashboard.html', context)


@admin_only
def manage_products(request):
    """View all products with admin options, including search and filtering"""
    products_list = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    if query:
        products_list = products_list.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if category_id:
        products_list = products_list.filter(category_id=category_id)

    paginator = Paginator(products_list, 10)  # 10 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'paginator': paginator,
        'page_obj': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
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


@admin_only
def manage_categories(request):
    """List product categories"""
    categories = Category.objects.all().order_by('name')
    context = {
        'categories': categories,
    }
    return render(request, 'store/admin/manage_categories.html', context)


@admin_only
@require_POST
def add_category_inline(request):
    """AJAX endpoint: create a category and return JSON {id, name}"""
    form = CategoryForm(request.POST)
    if form.is_valid():
        category = form.save()
        return JsonResponse({'success': True, 'id': category.pk, 'name': category.name})
    errors = {field: errs.as_text() for field, errs in form.errors.items()}
    return JsonResponse({'success': False, 'errors': errors}, status=400)


@admin_only
def add_category(request):
    """Add a new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'title': 'Add New Category'
    }
    return render(request, 'store/admin/category_form.html', context)


@admin_only
def edit_category(request, pk):
    """Edit an existing category"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('manage_categories')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'title': f'Edit {category.name}'
    }
    return render(request, 'store/admin/category_form.html', context)


@admin_only
def delete_category(request, pk):
    """Delete a category"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('manage_categories')
    
    context = {'category': category}
    return render(request, 'store/admin/delete_category.html', context)
