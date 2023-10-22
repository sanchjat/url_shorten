===============================
short_url
===============================

Generate short url

# Prerequisite
- Docker


# Description

* This is a URL shorten server. which give short url for long urls.

# Build
 - run `docker compose build`

# Run application
- run `docker compose up`.


# APIs
- Generate Token `curl -X POST -H "content-type:application/json" http://127.0.1:5000/users/login -d '{"email": "admin@admin.com", "password":"admin"}'`

  Response : `{
  "message": "Successfully fetched auth token", 
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsImNyZWF0ZWRfYXQiOiIyMDIzLTEwLTIyIDExOjIwOjAzLjAyMTA2OCJ9.KWnXM4mkVcPUjoXt5daq9Stjic5RuWHZExExDG2ff0I"
}`

- API request `curl -X POST    -H "Authorization:abc eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsImNyZWF0ZWRfYXQiOiIyMDIzLTEwLTIyIDExOjIwOjAzLjAyMTA2OCJ9.KWnXM4mkVcPUjoXt5daq9Stjic5RuWHZExExDG2ff0I"   -H "content-type:application/json" http://127.0.0.1:5000/url -d '{"original_url" : "http://google.com"}'` 
 
 Response: `{
  "short_url": "http://localhost:5000/gd"
}`



Notes:
- For now I am running flask server directly but in prod we can run via `uwsgi`
- Didn't get a time to write a testcase, just added 2 test for util
- I also wanted to added comments in functions.