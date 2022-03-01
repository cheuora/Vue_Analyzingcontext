# nginx -s stop and kill uwsgi process beforen run this script
# This file is deprecated (2022,03,01)
nginx
uwsgi start.ini &
