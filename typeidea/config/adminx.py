import xadmin
from django.contrib import admin

from typeidea.base_admin import BaseOwnerAdmin
from .models import Link, SideBar


@xadmin.sites.register(Link)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')


@xadmin.sites.register(SideBar)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time',)
    fields = ('title', 'display_type', 'content', 'status',)
