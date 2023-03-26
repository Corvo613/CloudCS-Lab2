# Лабораторная работа №2

### Цели и задачи:
1. Реализовать авторизацию сервиса через `OAuth2` с помощью стороннего сервиса Identity Provider.
2. Доработать код аутентификации сервиса из прошлой лабораторной работы.
3. Докеризировать созданный сервис и связать несколько сервисов в **docker compose** файл.
4. Настроить автоматическую публикацию образа сервиса в репозиторий `DockerHub` с помощью **Github Actions**.

### Шаги выполнения лабораторной работы

#### 1. Реализация сервиса Identity

#### 2. Доработка кода сервиса из прошлой лабораторной работы

#### 3. Оборачивание сервиса в Docker представление
1. Создайте новый файл в корне проекта с названием `ServerDockerfile`
2. Вставьте следующий код в созданный файл
````
FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./models ./models
COPY ./src/server .

CMD [ "uvicorn" , "main:app", "--host", "0.0.0.0", "--port", "8000"]
````
Тут из интересных моментов можно выделить следующее:
* Для запуска сервиса будем использовать python3.10, для этого возьмем образ с оф. репозитория `python:3.10-slim-buster`
* Необходимо скопировать все необходимые для развертывания файлы внутрь образа
* Запустить сервис с помощью команды `uvicorn main:app --host 0.0.0.0 --port 8000`. Тут мы указывает, что хотим прослушивать сервис на 8000 порту
3. Создайте образ вашего сервиса командой `docker build . -f ServerDockerfile -t server_image`, где:
* флаг **-f** указывает путь к вашему докер-файлу;
* флаг **-t** указывает имя, которым будет называться образ.
4. Найти новоиспеченный образ можно в списке всех образов с помощью команды `docker image ls`
5. Следующим шагом будет создание контейнера на основе образа с помощью команды: `docker run -p 8000:8000 --name server_container server_image`, где:
* флаг **-p** указывает порты, которые будут связаны между хост-машиной и контейнером;
* **--name** указывает имя контейнера;
* последним параметром указываем имя образа, по образу и подобию которого нужно создать контейнер.
6. Теперь создайте новый файл в корне проекта с названием `docker-compose.yml` и описанием запускаемых контейнеров:
````
version: "3.9"
services:
  server:
    container_name: server
    build: 
      context: .
      dockerfile: ServerDockerfile
    ports:
      - 8000:8000
````
7. После выполнения команды `docker compose up -d` у нас автоматически создадутся необходимые образы и контейнеры докер.

#### Настройка CI-конвеера



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
