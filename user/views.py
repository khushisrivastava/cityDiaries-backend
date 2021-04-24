from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.views import Response


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = serializers.CharField(required=False)

    def validate(self, attrs):
        data = self.context['request'].data
        keys = ['phone', 'firebase_id']

        for key in keys:
            if key not in data:
                raise ValidationError(f'Provide {key}')
        
        queryset = get_user_model().objects.filter(phone=data['phone'])

        if not queryset:
            user = get_user_model().objects.create_user(phone=data['phone'], firebase_id=data['firebase_id'])
        else:
            validate_user = queryset.filter(firebase_id=data['firebase_id'])
            if not validate_user:
                raise ValidationError('Invalid firebase_id')
            else:
                user = queryset.first()

        token = self.get_token(user)

        return {
            'user_id': user.pk,
            'token': str(token.access_token)
        }


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)
