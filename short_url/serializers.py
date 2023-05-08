from rest_framework import serializers

from short_url.models import ShortUrl


class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortUrl
        fields = ('url', 'alias')
