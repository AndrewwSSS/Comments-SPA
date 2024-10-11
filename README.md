# Comments-SPA

## Overview
Comments-SPA is a Single Page Application (SPA) designed to handle comment functionalities efficiently. This project allows users to create, view, and manage comments seamlessly. It provides a smooth user experience with real-time updates, leveraging modern front-end technologies.

Features
Real-time comment creation and management: Add, retrieve comments without page reloads.
API Integration: Uses a RESTful API to handle backend interactions.
Single Page Application: Built using SPA architecture for improved performance and user experience.
Technologies Used

Frontend:
JavaScript (Vue.js)
HTML5 & CSS3

Backend:
Django, DRF, WebSockets
PostrgreSQLMySQL for database management

Tools:
Docker (for containerization)
RESTful API for backend communication

## Requirements
1. Docker
2. Internet connection

## Installation
Clone the Repository:

```bash
git clone https://github.com/AndrewwSSS/Comments-SPA.git
cd Comments-SPA
```

### Configure settings

#### Backend:

```bash
cd backend
cat .env.template > .env
```

Specify required setting. For example:
```bash
POSTGRES_PASSWORD=db
POSTGRES_USER=db
POSTGRES_DB=db
POSTGRES_HOST=db
POSTGRES_PORT=5432
DJANGO_SECRET_KEY=dfgf34vuDs43f1ds3dsf
```

#### Frontend:

```bash
cd frontend
cat .env.temlate > .env
```
For running from docker no more changes needed

## Run application:
```bash
docker-compose up --build
```

Contributing
If you would like to contribute to this project, feel free to fork the repository and submit a pull request with your proposed changes.

License
This project is licensed under the MIT License.