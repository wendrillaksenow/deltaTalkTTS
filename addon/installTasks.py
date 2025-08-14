# -*- coding: UTF-8 -*-
# installTasks.py
# A part of the deltaTalkTTS driver for NVDA (Non Visual Desktop Access)
# Copyright (C) 1997-2001 Denis R. Costa <denis@micropowerglobal.com> & MicroPower Software <www.micropower.ai>
# Copyright (C) 2024-2025 Patrick Barboza <patrickbarboza774@gmail.com> & Wendrill Aksenow Brandão <wendrillaksenow@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import os
import gui
import wx
import addonHandler
from logHandler import log

# Initialize translation support
addonHandler.initTranslation()

def onInstall():
	# Check if any version of the "Informação Pausada" add-on is installed
	for addon in addonHandler.getAvailableAddons():
		if addon.name in ["Pausing Information", "pausingInfo"]:
			message = _(
				# Translators: Message asking if the user wants to uninstall the previous version of the add-on
				"The 'Pausing Information' add-on has been detected. This add-on has been integrated into DeltaTalk as the 'Virtual Vision Mode' plugin.\n\n"
				"To avoid conflicts, this add-on must be removed.\n\n"
				"Do you want to remove the 'Pausing Information' add-on now?"
			)
			# Translators: Question title
			title = _("Add-on Conflict Detected")
			result = gui.messageBox(message, title, style=wx.YES_NO | wx.ICON_WARNING, parent=gui.mainFrame)
			if result == wx.YES:
				addon.requestRemove()
				log.info(_("The '{addonName}' add-on has been successfully removed.").format(addonName=addon.name))
			else:
				log.info(_("User canceled removal of the '{addonName}' add-on.").format(addonName=addon.name))
				raise Exception(_("Installation canceled by the user due to conflict with '{addonName}'.").format(addonName=addon.name))