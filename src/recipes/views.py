from django.shortcuts import render

# Create your views here.

# Define home function that takes a request as an argument and returns a rendered object using the imported render function
def home(request):
    return render(request, 'recipes/recipes_home.html')