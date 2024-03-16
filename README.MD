The OCPP Management System is primarily designed for Charge Point Operators (CPOs).
----------
Supports both OCPP versions: 1.6 and 2.0.1.
----------

The system's main feature lies in its high scalability. It could become quite inconvenient to maintain websocket
connections from all your stations on a single server. Constantly connecting new stations poses a challenge,
and in the event of server failure, all stations will be disconnected,
potentially causing your business operations to come to a halt.

Fortunately, the solution offers the flexibility to distribute connections across as many servers as needed.

Deployment
----------

Setup environment variables

- ```$ cp .env.backend .env```

Run `api` service

- ```$ sh run.sh -s api```

Make sure to specify the correct `RABBITMQ_HOST` in your `.env` file, then proceed to run the worker service.

- ```$ sh run.sh -s worker```



