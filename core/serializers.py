from rest_framework import serializers

from .models import *


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('icon', 'name', 'place_id', 'address', 'rating', 'type',)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

class ReviewReadSerializer(serializers.ModelSerializer):
    place = PlaceSerializer()

    class Meta:
        model = Review
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = "__all__"
        read_only_field = ['photo']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = "__all__"