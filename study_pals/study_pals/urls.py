
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
]

# sudo lsof -t -i tcp:8000 | xargs kill -9
# (kills all ps)

#  python3 manage.py runserver     
# (start django server)


#python3 manage.py createsuperuser 
# (creating superuser for admin)


# python3 manage.py makemigrations  (stage tables for a specific model after defining its fields)
# python3 manage.py migrate  (create tables for a specific model)