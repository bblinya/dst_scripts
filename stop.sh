#!/bin/bash
#
NAME="dst_server"

if screen -list | grep -q "${NAME}"; then
  echo "shutdown previous dst server"
  screen -dr ${NAME} -X stuff "c_shutdown()\n"
  sleep 0.5
  screen -dr ${NAME} -X stuff "c_shutdown()\n"
  sleep 0.5
  screen -dr ${name} -X quit
  sleep 0.5
  echo "shutdown done."
fi
