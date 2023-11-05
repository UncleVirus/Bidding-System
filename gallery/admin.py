from django.contrib import admin
from .models import Arts
from .models import Video
from .models import Events
from .models import TeamMember
from .models import Transaction


@admin.register(Arts)
class ArtsAdmin(admin.ModelAdmin):
 list_display = [ "art_id", "title", "description", "cost"]


@admin.register(Video)
class Video(admin.ModelAdmin):
 list_display = ["title", "description",]


@admin.register(Events)
class Events(admin.ModelAdmin):
 list_display = ["title", "date", "time", "location", "description"]

@admin.register(TeamMember)
class TeamMembers(admin.ModelAdmin):
 list_display = ["name", "member_Id"]


@admin.register(Transaction)
class Transaction(admin.ModelAdmin):
  list_display = ("receipt_no","sender_no","amount","transaction_date","status")



from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

class CustomGroupAdmin(GroupAdmin):
    actions = ['add_users_action']  # Add the desired action to the group admin page

    def add_users_action(self, request, queryset):
        # Perform the action here (e.g., adding users to the group)
        # You can access the selected groups with `queryset`
        # and the current request using `request`
        pass  # Replace this with your desired implementation
    add_users_action.short_description = 'Add users'  # Set the action's display name


admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)