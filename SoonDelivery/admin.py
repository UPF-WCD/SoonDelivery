from django.contrib import admin
from .models import Test
from .models import User

admin.site.register(Test)
admin.site.register(User)