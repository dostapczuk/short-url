import random
import string

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
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
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(6))

    def create(self, request, *args, **kwargs):
        url = request.data['url']
        alias = self._create_alias()
        serializer = self.get_serializer(data={"url": url, "alias": alias})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"short_url": request.build_absolute_uri(f"/{serializer.data['alias']}")})

    def retrieve(self, request, pk):
        instance = get_object_or_404(ShortUrl, alias=pk)
        serializer = ShortURLSerializer(instance)
        return HttpResponseRedirect(redirect_to=serializer.data["url"])

    @action(methods=['GET'], detail=True)
    def get_url(self, request, pk):
        instance = get_object_or_404(ShortUrl, alias=pk)
        serializer = ShortURLSerializer(instance)
        return Response({"url": serializer.data["url"]})
