# snippets/views.py
from django.contrib.auth.models import User # new
from .permissions import IsOwnerOrReadOnly # new
from rest_framework import generics, permissions # new
from rest_framework import generics
from rest_framework.decorators import api_view # new
from rest_framework.response import Response # new
from rest_framework.reverse import reverse # new
from rest_framework import generics, permissions, renderers 



@api_view(['GET']) # new
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

from .models import Snippet
from .serializers import SnippetSerializer, UserSerializer # new

class SnippetHighlight(generics.GenericAPIView): # new
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
        
class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly) 


class UserList(generics.ListAPIView): # new
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView): # new
    queryset = User.objects.all()
    serializer_class = UserSerializer