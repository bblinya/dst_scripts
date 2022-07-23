STEAM_CMD_HOME="$HOME/steamcmd"

DST_HOME="$HOME/dst"

DST_KLEI="$HOME/.klei/DoNotStarveTogether"

TEMPLATE_DIR="$(pwd)/templates"

CLUSTER_NAME="BBWM_3"

CLUSTER_PATH="$DST_KLEI/$CLUSTER_NAME"

function fail()
{
	echo Error: "$@" >&2
	exit 1
}

function check_for_file()
{
	if [ ! -e "$1" ]; then
		fail "Missing file: $1"
	fi
}

echo "Init Cluster Name: $CLUSTER_NAME"

