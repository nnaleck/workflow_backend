from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from django.contrib.auth import password_validation
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True
    )
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'password', 'password_confirmation',
            'email', 'first_name', 'last_name'
        ]
        read_only_fields = ['username']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({
                'password': 'Passwords does not match.'
            })

        user_attributes = {x: attrs[x] for x in attrs if x not in {'password_confirmation'}}

        user = User(**user_attributes)

        try:
            password_validation.validate_password(password=attrs['password'], user=user)
        except ValidationError as e:
            raise serializers.ValidationError({
                'password': list(e.messages)
            })

        return attrs

    def create(self, validated_data):
        first_name = (validated_data['first_name'].replace(' ', '')).lower()
        last_name = (validated_data['last_name'].replace(' ', '')).lower()
        username = '_'.join([first_name, last_name])

        user = User.objects.create(
            username=username,
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
