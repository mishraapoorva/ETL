install docker and docker-compose

clone the repository

cd assignment/etl_project
docker-compose up -d sql-db
docker-compose exec sql-db bash
> mysql -u root -proot_password_123
$ create database sfl;
docker-compose build web
docker-compose up -d web
http://13.233.158.185/mysql

