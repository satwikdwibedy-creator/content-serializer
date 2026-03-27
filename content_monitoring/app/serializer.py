from rest_framework import serializers
from .models import Keyword, ContentItem, Flag


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'
class FlagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Flag
        fields='__all__'
        