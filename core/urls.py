from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register('place', PlaceViewSet, basename='place')
router.register('review', RatingsViewSet, basename='rating')
router.register('maps', GoogleMaps, basename='maps')
router.register('questions', QuestionViewSet, basename='questions')
router.register('cities', CityViewSet, basename='cities')

urlpatterns = router.urls
