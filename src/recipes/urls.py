from django.urls import path
from .views import home, RecipeListView, RecipeDetailView, RecipeSearchView

app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('recipes/', RecipeListView.as_view(), name='list'),  # List view for recipes
    path('recipes/<pk>', RecipeDetailView.as_view(), name='detail'),  # Detail view
    path('search/', RecipeSearchView.as_view(), name='recipe_search'),  # Search view
]