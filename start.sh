#!/bin/bash
#
echo "start dst server ..."

source common.sh

screen -dmS ${SC_NAME}
screen -dr ${SC_NAME} -X stuff "cd ${SCRIPT_DIR} && ./exec.sh\n"

echo "started dst server."
