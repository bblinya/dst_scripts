#!/bin/bash

#update of server

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo "${SCRIPT_DIR}"

source ${SCRIPT_DIR}/common.sh

echo "$(date +%Y-%m-%d/%H:%M:%S)> update dst in schedule" >> ${LOG_DIR}/schedule.log

cd ${SCRIPT_DIR}
./stop.sh
./update_dst.sh
./start.sh
