from django.shortcuts import render
from django.views.generic import ListView, DetailView   # To display list of recipes and their details
from .models import Recipe                  # To access Recipe model

# Create your views here.

# Define home function that takes a request as an argument and returns a rendered object using the imported render function
def home(request):
    return render(request, 'recipes/recipes_home.html')

# List view
class RecipeListView(ListView):                 # Class-based view
   model = Recipe                               # Specify model
   template_name = 'recipes/recipe_list.html'   # Specify template 

# Detail View
class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_details.html'