import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from short_url.models import ShortUrl
from short_url.serializers import ShortURLSerializer


class ShortURLViewSet(viewsets.ModelViewSet):
    queryset = ShortUrl.objects.all()
    serializer_class = ShortURLSerializer
    http_method_names = ['post', 'get']

    def _create_alias(self):
        """
        Creates 6-character alias for short url
        :return: Returns random alias
        """
        alias = str(uuid.uuid4())[:6]
        try:
            ShortUrl.objects.get(alias=alias)
            return self._create_alias()
        except ShortUrl.DoesNotExist:
            return alias

    def create(self, request):
        """
        Creates shorten url with random 6-letter string alias and returns
        shorten URL
        """
        url = request.data['url']
        alias = self._create_alias()
        serializer = self.get_serializer(data={"url": url, "alias": alias})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"short_url": request.build_absolute_uri(f"/{serializer.data['alias']}")})

    def retrieve(self, request, pk):
        """
        Gets alias and redirects to the base url
        """
        instance = get_object_or_404(ShortUrl, alias=pk)
        serializer = ShortURLSerializer(instance)
        return HttpResponseRedirect(redirect_to=serializer.data["url"])

    @action(methods=['GET'], detail=True, url_path='url')
    def get_url(self, request, pk):
        """
        Returns original URL
        """
        instance = get_object_or_404(ShortUrl, alias=pk)
        serializer = ShortURLSerializer(instance)
        return Response({"url": serializer.data["url"]})
