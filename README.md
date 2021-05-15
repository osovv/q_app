# Simple Flask app
**IMPORTANT NOTICE**:

This project was abandoned to work on [Musicality](https://github.com/osovv/musicality).
Musicality bases on ideas of this project, but is built better, more scalable, has better test coverage and also provides easier extensiblity.

## Description
A simple web application written in Flask.
Created by the following [this](https://www.youtube.com/watch?v=LcZ9uJn8ffA) video.\
This is a simple application with two database tables: `users` and `music_compositions`.\
The idea is that users can register and add some music compositions (something like Instagram, but only for music and without any typical social networking elements).
## Docker Dependencies
```
python:3.9.2
postgres:13.2
```
## Instructions
Run:
```
docker-compose up
```
Now you can connect to API at `0.0.0.0:5005`
## Task List
 - [ ] Get all settings from environmental variables.
 - [ ] Write CRUD functionality for musical compositions
 - [ ] Create simple frontend to visualize users and musical compositions


## Done Tasks List
 - [x] Finish CRUD functionality for user (now only CRU)
 - [x] Configure Docker to automatically create users for databases.
 - [x] Manage creation of database and tables if they do not exist.
 - [x] Write tests for requests.
