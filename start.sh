#!/bin/bash
#
echo "start dst server ..."

NAME="dst_server"

screen -dmS ${NAME}

# mkdir -p "${LOG_DIR}"
# screen -dr ${NAME} -X logfile "${LOG_DIR}/$(date +%Y-%m-%d).log"

screen -dr ${NAME} -X stuff "./exec.sh\n"

echo "started dst server."
