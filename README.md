# SRB2DiscordBot
<span style="font-size: 18px">Have a chat with SRB2 players on Discord!</span></b><br>​</div><b>
<b><span style="font-size: 15px">Python modules:</span></b><br>
<ul>
<li data-xf-list-type="ul">Discord 1.7.3;</li>
<li data-xf-list-type="ul">Tkinter 0.1.0;</li>
<li data-xf-list-type="ul">Colorama 0.4.6;</li>
<li data-xf-list-type="ul">C data types 1.1.0;</li>
<li data-xf-list-type="ul">Transliterate 1.10.2;</li>
<li data-xf-list-type="ul">Regular Expression Engine 2.2.1;</li>
<li data-xf-list-type="ul">JavaScript Object Notation 2.0.9.</li>
</ul><br>
<span style="font-size: 15px">What the bot is able to do:</span></b><br>
<ul>
<li data-xf-list-type="ul">translate the chat from the game in the discord and let communicate outside the game;</li>
<li data-xf-list-type="ul">Run the server with parameters, the parameters are specified in the .cfg file;</li>
<li data-xf-list-type="ul">Restart the server with a fatal error or at closing the server;</li>
<li data-xf-list-type="ul">Display server statistics (map, image (url), map number, number of emeralds, number of players, map time, server time, list of players and their statistics).</li>
<li data-xf-list-type="ul">Display messages in the console with timecodes;</li>
<li data-xf-list-type="ul">write log messages from the game and from Discord in the log file;</li>
<li data-xf-list-type="ul">Returns the current map after server restart;</li>
<li data-xf-list-type="ul">Save game logs in another folder (because of an auto restart, logs are not saved in the logs folder);</li>
<li data-xf-list-type="ul">Execute commands such as: csay, kick, ban, map, exitlevel, restart in Discord;</li>
<li data-xf-list-type="ul">Autorestart on the desired map or through the number of completed levels, changes parameters if this is configured in the autorestart.cfg;</li>
<li data-xf-list-type="ul">Pause the server if there are no players on the server.</li>
</ul><br>
<div style="text-align: center"><span style="font-size: 18px"><b>SRB2 command table</b></span>​</div><br>
<div class="bbTable">
<table style="width: 100%"><tbody><tr><th>Name</th><th>Description</th><th>Possible Value</th><th>Default Value</th></tr><tr><td>dbot_joinquit</td><td>Notifies in Discord if a player joins or leaves the game for any reason.</td><td>CV_OnOff</td><td>On</td></tr><tr><td>dbot_autopause</td><td>Pauses the game if the server has no players.</td><td>CV_OnOff</td><td>On</td></tr><tr><td>dbot_nospamchat</td><td>Puts Calmdown on second for messages.</td><td>CV_OnOff</td><td>Off</td></tr><tr><td>dbot_messagedelay</td><td>Delays messages and sends messages after two seconds.</td><td>CV_OnOff</td><td>On</td></tr></tbody></table>
</div><br>
<div style="text-align: center"><b><span style="font-size: 18px">CFG files</span></b>​</div><ul>
<li data-xf-list-type="ul">autorestart.cfg - configures autorestart and when to change server parameters;</li>
<li data-xf-list-type="ul">commandperms.cfg - configures command permissions;</li>
<li data-xf-list-type="ul">config.cfg - it contains the token and other standard settings;</li>
<li data-xf-list-type="ul">dontsavemap.cfg - ignores the return of levels on maps in the file the next time you start the server;</li>
<li data-xf-list-type="ul">emotes.cfg - configures emoji for information channel;</li>
<li data-xf-list-type="ul">serverparameters\parameters.cfg - parameters for the server, they will not change, unless you edit the file;</li>
<li data-xf-list-type="ul">serverparameters\pcfg&lt;X&gt;.cfg - parameters for the server, if you have configured restart they will change.</li>
</ul><br>
<div style="text-align: center"><b>SRB2Workshop Page - https://srb2workshop.org/resources/srb2discordbot.84/</b><br>
<div style="text-align: center"><b>Video Guide - https://youtu.be/ZiKhOHKt_xk</b><br>
<div class="bbMediaWrapper" data-media-site-id="youtube" data-media-key="ZiKhOHKt_xk">
</div><br>
