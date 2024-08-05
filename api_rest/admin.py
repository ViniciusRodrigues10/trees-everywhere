from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Account, Profile, Tree, PlantedTree


# Action to activate accounts
def activate_accounts(modeladmin, request, queryset):
    queryset.update(active=True)


activate_accounts.short_description = "Activate selected accounts"


# Action to deactivate accounts
def deactivate_accounts(modeladmin, request, queryset):
    queryset.update(active=False)


deactivate_accounts.short_description = "Deactivate selected accounts"


# Custom UserAdmin
class CustomUserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "date_joined", "profile_about")
    list_display_links = ("username", "email")
    search_fields = ("username", "email")
    list_per_page = 10

    fieldsets = ((None, {"fields": ("username", "email")}),)

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", "accounts"),
            },
        ),
    )

    def profile_about(self, obj):
        return obj.profile.about if hasattr(obj, "profile") else ""

    profile_about.short_description = "About"


class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "active")
    list_display_links = ("name",)
    search_fields = ("name", "created")
    list_per_page = 10
    actions = [activate_accounts, deactivate_accounts]


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "about", "joined")
    list_display_links = ("user",)
    search_fields = ("user__username", "joined")
    list_per_page = 10


class TreeAdmin(admin.ModelAdmin):
    list_display = ("name", "scientific_name")
    search_fields = ("name", "scientific_name")


class PlantedTreeAdmin(admin.ModelAdmin):
    list_display = ("tree", "user", "planted_at", "age", "location", "account")
    search_fields = ("tree__name", "user__username", "account__name")
    list_filter = ("account", "tree")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("tree", "user", "account")

    def tree_name(self, obj):
        return obj.tree.name

    tree_name.short_description = "Tree Name"


# Registration of models in the admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tree, TreeAdmin)
admin.site.register(PlantedTree, PlantedTreeAdmin)
