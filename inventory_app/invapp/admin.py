from django.contrib import admin
from .models import ItemType, InventoryItem, Location, ItemLocationAssignment, ItemAssociation

admin.site.register(ItemType)
admin.site.register(InventoryItem)
admin.site.register(Location)
admin.site.register(ItemLocationAssignment)
admin.site.register(ItemAssociation)
