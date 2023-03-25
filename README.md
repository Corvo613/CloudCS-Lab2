# CloudCS-Lab2

DockerHub link -> https://hub.docker.com/r/smirnoff410/cloudcs-lab2

docker compose file for pulling images example
````
version: "3.9"
services:
  server:
    image: smirnoff410/cloudcs-lab2:server
    container_name: server
    ports:
      - 8000:8000
  auth_server:
    image: smirnoff410/cloudcs-lab2:auth_server
    container_name: auth_server
    ports:
      - 8500:8500
````
