# DST Scripts README

**Notice: Do not edit any files out of `dst_scripts`, since you use this
project to control all DST server action. All you need to change about
configuration or server action are located at this directory. Generally,
all bash script is in the dst_script root and config file is put at
`dst_scripts/templates`.**

[TOC]

## Directory View

```bash
admin@iZ2ze9s4hsntd8abwlnn8zZ:~/dst_scripts$ tree .
.
├── attach.sh
├── common.sh
├── exec.sh
├── remove_archives.sh
├── restart.sh
├── schedule.sh
├── sync_config.sh
├── templates
│   ├── modoverrides.lua
│   └── worldgenoverride.lua
├── update_dst.sh
└── update_mods.sh

1 directory, 11 files
```

## Operation

### 服务器指令操作

要进行服务器指令设置，需要手动连接服务器的screen之后在输入命令，连接命令如下：

```bash
./attach.sh
```

会默认进入screen操作界面，想要退出按快捷键`Ctrl+a` + `Ctrl+d` or just kill the ssh terminal directly。

And you will see terminal output like this:

``` bash
Caves: [07:54:35]: Registering secondary shard in EU lobby
Caves: [07:59:35]: Registering secondary shard in EU lobby
Master: [08:00:09]: [200] Account Communication Success (6)
Master: [08:00:09]: Received (KU_wGWotiLQ) from TokenPurpose
Caves: [08:00:09]: [200] Account Communication Success (6)
Caves: [08:00:09]: Received (KU_wGWotiLQ) from TokenPurpose
Caves: [08:04:35]: Registering secondary shard in EU lobby
Caves: [08:09:35]: Registering secondary shard in EU lobby
Caves: [08:14:35]: Registering secondary shard in EU lobby
```

This is a interactive console that user can input instructions like:

``` bash
Caves: [08:04:35]: Registering secondary shard in EU lobby
Caves: [08:09:35]: Registering secondary shard in EU lobby
Caves: [08:14:35]: Registering secondary shard in EU lobby
c_listallplayers()   						<- user input
Caves: [08:16:41]: RemoteCommandInput: "c_listallplayers()" 	<- output
BetaBeauty							<- output
```

Here are some useful instructions pre-defined in dst console:

``` bash
c_listallplayers()

# 强制服务器立即保存。（服务器通常在夜晚结束的时候自动保存）
c_save()

# true 会保存游戏，false 不会保存游戏。 c_shutdown() 和 c_shutdown(true) 是一样的。
c_shutdown( true / false) 

# 回档服务器一定次数。 c_rollback() 会回档一次，c_rollback(3) 会回档三次。
c_rollback(count)

# 默认情况下设置为 true （新玩家可以加入）。设置为 false 将禁止玩家进入。
TheNet:SetAllowIncomingConnections( true / false )

# 可以发送一个公告给玩家，例如即将关闭 / 重启服务器，让玩家知道即将断线。
c_announce("announcement")

# 进入特定季节, spring(春), summmer(夏), autumn(秋), winter(冬)
TheWorld:PushEvent("ms_setseason", "spring")
TheWorld:PushEvent("ms_setseason", "summer")
TheWorld:PushEvent("ms_setseason", "autumn")
TheWorld:PushEvent("ms_setseason", "winter")
```

More details about the admin instructions, please refer to [The Wiki](https://dontstarve.fandom.com/zh/wiki/%E6%8E%A7%E5%88%B6%E5%8F%B0/%E5%A4%9A%E4%BA%BA%E7%89%88%E9%A5%91%E8%8D%92%E4%B8%AD%E7%9A%84%E5%91%BD%E4%BB%A4?variant=zh-sg).

### Mod Setup

1. Edit the file: `templates/dedicated_server_mods_setup.lua`.
	Add line such as `ServerModSetup("1837053004")`
	Refer to the lua comment for more details about mod setup.
2. Edit the file: `templates/modoverrides.lua`.
	You can add simple line of 
	`["workshop-"] = { configuration_options = {}, enabled = true }`
	for default options. Remember to add the id number after
	`workshop-`. Better to obey the unify format pre-defined at
	the file such as comment with mod name.
3. Run the `./update_mods.sh` to auto download the mods for server.
	And you will set in the output:
	``` bash
[00:00:00]: loaded modindex
[00:00:00]: ModIndex: Beginning normal load sequence for dedicated server.

[00:00:02]: DownloadPublishedFile [0] 1837053004 	<- mod id number
[00:00:09]: OnDownloadPublishedFile [1] 1837053004
[00:00:09]: FinishDownloadingServerMods Complete!
	```
4. Run the `./restart.sh` to restart the DST server, which will auto-load
the mod config in the above `modoverrides.lua`.

### Server Auto Update

DST server and mods may update by official team, so BB has write some
scripts including `update_dst.sh` and `schedule.sh` to update program
in the time point: 03:00 with `crontab` everyday automatically.

If you want to change this synchronized action, try to set with `crontab`
in this machine.






















