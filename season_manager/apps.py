from django.apps import AppConfig

class SeasonManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'season_manager'
    SEASON_MANAGER_SEASON = '2024-2025'
    SEASON_MANAGER_HEADER = 'Piliers de Kernilis'
