- python --version
- python -m venv venv
- pip install django
- pip install djangorestframework
- pip install psycopg2-binary
- Install the Python extension
- Select Interpreter
- git init
- create .gitignore
- add code into .gitignore
- git add .gitignore
- git commit -m "Initial commit with .gitignore"

1. Create a Django Project
activate the venv
- django-admin startproject myapi_project .
    django-admin: A command-line tool provided by Django.
    startproject: Tells Django to create a new project.
    myapi_project: The name of your project (can be anything, but we’ll use this).
    .: Specifies the current directory as the project root.

This generates files like manage.py and a myapi_project folder with settings.py, etc.

2. Create an App
- python manage.py startapp users
This creates a users folder (our app for user-related API logic).

3. Register the App
- Open myapi_project/settings.py in VS Code.
- Find the INSTALLED_APPS list and add 'users.apps.UsersConfig' to it, so it looks like:

4. Test the Setup:
Run: python manage.py runserver
rt a browser to http://127.0.0.1:8000/. You should see Django’s welcome page (“Congratulations!”).

4. 1 Write a Simple DRF Endpoint
go to the myapi_project/settings.py and add "rest_framework" in INSTALLED_APPS

Create a View:
Open users/views.py and replace its contents with

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, World!"})

4. 2 Set Up URL Routing

Open myapi_project/urls.py and modify it to

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),  # Added this
]

4. 3 Create a new file users/urls.py and add:

from django.urls import path
from .views import hello_world

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
]

5. Create a Request
Click “New” > “HTTP Request”
Set the method to GET
Enter the URL: http://127.0.0.1:8000/api/hello/.
Click “Send”.
Check the Response.

6. Configure PostgreSQL in Django

psql -U postgres
CREATE DATABASE myapi_db
update DATABASE settings in my_api/settings

7. Create a Users Model

Define a custom user model in Django to store user data

```from django.db import models

class User(models.Model):
    fullname = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    referral_code = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=128) #store hashed password
    confirm_password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     if self.password != self.confirm_password:
    #         raise ValueError("Password did not matched.")
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.username```

Register the Model:
Open users/admin.py and add:

`
from django.contrib import admin
from .models import User

admin.site.register(User)`

Make Migrations:
    In your VS Code terminal (with (myenv) active), run:
    python manage.py makemigrations (created migration files).
    python manage.py migrate (applied them to PostgreSQL).

Inspect the Database:
    psql -U postgres -d myapi_db
    0000
    \dt
    You should see users_user
    Check the table structure: \d users_user


8. Create a Serializer
In your users folder, create a new file serializers.py and add:
```from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['fullname', 'email', 'mobile_number', 'referral_code', 'password', 'confirm_password']
        extra_kwargs = {
            'password' : {'write_only':True},
            'confirm_password' : {'write_only':True}
        }

    def validation(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Password must match."})
        return data

    def create(self, validation_data):
        validation_data.pop('confirm_password')
        user = User(
            fullname=validation_data['fullname'],
            email=validation_data['email'],
            mobile_number=validation_data['mobile_number'],
            referral_code=validation_data.get['referral_code', None],
            password=validation_data['password']
        )
        user.save()
        return user```

9. Create a Registration View:
Open users/views.py and replace its contents with:
```from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Keep hello_world for testing
@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, World!"})```

10. Update URL Routing:
Open users/urls.py and ensure it includes the registration endpoint:

```from django.urls import path
from .views import hello_world, register_user

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('register/', register_user, name='register_user'),
]```

11. Send a POST request to http://127.0.0.1:8000/api/register/ with:

{
    "fullname": "John Doe",
    "email": "john@example.com",
    "mobile_number": "1234567890",
    "referral_code": "REF123",
    "password": "pass123",
    "confirm_password": "pass123"
}

12. 2: Hash Passwords
Update serializers.py
- from django.contrib.auth.hashers import make_password
- password=make_password(validated_data['password'])  # Hash the password

12.1 Verify Hashing
Connect to PostgreSQL: psql -U postgres -d myapi_db.
Query: SELECT fullname, password FROM users_user WHERE fullname = 'Jane Doe';