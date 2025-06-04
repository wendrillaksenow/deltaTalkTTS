#synthDrivers/deltatalk.py
#A part of the deltaTalkTTS driver for NVDA (Non Visual Desktop Access)
#Copyright (C) 1997-2001 Denis R. Costa <denis@micropowerglobal.com> & MicroPower Software <www.micropower.ai>
#Copyright (C) 2024-2025 Patrick Barboza <patrickbarboza774@gmail.com> & Wendrill Aksenow Brandão <wendrillaksenow@gmail.com>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

# Import the necessary modules
import os
import sys
import ctypes
from ctypes import *
from synthDriverHandler import SynthDriver as SynthDriverBase
from synthDriverHandler import synthDoneSpeaking, SynthDriver, synthIndexReached, VoiceInfo
import logging
from speech.commands import IndexCommand, PitchCommand, RateCommand, VolumeCommand, CharacterModeCommand
import shutil
import subprocess
import addonHandler

addonHandler.initTranslation()

# DeltaTalk error dictionary
ERROR_CODES = {
	0: "TTS_SUCCESSFUL",
	-1: "TTS_NOT_INITIALIZED",
	-5: "TTS_FILE_OPEN_ERROR",
	-7: "TTS_INIT_ENGINE_ERROR",
	-13: "TTS_WAVEOUT_NOT_AVAILABLE",
	-103: "TTS_DSP_NOT_FOUND",
	-106: "TTS_NO_LICENSE",
}

# Supported DSP modes
DSP_MODES = {
	"MULTIMEDIA": 0,
	"TELEPHONY": 1
}

# Available voices
VOICES = {
	"br1": "DeltaTalk - Marcelo (16 kHz)",
	"br2": "DeltaTalk - Paula (22 kHz)",
	"br3": "DeltaTalk - José (22 kHz)"
}

VOICE_MAP = {
	"br1": 0,  # Marcelo
	"br3": 1,  # José
	"br2": 2   # Paula
}

# Multiplier adjusted to convert values correctly
DT_MULTIPLIER = 20 / 100  # 100 (NVDA) → 20 (DeltaTalk), mínimo 1

def convert_nvda_to_dt(value):
	"""Converts a value from the NVDA scale (0-100) to the DeltaTalk scale (1-20)."""
	return max(1, min(20, int(value * DT_MULTIPLIER)))

class SynthDriver(SynthDriverBase):
	"""DeltaTalk Synthesizer driver for NVDA."""
	name = "deltatalk"
	# Translators: Description for a speech synthesizer for NVDA.
	description = _("MicroPower DeltaTalk TTS")
	language = "pt-BR"

	supportedSettings = [
		SynthDriver.VoiceSetting(),
		SynthDriver.RateSetting(),
		SynthDriver.PitchSetting(),
		SynthDriver.VolumeSetting(),
	]

	supportedCommands = {
		IndexCommand,
		RateCommand,
		PitchCommand,
		VolumeCommand,
		CharacterModeCommand,
	}

	supportedNotifications = {synthIndexReached, synthDoneSpeaking}

	@classmethod
	def check(cls):
		nvda_root = os.path.dirname(os.path.abspath(sys.executable))
		dll_path = os.path.join(nvda_root, "Dtalk32T.dll")
		if not os.path.isfile(dll_path):
			dll_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deltatalk", "Dtalk32T.dll")
		logging.debug(_("check: Checking the path: {path}").format(path=dll_path))
		if not os.path.isfile(dll_path):
			logging.debug(_("check: Dtalk32T.dll not found"))
			return False
		try:
			ctypes.WinDLL(dll_path)
			logging.debug(_("check: Dtalk32T.dll loaded successfully"))
			return True
		except Exception as e:
			logging.debug(_("check: Failed to load DLL: {error}").format(error=e))
			return False

	def __init__(self):
		super(SynthDriver, self).__init__()
		self._rate = 50
		self._pitch = 50
		self._volume = 100
		self._voice = "br1"
		self._lastIndex = 0
		self.instancia = None

		# NVDA and add-on path
		nvda_root = os.path.dirname(os.path.abspath(sys.executable))
		addon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deltatalk")
		dll_path = os.path.join(nvda_root, "Dtalk32T.dll")

		# Check and copy files if necessary
		required_files = ["br1.dsp", "br2.dsp", "br3.dsp", "brazil.alp", "brazil.des", "brazil.f0", "brazil.rul", "brazilf0.HHS", "brport.lng", "Dtalk32t.dll", "DTDsp32t.dll", "prosody.dll", "serial.dll"]
		missing_files = [f for f in required_files if not os.path.isfile(os.path.join(nvda_root, f))]
		if missing_files:
			logging.debug(_("Missing files in NVDA: {files}. Copying from the add-on.").format(files=", ".join(missing_files)))
			for f in missing_files:
				src = os.path.join(addon_path, f)
				dst = os.path.join(nvda_root, f)
				if os.path.isfile(src):
					try:
						shutil.copy2(src, dst)
						logging.debug(_("Copied: {file}").format(file=f))
					except PermissionError:
						logging.warning(_("Permission denied when copying {file}. Trying with elevation.").format(file=f))
						self._copy_with_elevation(src, dst)
					except Exception as e:
						logging.error(_("Error copying {file}: {error}").format(file=f, error=e))

		if not os.path.isfile(dll_path):
			logging.error(_("DLL not found in: {path}").format(path=dll_path))
			raise RuntimeError(_("DeltaTalk DLL not found. Check the installation of the add-on."))

		if hasattr(os, "add_dll_directory"):
			os.add_dll_directory(nvda_root)
		else:
			original_path = os.environ["PATH"]
			os.environ["PATH"] = nvda_root + os.pathsep + original_path

		try:
			self.dt = ctypes.WinDLL(dll_path)
			logging.debug(_("__init__: DLL loaded successfully"))
		except Exception as e:
			logging.error(_("Error loading DeltaTalk DLL in {path}: {error}").format(path=dll_path, error=e))
			self.dt = None
			raise RuntimeError(_("Failed to load DLL Dtalk32T.dll: {error}").format(error=e))
		finally:
			if not hasattr(os, "add_dll_directory"):
				os.environ["PATH"] = original_path

		if not self._initialize_tts():
			raise RuntimeError(_("DeltaTalk synthesizer failed to initialize"))

	def _copy_with_elevation(self, src, dst):
		"""Try copying a file with elevation via shell."""
		try:
			cmd = f'cmd.exe /c copy "{src}" "{dst}"'  # f-string permitido aqui, pois não é traduzido
			result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
			logging.debug(_("The copy with elevation was successful: {source} -> {destination}").format(source=src, destination=dst))
		except subprocess.CalledProcessError as e:
			logging.error(_("The copy with elevation failed: {output} Run NVDA as administrator and try again").format(output=e.output))

	def _initialize_tts(self):
		if not self.dt:
			logging.error(_("Attempt to initialize TTS without the DLL loaded."))
			return False

		nvda_root = os.path.dirname(os.path.abspath(sys.executable))
		logging.debug(_("NVDA directory: {path}").format(path=nvda_root))
		logging.debug(_("Files in the folder: {files}").format(files=", ".join(os.listdir(nvda_root))))
		original_cwd = os.getcwd()
		logging.debug(_("Original work directory: {path}").format(path=original_cwd))
		os.chdir(nvda_root)
		logging.debug(_("Work directory changed to: {path}").format(path=os.getcwd()))

		try:
			logging.debug(_("Starting TTS initialization"))
			self.instancia = self.dt.TTSENG_Init(False, None, DSP_MODES["MULTIMEDIA"])
			if self.instancia <= 0:
				logging.error(_("Error initializing TTS: {error}").format(error=ERROR_CODES.get(self.instancia, "Unknown error")))
				self.instancia = None
				return False
			logging.debug(_("DeltaTalk initialized. Instance: {instance}").format(instance=self.instancia))
			self._apply_settings()
			return True
		except Exception as e:
			logging.error(_("Error initializing TTS: {error}").format(error=e))
			self.instancia = None
			return False
		finally:
			os.chdir(original_cwd)
			logging.debug(_("Work directory restored"))

	def _apply_settings(self):
		if self.instancia:
			dt_rate = convert_nvda_to_dt(self._rate)
			dt_volume = convert_nvda_to_dt(self._volume)
			dt_pitch = convert_nvda_to_dt(self._pitch)
			
			result = self.dt.TTSENG_SetMode(self.instancia, dt_rate, dt_volume, dt_pitch)
			if result != 0:
				logging.error(_("Error when applying settings: {error} ({code})").format(
					error=ERROR_CODES.get(result, "Unknown error"), code=result))
			else:
				logging.debug(_("Settings applied: rate={rate}, volume={volume}, pitch={pitch}").format(
					rate=dt_rate, volume=dt_volume, pitch=dt_pitch))
			
			if self._voice in VOICE_MAP:
				voice_id = VOICE_MAP[self._voice]
				voice_result = self.dt.TTSENG_SetVoice(self.instancia, voice_id, 10)
				if voice_result != 0:
					logging.error(_("Error when applying voice: {error} ({code})").format(
						error=ERROR_CODES.get(voice_result, "Unknown error"), code=voice_result))
				else:
					logging.debug(_("Applied voice: {voice} (ID: {id})").format(
						voice=self._voice, id=voice_id))

	def speak(self, speechSequence):
		if not self.instancia:
			logging.error(_("Speech attempt without initialized instance."))
			return

		base_pitch = self._pitch
		char_mode = False
		for item in speechSequence:
			if isinstance(item, CharacterModeCommand):
				char_mode = item.state
			elif isinstance(item, str):
				text = item.strip()
				if not text:
					continue
				if char_mode:
					for char in text:
						self._speak_or_append(char)
				else:
					self._speak_or_append(text)
				if self._pitch != base_pitch:
					self._set_pitch(base_pitch)
			elif isinstance(item, IndexCommand):
				synthIndexReached.notify(synth=self, index=item.index)
			elif isinstance(item, (PitchCommand, RateCommand, VolumeCommand)):
				self._apply_command(item)

		synthDoneSpeaking.notify(synth=self)

	def _speak_or_append(self, text):
		if not text:
			return
		try:
			encoded_text = text.encode("ansi", errors="replace")
			play_result = self.dt.TTSENG_PlayText(self.instancia, c_char_p(encoded_text), True)
			if play_result == -2:  # TTS_BUSY
				append_result = self.dt.TTSENG_AppendText(self.instancia, c_char_p(encoded_text))
				if append_result != 0:
					logging.error(_("Error when attaching text: {error}").format(error=ERROR_CODES.get(append_result, "Unknown error")))
				else:
					logging.debug(_("Attached text: {text}").format(text=text))
			elif play_result != 0:
				logging.error(_("Error when speaking text: {error}").format(error=ERROR_CODES.get(play_result, "Unknown error")))
			else:
				logging.debug(_("Spoken text: {text}").format(text=text))
		except Exception as e:
			logging.error(_("Error when processing text: {error}").format(error=e))

	def _apply_command(self, command):
		if isinstance(command, PitchCommand):
			current_pitch = self._pitch
			new_pitch = max(0, min(100, current_pitch + command.offset))
			self._set_pitch(new_pitch)
		elif isinstance(command, RateCommand):
			self._set_rate(command.value)
		elif isinstance(command, VolumeCommand):
			self._set_volume(command.value)

	def _get_rate(self):
		return self._rate

	def _set_rate(self, value):
		self._rate = value
		if self.instancia:
			dt_rate = convert_nvda_to_dt(value)
			dt_volume = convert_nvda_to_dt(self._volume)
			dt_pitch = convert_nvda_to_dt(self._pitch)
			self.dt.TTSENG_SetMode(self.instancia, dt_rate, dt_volume, dt_pitch)
			logging.info(_("Speed set to {rate} (converted from {original})").format(rate=dt_rate, original=value))

	def _get_pitch(self):
		return self._pitch

	def _set_pitch(self, value):
		self._pitch = value
		if self.instancia:
			dt_rate = convert_nvda_to_dt(self._rate)
			dt_volume = convert_nvda_to_dt(self._volume)
			dt_pitch = convert_nvda_to_dt(value)
			self.dt.TTSENG_SetMode(self.instancia, dt_rate, dt_volume, dt_pitch)
			logging.info(_("Pitch set to {pitch} (converted from {original})").format(pitch=dt_pitch, original=value))

	def _get_volume(self):
		return self._volume

	def _set_volume(self, value):
		self._volume = value
		if self.instancia:
			dt_rate = convert_nvda_to_dt(self._rate)
			dt_volume = convert_nvda_to_dt(value)
			dt_pitch = convert_nvda_to_dt(self._pitch)
			self.dt.TTSENG_SetMode(self.instancia, dt_rate, dt_volume, dt_pitch)
			logging.info(_("Volume set to {volume} (converted from {original})").format(volume=dt_volume, original=value))

	@property
	def voice(self):
		return self._voice

	@voice.setter
	def voice(self, value):
		if value in VOICES:
			self._voice = value
			if self.instancia:
				voice_id = VOICE_MAP[value]
				result = self.dt.TTSENG_SetVoice(self.instancia, voice_id, 10)
				if result != 0:
					logging.error(_("Error configuring voice: {error} ({code})").format(
						error=ERROR_CODES.get(result, "Unknown error"), code=result))
				else:
					logging.info(_("Voice changed to {voice}").format(voice=VOICES[value]))

	@property
	def availableVoices(self):
		return {
			key: VoiceInfo(
				id=key,
				displayName=VOICES[key],
			) for key in VOICES
		}

	def pause(self, switch):
		if self.instancia:
			if switch:
				self.dt.TTSENG_PauseText(self.instancia)
				logging.debug(_("Text paused"))
			else:
				self.dt.TTSENG_ResumeText(self.instancia)
				logging.debug(_("Text resumed"))

	def cancel(self):
		if self.instancia:
			self.dt.TTSENG_StopText(self.instancia)
			logging.debug(_("Text stopped"))

def terminate(self):
	if self.instancia:
		try:
			self.dt.TTSENG_StopText(self.instancia)
			result = self.dt.TTSENG_Close(self.instancia)
			if result != 0:
				logging.error(_("Error when closing: {error} ({code})").format(
					error=ERROR_CODES.get(result, "Unknown error"), code=result))
			else:
				logging.debug(_("DeltaTalk synthesizer successfully closed"))
		except Exception as e:
			logging.error(_("Error closing the synthesizer: {error}").format(error=e))
		finally:
			self.instancia = None
			self.dt = None