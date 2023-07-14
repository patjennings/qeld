# base push
# scp -rp ~/Documents/dev/qeld/* debian@51.210.101.191:/var/www/piliers-kernilis.fr

# update
# scp -rp ~/Documents/dev/qeld/qeld/* debian@51.210.101.191:/var/www/piliers-kernilis.fr/qeld
scp -rp ~/Documents/dev/qeld/public/* debian@51.210.101.191:/var/www/piliers-kernilis.fr/qeld/public
scp -rp ~/Documents/dev/qeld/season_manager/static/assets/* debian@51.210.101.191:/var/www/piliers-kernilis.fr/qeld/season_manager/static/assets
scp -rp ~/Documents/dev/qeld/season_manager/static/js/* debian@51.210.101.191:/var/www/piliers-kernilis.fr/qeld/season_manager/static/js
scp -rp ~/Documents/dev/qeld/season_manager/static/postcss.config.js debian@51.210.101.191:/var/www/piliers-kernilis.fr/qeld/season_manager/static
scp -rp ~/Documents/dev/qeld/season_manager/static/tailwind.config.js debian@51.210.101.191:/var/www/piliers-kernilis.fr/qeld/season_manager/static
scp -rp ~/Documents/dev/qeld/season_manager/static/style.css debian@51.210.101.191:/var/www/piliers-kernilis.fr/qeld/season_manager/static
scp -rp ~/Documents/dev/qeld/season_manager/static/tailwind.css debian@51.210.101.191:/var/www/piliers-kernilis.fr/qeld/season_manager/static
scp -rp ~/Documents/dev/qeld/season_manager/management/* debian@51.210.101.191:/var/www/piliers-kernilis.fr/qeld/season_manager/management
scp -rp ~/Documents/dev/qeld/season_manager/templates/* debian@51.210.101.191:/var/www/piliers-kernilis.fr/qeld/season_manager/templates
scp -rp ~/Documents/dev/qeld/season_manager/models.py debian@51.210.101.191:/var/www/piliers-kernilis.fr/qeld/season_manager/
scp -rp ~/Documents/dev/qeld/season_manager/urls.py debian@51.210.101.191:/var/www/piliers-kernilis.fr/qeld/season_manager/
scp -rp ~/Documents/dev/qeld/season_manager/views.py debian@51.210.101.191:/var/www/piliers-kernilis.fr/qeld/season_manager/
scp -rp ~/Documents/dev/qeld/db.sqlite3 debian@51.210.101.191:/var/www/piliers-kernilis.fr/qeld/

