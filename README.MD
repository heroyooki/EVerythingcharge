The OCPP Management System is primarily designed for Charge Point Operators (CPOs).
----------
Supports both OCPP versions: 1.6 and 2.0.1.
----------

The system's main feature lies in its high scalability. It could become quite inconvenient to maintain websocket
connections from all your stations on a single server. Constantly connecting new stations poses a challenge,
and in the event of server failure, all stations will be disconnected,
potentially causing your business operations to come to a halt.

The system enables the distribution of WebSocket connections among various servers and providers. In this setup,
the server housing the API service is designated as the master server, while the server hosting the worker is
regarded as a slave server. Slave servers directly engage with the charge points and communicate with the
master server to exchange messages.
The number of slave servers can be adjusted as needed to meet business requirements.

Deployment
----------

Setup environment variables

- ```$ cp .env.backend .env```

Run `api` service

- ```$ sh run.sh -s api```

Make sure to specify the correct `RABBITMQ_HOST` in your `.env` file, then proceed to run the worker service.

- ```$ sh run.sh -s worker```

How it works.
----------
`API` - The only service that accepts requests from the front-end and has a monopoly access
to the database. It implements the entire business logic.

`Worker` - Accepts and maintains WebSocket connections from the charging stations. It receives messages from both
the stations and `API` service. If a station sends a message, the service forwards it to the `API` service
through the queue. If the `API` service sends a message, the service redirects it to the station through an existing
connection. Each new `worker` creates a new queue in rabbitmq and listens for messages from it.

`RabbitMQ` - Works independently from the other services. Fanout exchange applied.

`DB` - Postgresql database.

Currenlty implemented scenarios.
--------
`Station connected`.
Every time the station connects to the `worker`, the `API` service can reject the connection if the station
is not authorized. Conversely, if the station is recognized, the connection will be successfully established.

`Authenticate station`.
Authentication is based on the stations's existence in the `charge_points` table in the database.

`Station disconnected`.
Every time the `worker` loses connection with a specific station, the `API` service will be notified. Upon receiving
this notification, the statuses of the station and connectors will be updated to `Unavailable`.

`BootNotification`.
The station provides additional information about itself in the message, including model, vendor, serial number etc.
This information is used to update the charging station's details in the database. The `API` service responds
with a Heartbeat interval, specified in the env variable `HEARTBEAT_INTERVAL`.

`StatusNotification`.
In progress ...





