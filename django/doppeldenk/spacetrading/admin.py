from django.contrib import admin
import spacetrading

# Register your models here.

admin.site.register(spacetrading.models.Game)
admin.site.register(spacetrading.models.Planet)
admin.site.register(spacetrading.models.Player)
