# identity provider service
This service would do the following:

    - Authenticate users
    - Authorize users
    - Provide user information to other services

For api documentation, please visit swagger editor at http://localhost:80
and paste the content of `./OAS.json` into the editor.
docker run -d -p 80:8080 swaggerapi/swagger-editor