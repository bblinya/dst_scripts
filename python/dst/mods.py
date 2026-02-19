import re
import sys
import json
import logging
import traceback
from os import path
from dataclasses import dataclass

from . import common

from bbcode.common import bash

MODS: dict = {}
logger = logging.getLogger("mods")

def add_mod(modId, **kwargs):
    MODS.setdefault(modId, {})
    MODS[modId].update(kwargs)
    return MODS

def count_chi_char(text):
    count = 0
    for s in text:
        if (s >='\u4e00' and s <= '\u9fa5') or \
            s in ['；','：','，','（','）','！','？','——','……','、','》','《', '【', '】']:
            count += 1
    return count

def mod_string(modId):
    mod: dict = MODS[modId]
    mod_str = "{:>10}, desc={:{}}".format(
            modId, mod["desc"],
            max(40 - count_chi_char(mod["desc"]), 1))

    is_deprecated = mod.get("Deprecated", False)
    install_by_default = mod.get("InstallByDefault", False)

    mod_str = f"{'+' if install_by_default else ' '} {mod_str}"
    mod_str = f"{'!' if is_deprecated else ' '}{mod_str}"

    conf = ["=".join([k, str(v)]) for k, v in mod.items() \
            if k not in ["desc", "Deprecated", "InstallByDefault"]]
    mod_str += " | " + ", ".join(conf)
    return mod_str

def summary(installed_mods = []):
    logger.info(f"+: InstallByDefault; !: Deprecated")
    if len(installed_mods) > 0:
        logger.info(f"Installed Mods ({len(installed_mods)}):")
        for modId in sorted(installed_mods):
            logger.info(mod_string(modId))

    print()
    logger.info("Available Mods:")
    for modId in sorted(MODS.keys()):
        if modId not in installed_mods:
            logger.info(mod_string(modId))

add_mod("1991746508", desc="Myth Words Theme: 神话书说(80M)",
        language="CHINESE", ShowBuff=True)
add_mod("1699194522", desc="Myth Words Characters: 100M")
add_mod("1505270912", desc="Tropical Experience | The Volcano Biome",
        set_idioma="stringsCh")
add_mod("1289779251", desc="Cherry Forest")

add_mod("3361615927", desc="田园物语-花卉篇",
        InstallByDefault=True,
        )

# server
# !!! dst client should download this mod manually.
# Don't know why.
add_mod("3050607025", desc="防卡好多招",
        InstallByDefault=True,
        STACK_SIZE=999, TREES_NO_STUMP=False,
        TWIGGY=True, CLEAN_DAYS=30,
        )
add_mod("666155465", desc="Show Me",
        InstallByDefault=True
        )
add_mod("1207269058", desc="简易血条DST",
        InstallByDefault=True
        )
add_mod("1301033176", desc="中文语言包",
        InstallByDefault=True,
        LANG="simplified")
add_mod("1860955902", desc="Global Position", Deprecated=True,)
add_mod("378160973", desc="Global Position",
        InstallByDefault=True
        )
add_mod("458587300", desc="Fast Travel", Deprecated=True, Traval_Cost=128)
add_mod("1530801499", desc="Fast Travel",
        InstallByDefault=True
        )


add_mod("462434129", desc="Restart(重生)",
        Deprecated=True,
        InstallByDefault=True,
        MOD_RESTART_CD_RESTART=0, MOD_RESTART_CD_RESURRECT=0, MOD_RESTART_CD_KILL=0)

# person action
add_mod("501385076", desc="快速采集",
        Deprecated=True,
        InstallByDefault=True
        )
add_mod("2823458540", desc="富贵险中求",
        InstallByDefault=True
        )
add_mod("374550642", desc="Increased Stack Size")
add_mod("375850593", desc="Extra Equip Slots: may cave problem",
        Deprecated=True,
        InstallByDefault=True,)
add_mod("2798599672", desc="4/5/6格装备栏（适配mod版）",
        # InstallByDefault=True
        )
add_mod("2950956942", desc="更多动作")

# items
add_mod("356930882", desc="Infinite Tent Uses",
        InstallByDefault=True
        )
add_mod("1898181913", desc="冰箱 no rod",
        Deprecated=True,
        InstallByDefault=True,)
# add_mod("462372013", desc="Always Fresh",
#         InstallByDefault=True
#         )

add_mod("466732225", desc="No Thermal Stone Durability",
        Deprecated=True,
        InstallByDefault=True,)
add_mod("380423963", desc="Mineable Gems",
        Deprecated=True,
        InstallByDefault=True,)
add_mod("1595631294", desc="智能小木牌",
        InstallByDefault=True,
        Icebox=True, DragonflyChest=True)
add_mod("2528541304", desc="Not Enough Turfs",
        InstallByDefault=True
        )
add_mod("1607644339", desc="More cooking/整组烹饪、整组喂鸟",
        InstallByDefault=True
        )

# characters
add_mod("1645013096", desc="SONOKO NOGI: 乃木园子(22M)")
add_mod("684098549", desc="Remilia Scarlet 【蕾米莉娅斯卡雷特】")

# MOD_FILE = path.join(common.TEMP_ROOT, "mods_file.json")
# def load_mods():
#     if not path.exists(MOD_FILE):
#         return

#     with open(MOD_FILE, "r") as f:
#         loaded_mods = json.load(f)

#     for k, v in loaded_mods.items():
#         MODS.setdefault(k, {})
#         MODS[k].update(v)

# load_mods()

# def save_mods():
#     mod_str = {k: json.dumps(v, ensure_ascii=False) \
#             for k, v in MODS.items()}
#     mod_str = ["\n  \"%s\": %s" % (k, v) for k, v in mod_str.items()]
#     mod_str = ",".join(mod_str)
#     mod_str = "{%s\n}" % mod_str
#     with open(MOD_FILE, "w") as f:
#         f.write(mod_str)

def _load_lua_type(val: str):
    val = val.strip()
    if val in ["true", "false"]:
        return val == "true"
    elif val == "":
        return ""
    try:
        return eval(val)
    except:
        return val

def load_lua_mods(fpath):
    with open(fpath, "r") as f:
        conf = f.read()

    conf = conf.replace(" ", "").replace("\n", "")
    pat = "\[\"workshop-(\d+)\"\]={configuration_options={([^}]*)},enabled=true}"
    lua_mods = []
    for mat in re.findall(pat, conf):
        modId = mat[0]
        conf = [s.split("=") for s in mat[1].split(",") if s]
        conf = {k: _load_lua_type(v) for (k, v) in conf}
        #  print(modId, conf)
        MODS.setdefault(modId, {})
        MODS[modId].update(conf)
        lua_mods.append(modId)
    return lua_mods

def update_server_mods_setup():
    """ This function need be called before update mods, and
            will be overrided by steam update command.
    """
    mod_file = path.join(common.CLUSTER_PATH, "Master/modoverrides.lua")
    if not path.exists(mod_file):
        return

    installed_mods = load_lua_mods(mod_file)
    setup = ["ServerModSetup(\"%s\")" % s for s in installed_mods]

    setup_path = path.join(
            common.DST_HOME,
            "mods/dedicated_server_mods_setup.lua")
    logger.info("Updating mod setup file: %s" % setup_path)
    with open(setup_path, "w") as f:
        f.write("\n".join(setup))

def _format_lua_type(val):
    if isinstance(val, bool):
        return str(val).lower()
    elif isinstance(val, int):
        return str(val)
    assert isinstance(val, str)
    return "\"%s\"" % val

def save_lua_mods(confs_path, installed_mods):
    mod_confs = []
    for modId in installed_mods:
        mod = {k:v for k, v in MODS[modId].items()}
        desc = mod.pop("desc", None)
        conf = ["  %s = %s" % (k, _format_lua_type(v)) for k, v in mod.items()]
        conf = ",\n".join(conf)
        conf = conf and ("\n" + conf + "\n")
        conf = "[\"workshop-%s\"] = { configuration_options = {%s}, enabled = true }" % (modId, conf)
        if desc:
            conf = "-- %s\n%s" % (desc, conf)
        mod_confs.append(conf)

    conf = ",\n\n".join(mod_confs)
    conf = "return {\n%s\n}" % conf

    logger.info("Saving mod config to %s" % confs_path)
    for cp in confs_path:
        with open(cp, "w") as f:
            f.write(conf)

    logger.info("Cluster Mod populate done!")

def parse_mod_configuration(mod_path):
    with open(mod_path, "r") as f:
        data = [l.strip() for l in f.readlines()]
        data = [l for l in data if not l.startswith("--")]
        data = [l.split("--")[0] for l in data]
        data = "".join(data)

    pat = "({[^{]*?name.*?label.*?default.*?})"
    mats = re.findall(pat, data)
    options = {}
    for mat in mats:
        #  print(mat)
        data = re.findall("([a-zA-Z]+) *= *(\".*?\")?([^\" {]+?)?({.*})?,", mat)
        opt = {}
        for d in data:
            #  print(d)
            opt_data = []
            for v in re.findall("{.*?}", d[3][1:-2]):
                # print(v)
                opt_one_data = {}
                for k in re.findall("([a-za-z]+) *= *(\".*?\")?([^\" {]+?)?[, }]", v):
                    # print(k)
                    opt_one_data[k[0]] = _load_lua_type(k[1]) or _load_lua_type(k[2])
                opt_data.append(opt_one_data)

            #  print(_load_lua_type(d[1]), _load_lua_type(d[2]))
            opt[d[0]] = _load_lua_type(d[1]) or opt_data or _load_lua_type(d[2])
        #  print(opt)

        option = {}
        def _set_opt(key, miss_error = False):
            if key in opt:
                option[key] = opt[key]
            elif miss_error:
                logger.warning("option: `%s` miss key: %s" % (opt, key))
                return False
            return True

        is_ok = _set_opt("name", miss_error=True)
        is_ok = is_ok and _set_opt("label")
        is_ok = is_ok and _set_opt("hover")
        is_ok = is_ok and _set_opt("options")
        is_ok = is_ok and _set_opt("default")
        if is_ok:
            options[option["name"]] = option
        # if option["name"] == "STACK_SIZE":
        #     return {}
        # duplicate with miss_error
        # else:
        #     logger.warning("Mod: %s configuration parse failed" % mat)
    return options

_MODS_INFO = {}

def is_ready():
    """ Check all mods are downloaded local. """
    mod_file = path.join(common.CLUSTER_PATH, "Master/modoverrides.lua")
    if not path.exists(mod_file):
        return True

    installed_mods = load_lua_mods(mod_file)
    for m in installed_mods:
        locs = bash.shell_output(
                "find", common.DST_HOME,
                "-name '*%s'" % m)
        locs = [s.strip() for s in locs.split("\n") if s.strip()]
        if len(locs) == 0:
            logger.warning("Mod: %s not downloaded" % m)
            return False

    return True

def print_mod_info(modId, opt_keys):
    if modId not in _MODS_INFO:
        mod_info = { "locs": [], "options": {} }
        locs = bash.shell_output(
                "find", common.DST_HOME,
                "-name '*%s'" % modId)
        locs = [s.strip() for s in locs.split("\n") if s.strip()]

        options = {}
        for l in locs:
            if path.exists(path.join(l, "modinfo.lua")):
                lua_loc = path.join(l, "modinfo.lua")
                mod_info["locs"].append(lua_loc)
                try:
                    mod_info["options"].update(parse_mod_configuration(lua_loc))
                except Exception as e:
                    traceback.print_exc()
                    logger.error("Mod: %s configuration parse failed" % modId)
                    continue
        _MODS_INFO[modId] = mod_info

    mod_info = _MODS_INFO[modId]
    logger.info("Mod Info Location: %s" % mod_info["locs"])

    if "A" in opt_keys:
        opt_keys = list(mod_info["options"].keys())

    for name, opt in mod_info["options"].items():
        # print(opt)
        logger.info("{:>40} = {:10} | {}".format(
            name, str(opt.get("default", "Unknown")), opt.get("label", "")))
        if len(opt_keys) == 0:
            # print(opt)
            hover_str = opt.get("hover", "")
            opt_data = opt.get("options", {})
            logger.info("{:>{}} ^ {}".format(
                opt.get("hover", ""),
                max(53 - count_chi_char(hover_str), 1),
                [s["data"] for s in opt_data] if isinstance(opt_data, list) else ""))
        if name in opt_keys:
            logger.info(">>> {}".format(opt.get("hover", "")))
            if "options" in opt:
                logger.info("Optional Data:")
            for d in opt.get("options", []):
                desc = d.get("description", "")
                logger.info("{:>15} ({:{}}) | {}".format(
                    d.get("data", None), desc,
                    max(20 - count_chi_char(desc), 1), d.get("hover", "")))

def config_mods(args):
    installed_mods = []

    mod_file = path.join(common.CLUSTER_PATH, "Master/modoverrides.lua")

    preset = getattr(args, "preset", 1)

    if preset == 0: # no use mods
        logger.info("No use mods.")
        pass
    elif preset == 1 and path.exists(mod_file):
        logger.info("Load existed mods.")
        installed_mods = load_lua_mods(mod_file)
    elif preset in [1, 2]:
        logger.info("Use pre-defined mods.")
        installed_mods = [modId for modId, conf in MODS.items() \
                if conf.get("InstallByDefault", False)]
    else:
        logger.error(f"Unknown preset: {preset}, candidates: [0, 1, 2]")
        sys.exit()

    summary(installed_mods)

    input_str = ""
    while True:
        print()
        logger.info("""\
Supported Commands:
- [p] print all mods.
- [y] use current mods in cluster.
- [n] abort all operations.
- [/modId,conf1=,conf2=,] print mod and conf details, use A to print all.
- [+modId] add embeded modId.
- [+modId,desc=v1,conf1=v2,...] format string to add custom mod.
- [-modId] format string to remove mod.\
        """)
        input_str = "Y" if args.yes else input("> ")
        if input_str.upper() in ["Y", "YES"]:
            logger.info("Use above mods for cluster")
            break
        elif input_str.upper() in ["N", "NO"]:
            logger.info("Abort.")
            sys.exit(0)
        elif len(input_str) == 0:
            continue
        elif input_str.upper() in ["P", "PRINT"]:
            summary(installed_mods)
            continue

        act, input_str = input_str[0], input_str[1:]
        if act not in ["+", "-", "/"]:
            logger.error("Invalid mod action, add +/- before modId")
            continue

        values = [s.strip() for s in input_str.split(",") if s.strip()]
        values = [s.split("=") for s in values]
        mod_config = {}
        for v in values:
            if len(v) > 2:
                logger.error("Unknown input for `%s`" % v)
                break
            elif len(v) == 1:
                s = v[0].strip()
                if "modId" in mod_config:
                    logger.error("Duplicated modId")
                    break
                if not s.isdigit():
                    logger.error("Invalid modId format, not digit")
                    break
                mod_config["modId"] = s
            elif len(v) == 2:
                k, v = v[0].strip(), v[1].strip()
                if k in mod_config:
                    logger.error("Duplicated mod config key: %s" % v[0])
                    break
                mod_config[k] = v and eval(v)

        if "modId" not in mod_config:
            logger.error("Miss mod id")
            continue
        if not mod_config["modId"].isdigit():
            logger.error("Invalid modId format, not digit: %s" % mod_config["modId"])
            continue

        if act == "+":
            installed_mods.append(mod_config["modId"])
            add_mod(**mod_config)
        elif act == "/":
            modId = mod_config.pop("modId")
            print_mod_info(modId, mod_config)
        else: # act == "-"
            installed_mods.remove(mod_config["modId"])

    # save_mods()
    save_lua_mods(
            [ path.join(common.MASTER_PATH, "modoverrides.lua"),
              path.join(common.CAVES_PATH, "modoverrides.lua")],
            installed_mods)

