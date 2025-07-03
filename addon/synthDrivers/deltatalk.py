# synthDrivers/deltatalk.py
# A part of the deltaTalkTTS driver for NVDA (Non Visual Desktop Access)
# Copyright (C) 1997-2001 Denis R. Costa <denis@micropowerglobal.com> & MicroPower Software <www.micropower.ai>
# Copyright (C) 2024-2025 Patrick Barboza <patrickbarboza774@gmail.com> & Wendrill Aksenow Brandão <wendrillaksenow@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Import the necessary modules
import os
import sys
import ctypes
import hashlib
import tempfile
import queue
import threading
import time
import config
import nvwave
from ctypes import *
from synthDriverHandler import SynthDriver as SynthDriverBase
from synthDriverHandler import synthDoneSpeaking, SynthDriver, synthIndexReached, VoiceInfo
from logHandler import log
from speech.commands import IndexCommand, PitchCommand, RateCommand, VolumeCommand, CharacterModeCommand
import shutil
import addonHandler
from systemUtils import execElevated

addonHandler.initTranslation()

# DeltaTalk error dictionary
ERROR_CODES = {
	0: {"code": 0, "literal": "TTS_SUCCESSFUL", "friendly": _("Operation completed successfully")},
	-1: {"code": -1, "literal": "TTS_NOT_INITIALIZED", "friendly": _("The synthesizer is not initialized")},
	-2: {"code": -2, "literal": "TTS_BUSY", "friendly": _("The synthesizer is busy processing another task")},
	-3: {"code": -3, "literal": "TTS_BAD_COMMAND", "friendly": _("Invalid command issued to the synthesizer")},
	-4: {"code": -4, "literal": "TTS_DSP_INIT_ERROR", "friendly": _("Failed to initialize audio processing subsystem")},
	-5: {"code": -5, "literal": "TTS_FILE_OPEN_ERROR", "friendly": _("Failed to open the required file")},
	-6: {"code": -6, "literal": "TTS_FILE_WRITE_ERROR", "friendly": _("Failed to write to the specified file")},
	-7: {"code": -7, "literal": "TTS_INIT_ENGINE_ERROR", "friendly": _("Failed to initialize the synthesizer engine")},
	-8: {"code": -8, "literal": "TTS_MEM_ALLOC_ERROR", "friendly": _("Insufficient memory to process the request")},
	-9: {"code": -9, "literal": "TTS_WAVEOUT_BUSY", "friendly": _("Audio device is already in use by another program")},
	-10: {"code": -10, "literal": "TTS_WAVEOUT_OPEN_ERROR", "friendly": _("Failed to open the audio device")},
	-11: {"code": -11, "literal": "TTS_WAVEOUT_WRITE_ERROR", "friendly": _("Failed to send audio buffer to the sound card")},
	-12: {"code": -12, "literal": "TTS_WAVEOUT_FORMAT_ERROR", "friendly": _("Audio format not supported by the sound card")},
	-13: {"code": -13, "literal": "TTS_WAVEOUT_NOT_AVAILABLE", "friendly": _("Audio output device is not available")},
	-14: {"code": -14, "literal": "TTS_WAVEOUT_ERROR", "friendly": _("Error communicating with the sound card driver")},
	-15: {"code": -15, "literal": "TTS_WAVEOUT_MEM_ALLOC_ERROR", "friendly": _("Insufficient memory to store synthesized audio")},
	-16: {"code": -16, "literal": "TTS_VALUE_OUT_OF_RANGE", "friendly": _("The provided value is out of range")},
	-17: {"code": -17, "literal": "TTS_PCM_FINISHED", "friendly": _("PCM audio processing completed")},
	-100: {"code": -100, "literal": "TTS_MBR_ERROR", "friendly": _("Internal signal processing error")},
	-103: {"code": -103, "literal": "TTS_DSP_NOT_FOUND", "friendly": _("DSP file not found")},
	-104: {"code": -104, "literal": "TTS_PROSODY_INIT_ERROR", "friendly": _("Prosody modeling file not found")},
	-106: {"code": -106, "literal": "TTS_NO_LICENSE", "friendly": _("The number of simultaneous instances of the synthesizer has been extrapolated")},
}

# Supported DSP modes
DSP_MODES = {
	"MULTIMEDIA": 0,
	"TELEPHONY": 1
}

# Constants for TTSENG_GenAudioBuffer
TTS_GENPCM_NEW_SIMPLE_BLOCK = 0
TTS_GENPCM_NEW_MULTI_BLOCK = 1
TTS_GENPCM_NEXT_BLOCK = 2
TTS_GENPCM_16BITS = 0
TTS_GENPCM_8BITS = 1
TTS_GENPCM_ULAW = 2
TTS_GENPCM_ALAW = 3

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

def test_write_permission(target_path):
	"""Test if we have write permission to the target directory."""
	test_file = os.path.join(target_path, "test_write_permission.tmp")
	try:
		with open(test_file, "w") as f:
			f.write("test")
		os.remove(test_file)
		return True
	except (OSError, IOError):
		return False

def copy_files_with_elevation(source_dir, target_dir, file_list):
	"""
	Copy specific files with elevated permissions using batch file approach.
	Returns True if successful, False otherwise.
	"""
	if not file_list:
		return True
	
	batch_content = "@echo off\n"
	batch_content += f'echo Copying DeltaTalk files from "{source_dir}" to "{target_dir}"\n'
	# Add copy commands for each file
	try:
		for filename in file_list:
			source_file = os.path.join(source_dir, filename)
			target_file = os.path.join(target_dir, filename)
			if os.path.isfile(source_file):
				# Use xcopy for better reliability
				batch_content += f'xcopy /Y "{source_file}" "{target_file}*"\n'
		
		batch_content += "echo Copy operation completed\n"
		
		# Create temporary batch file
		with tempfile.NamedTemporaryFile(delete=False, suffix=".bat", mode="w", encoding="utf-8") as batch_file:
			batch_file.write(batch_content)
			batch_path = batch_file.name
		
		try:
			# Execute batch file with elevation
			log.debug(_("Executing batch file with elevation: {path}").format(path=batch_path))
			result = execElevated("cmd.exe", ["/c", batch_path], wait=True)
			if result == 0:
				log.info(_("Files copied successfully with elevated permissions"))
				return True
			else:
				log.error(_("Batch file execution failed with code: {code}").format(code=result))
				return False
		finally:
			# Clean up batch file
			try:
				os.remove(batch_path)
			except Exception as e:
				log.warning(_("Failed to delete temporary batch file: {error}").format(error=e))
	except Exception as e:
		log.error(_("Error creating/executing batch file: {error}").format(error=e))
		return False

class SynthDriver(SynthDriverBase):
	"""DeltaTalk Synthesizer driver for NVDA."""
	name = "deltatalk"
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
		log.debug(_("Checking the path: {path}").format(path=dll_path))
		if not os.path.isfile(dll_path):
			log.debug(_("Dtalk32T.dll not found"))
			return False
		try:
			ctypes.WinDLL(dll_path)
			log.debug(_("Dtalk32T.dll loaded successfully"))
			return True
		except Exception as e:
			log.debug(_("Failed to load DLL: {error}").format(error=e))
			return False

	def __init__(self):
		super(SynthDriver, self).__init__()
		self._rate = 50
		self._pitch = 50
		self._volume = 100
		self._voice = "br1"
		self._lastIndex = 0
		self.instancia = None
		self._nvwave_player = None
		self._use_nvwave = False  # Change to True to test audio playback via nvwave
		self._audio_thread = None
		self._audio_queue = queue.Queue(maxsize=50)  # Reduced to avoid overloading
		self._audio_thread_running = False
		self._audio_lock = threading.Lock()
		self._is_speaking = False  # Status to track if the DLL is busy


		# NVDA and add-on path
		nvda_root = os.path.dirname(os.path.abspath(sys.executable))
		addon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deltatalk")
		dll_path = os.path.join(nvda_root, "Dtalk32T.dll")

		# Check and copy files if necessary
		required_files = [
			"br1.dsp", "br2.dsp", "br3.dsp", "brazil.alp", "brazil.des",
			"brazil.f0", "brazil.rul", "brazilf0.HHS", "brport.lng",
			"Dtalk32T.dll", "DTDsp32T.dll", "prosody.dll", "serial.dll"
		]

		# Check dictionary file (brport.lng) for updates
		dictionary_file = "brport.lng"
		dictionary_needs_update = False
		missing_files = []

		source_dict = os.path.join(addon_path, dictionary_file)
		target_dict = os.path.join(nvda_root, dictionary_file)

		if os.path.isfile(source_dict):
			if not os.path.isfile(target_dict):
				dictionary_needs_update = True
				missing_files.append(dictionary_file)
				log.info(_("Dictionary file {file} missing in NVDA. Will be copied.").format(file=dictionary_file))
			else:
				source_hash = self._calculate_file_hash(source_dict)
				target_hash = self._calculate_file_hash(target_dict)
				if source_hash != target_hash:
					dictionary_needs_update = True
					missing_files.append(dictionary_file)
					log.info(_("Dictionary file {file} is outdated in NVDA. Will be copied.").format(file=dictionary_file))
				else:
					log.debug(_("Dictionary file {file} is up to date.").format(file=dictionary_file))
		else:
			log.warning(_("Dictionary file {file} not found in add-on. Skipping.").format(file=dictionary_file))

		# Check other required files (only if missing)
		for f in required_files:
			if f == dictionary_file:
				continue  # Already checked
			source_file = os.path.join(addon_path, f)
			target_file = os.path.join(nvda_root, f)
			if not os.path.isfile(source_file):
				log.warning(_("Required file not found in add-on: {file}").format(file=f))
				continue
			if not os.path.isfile(target_file):
				missing_files.append(f)
				log.info(_("File missing in NVDA: {file}.").format(file=f))

		if missing_files:
			log.info(_("Missing or outdated files in NVDA: {files}. Attempting to copy from add-on.").format(
				files=", ".join(missing_files)))
			
			# Check if we need elevation
			need_elevation = not test_write_permission(nvda_root)
			copy_success = False
			
			if need_elevation:
				log.info(_("Elevated permissions required. Attempting elevated copy."))
				copy_success = copy_files_with_elevation(addon_path, nvda_root, missing_files)
				
				if not copy_success:
					log.warning(_("Elevated copy failed. Synthesizer may use outdated dictionary or some files may be missing."))
			else:
				log.info(_("Normal permissions sufficient. Copying files."))
				try:
					for f in missing_files:
						src = os.path.join(addon_path, f)
						dst = os.path.join(nvda_root, f)
						if os.path.isfile(src):
							shutil.copy2(src, dst)
							log.debug(_("Copied: {file}").format(file=f))
					copy_success = True
				except Exception as e:
					log.error(_("Error copying files: {error}").format(error=e))
					copy_success = False
			if copy_success:
				log.info(_("DeltaTalk files successfully copied/updated to {path}.").format(path=nvda_root))
			else:
				log.warning(_("Some files may not have been copied. Synthesizer functionality may be limited."))

		# Verify DLL exists after copy attempt
		if not os.path.isfile(dll_path):
			log.error(_("DLL not found in: {path}").format(path=dll_path))
			raise RuntimeError(_("DeltaTalk DLL not found. Check the installation of the add-on."))

		# Set up DLL path
		if hasattr(os, "add_dll_directory"):
			os.add_dll_directory(nvda_root)
		else:
			original_path = os.environ["PATH"]
			os.environ["PATH"] = nvda_root + os.pathsep + original_path

		try:
			self.dt = ctypes.WinDLL(dll_path)
			log.debug(_("DLL loaded successfully"))
		except Exception as e:
			log.error(_("Error loading DeltaTalk DLL in {path}: {error}").format(path=dll_path, error=e))
			self.dt = None
			raise RuntimeError(_("Failed to load DLL Dtalk32T.dll: {error}").format(error=e))
		finally:
			if not hasattr(os, "add_dll_directory"):
				os.environ["PATH"] = original_path

		if not self._initialize_tts():
			raise RuntimeError(_("DeltaTalk synthesizer failed to initialize"))

		# Activate symbol dictionary
		try:
			self._ensure_symbol_dictionary_active()
		except Exception as e:
			log.error(_("Error managing symbol dictionary: {error}").format(error=e))

		# Configure nvwave after TTS initialization
		if self.instancia:
			self._setup_nvwave()
			self._start_audio_thread()

	def _calculate_file_hash(self, file_path):
		"""Calculate SHA-256 hash of a file."""
		try:
			sha_hash = hashlib.sha256()
			with open(file_path, "rb") as f:
				for chunk in iter(lambda: f.read(4096), b""):
					sha_hash.update(chunk)
			return sha_hash.hexdigest()
		except Exception as e:
			log.error(_("Error calculating hash for {file}: {error}").format(file=file_path, error=e))
			return None

	def _initialize_tts(self):
		if not self.dt:
			log.error(_("Attempt to initialize TTS without the DLL loaded."))
			return False
		nvda_root = os.path.dirname(os.path.abspath(sys.executable))
		log.debug(_("NVDA directory: {path}").format(path=nvda_root))
		log.debug(_("Files in the folder: {files}").format(files=", ".join(os.listdir(nvda_root))))
		original_cwd = os.getcwd()
		log.debug(_("Original work directory: {path}").format(path=original_cwd))
		os.chdir(nvda_root)
		log.debug(_("Work directory changed to: {path}").format(path=os.getcwd()))
		try:
			log.debug(_("Starting TTS initialization"))
			self.instancia = self.dt.TTSENG_Init(False, None, DSP_MODES["MULTIMEDIA"])
			if self.instancia <= 0:
				log.error(_("Error initializing TTS: {error}").format(error=ERROR_CODES.get(self.instancia, {"friendly": _("Unknown error")})["friendly"]))
				self.instancia = None
				return False
			log.debug(_("DeltaTalk initialized. Instance: {instance}").format(instance=self.instancia))
			self._apply_settings()
			return True
		except Exception as e:
			log.error(_("Error initializing TTS: {error}").format(error=e))
			self.instancia = None
			return False
		finally:
			os.chdir(original_cwd)
			log.debug(_("Work directory restored"))

	def _ensure_symbol_dictionary_active(self):
		"""Ensures that the DeltaTalk symbol dictionary is active when the synthesizer is selected."""
		try:
			current_dictionaries = config.conf["speech"].get("symbolDictionaries", [])
			if "deltatalk" not in current_dictionaries:
				new_dictionaries = current_dictionaries[:] + ["deltatalk"]
				config.conf["speech"]["symbolDictionaries"] = new_dictionaries
				log.info(_("DeltaTalk symbol dictionary automatically activated"))
			else:
				log.debug(_("DeltaTalk symbol dictionary already active"))
		except Exception as e:
			log.error(_("Error managing symbol dictionary: {error}").format(error=e))

	def _get_voice_sample_rate(self):
		"""Returns the sample rate based on the selected voice."""
		return 16000 if self._voice == "br1" else 22050

	def _setup_nvwave(self):
		"""Configures nvwave for audio playback."""
		try:
			sample_rate = self._get_voice_sample_rate()
			channels = 1
			bits_per_sample = 16
			output_device=config.conf["audio"]["outputDevice"]
			self._nvwave_player = nvwave.WavePlayer(
				channels=channels,
				samplesPerSec=sample_rate,
				bitsPerSample=bits_per_sample,
				outputDevice=output_device,
			)
			log.info(_("nvwave configured: {rate}Hz, {channels} channels, {bits} bits, device: {device}").format(
				rate=sample_rate, channels=channels, bits=bits_per_sample, device=output_device))
		except Exception as e:
			log.error(_("Error configuring nvwave: {error}").format(error=e))
			self._nvwave_player = None
			self._use_nvwave = False

	def _start_audio_thread(self):
		"""Starts the audio processing thread."""
		if self._use_nvwave and self._nvwave_player:
			self._audio_thread_running = True
			self._audio_thread = threading.Thread(target=self._audio_worker, daemon=True)
			self._audio_thread.start()
			log.debug(_("Audio thread started"))

	def _audio_worker(self):
		"""Worker thread that processes the audio queue."""
		while self._audio_thread_running:
			try:
				item = self._audio_queue.get(timeout=1.0)
				if item is None:
					break
				text, index = item  # Now accepts (text, index)
				log.debug(_("Processing text in audio worker: {text}, index: {index}").format(text=text, index=index))
				# Split long texts into smaller pieces
				if len(text) > 100:
					chunks = [text[i:i+100] for i in range(0, len(text), 100)]
					for chunk in chunks:
						self._generate_and_play_audio(chunk, index)
						index = None  # Index only for the first chunk
				else:
					self._generate_and_play_audio(text, index)
				self._audio_queue.task_done()
			except queue.Empty:
				continue
			except Exception as e:
				log.error(_("Error in audio worker: {error}").format(error=e))

	def _generate_and_play_audio(self, text, index=None):
		"""Generates audio using TTSENG_GenAudioBuffer in multi-block mode and plays via nvwave."""
		if not self.instancia or not self._nvwave_player:
			log.warning(_("Falling back to direct playback due to missing instance or nvwave player"))
			return self._speak_or_append_direct(text)
		
		with self._audio_lock:
			if self._is_speaking:
				log.debug(_("Waiting for previous synthesis to complete"))
				timeout = time.time() + 2.0
				while self._is_speaking and time.time() < timeout:
					time.sleep(0.01)
				if self._is_speaking:
					log.warning(_("Synthesis timeout, falling back to direct playback"))
					return self._speak_or_append_direct(text)
			
			self._is_speaking = True
		
		try:
			log.debug(_("Attempting to generate audio for text: {text}, index: {index}").format(text=text, index=index))
			buffer_size = 16384  # Increased for multi-blocks
			encoded_text = text.encode("ansi", errors="replace")
			log.debug(_("Starting multi-block audio generation, text length: {length}").format(length=len(encoded_text)))
			
			# Start generation with NEW_MULTI_BLOCK
			audio_buffer = (ctypes.c_byte * buffer_size)()
			bytes_written = ctypes.c_int(0)
			log.debug(_("Calling TTSENG_GenAudioBuffer with NEW_MULTI_BLOCK, buffer size: {size}").format(size=buffer_size))
			result = self.dt.TTSENG_GenAudioBuffer(
				self.instancia,
				c_char_p(encoded_text),
				TTS_GENPCM_NEW_MULTI_BLOCK,
				TTS_GENPCM_16BITS,
				audio_buffer,
				buffer_size,
				ctypes.byref(bytes_written)
			)
			log.debug(_("TTSENG_GenAudioBuffer (NEW_MULTI_BLOCK) returned: {result}, bytes written: {bytes}").format(
				result=result, bytes=bytes_written.value))
			
			if result != 0:
				log.error(_("Error starting multi-block audio: {error} ({code})").format(
					error=ERROR_CODES.get(result, {"friendly": _("Unknown error")})["friendly"], code=result))
				self._is_speaking = False
				return self._speak_or_append_direct(text)
			
			# Process initial blocks
			if bytes_written.value > 0:
# Convert c_byte to bytes handling negative values
				audio_data = bytes((b & 0xFF) for b in audio_buffer[:bytes_written.value])
				log.debug(_("Feeding initial audio data to nvwave: {bytes} bytes").format(bytes=len(audio_data)))
				self._nvwave_player.feed(audio_data, onDone=lambda: self._on_audio_done(index))
			
			# Continue with NEXT_BLOCK until complete
			while True:
				audio_buffer = (ctypes.c_byte * buffer_size)()
				bytes_written = ctypes.c_int(0)
				log.debug(_("Calling TTSENG_GenAudioBuffer with NEXT_BLOCK, buffer size: {size}").format(size=buffer_size))
				result = self.dt.TTSENG_GenAudioBuffer(
					self.instancia,
					None,
					TTS_GENPCM_NEXT_BLOCK,
					TTS_GENPCM_16BITS,
					audio_buffer,
					buffer_size,
					ctypes.byref(bytes_written)
				)
				log.debug(_("TTSENG_GenAudioBuffer (NEXT_BLOCK) returned: {result}, bytes written: {bytes}").format(
					result=result, bytes=bytes_written.value))
				
				if result == -17:  # TTS_PCM_FINISHED
					log.debug(_("PCM audio processing completed"))
					break
				elif result != 0:
					log.error(_("Error processing multi-block audio: {error} ({code})").format(
						error=ERROR_CODES.get(result, {"friendly": _("Unknown error")})["friendly"], code=result))
					self._is_speaking = False
					return self._speak_or_append_direct(text)
				
				if bytes_written.value > 0:
					audio_data = bytes((b & 0xFF) for b in audio_buffer[:bytes_written.value])
					log.debug(_("Feeding audio data to nvwave: {bytes} bytes").format(bytes=len(audio_data)))
					self._nvwave_player.feed(audio_data, onDone=lambda: self._on_audio_done(None))
				
				# Adjustable delay
				time.sleep(0.05)
			
			log.debug(_("Audio successfully fed to nvwave for text: {text}").format(text=text))
		
		except Exception as e:
			log.error(_("Exception in audio generation: {error}").format(error=e))
			self._is_speaking = False
			self._speak_or_append_direct(text)
		
		finally:
			self._is_speaking = False

	def _on_audio_done(self, index):
		"""Callback called when the audio finishes playing."""
		if index is not None:
			synthIndexReached.notify(synth=self, index=index)
		synthDoneSpeaking.notify(synth=self)

	def _speak_or_append_direct(self, text):
		"""Direct playback as fallback."""
		if not text:
			return
		with self._audio_lock:
			if self._is_speaking:
				log.debug(_("Waiting for previous direct playback to complete"))
				timeout = time.time() + 2.0
				while self._is_speaking and time.time() < timeout:
					time.sleep(0.01)
				if self._is_speaking:
					log.warning(_("Direct playback timeout, skipping"))
					return
			
			self._is_speaking = True
		
		try:
			log.debug(_("Using direct playback for text: {text}").format(text=text))
			encoded_text = text.encode("ansi", errors="replace")
			play_result = self.dt.TTSENG_PlayText(self.instancia, c_char_p(encoded_text), True)
			if play_result == -2:
				append_result = self.dt.TTSENG_AppendText(self.instancia, c_char_p(encoded_text))
				if append_result != 0:
					log.error(_("Error when attaching text: {error}").format(
						error=ERROR_CODES.get(append_result, {"friendly": _("Unknown error")})["friendly"]))
				else:
					log.debug(_("Attached text: {text}").format(text=text))
			elif play_result != 0:
				log.error(_("Error when speaking text: {error}").format(
					error=ERROR_CODES.get(play_result, {"friendly": _("Unknown error")})["friendly"]))
			else:
				log.debug(_("Spoken text: {text}").format(text=text))
		except Exception as e:
			log.error(_("Error when processing text: {error}").format(error=e))
		finally:
			self._is_speaking = False

	def _speak_or_append(self, text, index=None):
		"""Main synthesis method - chooses between nvwave or direct playback."""
		if not text:
			return
		if self._use_nvwave and self._nvwave_player and self._audio_thread_running:
			try:
				self._audio_queue.put((text, index))  # timeout=1.0
				log.debug(_("Text queued for nvwave: {text}, index: {index}").format(text=text, index=index))
			except queue.Full:
				log.warning(_("Audio queue full, using direct playback"))
				self._speak_or_append_direct(text)
		else:
			log.debug(_("Using direct playback due to nvwave not available"))
			self._speak_or_append_direct(text)

	def speak(self, speechSequence):
		if not self.instancia:
			log.error(_("Speech attempt without initialized instance."))
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

	def _apply_settings(self):
		if self.instancia:
			dt_rate = convert_nvda_to_dt(self._rate)
			dt_volume = convert_nvda_to_dt(self._volume)
			dt_pitch = convert_nvda_to_dt(self._pitch)
			result = self.dt.TTSENG_SetMode(self.instancia, dt_rate, dt_volume, dt_pitch)
			if result != 0:
				log.error(_("Error when applying settings: {error} ({code})").format(
					error=ERROR_CODES.get(result, {"friendly": _("Unknown error")})["friendly"], code=result))
			else:
				log.debug(_("Settings applied: rate={rate}, volume={volume}, pitch={pitch}").format(
					rate=dt_rate, volume=dt_volume, pitch=dt_pitch))
			if self._voice in VOICE_MAP:
				voice_id = VOICE_MAP[self._voice]
				voice_result = self.dt.TTSENG_SetVoice(self.instancia, voice_id, 10)
				if voice_result != 0:
					log.error(_("Error when applying voice: {error} ({code})").format(
						error=ERROR_CODES.get(voice_result, {"friendly": _("Unknown error")})["friendly"], code=voice_result))
				else:
					log.debug(_("Applied voice: {voice} (ID: {id})").format(voice=self._voice, id=voice_id))

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
			log.debug(_("Speed set to {rate} (converted from {original})").format(rate=dt_rate, original=value))

	def _get_pitch(self):
		return self._pitch

	def _set_pitch(self, value):
		self._pitch = value
		if self.instancia:
			dt_rate = convert_nvda_to_dt(self._rate)
			dt_volume = convert_nvda_to_dt(self._volume)
			dt_pitch = convert_nvda_to_dt(value)
			self.dt.TTSENG_SetMode(self.instancia, dt_rate, dt_volume, dt_pitch)
			log.debug(_("Pitch set to {pitch} (converted from {original})").format(pitch=dt_pitch, original=value))

	def _get_volume(self):
		return self._volume

	def _set_volume(self, value):
		self._volume = value
		if self.instancia:
			dt_rate = convert_nvda_to_dt(self._rate)
			dt_volume = convert_nvda_to_dt(value)
			dt_pitch = convert_nvda_to_dt(self._pitch)
			self.dt.TTSENG_SetMode(self.instancia, dt_rate, dt_volume, dt_pitch)
			log.debug(_("Volume set to {volume} (converted from {original})").format(volume=dt_volume, original=value))

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
					log.error(_("Error configuring voice: {error} ({code})").format(
						error=ERROR_CODES.get(result, {"friendly": _("Unknown error")})["friendly"], code=result))
				else:
					log.info(_("Voice changed to {voice}").format(voice=VOICES[value]))
					self._reconfigure_nvwave_if_needed()

	@property
	def availableVoices(self):
		return {key: VoiceInfo(id=key, displayName=VOICES[key]) for key in VOICES}

	def _reconfigure_nvwave_if_needed(self):
		"""Reconfigures nvwave if settings change (e.g., voice change)."""
		if self._use_nvwave and self._nvwave_player:
			current_rate = self._get_voice_sample_rate()
			if hasattr(self._nvwave_player, 'samplesPerSec') and self._nvwave_player.samplesPerSec != current_rate:
				log.info(_("Reconfiguring nvwave for new sample rate: {rate}Hz").format(rate=current_rate))
				try:
					self._nvwave_player.close()
				except:
					pass
				self._setup_nvwave()

	def pause(self, switch):
		"""Pauses/resumes playback in both modes."""
		if self.instancia:
			if switch:
				self.dt.TTSENG_PauseText(self.instancia)
				log.debug(_("Text paused"))
			else:
				self.dt.TTSENG_ResumeText(self.instancia)
				log.debug(_("Text resumed"))
		if self._nvwave_player:
			try:
				self._nvwave_player.pause(switch)
				log.debug(_("nvwave paused") if switch else _("nvwave resumed"))
			except Exception as e:
				log.debug(_("Error pausing/resuming nvwave: {error}").format(error=e))

	def cancel(self):
		"""Cancels playback in both modes."""
		if self.instancia:
			self.dt.TTSENG_StopText(self.instancia)
			log.debug(_("Text stopped"))
		if self._nvwave_player:
			try:
				self._nvwave_player.stop()
				log.debug(_("nvwave stopped"))
			except Exception as e:
				log.debug(_("Error stopping nvwave: {error}").format(error=e))
		with self._audio_lock:
			self._is_speaking = False
			while not self._audio_queue.empty():
				try:
					self._audio_queue.get_nowait()
					self._audio_queue.task_done()
				except queue.Empty:
					break

def terminate(self):
	"""Cleans up all resources including nvwave and audio thread."""
	self._audio_thread_running = False
	try:
		self._audio_queue.put(None, timeout=0.5)
	except queue.Full:
		pass
	if self._audio_thread and self._audio_thread.is_alive():
		self._audio_thread.join(timeout=2.0)
		if self._audio_thread.is_alive():
			log.warning(_("Audio thread did not terminate gracefully"))
	if self._nvwave_player:
		try:
			self._nvwave_player.close()
			self._nvwave_player = None
			log.debug(_("nvwave player closed"))
		except Exception as e:
			log.error(_("Error closing nvwave player: {error}").format(error=e))
	if self.instancia:
		try:
			self.dt.TTSENG_StopText(self.instancia)
			result = self.dt.TTSENG_Close(self.instancia)
			if result != 0:
				log.error(_("Error when closing: {error} ({code})").format(
					error=ERROR_CODES.get(result, {"friendly": _("Unknown error")})["friendly"], code=result))
			else:
				log.debug(_("DeltaTalk synthesizer successfully closed"))
		except Exception as e:
			log.error(_("Error closing the synthesizer: {error}").format(error=e))
		finally:
			self.instancia = None
			self.dt = None