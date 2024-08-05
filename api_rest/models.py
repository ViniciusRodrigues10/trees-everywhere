from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Account(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    about = models.TextField()
    joined = models.DateTimeField(auto_now_add=True)


class Tree(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)


class PlantedTree(models.Model):
    planted_at = models.DateTimeField(auto_now_add=True)
    age = models.IntegerField(default=0)
    location = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)


class User(User):
    def plant_tree(self, tree, location):
        PlantedTree.objects.create(
            tree=tree,
            user=self,
            account=self.account,
            location=location,
        )

    def plant_trees(self, plants):
        for tree, location in plants:
            self.plant_tree(tree, location)
