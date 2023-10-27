#!/bin/bash

#update of server

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo "${SCRIPT_DIR}"

echo "$(date +%Y-%m-%d/%H:%M:%S)> update dst in schedule" >> ${SCRIPT_DIR}/logs/schedule.log

cd ${SCRIPT_DIR}
./stop.sh
# ./update_dst.sh
./start.sh
