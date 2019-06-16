from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import  Post, Category
from .serializers import PostSerializer, PostDetailSerializer, CategorySerializer, CategoryDetailSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NOMAL)
    #permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class =  CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NOMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)
