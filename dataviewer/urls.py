from django.urls import path, include
from . import views # . is relative import

urlpatterns = [
    path('', views.index, name="index") # this is /dataviewer/"" ("" is just a blank)
    # displays the view from the function views.index
]
