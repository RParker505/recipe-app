from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
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

class RecipeFormTests(TestCase):

    def setUp(self):
        # Create a user for login tests
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create some test recipes
        Recipe.objects.create(name="Pasta", cooking_time=30, ingredients="Tomato, Pasta")
        Recipe.objects.create(name="Salad", cooking_time=10, ingredients="Lettuce, Tomato, Cucumber")

    def test_login_required(self):
        """Test that the search view is login-protected."""
        response = self.client.get(reverse('recipe_search'))  # No namespace needed
        self.assertNotEqual(response.status_code, 200)  # Should redirect if not logged in
        self.assertRedirects(response, '/accounts/login/?next=/search/')  # Now it reflects the '/search/' path

    def test_page_loads_after_login(self):
        """Test that the search page loads after the user logs in."""
        self.client.login(username='testuser', password='testpass')  # Log in the user
        response = self.client.get(reverse('recipe_search'))  # No namespace needed
        self.assertEqual(response.status_code, 200)  # Check if page loads
        self.assertTemplateUsed(response, 'recipes/recipe_search.html')  # Check if correct template is used

    def test_form_submission_filters_recipes(self):
        """Test that the form filters recipes by name."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('recipe_search'), {'Recipe_Name': 'Pasta'})
        
        # Check if only the "Pasta" recipe is in the response context
        self.assertContains(response, 'Pasta')
        self.assertNotContains(response, 'Salad')  # Ensure other recipes are filtered out

    def test_form_chart_generation(self):
        """Test that the chart is generated when a valid chart type is selected."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('recipe_search'), {
            'Recipe_Name': 'Pasta',
            'chart_type': 'pie',  # Assuming 'pie' is a valid chart type
        })
        self.assertIn('chart', response.context)  # Check if chart is in the context
        self.assertIsNotNone(response.context['chart'])  # Ensure the chart is generated

    def test_form_invalid_submission(self):
        """Test that an invalid form submission doesn't break the view."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('recipe_search'), {'chart_type': 'invalid_chart'})
        self.assertEqual(response.status_code, 200)  # Page should still load
        self.assertIsNone(response.context.get('chart'))  # No chart should be generated with invalid data