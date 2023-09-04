from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from django.contrib import admin
from .models import Game,Player,Poll,Ground

# Register your models here.
# admin.site.register(Game)
# admin.site.register(Player)
admin.site.register(Poll)
# admin.site.register(Ground)

@admin.register(Game)
class GameAdmin(ImportExportModelAdmin):
    list_display = ['game_title', 'game_date', 'game_type', 'game_season', 'ground_name', 'game_poll_id', 'id']
    list_filter = ['game_season']

# class GameResource(resources.ModelResource):
    # poll = fields.Field(
        # column_name='game_poll',
        # attribute='game_poll',
        # widget=ForeignKeyWidget(Poll, 'game_poll')
    # )
    # print(poll)
    # def before_import(self, row, field, **kwargs):
        # print('this before import')

# def before_import_row(self, row, **kwargs):
    # print('this is before import')
    # poll = row.get('game_season')

    # print(poll)
    
    # Poll.objects.get_or_create(poll_season=season, defaults={"poll_season": season})
    # class Meta:
        # model = Poll

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'status', 'id']
    list_filter = ['status']

@admin.register(Ground)
class GroundAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'id']


