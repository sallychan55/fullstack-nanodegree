# fullstack-nanodegree
Full Stack Nanodegree Project

## Table of contents
- [Movies](#movies)
- [Portfolio_Site](#portfolio_site)
- [Multi_User_Blog](#multi_user_blog)
- [Tournament](#tournament)

## Movies
This folder is for a project "Movie Trailer Website".
To open the movie trailer website, run entertaiment_center.py.
So that the page is came up and you can see movies and watch the trailers by clicking poster images. 

## Portfolio_Site
The folder contains all codes for "Portfolio Site" project. Index.html shows the page.

## Multi_User_Blog
This project codes are stored under multi_user_blog folder.

This project runs on Google Cloud Platform. You can visit [the page](https://hello-world-sally-158219.appspot.com) to see a sample.

From the top page, a user can:

1. view existing posts but cannot edit them until login
2. create a new account (/signup)
3. login (/login)

After logged in, a user can:

1. create a new post (/blog/newpost)
2. edit/delete posts that are owned by the user
3. create a new comment on posts
4. edit/delete comments that are owned by the user
5. like/unlike other users' posts
6. logout (/logout)

## Tournament
This folder contains one database configuration file and two python files.

* tournament.sql -  This file is used to set up database schema.
* tournament.py - This file is a library of functions to provide access to the database for adding, deleting or querying data from a client program.
* tournament_test.py - This is a client program to verify functions in the tournament.py.

To start this application:

1. Run tournament.sql from psql by following command "\i tournament.sql". That works to build a tournament database, players and matches tables.
2. Then run tournament_test.py to verify functions in tournament.py to manage players and games.
3. After running the test script, you will see results of 10 tests.

