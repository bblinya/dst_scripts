#!/bin/bash

#Start or Restart the server
# screen -dr dst_server -X -S "c_shutdown()"
screen -dr dst_server -X -S quit
screen -dmS dst_server "./exec.sh"
