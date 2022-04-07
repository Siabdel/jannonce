## create database
## psql -h 192.168.59.103 -p 49159 -d docker -U docker --password
# passd postgres = "gr1"
su - postgres -c "psql -f /home/django/.virtualenvs/envMagenda/jannonces/docker/sql/dbcreate.sql;"
