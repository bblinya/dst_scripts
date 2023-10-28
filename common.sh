STEAM_CMD_HOME="$HOME/steamcmd"

DST_HOME="$HOME/dst"

DST_KLEI="$HOME/.klei/DoNotStarveTogether"

TEMPLATE_DIR="$(pwd)/templates"

export CLUSTER_NAME="Myth"
# CLUSTER_NAME="BBWM"

CLUSTER_PATH="$DST_KLEI/$CLUSTER_NAME"

SC_NAME="dst_server"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
LOG_DIR="${SCRIPT_DIR}/logs"

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

