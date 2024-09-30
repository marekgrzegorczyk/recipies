from django.urls import path, include
from recipe import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()  # autogenerate urls for viewset
router.register('recipes', views.RecipeViewSet)  # register viewset with router

app_name = 'recipe'

urlpatterns = [
    # path('', RecipeViewSet.as_view({'get': 'list'}), name='recipe-list'),
    path('', include(router.urls))
]
