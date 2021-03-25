# Simple Flask app
## Description
A simple web application written in Flask.
Created by the following [this](https://www.youtube.com/watch?v=LcZ9uJn8ffA) video.\
This is a simple application with two database tables: users and music_compositions.\
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
 - [ ] Write tests for requests.
 - [ ] Write CRUD functionality for musical compositions
 - [ ] Create simple frontend to visualize users and musical compositions
 - [ ] Get settings from environmental variables.

## Done Tasks List
 - [x] Finish CRUD functionality for user (now only CRU)
