#!/bin/sh
sudo docker run --name some_mysql -e MYSQL_ROOT_PASSWORD=pass -p 3306:3306 -d mysql:latest
