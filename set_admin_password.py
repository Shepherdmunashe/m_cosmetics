#!/usr/bin/env python
import os
import django # type: ignore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'm_cosmetics_project.settings')
django.setup()

from django.contrib.auth.models import User # type: ignore

try:
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('admin123')
    admin_user.save()
    print("Password set successfully for admin user")
except User.DoesNotExist:
    print("Admin user not found")
