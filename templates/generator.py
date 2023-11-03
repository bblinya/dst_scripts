import os

PY_DIR = os.path.dirname(__file__)

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
    def __init__(
            self,
            confs_path = "%s/modoverrides.lua" % PY_DIR,
            setup_path = "%s/dedicated_server_mods_setup.lua" % PY_DIR):
        self.ident = 0

        self.mod_confs = []
        self.confs_path = confs_path

        self.mod_setup = []
        self.setup_path = setup_path

    def add_config(self, idt, **kwargs):
        self.mod_confs.append(config_modoverride(
            idt, self.ident+1, **kwargs))
        self.mod_setup.append(config_mod_setup(idt))

    def populate(self):
        conf = ",\n\n".join(self.mod_confs)
        conf = self.CONF_PAT % conf
        print("write mod config to", self.confs_path)
        with open(self.confs_path, "w") as f:
            f.write(conf)

        print("write mod setup to", self.setup_path)
        setup = "\n".join(self.mod_setup)
        with open(self.setup_path, "w") as f:
            f.write(setup)

        print("populate done!")

MYTH = "Myth"
""" Myth Words """
BBWM = "BBWM"
""" tropical experience """

if __name__ == "__main__":
    cluster_name = os.environ.get("CLUSTER_NAME", MYTH)
    assert cluster_name in [MYTH, BBWM]
    print("Generate mod config for %s" % cluster_name)

    mods = ModsConfig()
    # themes
    if cluster_name == MYTH:
        mods.add_config("1991746508", desc="Myth Words Theme: 神话书说(80M)",
                        language="CHINESE", ShowBuff=True)
        mods.add_config("1699194522", desc="Myth Words Characters: 100M")
    if cluster_name == BBWM:
        mods.add_config("1505270912", desc="Tropical Experience | The Volcano Biome",
                        set_idioma="stringsCh")
    mods.add_config("1289779251", desc="Cherry Forest")

    # map
    mods.add_config("666155465", desc="Show Me")
    mods.add_config("1207269058", desc="简易血条DST")
    mods.add_config("1301033176", desc="中文语言包")
    mods.add_config("1860955902", desc="Global Position")
    mods.add_config("458587300", desc="Fast Travel", Traval_Cost=128)
    mods.add_config("462434129", desc="Restart(重生)",
                    MOD_RESTART_CD_RESTART=0, MOD_RESTART_CD_RESURRECT=0, MOD_RESTART_CD_KILL=0)

    # person
    mods.add_config("501385076", desc="快速采集")
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
    mods.add_config("1645013096", desc="SONOKO NOGI: 乃木园子(22M)")
    mods.add_config("684098549", desc="Remilia Scarlet 【蕾米莉娅斯卡雷特】")
    # mods.add_config("1837053004", desc="晓美焰 11.042M",
    #                 language="CHI", skillkey_v2="T")

    mods.populate()

