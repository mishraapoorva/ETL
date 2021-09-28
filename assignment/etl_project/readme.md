# To Dockerize the ETL Pipeline
- install docker and docker-compose
- clone the repository
- cd assignment/etl_project

# To Start SQL as a deamonized service and run it on bash to validate results
- docker-compose up -d sql-db
- docker-compose exec sql-db bash
- mysql -u root -proot_password_123
> create database sfl;

# To Start Mongo as a deamonized service and run it on bash to validate results
- docker-compose up -d mongodb
- docker-compose exec mongodb bash
- mongo -u root -p
> - root
> - show dbs

# Start the webservice
- docker-compose build web
- docker-compose up -d web

# Navigate to the following URL's on browser
- http://13.233.158.185/mysql
- http://13.233.158.185/mongo



