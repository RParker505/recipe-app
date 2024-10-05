from django import forms
from .models import Recipe   # Access Recipe model

# Set chart choices
CHART_CHOICES = (
    ("#1", "Bar Chart"),
    ("#2", "Pie Chart"),
    ("#3", "Line Chart"),
)

# Define form to allow users to search by recipe name, ingredient and optional chart
class RecipeSearchForm(forms.Form):
    Recipe_Name = forms.CharField(
        required=False,
        max_length=100,
        label="Recipe Name",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter a Recipe Name"}
        ),
    )

    # Dynamically populate the Ingredients choices
    def get_ingredients_choices():
        all_ingredients = set()
        recipes = Recipe.objects.all()
        for recipe in recipes:
            ingredients_list = recipe.ingredients.split(',')
            all_ingredients.update([ingredient.strip() for ingredient in ingredients_list])

        return [(ingredient, ingredient) for ingredient in sorted(all_ingredients)]

    Ingredients = forms.MultipleChoiceField(
        required=False,
        choices=get_ingredients_choices(),
        label="Ingredients",
        widget=forms.SelectMultiple(),
    )

    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES,
        widget=forms.Select(),
        required=False,
        label="Chart Type",
    )

    # Validate that user has selected as least a name or ingredient
    def clean(self):
        cleaned_data = super().clean()
        recipe_name = cleaned_data.get("Recipe_Name")
        ingredients = cleaned_data.get("Ingredients")

        if not recipe_name and not ingredients:
            raise forms.ValidationError("Please enter a recipe name or select ingredients.")
        return cleaned_data