import os
from os import path
from dataclasses import dataclass

@dataclass
class ClusterConfig:
    name: str
    token: str
    password: str

    # gameplay
    max_players: int = 16

    # network
    desc: str = "Easy & Happy to play."

    # shard
    master_port: int = 10888

    # server ini
    server_port: int = 11000
    steam_server_port: int = 27016
    authentication_port: int = 8768

    def __eq__(self, other: str):
        if isinstance(other, str):
            return self.name == other
        return self.name == other.name

TOKEN_BBWM_1 = "pds-g^KU_wGWotiLQ^oX7K/9mB9Ul+P2ynzAA+bBJBTUViYHaY0k0FIx5SVsw="
TOKEN_CROWNBIOS = "pds-g^KU_wGWotiLQ^jytcPFacI4GTd0qzCmnBTBjEQxlHIHqfqjcIgDqMQ9g="

CLUSTERS = [
    ClusterConfig("Myth", TOKEN_BBWM_1, "4064"),
    ClusterConfig("BBWM", TOKEN_BBWM_1, "4064"),
    ClusterConfig(
        "CrownBios", TOKEN_CROWNBIOS, "bios",
        desc="一群快乐的小菜狗",
        master_port=10899,
        server_port=12000,
        steam_server_port=27116,
        authentication_port=8868,),
        ]
MYTH, BBWM, CROWNBIOS = CLUSTERS

cluster = os.environ.get("CLUSTER_NAME", MYTH)
assert cluster in CLUSTERS, cluster
cluster: ClusterConfig = next((c for c in CLUSTERS if c == cluster))

cluster_path = os.environ.get("CLUSTER_PATH")
ins_path = [ path.join(cluster_path, s) for s in ["Master", "Caves"]]
master_path, cave_path = ins_path

dst_mod_path = path.join(os.environ.get("DST_HOME"), "mods")

def config_token():
    with open(path.join(cluster_path, "cluster_token.txt"), "w") as f:
        f.write(cluster.token)

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
def config_cluster_ini():
    with open(path.join(cluster_path, "cluster.ini"), "w") as f:
        f.write(CLUSTER_INI_TEMP.format(
            name=cluster.name,
            desc=cluster.desc,
            max_players=cluster.max_players,
            password=cluster.password,
            master_port=cluster.master_port,))

    with open(path.join(master_path, "server.ini"), "w") as f:
        f.write(CLUSTRE_SERVER_TEMP.format(
            server_port=cluster.server_port,
            is_master=True, cave_temp="",
            master_server_port=cluster.steam_server_port,
            authentication_port=cluster.authentication_port,
            ))

    with open(path.join(cave_path, "server.ini"), "w") as f:
        f.write(CLUSTRE_SERVER_TEMP.format(
            server_port=cluster.server_port + 1,
            is_master=False, cave_temp="name = Caves",
            master_server_port=cluster.steam_server_port + 1,
            authentication_port=cluster.authentication_port + 1,
            ))

def _format_lua_type(val):
    if isinstance(val, bool):
        return str(val).lower()
    elif isinstance(val, int):
        return str(val)
    assert isinstance(val, str)
    return "\"%s\"" % val

def config_modoverride(idt, ident, desc=None, **kwargs):
    idt_str = "  " * (ident + 1)
    conf = ["%s%s = %s" % (idt_str, k, _format_lua_type(v)) for k, v in kwargs.items()]
    conf = ",\n".join(conf)
    conf = conf and ("\n" + conf + "\n")
    conf = "[\"workshop-%s\"] = { configuration_options = {%s}, enabled = true }" % (idt, conf)
    if desc:
        conf = "-- %s\n%s" % (desc, conf)
    return conf

def config_mod_setup(idt):
    return "ServerModSetup(\"%s\")" % idt

class ModsConfig:
    CONF_PAT = """return {\n%s\n}"""
    def __init__(self):
        self.ident = 0

        self.mod_confs = []
        # self.confs_path = confs_path
        self.confs_path = [path.join(s, "modoverrides.lua") \
                for s in ins_path]

        self.mod_setup = []
        self.setup_path = path.join(
                dst_mod_path, "dedicated_server_mods_setup.lua")
        # self.setup_path = setup_path

    def add_config(self, idt, **kwargs):
        print("Enable mod:", idt)
        self.mod_confs.append(config_modoverride(
            idt, self.ident+1, **kwargs))
        self.mod_setup.append(config_mod_setup(idt))

    def populate(self):
        conf = ",\n\n".join(self.mod_confs)
        conf = self.CONF_PAT % conf
        print("write mod config to", self.confs_path)
        for cp in self.confs_path:
            with open(cp, "w") as f:
                f.write(conf)

        print("write mod setup to", self.setup_path)
        setup = "\n".join(self.mod_setup)
        with open(self.setup_path, "w") as f:
            f.write(setup)

        print("populate done!")

if __name__ == "__main__":
    print("Generate mod config for %s" % cluster)

    config_token()
    config_cluster_ini()

    mods = ModsConfig()
    # themes
    if cluster == MYTH:
        mods.add_config("1991746508", desc="Myth Words Theme: 神话书说(80M)",
                        language="CHINESE", ShowBuff=True)
        mods.add_config("1699194522", desc="Myth Words Characters: 100M")
    if cluster == BBWM:
        mods.add_config("1505270912", desc="Tropical Experience | The Volcano Biome",
                        set_idioma="stringsCh")
    if cluster in [ MYTH, BBWM, ]:
        mods.add_config("1289779251", desc="Cherry Forest")

    # map
    mods.add_config("666155465", desc="Show Me")
    mods.add_config("1207269058", desc="简易血条DST")
    mods.add_config("1301033176", desc="中文语言包",
                    LANG="simplified")
    mods.add_config("1860955902", desc="Global Position")
    mods.add_config("458587300", desc="Fast Travel", Traval_Cost=128)
    mods.add_config("462434129", desc="Restart(重生)",
                    MOD_RESTART_CD_RESTART=0, MOD_RESTART_CD_RESURRECT=0, MOD_RESTART_CD_KILL=0)

    # person
    mods.add_config("501385076", desc="快速采集")
    if cluster in [ MYTH, BBWM, ]:
        mods.add_config("2823458540", desc="富贵险中求")
    mods.add_config("374550642", desc="Increased Stack Size")
    mods.add_config("375850593", desc="Extra Equip Slots: may have problem through caves")
    # mods.add_config("2950956942", desc="更多动作")

    # items
    mods.add_config("356930882", desc="Infinite Tent Uses")
    mods.add_config("1898181913", desc="冰箱  no rod")
    mods.add_config("466732225", desc="No Thermal Stone Durability")
    mods.add_config("380423963", desc="Mineable Gems")
    mods.add_config("1595631294", desc="智能小木牌",
                    Icebox=True, DragonflyChest=True)
    mods.add_config("2528541304", desc="Not Enough Turfs")
    mods.add_config("1607644339", desc="More cooking/整组烹饪、整组喂鸟")

    # characters
    if cluster in [ MYTH, BBWM, ]:
        mods.add_config("1645013096", desc="SONOKO NOGI: 乃木园子(22M)")
        mods.add_config("684098549", desc="Remilia Scarlet 【蕾米莉娅斯卡雷特】")
    # mods.add_config("1837053004", desc="晓美焰 11.042M",
    #                 language="CHI", skillkey_v2="T")

    mods.populate()

