rawset(_G, "DiscordBot", {})
DiscordBot.Data = {}
DiscordBot.Data.msgsrb2 = ''
DiscordBot.Data.pcmtsrb2 = ''
DiscordBot.Data.stats = ''
DiscordBot.Data.pcmp = ''
DiscordBot.Data.log = ''
DiscordBot.Data.console = ''
DiscordBot.Data.paused = false
DiscordBot.Data.maptitle = ''
DiscordBot.Data.nextlevel = ''
DiscordBot.Data.iconemeralds = ''
DiscordBot.Data.gametype = nil
DiscordBot.Data.countemeralds = 0
DiscordBot.Data.servertime = 0

DiscordBot.Commands = {}
DiscordBot.Commands.cv_joinquit = CV_RegisterVar({name = "dbot_joinquit", defaultvalue = "On", flags = CV_NETVAR, PossibleValue = CV_OnOff})
DiscordBot.Commands.cv_autopause = CV_RegisterVar({name = "dbot_autopause", defaultvalue = "On", flags = CV_NETVAR, PossibleValue = CV_OnOff})
DiscordBot.Commands.cv_nospamchat = CV_RegisterVar({name = "dbot_nospamchat", defaultvalue = "Off", flags = CV_NETVAR, PossibleValue = CV_OnOff})
DiscordBot.Commands.cv_messagedelay = CV_RegisterVar({name = "dbot_messagedelay", defaultvalue = "On", flags = CV_NETVAR, PossibleValue = CV_OnOff})

DiscordBot.Messages = {}

DiscordBot.Functions = {}
DiscordBot.Functions.spamchatbug = function(player, msg, joinquit) 
	local checked = false
	if DiscordBot.Commands.cv_nospamchat.value == 0 and not joinquit
		DiscordBot.Data.msgsrb2 = DiscordBot.Data.msgsrb2..msg
		return true
	end
	if player != server
		if not DiscordBot.Messages[player.name] then DiscordBot.Messages[player.name] = DiscordBot.Data.servertime checked = true end
		//if not DiscordBot.Messages[player.name][msg] then DiscordBot.Messages[player.name][msg] = DiscordBot.Data.servertime checked = true end
		if checked == false
			//if DiscordBot.Data.servertime - DiscordBot.Messages[player.name][msg] < 5*TICRATE then return false end
			if DiscordBot.Data.servertime - DiscordBot.Messages[player.name] < 35 then DiscordBot.Messages[player.name] = DiscordBot.Data.servertime return false end
		end
		DiscordBot.Messages[player.name] = DiscordBot.Data.servertime
	end
	DiscordBot.Data.msgsrb2 = DiscordBot.Data.msgsrb2..msg
	if DiscordBot.Commands.cv_messagedelay == 0
		COM_BufInsertText(server, "server_log msg")
		COM_BufInsertText(server, "server_log discord")
		COM_BufInsertText(server, "server_log console")
		COM_BufInsertText(server, "server_log logcom")
	end
	return true
end

DiscordBot.Functions.playerontheserver = function()
	local count = 0
	for player in players.iterate do
		if player
			count = $ + 1
		end
	end
	return count
end

DiscordBot.Functions.statsofserver = function()
	local playerstats = ''
	for player in players.iterate do
		if player
			local pname = string.gsub(player.name, "`", "")
			local ping = 0
			local statms = ''
			local iconskin = ':unknown:'
			local pffinished = ':black_large_square:'
			local admin = ':black_large_square:'
			if player.cmd.latency then ping = player.cmd.latency * 13 end
			if (ping < 32) then statms = ':ping_blue:'
			elseif (ping < 64) then statms = ':ping_green:'
			elseif (ping < 128) then statms = ':ping_yellow:'
			elseif (ping < 256) then statms = ':ping_red:' end
			if player.mo and player.spectator != true
				iconskin = ":"..player.mo.skin..":"
			end
			if player.spectator == true
				iconskin = ':spectator:'
			elseif player.playerstate == PST_DEAD
				iconskin = ':dead:'
			end
			if player.mo and (player.pflags & PF_FINISHED) then pffinished = ":completed:" end
			if IsPlayerAdmin(player) then admin = ":remote_admin:" end
			if player.playtime == nil then player.playtime = 0 end
			local seconds = G_TicsToSeconds(player.playtime)
			if string.len(seconds) == 1 then seconds = "0"..tostring(seconds) end
			local pptime = G_TicsToMinutes(player.playtime, true)..":"..seconds
			playerstats = $ + statms..iconskin..pffinished..admin.."["..#player.."] `"..pname.."`: Score - "..player.score.."; Time - "..pptime.."\n"
		end
	end
	if playerstats == ''
		playerstats = "There's no one here."
	end
	return playerstats
end

COM_AddCommand("server_log", function(player, arg, text)
	if player != server then return end
	if arg == "msg"
		if DiscordBot.Data.msgsrb2
			local logmsg = io.openlocal("client/DiscordBot/Messages.txt", "a+")
			logmsg:write(DiscordBot.Data.msgsrb2)
			logmsg:close()
		end
	elseif arg == "logcom"
		if DiscordBot.Data.log
			local logcom = io.openlocal("client/DiscordBot/logcom.txt", "a+")
			logcom:write(DiscordBot.Data.log)
			logcom:close()
		end
	elseif arg == "pause"
		if DiscordBot.Data.pcmtsrb2
			local logmsg = io.openlocal("client/DiscordBot/Players.txt", "w")
			logmsg:write("Game is paused, no players")
			logmsg:close()
		end
	elseif arg == "players"
		if DiscordBot.Data.pcmtsrb2
			local logmsg = io.openlocal("client/DiscordBot/Players.txt", "w")
			logmsg:write(DiscordBot.Data.pcmtsrb2)
			logmsg:close()
		end
		if DiscordBot.Data.stats
			-- Server name
			local cv_servername = CV_FindVar("servername")
			local playerskins = ''
			-- skins
			for i = 0, #skins-1 do
				playerskins = playerskins..":"..skins[i].name..": "
			end
			-- Leveltime
			local lseconds = G_TicsToSeconds(leveltime)
			if string.len(lseconds) == 1 then lseconds = "0"..tostring(lseconds) end
			local ltime = G_TicsToMinutes(leveltime, true)..":"..lseconds
			-- Servertime
			local sseconds = G_TicsToSeconds(DiscordBot.Data.servertime)
			if string.len(sseconds) == 1 then sseconds = "0"..tostring(sseconds) end
			local stime = G_TicsToMinutes(DiscordBot.Data.servertime, true)..":"..sseconds
			if DiscordBot.Data.paused == true
				DiscordBot.Data.stats = "There's no one here."
			end
			local logmsg = io.openlocal("client/DiscordBot/Stats.txt", "w")
			logmsg:write(cv_servername.string.."\n"..DiscordBot.Data.maptitle.." ("..gamemap..")\n"..gamemap.."\n"..DiscordBot.Data.nextlevel.."\n"..DiscordBot.Data.iconemeralds.."\n"..playerskins.."\n"..ltime.."\n"..stime.."\n"..DiscordBot.Data.pcmp.."\n"..DiscordBot.Data.stats)
			logmsg:close()
		end
	elseif arg == "console"
		if DiscordBot.Data.console
			local d_console = io.openlocal("client/DiscordBot/console.txt", "r")
			if d_console
				local clear = false
				while true do
					local line = ''
					line = d_console:read("*l") or $
					if line == "" then break end
					line = string.sub(line,1 , 220)
					if string.find(string.sub(string.lower(line),1,5), string.lower("quit")) == nil and string.find(string.sub(string.lower(line),1,9), string.lower("exitgame")) == nil
						COM_BufInsertText(server, line)
					end
					clear = true
				end
				d_console:close()
				if clear == true
					local d_console = io.openlocal("client/DiscordBot/console.txt", "w")
					d_console:write("")
					d_console:close()
				end
			end
		end
	elseif arg == "discord"
		local d_msg = io.openlocal("client/DiscordBot/discordmessage.txt", "r")
		if d_msg
			local d_msgread = nil
			local partmsg = ''
			d_msgread = d_msg:read("*a") or $
			d_msg:close()
			if string.len(d_msgread) > 220
				partmsg = string.sub(d_msgread,221 , 440)
				d_msgread = string.sub(d_msgread,1 , 220)
			end
			if d_msgread != ""
				COM_BufInsertText(server, "discord_message "..d_msgread)
				local d_msg = io.openlocal("client/DiscordBot/discordmessage.txt", "w")
				if partmsg == ''
					d_msg:write("")
				else
					d_msg:write("\""..partmsg.."\"")
				end
				d_msg:close()
			end
		end
	end
end, COM_LOCAL)

COM_AddCommand("discord_message", function(player, ...)
	if player != server then return end
	if not ... then return end
	for _,i in ipairs({...}) do
		chatprint("\x89".."[Discord]".."\x80"..i, true)
	end
end)

local function bot_function()
	DiscordBot.Data.servertime = DiscordBot.Data.servertime + 1
	if (leveltime % 70) == 35
		DiscordBot.Data.stats = DiscordBot.Functions.statsofserver()
		local cv_maxplayer = CV_FindVar("maxplayers")
		local playercount = 0
		DiscordBot.Data.countemeralds = 0
		DiscordBot.Data.iconemeralds = ''
		playercount = DiscordBot.Functions.playerontheserver()
		if not playercount
			playercount = 0
		end
		if DiscordBot.Data.gametype != gametype
			COM_BufInsertText(server, "gametype")
			DiscordBot.Data.gametype = gametype
		end
		if not G_IsSpecialStage(gamemap)
			if mapheaderinfo[gamemap].nextlevel != nil
				if mapheaderinfo[gamemap].nextlevel >= 1100
					DiscordBot.Data.nextlevel = "Ending"
				else
					local nextlevelint = mapheaderinfo[gamemap].nextlevel
					local nextlevel = mapheaderinfo[mapheaderinfo[gamemap].nextlevel]
					if nextlevel != nil
						if nextlevel.actnum == 0
							DiscordBot.Data.nextlevel = (nextlevel.lvlttl.." ("..nextlevelint..")")
						else
							DiscordBot.Data.nextlevel = (nextlevel.lvlttl.." Act "..nextlevel.actnum.." ("..nextlevelint..")")
						end
					else
						DiscordBot.Data.nextlevel =  "None"
					end
				end
			end
			if gametype != GT_COOP
				local cv_advancemap = CV_FindVar("advancemap") 
				if cv_advancemap.value == 0
					if mapheaderinfo[gamemap].actnum == 0
						DiscordBot.Data.nextlevel = (mapheaderinfo[gamemap].lvlttl.." ("..gamemap..")")
					else
						DiscordBot.Data.nextlevel = (mapheaderinfo[gamemap].lvlttl.." Act "..mapheaderinfo[gamemap].actnum.." ("..gamemap..")")
					end
				elseif cv_advancemap.value == 2
					DiscordBot.Data.nextlevel = "Random"
				end
			end
		end
		if mapheaderinfo[gamemap].actnum == 0
			DiscordBot.Data.maptitle = (mapheaderinfo[gamemap].lvlttl)
		else
			DiscordBot.Data.maptitle = (mapheaderinfo[gamemap].lvlttl.." Act "..mapheaderinfo[gamemap].actnum)
		end
		if emeralds & EMERALD1
			DiscordBot.Data.countemeralds = $ + 1
			DiscordBot.Data.iconemeralds = DiscordBot.Data.iconemeralds..":emerald1:"
		end
		if emeralds & EMERALD2
			DiscordBot.Data.countemeralds = $ + 1
			DiscordBot.Data.iconemeralds = DiscordBot.Data.iconemeralds..":emerald2:"
		end
		if emeralds & EMERALD3
			DiscordBot.Data.countemeralds = $ + 1
			DiscordBot.Data.iconemeralds = DiscordBot.Data.iconemeralds..":emerald3:"
		end
		if emeralds & EMERALD4
			DiscordBot.Data.countemeralds = $ + 1
			DiscordBot.Data.iconemeralds = DiscordBot.Data.iconemeralds..":emerald4:"
		end
		if emeralds & EMERALD5
			DiscordBot.Data.countemeralds = $ + 1
			DiscordBot.Data.iconemeralds = DiscordBot.Data.iconemeralds..":emerald5:"
		end
		if emeralds & EMERALD6
			DiscordBot.Data.countemeralds = $ + 1
			DiscordBot.Data.iconemeralds = DiscordBot.Data.iconemeralds..":emerald6:"
		end
		if emeralds & EMERALD7
			DiscordBot.Data.countemeralds = $ + 1
			DiscordBot.Data.iconemeralds = DiscordBot.Data.iconemeralds..":emerald7:"
		end
		if emeralds == 0
			DiscordBot.Data.iconemeralds = "No emeralds"
		end
		if playercount
			DiscordBot.Data.pcmp = (playercount.."/"..cv_maxplayer.value)
			DiscordBot.Data.pcmtsrb2 = ("Players : "..playercount.."/"..cv_maxplayer.value)
		else
			DiscordBot.Data.pcmp = ("0/"..cv_maxplayer.value)
			DiscordBot.Data.pcmtsrb2 = ("Players : 0/"..cv_maxplayer.value)
		end
		COM_BufInsertText(server, "server_log discord")
		COM_BufInsertText(server, "server_log console")
		if DiscordBot.Data.msgsrb2 != ''
			COM_BufInsertText(server, "server_log msg")
			DiscordBot.Data.msgsrb2 = ''
		end
		if DiscordBot.Data.log != ''
			COM_BufInsertText(server, "server_log logcom")
			DiscordBot.Data.log = ''
		end
		COM_BufInsertText(server, "server_log players")
		if DiscordBot.Commands.cv_autopause.value == 1
			local count = 0
			count = DiscordBot.Functions.playerontheserver()
			if count == 0
				if paused == false
					DiscordBot.Data.paused = true
					COM_BufInsertText(server, "server_log players")
					COM_BufInsertText(server, "server_log pause")
					COM_BufInsertText(server, "pause")
				end
			end
		end
	end
end

addHook("ThinkFrame", bot_function)

addHook("PlayerMsg", function(player, type, target, msg)
	if not player then return end
	if type == 0
		local text = nil
		local message = msg
		local sendit = false
		/*
		message = string.gsub(message, "@owners", "<@&1007014838326796298>")
		message = string.gsub(message, "@moderators", "<@&1007015806716096645>")
		message = string.gsub(message, "@Owners", "<@&1007014838326796298>")
		message = string.gsub(message, "@Moderators", "<@&1007015806716096645>")
		*/
		if server == player
			if isdedicatedserver == true
				text = "["..#player.."]".."**<~Server>**".." "..message.."\n"
				DiscordBot.Functions.spamchatbug(player, text)
				chatprint("<\x82~\x80Server>".." "..message)
				return true
			end
		end
		text = "["..#player.."]".."**<"..player.name..">**".." "..message.."\n"
		if IsPlayerAdmin(player) then text = "["..#player.."]".."**<@"..player.name..">**".." "..message.."\n" end
		if text
			sendit = DiscordBot.Functions.spamchatbug(player, text)
			if sendit == true
				return false
			end
			if sendit == false
				//chatprintf(player, "You're repeating yourself, please wait "..((5*TICRATE - (DiscordBot.Data.servertime - DiscordBot.Messages[player.name][text]))/TICRATE).." sec. or send a different message.")
				chatprintf(player, "Wait a second before sending a message and chat again.")
				return true
			end
		end
	end
	if type == 3
		local text = nil
		text = "CSAY: "..msg.."\n"
		DiscordBot.Data.msgsrb2 = DiscordBot.Data.msgsrb2..text
	end
end)

addHook("PlayerThink", function(player)
	if not player.playtime then player.playtime = 0 end
	if player.playtime != nil then player.playtime = $ + 1 end
	if not player.oldname then player.oldname = player.name end
	if player.name != player.oldname
	string.gsub(player.name, "`", "")
		local text = "["..#player.."]"..":pencil2:**"..string.gsub(player.oldname, "*", "").."** renamed to **"..string.gsub(player.name, "*", "").."**:pencil2:\n"
		DiscordBot.Data.msgsrb2 = DiscordBot.Data.msgsrb2..text
		player.oldname = player.name
	end
	if DiscordBot.Commands.cv_joinquit.value == 1
		if player.logjoin != true
			local text = "["..#player.."]"..":rocket:**"..player.name.."** has joined the game:rocket:\n"
			if text
				DiscordBot.Functions.spamchatbug(player, text, true)
				player.logjoin = true
			end
		end
	end
end, MT_PLAYER)

addHook("PlayerJoin", function(playernum)
	--unpause if player has joined the game
	if DiscordBot.Commands.cv_autopause.value == 1
		if paused == true
			DiscordBot.Data.paused = false
			COM_BufInsertText(server, "pause")
		end
	end
end)

addHook("PlayerQuit", function(player, reason)
	local text = nil
	if DiscordBot.Commands.cv_joinquit.value == 1
		player.quitlog = true
		if reason == KR_KICK
			text = "["..#player.."]"..":boot:**"..player.name.."** has been kicked:boot:\n"
		end
		if reason == KR_PINGLIMIT
			text = "["..#player.."]"..":red_square:**"..player.name.."** left the game (Ping limit):red_square:\n"
		end
		if reason == KR_SYNCH
			text = "["..#player.."]"..":o:**"..player.name.."** left the game (Synch Failure):o:\n"
		end
		if reason == KR_TIMEOUT
			text = "["..#player.."]"..":o:**"..player.name.."** left the game (Connection timeout):o:\n"
		end
		if reason == KR_BAN
			text = "["..#player.."]"..":hammer:**"..player.name.."** has been banned:hammer:\n"
		end
		if reason == KR_LEAVE
			text = "["..#player.."]"..":door:**"..player.name.."** left the game:door:\n"
		end
		if text
			DiscordBot.Functions.spamchatbug(player, text, true)
		end
	end
	/*
	--pause if server is empty
	if DiscordBot.Commands.cv_autopause.value == 1
		local count = 0
		count = DiscordBot.Functions.playerontheserver()
		count = $ - 1
		if count == 0
			if paused == false
				DiscordBot.Data.paused = true
				COM_BufInsertText(server, "server_log players")
				COM_BufInsertText(server, "server_log pause")
				COM_BufInsertText(server, "pause")
			end
		end
	end
	*/
end, MT_PLAYER)

addHook("NetVars", function(n)
	 DiscordBot.Data = n($)
	 DiscordBot.Messages = n($)
end)
