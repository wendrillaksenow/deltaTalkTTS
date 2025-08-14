# globalPlugins/deltaTalkSettings.py
# DeltaTalk settings as GlobalPlugin for NVDA
# A part of the deltaTalkTTS driver for NVDA (Non Visual Desktop Access)
# Copyright (C) 1997-2001 Denis R. Costa <denis@micropower.ai> & MicroPower Software <www.micropower.ai>
# Copyright (C) 2024-2025 Patrick Barboza <patrickbarboza774@gmail.com> & Wendrill Aksenow Brandão <wendrillaksenow@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import globalPluginHandler
import gui
from gui import guiHelper, nvdaControls
import wx
import config
from logHandler import log
import addonHandler
from synthDriverHandler import getSynth
from .virtualVision import VirtualVisionSettingsDialog

addonHandler.initTranslation()

# DeltaTalk configuration options
confspec = {
	"useNVWave": "boolean(default=False)",
}

config.conf.spec["deltaTalk"] = confspec

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super().__init__()
		# Register the DeltaTalk settings panel
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(DeltaTalkSettingsPanel)

	def terminate(self):
		# Remove the settings panel on shutdown
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(DeltaTalkSettingsPanel)
		super().terminate()

class DeltaTalkSettingsPanel(gui.settingsDialogs.SettingsPanel):
	title = _("DeltaTalk")

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		self.useNVWaveCheckbox = sHelper.addItem(wx.CheckBox(self, label=_("&Use NVWave for audio playback")))
		self.useNVWaveCheckbox.SetValue(config.conf["deltaTalk"]["useNVWave"])
		self.useNVWaveCheckbox.Bind(wx.EVT_CHECKBOX, self.onUseNVWaveCheckbox)

		self.virtualVisionButton = sHelper.addItem(wx.Button(self, label=_("&Virtual Vision Mode...")))
		self.virtualVisionButton.Bind(wx.EVT_BUTTON, self.onVirtualVisionSettings)

	def onUseNVWaveCheckbox(self, event):
		if event.IsChecked():
			result = gui.messageBox(
				_("The NVWave audio playback is an experimental feature and may cause problems.\n\n"
				  "You should only use it for testing purposes and if you know exactly what you are doing.\n\n"
				  "Are you shure you want to enable it?"),
				_("Confirmation"),
				wx.YES_NO | wx.ICON_QUESTION,
				self
			)
			if result == wx.NO:
				self.useNVWaveCheckbox.SetValue(False)
				log.debug(_("NVWave activation cancelled by user"))
			else:
				log.debug(_("NVWave has been activated"))

	def onVirtualVisionSettings(self, event):
		try:
			dialog = VirtualVisionSettingsDialog(self)
			dialog.ShowModal()
			dialog.Destroy()
		except RuntimeError:
			# The message has already been displayed in the VirtualVisionSettingsDialog
			pass

	def onSave(self):
		old_use_nvwave = config.conf["deltaTalk"]["useNVWave"]
		new_use_nvwave = self.useNVWaveCheckbox.GetValue()

		config.conf["deltaTalk"]["useNVWave"] = new_use_nvwave

		# Display restart message only if useNVWave has changed
		if old_use_nvwave != new_use_nvwave:
			gui.messageBox(
				_("Changing the NVWave configuration requires DeltaTalk to be reloaded to take effect."),
				_("Warning"),
				wx.OK | wx.ICON_INFORMATION,
				gui.mainFrame
			)