from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from recipEasyApp.models import *
from recipEasyApp.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', Users, 'user')
router.register(r'recipes', Recipes, 'recipe')
router.register(r'locations', Locations, 'location')
router.register(r'ingredients', Ingredients, 'ingredient')
router.register(r'recipeingredients', RecipeIngredients, 'recipeingredient')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
