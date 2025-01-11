# RabbitMQ Flask React Demo

A simple message queue application built with Flask, React, RabbitMQ, Redis, and PostgreSQL.

**Stack**

* **Backend:** Flask
* **Frontend:** React
* **Message Broker:** RabbitMQ
* **Cache:** Redis
* **Database:** PostgreSQL

**Quick Start**

```bash
# Clone the repository
git clone https://github.com/amurpo/rabbitmq-flask-app>

# Start the application
docker-compose up --build
```

## Services

* **Frontend:** http://localhost:3000
* **Backend API:** http://localhost:5000
* **RabbitMQ Management:** http://localhost:15672 (guest/guest)

## API Endpoints

* **POST /send:** Send a message
* **GET /receive:** Receive a message
* **GET /last:** Get last cached message