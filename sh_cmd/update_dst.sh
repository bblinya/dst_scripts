#!/bin/bash

source common.sh

$STEAM_CMD_HOME/steamcmd.sh \
	+@ShutdownOnFailedCommand 1 \
	+@NoPromptForPassword 1 \
	+force_install_dir ${DST_HOME} \
	+login anonymous \
	+app_update 343050 validate +quit

source ./update_mods.sh
