import os
import sys
import socket
import random
import logging
import configparser
from os import path
from dataclasses import dataclass

from . import mods
from . import common

from bbcode.common import bash

logger = logging.getLogger(common.CLUSTER or "Cluster")

TOKEN_BBWM_1 = "pds-g^KU_wGWotiLQ^oX7K/9mB9Ul+P2ynzAA+bBJBTUViYHaY0k0FIx5SVsw="
TOKEN_CROWNBIOS = "pds-g^KU_wGWotiLQ^jytcPFacI4GTd0qzCmnBTBjEQxlHIHqfqjcIgDqMQ9g="

def config_token(args):
    token_path = path.join(common.CLUSTER_PATH, "cluster_token.txt")
    if path.exists(token_path):
        with open(token_path, "r") as f:
            token = f.read()
        logger.info("Use existing cluster token: %s" % token)
        return

    token = ""
    while not token.startswith("pds-"):
        logger.info("""\
Cluster token not exist, type one option (Enter to confirm):
1. [Y] to use embeded token BBWM: %s;
2. [pds-] prefix string to use custom token,
    you can get token from the official klei server:
    https://accounts.klei.com/account/game/servers?game=DontStarveTogether
3. [N] to abort\
                    """ % TOKEN_BBWM_1)
        token = "Y" if args.yes else input("> ")

        if token.upper() in ["Y", "YES"]:
            token = TOKEN_BBWM_1
            break
        elif token.upper() in ["N", "NO"]:
            sys.exit(-1)

    with open(token_path, "w") as f:
        f.write(token)

    logger.info("Use cluster token: %s" % token)

CLUSTER_INI_TEMP = """
[GAMEPLAY]
game_mode = endless
max_players = {max_players}
pvp = false
pause_when_empty = true

[NETWORK]
cluster_name = {name}
cluster_description = {desc}
cluster_intention = social
cluster_password = {password}

[MISC]
console_enabled = true

[SHARD]
shard_enabled = true
bind_ip = 127.0.0.1
master_ip = 127.0.0.1
master_port = {master_port}
cluster_key = defaultPass

"""

CLUSTRE_SERVER_TEMP = """
[NETWORK]
server_port = {server_port}

[SHARD]
is_master = {is_master}
{cave_temp}

[ACCOUNT]
encode_user_path = true


[STEAM]
master_server_port = {master_server_port}
authentication_port = {authentication_port}
"""

def port_in_use(port_num: int) -> bool:
    # check udp bind
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.bind(("127.0.0.1", port_num))
    except Exception as e:
        s.close()
        return True
    s.close()
    return False

def port_lookup(port_num: int) -> int:
    count = 0
    while port_in_use(port_num):
        count += 1
        port_num += random.randint(1, 10)
        if count > 100:
            logger.error("Cannot find available port to bind.")
            sys.exit(-1)
    return port_num

def get_api_config(default_conf = {}) -> dict:
    """ Return user-related configurations. """
    conf = {k: v for k, v in default_conf.items()}

    cluster_ini_path = path.join(common.CLUSTER_PATH, "cluster.ini")
    cluster_ini = configparser.ConfigParser()
    if path.exists(cluster_ini_path):
        cluster_ini.read(cluster_ini_path)
    cluster_ini = dict(cluster_ini.items())
    net_ini = cluster_ini.setdefault("NETWORK", {})

    master_ini_path = path.join(common.MASTER_PATH, "server.ini")
    master_ini = configparser.ConfigParser()
    if path.exists(master_ini_path):
        master_ini.read(master_ini_path)
    master_ini = dict(master_ini.items())

    def _set_val(key, src_dict, src_key = None, transformer = None):
        """ Set value(corresponding with src_key) from src_dict to conf. """
        src_key = src_key or key # use key by default
        if src_key in src_dict:
            val = src_dict[src_key]
            conf[key] = transformer(val) if transformer else val

    _set_val("name", net_ini, "cluster_name")
    _set_val("desc", net_ini, "cluster_description")
    _set_val("max_players", cluster_ini.get("GAMEPLAY", {}))
    _set_val("password", net_ini, "cluster_password")
    _set_val("master_port", cluster_ini.get("SHARD", {}))
    _set_val("server_port", master_ini.get("NETWORK", {}), transformer=int)
    _set_val("steam_server_port", master_ini.get("STEAM", {}), transformer=int)
    _set_val("authentication_port", master_ini.get("STEAM", {}), transformer=int)

    # conf.update({
    #     "name": net_ini.get("cluster_name", conf["name"]),
    #     "desc": net_ini.get("cluster_description", conf["desc"]),
    #     "max_players": cluster_ini.get("GAMEPLAY", {}).get(
    #         "max_players", conf["max_players"]),
    #     "password": net_ini.get("cluster_password", conf["password"]),
    #     "master_port": cluster_ini.get("SHARD", {}).get("master_port", conf["master_port"]),
    #     "server_port": int(master_ini.get("NETWORK", {}).get("server_port", conf["server_port"])),
    #     "steam_server_port": int(master_ini.get("STEAM", {}).get(
    #         "master_server_port", conf["steam_server_port"])),
    #     "authentication_port": int(master_ini.get("STEAM", {}).get(
    #         "authentication_port", conf["authentication_port"])),
    #     })
    return conf


def config_cluster_ini(args):
    conf: dict = {
        "name": common.CLUSTER,
        "desc": "",
        "max_players": 64,
        "password": "4064",
        "master_port": port_lookup(10888),
        "server_port": port_lookup(11000),
        "steam_server_port": port_lookup(27016),
        "authentication_port": port_lookup(8768),
            }

    conf = get_api_config(conf)

    input_str = ""
    while True:
        logger.info("""\
Cluster Configure, use options below by default:
    name\t= {name}\t# Cluster name, show at the room search page
    desc\t= {desc}\t# Cluster description
    max_players\t= {max_players}\t# Max players to support in room
    password\t= {password}\t# Room password to authenticate

    # Port to communicate with shard instance if cave enabled, ignore if not concern
    master_port\t= {master_port}

    # Server port to interact with different dst, players can find current
    #   room in dst search page, or press `~` to enter command line and
    #   type server IP(LAN or WAN) & this port, e.g.:
    #       c_connect("192.168.2.163", {server_port})
    #       c_connect("114.66.27.85", {server_port})
    #   The second approach can reach less network delay in theoretically.
    # These three ports are used by master instance, cave's ports are increased
    #   by +1 and find available ports.
    server_port\t= {server_port}
    steam_server_port\t= {steam_server_port}
    authentication_port\t= {authentication_port}

choose one option and type (Enter to confirm):
1. [Y] to use above config
2. [n1=v1,n2=v2,...] formated string to use custom settings
3. [N] to abort\
            """.format(**conf))
        input_str = "Y" if args.yes else input("> ")
        if input_str.upper() in ["Y", "YES"]:
            logger.info("Use above config for cluster")
            break
        elif input_str.upper() in ["N", "NO"]:
            logger.info("Abort.")
            sys.exit(-1)

        values = [s.strip() for s in input_str.split(",") if s.strip()]
        values = [s.split("=") for s in values]
        for v in values:
            v = [s.strip() for s in v if s.strip()]
            if len(v) != 2:
                logger.error("Unknown input for `%s`" % v)
                continue
            if v[0] not in conf:
                logger.error("Unknown input key for `%s`" % v[0])
                continue
            ktype = type(conf[v[0]])
            try:
                conf[v[0]] = ktype(v[1])
            except Exception:
                logger.error("Unknown input value type: %s for `%s`" % (ktype.__name__, v[1]))
                continue
            conf[v[0]] = v[1]

    logger.info("Saving cluster config...")
    with open(path.join(common.CLUSTER_PATH, "cluster.ini"), "w") as f:
        f.write(CLUSTER_INI_TEMP.format(
            name=conf["name"], desc=conf["desc"],
            max_players=conf["max_players"],
            password=conf["password"],
            master_port=conf["master_port"],))

    autossh_cmd = """
autossh -NR {server_host}:{server_port}:{local_host}:{local_port} rainyun
    """
    autossh_fpath = path.join(common.CLUSTER_PATH, "proxy.sh")
    with open(autossh_fpath, "w") as f:
        f.write(autossh_cmd.format(
            server_host = "*",
            server_port = conf["server_port"],
            local_host = "127.0.0.1",
            local_port = conf["server_port"]
            ))
    bash.shell_exec("chmod +x", autossh_fpath)
    logger.info(f"Register [autossh] proxy: {autossh_fpath}")

    with open(path.join(common.MASTER_PATH, "server.ini"), "w") as f:
        f.write(CLUSTRE_SERVER_TEMP.format(
            server_port=conf["server_port"],
            is_master=True, cave_temp="",
            master_server_port=conf["steam_server_port"],
            authentication_port=conf["authentication_port"],
            ))

    with open(path.join(common.CAVES_PATH, "server.ini"), "w") as f:
        f.write(CLUSTRE_SERVER_TEMP.format(
            server_port=port_lookup(conf["server_port"] + 1),
            is_master=False, cave_temp="name = Caves",
            master_server_port=port_lookup(conf["steam_server_port"] + 1),
            authentication_port=port_lookup(conf["authentication_port"] + 1),
            ))
    logger.info("Saved cluster: %s config." % common.CLUSTER)

def config(args):
    config_token(args)
    config_cluster_ini(args)
    mods.config_mods(args)
