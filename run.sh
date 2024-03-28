#!/bin/bash

set -a
source .env

if [ $# -lt 1 ]; then
    echo "Usage: $0 -s [api|worker]"
    exit 1
fi

api_flag=0
worker_flag=0

while getopts ":s:" opt; do
    case ${opt} in
        s )
            case $OPTARG in
                api )
                    api_flag=1
                    ;;
                worker )
                    worker_flag=1
                    ;;
                * )
                    echo "Invalid argument: $OPTARG"
                    exit 1
                    ;;
            esac
            ;;
        \? )
            echo "Invalid option: $OPTARG"
            exit 1
            ;;
        : )
            echo "Option -$OPTARG requires an argument."
            exit 1
            ;;
    esac
done

set_origin() {
    if [ -z "$ALLOWED_ORIGIN" ]; then
        echo "Environment variable ALLOWED_ORIGIN is not set or empty."
        read -p "Enter a value for ALLOWED_ORIGIN: " input_value
        export "$ALLOWED_ORIGIN"="$input_value"
    else
        echo "Value for environment variable ALLOWED_ORIGIN is already set as '$ALLOWED_ORIGIN'"
        read -p "Are you sure you want to keep the current value? (y/n): " confirmation
        if [ "$confirmation" = "y" ]; then
            echo "Keeping the current value: $ALLOWED_ORIGIN"
        else
            read -p "Enter a new value for ALLOWED_ORIGIN: " new_value
            export "$ALLOWED_ORIGIN"="$new_value"
        fi
    fi
}

echo "VITE_API_URL=$ALLOWED_ORIGIN:$HTTP_SERVER_PORT" > frontend/.env.local


if [ $api_flag -eq 1 ] && [ $worker_flag -eq 0 ]; then
    set_origin
    echo "\n >>> Build and run 'api' service ... \n"
    docker-compose up --build -d
    docker logs -f --tail 50 EVapi

# This option is using to run the worker and api on the same server.
elif [ $worker_flag -eq 1 ] && [ $api_flag -eq 1 ]; then
    set_origin
    echo "\n >>> Build and run 'api' and 'worker' services ... \n"
    docker-compose up --build -d
    inspect_output=$(docker inspect everythingcharge-rabbitmq)
    ip_address=$(echo "$inspect_output" | jq -r '.[0].NetworkSettings.Networks."everythingcharge_app-network".IPAddress')
    docker build -t everythingcharge-worker .
    docker run -it -d --env-file .env \
      --network everythingcharge_app-network \
      --name EVworker \
      -p "$WS_SERVER_PORT:$WS_SERVER_PORT" \
      -e RABBITMQ_HOST=$ip_address \
      everythingcharge-worker
    echo "\n >>> Connecting worker to the queue on the '$ip_address' host ... \n"
    docker logs -f --tail 50 EVapi & docker logs -f --tail 50 EVworker

# This option is using to run the worker on the different server.
elif [ $worker_flag -eq 1 ] && [ $api_flag -eq 0 ]; then
    echo "\n >>> Build and run 'worker' service ... \n"
    docker build -t everythingcharge-worker .
    docker run -it -d --env-file .env \
      --name EVworker \
      -p "$WS_SERVER_PORT:$WS_SERVER_PORT" \
      everythingcharge-worker
    echo "\n >>> Connecting worker to the queue on the '$RABBITMQ_HOST' host ... \n"
    docker logs -f --tail 50 EVworker
fi
