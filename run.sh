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

docker system prune -f
docker volume prune -f

if [ $api_flag -eq 1 ]; then
    docker-compose up --build -d
elif [ $worker_flag -eq 1 ]; then
    docker build -t everythingcharge-worker .
    docker run -it -d --env-file .env \
      --network everythingcharge_app-network \
      --name everythingcharge-worker \
      -p "$WS_SERVER_PORT:$WS_SERVER_PORT" \
      everythingcharge-worker
    echo "Connecting worker to the queue on the '$RABBITMQ_HOST' host ..."
fi
