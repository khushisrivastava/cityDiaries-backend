from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.core.cache import cache

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.utils import json
from django.db.models.functions import Cast
from django.db.models import Avg, FloatField
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.core.files import File, temp
from django.http import HttpResponse
import urllib
import requests as r
import os

from .models import *
from .serializers import *


def fetch_or_create_place(data):
    fields = ['icon', 'name', 'place_id', 'address', 'rating', 'type']
    for x in fields:
        if x not in data:
            raise Exception(f"Missing {x}")
        # if data[x] == None:
            # data.pop(x)
    
    query = Place.objects.filter(place_id=data['place_id'])
    if query:
        return query.first()
    else:
        return Place.objects.create(**data)


class GoogleMaps(viewsets.ViewSet):
    # @method_decorator(cache_page(60*60*2))
    @action(methods=['GET'], detail=False)
    def places_nearby(self, request):
        key = os.environ.get('gmap_key')
        baseUrl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        location = request.query_params.get('location', "")
        radius = request.query_params.get('radius', "")
        types = request.query_params.get('types', "")
        name = request.query_params.get('name', "")
        next_page_token = request.query_params.get('next_page_token', "")

        location = ",".join(map(lambda x: f"{float(x):.2f}", location.split(",")))
        
        query = baseUrl + \
            "location={}&radius=1500&types={}&name={}&next_page_token={}&key={}".format(
                location, types, name, next_page_token, key)
        
        # caching_page = cache.get(query)

        # if caching_page == None:
        #     print('\n\nIN IF')
        #     cache.set(query, r.get(query), 60*60*2)
        #     caching_page = cache.get(query)
        
        # data = r.get(query)
        # data = json.loads(caching_page.text)

        with open("./core/json/place.json", 'r') as f:
            data = json.load(f)[types]

        if data:
            data = data
            if 'next_page_token' not in data.keys():
                data['next_page_token'] = None

            for x in data['results']:
                x['type'] = types

                review = Review.objects.filter(place__place_id=x['place_id']).only('review', 'place__type')
                if review.count() == 0:
                    x['avg_ratings'] = 0
                else:
                    questions = Question.objects.filter(type=review.first().place.type).values_list('id', flat=True)
                    
                    ratings = 0
                    for question in questions:
                        ratings += review.annotate(rating_value=Cast(KeyTextTransform("q" + str(question), 'review'), FloatField())).aggregate(Avg('rating_value'))['rating_value__avg']

                    x['avg_ratings'] = round(ratings/len(questions), 1)
                    print(x['avg_ratings'])

            if request.user.is_authenticated:
                fav_places = request.user.fav_places.only('place_id')
                for x in data['results']:
                    
                    if fav_places.filter(place_id=x['place_id']):
                        x['is_favourite'] = True
                    else:
                        x['is_favourite'] = False
        else:
            data = {
                "message": "something went wrong"
                }
        return Response(data)
    
    # @method_decorator(cache_page(60*60*2))
    @action(methods=['GET'], detail=False)
    def details(self, request):
        
        key = os.environ.get('gmap_key')
        baseUrl = "https://maps.googleapis.com/maps/api/place/details/json?"
        place_id = request.query_params.get('place_id', "")

        query = baseUrl + \
            "place_id={}&key={}".format(place_id, key)
        print("\n\nQUERY:", query)

        # caching_page = cache.get(query)

        # if caching_page == None:
        #     print('\n\nIN IF')
        #     cache.set(query, r.get(query), 60*60*2)
        #     caching_page = cache.get(query)
        
        # data = r.get(query)
        # data = json.loads(caching_page.text)
        with open("./core/json/detail.json", 'r') as f:
            data = json.load(f)[place_id]
        
        if data:
            response_data = data
            if request.user.is_authenticated:
                if request.user.fav_places.filter(place_id=response_data['result']['place_id']):
                    response_data['result']['is_favourite'] = True
                else:
                    response_data['result']['is_favourite'] = False
            
            review = Review.objects.filter(place__place_id=place_id).only('review', 'place__type')
            
            if review.count() == 0:
                response_data['result']['avg_ratings'] = None
            else:
                questions = Question.objects.filter(type=review.first().place.type).values_list('id', flat=True)
                
                response_data['result']['avg_ratings'] = {}
                
                for question in questions:
                    response_data['result']['avg_ratings'][question] = review.annotate(rating_value=Cast(KeyTextTransform("q" + str(question), 'review'), FloatField())).aggregate(Avg('rating_value'))['rating_value__avg']
                
        else:
            response_data = {
                "message": "Something went wrong!"
            }
        return Response(response_data)

    # @method_decorator(cache_page(60*60*2))
    @action(methods=['GET'], detail=False)
    def place_photos(self, request):

        key = os.environ.get('gmap_key')
        baseUrl = "https://maps.googleapis.com/maps/api/place/photo?"

        photoreference = request.query_params.get('photoreference')
        
        place_photo = Photos.objects.filter(photo_reference=photoreference)
        
        if place_photo:
            img = place_photo.first().photo
            return HttpResponse(img, content_type='image/jpg')
        
        else:
            query = baseUrl + \
            "maxwidth={}&photoreference={}&key={}".format(
                request.query_params.get('maxwidth',''), photoreference, key)
            data = r.get(query, stream=True)
            image = temp.NamedTemporaryFile()
            for i in data.iter_content(1024*8):
                if not i:
                    break
                image.write(i)
            image_name = f'photoreference.jpg'
            image.flush()
            file = File(image, name=image_name)
            
            serializer = PhotoSerializer(data={'photo_reference':photoreference, 'photo':file})
            if serializer.is_valid():
                serializer.save()
        
            image_data = serializer.instance.photo
            return HttpResponse(image_data, content_type='image/jpg')


    # @method_decorator(cache_page(60*60*2))
    @action(methods=['GET'], detail=False)
    def rev_geocode(self, request):

        key = os.environ.get('gmap_key')
        baseUrl = "https://maps.googleapis.com/maps/api/geocode/json?"

        latlng = request.query_params.get('location')

        query = baseUrl + \
            "latlng={}&key={}".format(latlng, key)

        print('\n\n\nQUERY:',query)
        data = r.get(query)
        data = json.loads(data.text)

        if data:
            request_data = data
        else:
            request_data = {
                "message": "Something Went Wrong"
            }
        return Response(request_data)


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['POST'], detail=False)
    def toggle_fav(self, request):
        try:
            place = fetch_or_create_place(request.data)
            if place in request.user.fav_places.all():
                request.user.fav_places.remove(place)
            else:
                request.user.fav_places.add(place)

            return Response({
                'message': 'Success'
            })

        except Exception as e:
            return Response({
                'details': str(e)
            }, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['GET'], detail=False)
    def fav_places(self, request):
        response_data = PlaceSerializer(request.user.fav_places.all(), many=True).data
        return Response(response_data)


class RatingsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            return ReviewReadSerializer
        else:
            return ReviewSerializer

    @action(methods=['POST'], detail=False)
    def rate_restaurant(self, request):
        review = request.data.get('review')
        
        place = fetch_or_create_place({
            'type': request.data.get('type'),
            'place_id': request.data.get('place_id'),
            'icon': request.data.get('icon'),
            'name': request.data.get('name'),
            'address': request.data.get('address'),
            'rating': request.data.get('rating')
        })
        
        review = Review.objects.create(
            user=request.user,
            place=place,
            review=review
        )
        
        rated_restaurants = self.queryset.filter(place__id=place.id).only('review', 'place__type')
        questions = Question.objects.filter(type=rated_restaurants.first().place.type).values_list('id', flat=True)
                    
        ratings = 0
        for question in questions:
            ratings = rated_restaurants.annotate(rating_value=Cast(KeyTextTransform("q" + str(question), 'review'), FloatField())).aggregate(Avg('rating_value'))['rating_value__avg']

        place.rating = ratings
        place.save()
        
        return Response({
            'review_id': review.pk,
            'message': 'success'
        })

    @action(methods=['GET'], detail=False)
    def review_list(self, request):
        response_data = self.get_serializer_class()(Review.objects.filter(user=request.user), many=True).data

        fav_places = request.user.fav_places.only('place_id')
        for x in response_data:
            if fav_places.filter(place_id=x['place']['place_id']):
                x['place']['is_favourite'] = True
            else:
                x['place']['is_favourite'] = False
            x['place']['rating'] = sum(x['review'].values())/len(x['review'].values())

        return Response(response_data)


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(type=self.request.query_params.get("type")).order_by('id')


class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer

    def get_queryset(self):
        return Cities.objects.filter(name__istartswith=self.request.query_params.get("city"))[:15]
