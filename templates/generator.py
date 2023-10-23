import os

PY_DIR = os.path.dirname(__file__)

def config_modoverride(idt, ident, desc=None, **kwargs):
    idt_str = "  " * (ident + 1)
    conf = ["%s%s = %s" % (idt_str, k, v) for k, v in kwargs.items()]
    conf = ",\n".join(conf)
    conf = conf and ("\n" + conf + "\n")
    conf = "[\"workshop-%s\"] = { configuration_options = { %s }, enabled = true }" % (idt, conf)
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


if __name__ == "__main__":
    mods = ModsConfig()

    # themes
    mods.add_config("1991746508", desc="Myth Words Theme: 神话书说(80M)", ShowBuff="true")
    mods.add_config("1699194522", desc="Myth Words Characters: 100M")

    # map
    mods.add_config("666155465", desc="Show Me")
    mods.add_config("1860955902", desc="Global Position")
    mods.add_config("458587300", desc="Fast Travel", Traval_Cost=128)
    mods.add_config("462434129", desc="Restart(重生)",
                    MOD_RESTART_CD_RESTART=0, MOD_RESTART_CD_RESURRECT=0, MOD_RESTART_CD_KILL=0)

    # person
    mods.add_config("501385076", desc="快速采集")
    mods.add_config("2823458540", desc="富贵险中求")
    mods.add_config("374550642", desc="Increased Stack Size")
    mods.add_config("375850593", desc="Extra Equip Slots: may have problem through caves")

    # items
    mods.add_config("356930882", desc="Infinite Tent Uses")
    mods.add_config("1898181913", desc="冰箱  no rod")
    mods.add_config("466732225", desc="No Thermal Stone Durability")
    mods.add_config("380423963", desc="Mineable Gems")
    mods.add_config("1595631294", desc="智能小木牌")

    # characters
    mods.add_config("1645013096", desc="SONOKO NOGI: 乃木园子(22M)")
    mods.add_config("1837053004", desc="晓美焰 11.042M")

    mods.populate()

