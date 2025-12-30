# M Cosmetics Admin Panel Setup Guide

## Overview
A custom admin panel has been created to manage your e-commerce store without using Django's default admin interface.

## Features
- **Dashboard**: Overview of store statistics (products, users, stock status)
- **Product Management**: Add, edit, delete products with image uploads
- **User Management**: View all registered customers and their details
- **Admin-Only Access**: Protected routes that only superusers/staff can access

## Accessing the Admin Panel

### Step 1: Create a Superuser Account
Run this command in your terminal:
```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account with:
- Username
- Email
- Password

### Step 2: Access the Admin Panel
Once logged in, visit:
```
http://localhost:8000/admin/
```

You will be redirected to the dashboard.

## Admin Panel URLs

| URL | Description |
|-----|-------------|
| `/admin/` | Dashboard (overview & statistics) |
| `/admin/products/` | Manage all products |
| `/admin/products/add/` | Add a new product |
| `/admin/products/<id>/edit/` | Edit a product |
| `/admin/products/<id>/delete/` | Delete a product |
| `/admin/users/` | View all registered users |

## Features Breakdown

### Dashboard
- Total products count
- In-stock vs out-of-stock items
- Total registered users
- Recent products list with quick edit/delete options

### Product Management
- View all products in a table
- Search and filter products (pagination supported)
- Edit product details (name, description, price, image, stock status)
- Delete products with confirmation
- Upload product images
- Toggle stock status on/off

### User Management
- View all registered customers
- See user details (name, email, username, join date)
- User roles (Admin, Staff, Customer)
- User status (Active/Inactive)

## Security

The admin panel is protected by:
1. **Login Required**: Users must be authenticated
2. **Admin-Only Decorator**: Only superusers/staff can access
3. **Permission Checks**: Non-admin users are redirected with error messages

## Adding Another Admin

To make a user an admin, run:
```bash
python manage.py shell
```

Then in the Python shell:
```python
from django.contrib.auth.models import User
user = User.objects.get(username='username_here')
user.is_staff = True
user.is_superuser = True
user.save()
```

## Product Upload Tips

1. **Image Formats**: Use JPG, PNG, or WebP for best compatibility
2. **Image Size**: Recommended 500x500px or larger
3. **Price**: Enter as decimal (e.g., 25.99)
4. **Description**: Use clear, descriptive text for better SEO

## Troubleshooting

**Can't access admin panel?**
- Make sure you're logged in
- Check that your user is a superuser: `user.is_superuser = True`

**Product images not uploading?**
- Ensure the `media/products/` directory exists
- Check file permissions on the media folder

**Pagination not working?**
- Make sure you have more than 10 products (products) or 10 users (users)

