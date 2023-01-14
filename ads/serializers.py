from rest_framework import serializers

import users.models
from ads.models import Ad, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = users.models.User
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Ad
        fields = '__all__'


class AdDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Ad
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Ad
        fields = ['id', 'name', 'author', 'price', 'description', 'category']


class AdCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        ad = Ad.objects.create(**validated_data)

        ad.save()
        return ad

    class Meta:
        model = Ad
        fields = '__all__'


class AdUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    def save(self):
        ad = super().save()

        ad.save()
        return ad

    class Meta:
        model = Ad
        fields = ['name', 'author', 'price', 'description', 'category']


class AdDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ["id"]
