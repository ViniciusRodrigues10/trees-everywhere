from django.urls import path
from .views import (
    LoginView,
    UserPlantedTreesView,
    PlantedTreeDetailView,
    PlantTreeView,
    UserPlantedTreesView,
)
from knox import views as knox_views

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", knox_views.LogoutView.as_view(), name="logout"),
    # path("logoutall/", knox_views.LogoutAllView.as_view(), name="logoutall"),
    path("planted_trees/", UserPlantedTreesView.as_view(), name="planted_trees"),
    path(
        "planted_tree/<int:pk>/",
        PlantedTreeDetailView.as_view(),
        name="planted_tree_detail",
    ),
    path("plant_tree/", PlantTreeView.as_view(), name="plant_tree"),
    path(
        "account_planted_trees/",
        UserPlantedTreesView.as_view(),
        name="account_planted_trees",
    ),
]
