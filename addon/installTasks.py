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
import hashlib
import tempfile
import addonHandler
from logHandler import log
from systemUtils import execElevated
import glob
from globalVars import appDir
import ctypes
import shutil

# Initialize translation support
addonHandler.initTranslation()

def _calculate_file_hash(file_path):
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

def _copyWithBatchFile(source_dir, target_dir, files_to_copy):
	"""Copy specified files with a batch file executed with elevation."""
	if not files_to_copy:
		return True

	batch_content = "@echo off\n"
	batch_content += f'echo Copying DeltaTalk files from "{source_dir}" to "{target_dir}"\n'

	try:
		for item in files_to_copy:
			source_file = os.path.join(source_dir, item)
			target_file = os.path.join(target_dir, item)
			if os.path.isfile(source_file):
				batch_content += f'xcopy /Y "{source_file}" "{target_file}*"\n'

		batch_content += "echo Copy operation completed.\n"

		with tempfile.NamedTemporaryFile(delete=False, suffix=".bat", mode="w", encoding="utf-8") as batch_file:
			batch_file.write(batch_content)
			batch_path = batch_file.name

		try:
			log.info(_("Executing batch file with elevation: {path}").format(path=batch_path))
			result = execElevated("cmd.exe", ["/c", batch_path], wait=True)
			if result == 0:
				log.info(_("Batch file executed successfully"))
				return True
			log.error(_("Batch file execution failed with code: {code}").format(code=result))
			return False
		finally:
			try:
				os.remove(batch_path)
			except Exception as e:
				log.warning(_("Failed to delete temporary batch file: {error}").format(error=e))
	except Exception as e:
		log.error(_("Error creating/executing batch file: {error}").format(error=e))
		return False

def copyDeltaTalkFilesElevated(source_dir, target_dir, files_to_copy):
	"""Copy DeltaTalk files with elevated permissions."""
	if ctypes.windll.shell32.IsUserAnAdmin():
		try:
			for item in files_to_copy:
				source_file = os.path.join(source_dir, item)
				target_file = os.path.join(target_dir, item)
				if os.path.isfile(source_file):
					log.info(_("Copying {source} to {target}").format(source=source_file, target=target_file))
					shutil.copy2(source_file, target_file)
			log.info(_("Successfully copied {count} files").format(count=len(files_to_copy)))
			return True
		except Exception as e:
			log.error(_("Error during elevated copy operation: {error}").format(error=e))
			return False
	else:
		return _copyWithBatchFile(source_dir, target_dir, files_to_copy)

def copy_files_normal(source_dir, target_dir, files_to_copy):
	"""Copy files without elevation (fallback method)."""
	try:
		files_copied = 0
		for item in files_to_copy:
			source_file = os.path.join(source_dir, item)
			target_file = os.path.join(target_dir, item)
			if os.path.isfile(source_file):
				log.info(_("Copying {source} to {target}").format(source=source_file, target=target_file))
				shutil.copy2(source_file, target_file)
				files_copied += 1
		log.info(_("Successfully copied {count} files without elevation").format(count=files_copied))
		return True
	except Exception as e:
		log.error(_("Error during normal copy operation: {error}").format(error=e))
		return False

def onInstall():
	try:
		# Path to the add-on's data files
		addon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "synthDrivers", "deltatalk")
		# Target path is the NVDA root directory
		target_path = appDir

		# List of required files (same as in deltatalk.py)
		required_files = [
			"br1.dsp", "br2.dsp", "br3.dsp", "brazil.alp", "brazil.des",
			"brazil.f0", "brazil.rul", "brazilf0.HHS", "brport.lng",
			"Dtalk32T.dll", "DTDsp32T.dll", "prosody.dll", "serial.dll"
		]

		log.debug(_("DeltaTalk installation started"))
		log.debug(_("Source path: {path}").format(path=addon_path))
		log.debug(_("Target path: {path}").format(path=target_path))

		# Verify source directory exists
		if not os.path.exists(addon_path):
			error_msg = _("Source directory not found: {path}").format(path=addon_path)
			log.error(error_msg)
			gui.messageBox(
				error_msg,
				_("Installation Error"),
				wx.OK | wx.ICON_ERROR,
				gui.mainFrame
			)
			raise Exception(error_msg)

		# Check dictionary file (brport.lng) for updates
		dictionary_file = "brport.lng"
		dictionary_needs_update = False
		files_to_copy = []
		missing_core_files = []  # NEW: Track missing core files

		source_dict = os.path.join(addon_path, dictionary_file)
		target_dict = os.path.join(target_path, dictionary_file)

		if os.path.isfile(source_dict):
			if not os.path.isfile(target_dict):
				dictionary_needs_update = True
				files_to_copy.append(dictionary_file)
				log.info(_("Dictionary file {file} missing in target. Will be copied.").format(file=dictionary_file))
			else:
				source_hash = _calculate_file_hash(source_dict)
				target_hash = _calculate_file_hash(target_dict)
				if source_hash != target_hash:
					dictionary_needs_update = True
					files_to_copy.append(dictionary_file)
					log.info(_("Dictionary file {file} has changed. Will be copied.").format(file=dictionary_file))
				else:
					log.debug(_("Dictionary file {file} is up to date.").format(file=dictionary_file))
		else:
			log.warning(_("Dictionary file {file} not found in add-on. Skipping.").format(file=dictionary_file))

		# Check other required files (only if missing)
		for item in required_files:
			if item == dictionary_file:
				continue  # Already checked
			source_file = os.path.join(addon_path, item)
			target_file = os.path.join(target_path, item)
			if not os.path.isfile(source_file):
				log.warning(_("Source file not found in add-on: {file}. Skipping.").format(file=item))
				continue
			if not os.path.isfile(target_file):
				files_to_copy.append(item)
				missing_core_files.append(item)  # NEW: Track as core file
				log.info(_("File missing in target: {file}. Will be copied.").format(file=item))

		if not files_to_copy:
			log.debug(_("No files need to be copied to {path}").format(path=target_path))
			gui.messageBox(
				_("All DeltaTalk files, including the pronunciation dictionary ({dict}), are already present and up to date in the NVDA program directory ({path}).\n\n"
				  "Installation will proceed without copying new files."
				).format(
					path=target_path,
					dict=dictionary_file
				),
				_("Installation Information"),
				wx.OK | wx.ICON_INFORMATION,
				gui.mainFrame
			)
			return

		# Check if elevation is needed
		need_elevation = not test_write_permission(target_path)
		log.info(_("Elevation needed: {status}").format(status=need_elevation))

		# NEW: Determine installation type and show appropriate message
		is_fresh_install = len(missing_core_files) > 0
		is_dictionary_only_update = dictionary_needs_update and len(missing_core_files) == 0

		# Confirmation message based on installation type
		if is_fresh_install:
			# Fresh installation or reinstallation after uninstall
			message = _(
				"This add-on requires copying DeltaTalk files to the NVDA program directory ({path}).\n\n"
				"{uac_message}\n\n"
				"If the files are not copied, the DeltaTalk synthesizer may not work.\n\n"
				"Do you want to proceed with the installation?"
			).format(
				path=target_path,
				uac_message=_("Administrator permission (UAC) will be required.") if need_elevation else ""
			)
			dialog_title = _("Installation Confirmation")
		elif is_dictionary_only_update:
			# Dictionary update only
			message = _(
				"This version includes an updated DeltaTalk pronunciation dictionary ({dict}).\n\n"
				"The updated dictionary needs to be copied to the NVDA program directory ({path}).\n\n"
				"{uac_message}\n\n"
				"Do you want to copy the updated dictionary now? If not, the synthesizer will work, but pronunciation corrections will not be applied."
			).format(
				path=target_path,
				dict=dictionary_file,
				uac_message=_("Administrator permission (UAC) will be required.") if need_elevation else ""
			)
			dialog_title = _("Dictionary Update Confirmation")
		else:
			# Mixed scenario (shouldn't happen, but fallback)
			message = _(
				"This add-on needs to copy/update DeltaTalk files to the NVDA program directory ({path}).\n\n"
				"{uac_message}\n\n"
				"Do you want to proceed?"
			).format(
				path=target_path,
				uac_message=_("Administrator permission (UAC) will be required.") if need_elevation else ""
			)
			dialog_title = _("Installation Confirmation")

		result = gui.messageBox(
			message,
			dialog_title,
			wx.YES_NO | wx.ICON_QUESTION,
			gui.mainFrame
		)

		if result != wx.YES:
			log.info(_("Installation canceled by user during file copy confirmation"))
			gui.messageBox(
				_("The copy of the files has been canceled. The synthesizer will try to copy the files before it is loaded for the first time.\n\n"
				  "If this fails, the synthesizer may not work correctly. To avoid issues, you can reinstall the add-on and allow the file copy or manually copy the files from the add-on directory (synthDrivers/deltatalk) to the NVDA program folder ({path}).").format(path=target_path),
				_("File Copy Canceled"),
				wx.OK | wx.ICON_INFORMATION,
				gui.mainFrame
			)
			return

		# Perform the copy operation
		success = False

		if need_elevation:
			log.info(_("Attempting to copy files with elevated permissions"))
			success = copyDeltaTalkFilesElevated(addon_path, target_path, files_to_copy)
		else:
			log.info(_("Copying files with normal permissions"))
			success = copy_files_normal(addon_path, target_path, files_to_copy)

		if success:
			log.info(_("DeltaTalk files successfully copied/updated to {path}").format(path=target_path))
			
			# Show appropriate success message
			if is_fresh_install:
				gui.messageBox(
					_("DeltaTalk files successfully copied to:\n{path}\n\n"
					  "The DeltaTalk synthesizer is now ready to use.\n\n"
					  "You can now select MicroPower DeltaTalk TTS as your synthesizer in NVDA settings.\n\n"
					  "Note: These files will be automatically removed if you uninstall this add-on.").format(path=target_path),
					_("Installation Completed"),
					wx.OK | wx.ICON_INFORMATION,
					gui.mainFrame
				)
			elif is_dictionary_only_update:
				gui.messageBox(
					_("The DeltaTalk pronunciation dictionary ({dict}) was successfully updated in:\n{path}\n\n"
					  "The synthesizer is now ready to use with the latest pronunciation corrections."
					).format(
						path=target_path,
						dict=dictionary_file
					),
					_("Dictionary Update Completed"),
					wx.OK | wx.ICON_INFORMATION,
					gui.mainFrame
				)
		else:
			log.warning(_("Failed to copy/update DeltaTalk files."))
			gui.messageBox(
				_("Failed to copy or update some DeltaTalk files to:\n{path}\n\n"
				  "The synthesizer will try to copy these files before it is loaded for the first time. If this fails, you may need to:\n"
				  "1. Run NVDA as administrator and reinstall the add-on, or\n"
				  "2. Manually copy the files from the add-on directory (synthDrivers/deltatalk) to the NVDA program folder.\n\n"
				  "Please check the NVDA log for more details.").format(path=target_path),
				_("Installation Warning"),
				wx.OK | wx.ICON_WARNING,
				gui.mainFrame
			)

	except Exception as e:
		log.error(_("Error during DeltaTalk add-on installation: {error}").format(error=e))
		gui.messageBox(
			_("Error during installation: {error}\n\n"
			  "Please check the NVDA log for more details.").format(error=str(e)),
			_("Installation Error"),
			wx.OK | wx.ICON_ERROR,
			gui.mainFrame
		)
		raise

def _removeWithBatchFile(target_dir, files_to_remove):
	"""Remove specified files with a batch file executed with elevation."""
	if not files_to_remove:
		return True

	batch_content = "@echo off\n"
	batch_content += f'echo Removing DeltaTalk files from "{target_dir}"\n'

	try:
		for file_name in files_to_remove:
			file_path = os.path.join(target_dir, file_name)
			batch_content += f'if exist "{file_path}" (\n'
			batch_content += f'    erase /F /Q "{file_path}"\n'
			batch_content += f'    echo Removed: {file_name}\n'
			batch_content += f') else (\n'
			batch_content += f'    echo File not found: {file_name}\n'
			batch_content += f')\n'

		batch_content += "echo DeltaTalk file removal completed.\n"

		with tempfile.NamedTemporaryFile(delete=False, suffix=".bat", mode="w", encoding="utf-8") as batch_file:
			batch_file.write(batch_content)
			batch_path = batch_file.name

		try:
			log.info(_("Executing removal batch file with elevation: {path}").format(path=batch_path))
			# Use a different approach for uninstallation - execute without waiting
			result = execElevated("cmd.exe", ["/c", batch_path], wait=False)
			# Since we can't wait during uninstall, assume success if no immediate error
			log.info(_("Removal batch file executed"))
			return True
		except Exception as e:
			log.error(_("Failed to execute elevated removal batch: {error}").format(error=e))
			return False
		finally:
			# Clean up batch file after a delay (since we can't wait)
			try:
				import threading
				def cleanup_batch():
					import time
					time.sleep(5)  # Wait 5 seconds before cleanup
					try:
						if os.path.exists(batch_path):
							os.remove(batch_path)
					except:
						pass
				thread = threading.Thread(target=cleanup_batch)
				thread.daemon = True
				thread.start()
			except Exception as e:
				log.warning(_("Failed to schedule batch file cleanup: {error}").format(error=e))
	except Exception as e:
		log.error(_("Error creating/executing removal batch file: {error}").format(error=e))
		return False

def _removeDeltaTalkFilesElevated(target_dir, files_to_remove):
	"""Remove DeltaTalk files with elevated permissions if needed."""
	if ctypes.windll.shell32.IsUserAnAdmin():
		# Already running as admin, remove directly
		try:
			removed_count = 0
			for file_name in files_to_remove:
				file_path = os.path.join(target_dir, file_name)
				if os.path.isfile(file_path):
					os.remove(file_path)
					log.info(_("Removed file: {file}").format(file=file_path))
					removed_count += 1
			log.info(_("Successfully removed {count} files with admin privileges").format(count=removed_count))
			return True, removed_count
		except Exception as e:
			log.error(_("Error during elevated removal operation: {error}").format(error=e))
			return False, 0
	else:
		# Try batch file method for elevation
		success = _removeWithBatchFile(target_dir, files_to_remove)
		if success:
			# We can't know exact count since batch runs async
			return True, len(files_to_remove)
		return False, 0

def _remove_files_normal(target_dir, files_to_remove):
	"""Remove files without elevation (fallback method)."""
	try:
		removed_count = 0
		failed_files = []
		for file_name in files_to_remove:
			file_path = os.path.join(target_dir, file_name)
			try:
				if os.path.isfile(file_path):
					os.remove(file_path)
					log.info(_("Removed file: {file}").format(file=file_path))
					removed_count += 1
			except Exception as e:
				log.error(_("Failed to remove file {file}: {error}").format(file=file_path, error=e))
				failed_files.append(file_name)
		return True, removed_count, failed_files
	except Exception as e:
		log.error(_("Error during normal removal operation: {error}").format(error=e))
		return False, 0, files_to_remove

def onUninstall():
	"""Remove DeltaTalk files from NVDA directory during add-on uninstallation."""
	try:
		import glob
		
		# Use appDir (same as in onInstall)
		target_path = appDir
		
		# List of DeltaTalk file patterns to remove
		deltatalk_patterns = [
			"br*.dsp",
			"brazil*.*",
			"brport.lng", 
			"Dtalk32T.dll",
			"DTDsp32T.dll",
			"prosody.dll",
			"serial.dll"
		]
		
		log.debug(_("DeltaTalk uninstallation started"))
		log.debug(_("Target path: {path}").format(path=target_path))
		
		# Find all DeltaTalk files that exist
		files_to_remove = []
		for pattern in deltatalk_patterns:
			if '*' in pattern or '?' in pattern:
				# Use glob for wildcard patterns
				matching_files = glob.glob(os.path.join(target_path, pattern))
				for file_path in matching_files:
					if os.path.isfile(file_path):
						files_to_remove.append(os.path.basename(file_path))
			else:
				# Direct file check
				file_path = os.path.join(target_path, pattern)
				if os.path.isfile(file_path):
					files_to_remove.append(pattern)
		
		if not files_to_remove:
			log.debug(_("No DeltaTalk files found to remove from {path}").format(path=target_path))
			return
		
		log.info(_("Found {count} DeltaTalk files to remove: {files}").format(
			count=len(files_to_remove), 
			files=", ".join(files_to_remove)
		))
		
		# Check if elevation is needed (same logic as install)
		need_elevation = not test_write_permission(target_path)
		log.info(_("Elevation needed for removal: {status}").format(status=need_elevation))
		
		# Try elevated removal first if needed
		if need_elevation:
			log.info(_("Attempting to remove files with elevated permissions"))
			success, removed_count = _removeDeltaTalkFilesElevated(target_path, files_to_remove)
			
			if success:
				log.info(_("DeltaTalk files successfully removed with elevation from {path}").format(path=target_path))
			else:
				log.warning(_("Failed to remove files with elevation, trying normal method as fallback"))
				# Fallback to normal removal
				success, removed_count, failed_files = _remove_files_normal(target_path, files_to_remove)
				if failed_files:
					log.warning(_("Some files could not be removed without elevation: {files}").format(
						files=", ".join(failed_files)
					))
					log.info(_("You may need to manually remove these files from {path}").format(path=target_path))
		else:
			# Normal removal
			log.info(_("Removing files with normal permissions"))
			success, removed_count, failed_files = _remove_files_normal(target_path, files_to_remove)
			
			if failed_files:
				log.warning(_("Failed to remove some files: {files}").format(
					files=", ".join(failed_files)
				))
		
		# Final log message
		if removed_count > 0:
			log.info(_("DeltaTalk uninstallation completed. Removed {count} files from {path}").format(
				count=removed_count,
				path=target_path
			))
		else:
			log.warning(_("No DeltaTalk files were removed. Check permissions or remove manually from {path}").format(
				path=target_path
			))
	
	except Exception as e:
		log.error(_("Error during DeltaTalk add-on uninstallation: {error}").format(error=e))
		# Don't re-raise exception to avoid blocking NVDA shutdown