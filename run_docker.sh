#!/bin/sh
sudo docker run --name flask_app_pg -e POSTGRES_USER=root -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=flask_app_db -p 5432:5432 -d postgres:13.2
