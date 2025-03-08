from django.urls import path
from .views import ask, index 

urlpatterns = [
    path("", index, name="index"), 
    path("ask/", ask, name="ask"),  
]
