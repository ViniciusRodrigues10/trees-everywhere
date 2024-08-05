from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from .models import PlantedTree
from .serializers import PlantedTreeSerializer, AuthSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# 1. Log in as a user registered by the admin.
class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return super().post(request, format=None)


# 2. View trees planted by a user.
class UserPlantedTreesView(generics.ListAPIView):
    serializer_class = PlantedTreeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PlantedTree.objects.filter(user=self.request.user)


# 3. Display the data of a selected planted tree.
class PlantedTreeDetailView(generics.RetrieveAPIView):
    queryset = PlantedTree.objects.all()
    serializer_class = PlantedTreeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PlantedTree.objects.filter(user=self.request.user)


class PlantTreeView(generics.CreateAPIView):
    serializer_class = PlantedTreeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user, account=self.request.user.profile.account
        )

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id
        print(data)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class UserPlantedTreesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        planted_trees = PlantedTree.objects.filter(user=request.user)
        serializer = PlantedTreeSerializer(planted_trees, many=True)

        return Response(serializer.data)
