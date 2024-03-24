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


if [ $api_flag -eq 1 ] && [ $worker_flag -eq 0 ]; then
    echo "\n >>> Build and run 'api' service ... \n"
    docker-compose up --build -d
    docker logs -f --tail 50 EVapi

# This option is using to run the worker and api on the same server.
elif [ $worker_flag -eq 1 ] && [ $api_flag -eq 1 ]; then
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
