from django.test import TestCase
from .models import Recipe    #to access Recipe model

# Create your tests here.
class RecipeModelTest(TestCase):

    # Define test data to initialize variables in test database
    def setUpTestData():
        # Set up non-modified objects used by all test methods
        Recipe.objects.create(name='Tea', cooking_time=5, ingredients='tea-leaves, water, sugar')

    # Test if recipe name is initialized as expected
    def test_recipe_name(self):
       # Get a recipe object to test
       recipe = Recipe.objects.get(id=1)

       # Get the metadata for the 'name' field and use it to query its data
       recipe_name_label = recipe._meta.get_field('name').verbose_name

       # Compare the value to the expected result
       self.assertEqual(recipe_name_label, 'name')

    # Test that recipe name is a max of 120 characters
    def test_recipe_name_max_length(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the 'ingredients' field and use it to query its max_length
        max_length = recipe._meta.get_field('name').max_length

        # Compare the value to the expected result i.e. 400
        self.assertEqual(max_length, 120)

    # Test that ingredients is a max of 400 characters
    def test_ingredients_max_length(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the 'ingredients' field and use it to query its max_length
        max_length = recipe._meta.get_field('ingredients').max_length

        # Compare the value to the expected result i.e. 400
        self.assertEqual(max_length, 400)

    # Test that cooking_time is an integer
    def test_cooking_time_integer(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the 'cooking_time' field and use it to query its type
        cooking_time = recipe.cooking_time

        # Assert that cooking_time is a whole number (integer-like)
        self.assertTrue(cooking_time.is_integer(), "Cooking time is not an integer")

    # Test that difficulty is accurately calculated
    def test_difficulty_calc(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Assert the difficulty is calculated accurately
        self.assertEqual(recipe.calculate_difficulty(), 'Easy')

    # Test that absolute URL is correctly generated and that the RecipeDetailView loads with name is clicked
    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        # get_absolute_url() should take you to the detail page of recipe #1 and load the URL recipes/list/1
        self.assertEqual(recipe.get_absolute_url(), '/recipes/1')