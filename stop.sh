#!/bin/bash

source common.sh

if screen -list | grep -q "${SC_NAME}"; then
  echo "shutdown previous dst server"
  screen -dr ${SC_NAME} -X stuff "c_shutdown()\n"
  screen -dr ${SC_NAME} -X stuff "c_shutdown()\n"
  sleep 2
  screen -dr ${SC_NAME} -X quit
  echo "shutdown done."
fi
