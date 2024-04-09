### Forever public and in free access!

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

Deployment
----------

### Raise app on the single server:

- ```$ cp .env.backend .env```
- Setup environment variables
- ```$ sh run.sh -s api -s worker```

### Raise one more `worker` on the different server:

- ```$ cp .env.backend .env```
- Make sure that the `RABBITMQ_HOST` refers to the host with running `api`.
- ```$ sh run.sh -s worker```

#### Websocket URL `ws://{your_host}:{your_port}/{charge_point_id}` (example: `ws://localhost:3000/CP0001`)

### API documentation is available on the `http://{your_host}:8000/docs`

Currenlty implemented scenarios.
--------

| Action             | Description                                                                                                                                                                                                                                                                                                       |
|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Station connected  | Every time the station connects to the `worker`, the `API` service can reject the connection if the station is not authorized. Conversely, if the station is recognized, the connection will be successfully established.                                                                                         |
| Authenticate station | Authentication is based on the stations's existence in the `charge_points` table in the database.                                                                                                                                                                                                                 |
| Station disconnected | Every time the `worker` loses connection with a specific station, the `API` service will be notified. Upon receiving this notification, the statuses of the station and connectors will be updated to `Unavailable`.                                                                                              |
| BootNotification   | The station provides additional information about itself in the message, including model, vendor, serial number etc. This information is used to update the charging station's details in the database. The `API` service responds with a Heartbeat interval, specified in the env variable `HEARTBEAT_INTERVAL`. |
| StatusNotification | Updates charge point's status. Creates connectors or updates ones with statuses and error codes.                                                                                                                                                                                                                  |
| Heartbeat          | Sync current `API's` (not `worker`) and the station's UTC.                                                                                                                                                                                                                                                        |    
| Reset              | Every status, except 'Rejected' is getting considered as a permission to reset statuses to 'Unavailable'. If the client received charge_point in the response with 'Unavailable' status, this means the operation was accepted by the station.                                                                                                              |  
|   Unlock connector | In progress ...|



