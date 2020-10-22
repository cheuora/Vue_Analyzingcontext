# nginx -s stop and kill uwsgi process beforen run this script
nginx
uwsgi start.ini &
