#!/bin/bash

set -a
. ./.env

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

ensure_backend_env() {
    local var_name="$1"
    echo "Start ensure backend env with '$var_name'."

    local var_value="${!var_name}"
    if [ -z "$var_value" ]; then
        echo "Environment variable $var_name is not set or empty."
        read -p "Enter a value for $var_name: " input_value
        export "$var_name"="$input_value"
    else
        echo "Value for environment variable $var_name is already set as '$var_value'"
        read -p "Are you sure you want to keep the current value? (y/n): " confirmation
        if [ "$confirmation" = "y" ]; then
            echo "Keeping the current value: $var_value"
        else
            read -p "Enter a new value for $var_name: " new_value
            export "$var_name"="$new_value"
        fi
    fi
}

ensure_frontend_env() {
    echo "VITE_API_URL=$ALLOWED_ORIGIN:$HTTP_SERVER_PORT" > frontend/.env.local
}

if [ $api_flag -eq 1 ] && [ $worker_flag -eq 0 ]; then
    ensure_backend_env "ALLOWED_ORIGIN"
    ensure_frontend_env
    echo "\n >>> Build and run 'api' service ... \n"
    docker-compose up --build -d
    docker logs -f --tail 50 EVapi

# This option is using to run the worker and api on the same server.
elif [ $worker_flag -eq 1 ] && [ $api_flag -eq 1 ]; then
    ensure_backend_env "ALLOWED_ORIGIN"
    ensure_frontend_env
    echo "\n >>> Build and run 'api' and 'worker' services ... \n"
    echo "VITE_API_URL=$ALLOWED_ORIGIN:$HTTP_SERVER_PORT" > frontend/.env.local
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
    ensure_env "RABBITMQ_HOST"
    echo "\n >>> Build and run 'worker' service ... \n"
    docker build -t everythingcharge-worker .
    docker run -it -d --env-file .env \
      --name EVworker \
      -p "$WS_SERVER_PORT:$WS_SERVER_PORT" \
      everythingcharge-worker
    echo "\n >>> Connecting worker to the queue on the '$RABBITMQ_HOST' host ... \n"
    docker logs -f --tail 50 EVworker
fi