# Employee Lunch API

Internal service for its company employees which helps them to  make a decision at the lunch place.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [API online access](#live-demo)
- [DB scheme](https://monosnap.com/file/rLG56LIZWY1h6Rsa29PjaRvvL2Jrqc](https://monosnap.com/file/6lszCRY8VrNOfcQJrYoN6ilgytsHmi)
- [User permissions](#user-permissions)

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3 must be installed on your machine.
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- p.s. Docker daemon should be running on your machine.

### Installation

1. Clone the repository:

   ```shell
   https://github.com/maxkatkalov/employee-lunch-api.git

2. Clone the repository:

   ```shell
   cd employee-lunch-api

3. Create a .env file and configure the environment variables required by your project. You can use the provided .env.example as a starting point.

   ```shell
   cp .env.example .env

4. Build and start the Docker containers:

   ```shell
   docker-compose up --build

5. Create SU:
   ```shell	
   docker ps

  Connect to your Docker container: ```docker exec -it <your Docker image id> bash```

  Then: ```python manage.py createsuperuser```

6. Access the application in your web browser at http://127.0.0.1:8000/

7. To have access in browser or to send requests to all API endpoints you need to send Authorization header along with your request:
   
   - For browsers you can use [ModHeader](https://modheader.com/?ref=me&product=ModHeader&version=5.0.7&browser=chrome).
   - [Postman](https://monosnap.com/file/yX9vn5LwypObGy1nRNBC6NLlGaSdBj).
   - Default lifetime of JWT: 60 minutes. You can change this value in settings.py.

### Live demo

- You can access the live project demo [employee-lunch-api.max-katkalov.pp.ua](https://employee-lunch-api.max-katkalov.pp.ua/).
- Several points here:
  - live demo running in DEBUG mode, so you can use Django Debug Toolbar to explore the API;
  - demo has preinstalled dummy data.

- For [login]([https://care-express-api.techone.pp.ua/api/station-user/token/login/](https://employee-lunch-api.max-katkalov.pp.ua/api/user-area/token/login/)) (admin with prepared order data), you can use the following credits:

   **Logins:** 
     - admin@gmail.com (superuser);
     - dawn32@example.org (restaurant owner);
     - aliciaguerrero@example.org (employee).

   **Password:** 
     - ```LSK33D1JG*(PSJ'``` (the same for all users).

   Or you can [register](https://employee-lunch-api.max-katkalov.pp.ua/api/user-area/register/) a new user.

- For exploring the API endpoints, access the documentation:

  - [Swagger](https://employee-lunch-api.max-katkalov.pp.ua/api/doc/swagger/)
  - [Redoc](https://employee-lunch-api.max-katkalov.pp.ua/api/doc/redoc/)

### User permissions
- **Restaurant owners**:
  - GET, POST, HEAD, OPTIONS: ```/api/restaurants-management/restaurants/```
  - GET, PUT, PATCH, DELETE, HEAD, OPTIONS: ```/api/restaurants-management/restaurants/<int:pk>/```
  - GET, POST, HEAD, OPTIONS: ```/api/restaurants-management/menus/```
  - GET, PUT, PATCH, DELETE, HEAD, OPTIONS: ```/api/restaurants-management/menus/<int:pk>/```
  - p.s. user can manage only his restaurants and its menus and has no access to ```/api/polling/``` endpoints.
  
- **Employees**:
  - GET: ```/api/restaurants-management/restaurants/``` – all restaurants in DB;
  - GET: ```/api/restaurants-management/restaurants/{int:restaurant_id}```;
  - No access to ```/api/restaurants-management/menus/``` endpoint;
  - GET: ```/api/polling/polls/``` – all polls in DB;
  - GET: ```/api/polling/polls/{int:poll_id}```;
  - GET, POST, HEAD, OPTIONS: ```/api/polling/votes/``` – employee votes;
  - GET, PUT, PATCH, DELETE, HEAD, OPTIONS: ```/api/polling/votes/<int:pk>/```.

