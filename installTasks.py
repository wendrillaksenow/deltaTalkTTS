# -*- coding: UTF-8 -*-
# installTasks.py
#A part of the deltaTalkTTS driver for NVDA (Non Visual Desktop Access)
#Copyright (C) 1997-2001 Denis R. Costa <denis@micropowerglobal.com> & MicroPower Software <www.micropower.ai>
#Copyright (C) 2024-2025 Patrick Barboza <patrickbarboza774@gmail.com> & Wendrill Aksenow Brandão <wendrillaksenow@gmail.com>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import gui
import wx
import addonHandler
import shutil
import ctypes
from logHandler import log
from systemUtils import execElevated
from globalVars import appDir
import sys

# Initialize translation support
addonHandler.initTranslation()

# Path to NVDA's slave executable (used for elevated operations)
SLAVE_FILENAME = os.path.join(appDir, "nvda_slave.exe")

def _copyDeltaTalkFiles(source_dir, target_dir):
    """
    Internal function to copy DeltaTalk files.
    This function will be called by the elevated process.
    """
    try:
        log.info(f"Starting elevated copy operation from {source_dir} to {target_dir}")
        
        if not os.path.exists(source_dir):
            log.error(f"Source directory not found: {source_dir}")
            return False
            
        if not os.path.exists(target_dir):
            log.error(f"Target directory not found: {target_dir}")
            return False
        
        # Copy each file from source to target
        files_copied = 0
        for item in os.listdir(source_dir):
            source_file = os.path.join(source_dir, item)
            target_file = os.path.join(target_dir, item)
            
            if os.path.isfile(source_file):
                log.info(f"Copying {source_file} to {target_file}")
                try:
                    shutil.copy2(source_file, target_file)
                    files_copied += 1
                    log.info(f"Successfully copied {item}")
                except Exception as e:
                    log.error(f"Failed to copy {item}: {e}")
                    return False
        
        log.info(f"Successfully copied {files_copied} files")
        return True
        
    except Exception as e:
        log.error(f"Error during elevated copy operation: {e}")
        return False

def copyDeltaTalkFilesElevated(source_dir, target_dir):
    """
    Copy DeltaTalk files with elevated permissions using NVDA's slave system.
    """
    if ctypes.windll.shell32.IsUserAnAdmin():
        # Already running as admin, copy directly
        return _copyDeltaTalkFiles(source_dir, target_dir)
    else:
        # Need elevation, use NVDA's slave system
        try:
            # Check if slave executable exists
            if not os.path.exists(SLAVE_FILENAME):
                log.error(f"NVDA slave executable not found: {SLAVE_FILENAME}")
                return False
            
            log.info("Requesting elevated permissions for file copy operation")
            
            # Use execElevated with NVDA's slave system
            # Note: This approach might not work directly as the slave might not know about our function
            # We'll need to try a different approach
            
            # Alternative: Use a simpler approach with a batch file
            return _copyWithBatchFile(source_dir, target_dir)
            
        except Exception as e:
            log.error(f"Error during elevated copy request: {e}")
            return False

def _copyWithBatchFile(source_dir, target_dir):
    """
    Alternative approach: Create a batch file and execute it with elevation.
    """
    import tempfile
    
    batch_content = "@echo off\n"
    batch_content += f'echo Copying DeltaTalk files from "{source_dir}" to "{target_dir}"\n'
    
    # Add copy commands for each file
    try:
        for item in os.listdir(source_dir):
            source_file = os.path.join(source_dir, item)
            target_file = os.path.join(target_dir, item)
            
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
            log.info(f"Executing batch file with elevation: {batch_path}")
            result = execElevated("cmd.exe", ["/c", batch_path], wait=True)
            
            if result == 0:
                log.info("Batch file executed successfully")
                return True
            else:
                log.error(f"Batch file execution failed with code: {result}")
                return False
                
        finally:
            # Clean up batch file
            try:
                os.remove(batch_path)
            except Exception as e:
                log.warning(f"Failed to delete temporary batch file: {e}")
        
    except Exception as e:
        log.error(f"Error creating/executing batch file: {e}")
        return False

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

def copy_files_normal(source_dir, target_dir):
    """Copy files without elevation (fallback method)."""
    try:
        files_copied = 0
        for item in os.listdir(source_dir):
            source_file = os.path.join(source_dir, item)
            target_file = os.path.join(target_dir, item)
            
            if os.path.isfile(source_file):
                log.info(f"Copying {source_file} to {target_file}")
                shutil.copy2(source_file, target_file)
                files_copied += 1
        
        log.info(f"Successfully copied {files_copied} files without elevation")
        return True
    except Exception as e:
        log.error(f"Error during normal copy operation: {e}")
        return False

def onInstall():
    try:
        # Path to the add-on's data files
        addon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "synthDrivers", "deltatalk")
        # Target path is the NVDA root directory
        target_path = appDir

        log.info(f"DeltaTalk installation starting")
        log.info(f"Source path: {addon_path}")
        log.info(f"Target path: {target_path}")

        # Verify source directory exists
        if not os.path.exists(addon_path):
            error_msg = f"Source directory not found: {addon_path}"
            log.error(error_msg)
            gui.messageBox(
                _("Error: Source directory not found:\n{addon_path}").format(addon_path=addon_path),
                _("Installation Error"),
                wx.OK | wx.ICON_ERROR,
                gui.mainFrame
            )
            raise Exception(error_msg)

        # Get list of source files
        source_files = [item for item in os.listdir(addon_path) if os.path.isfile(os.path.join(addon_path, item))]
        
        if not source_files:
            log.warning("No files found in source directory")
            gui.messageBox(
                _("No DeltaTalk files found in the add-on package."),
                _("Installation Warning"),
                wx.OK | wx.ICON_WARNING,
                gui.mainFrame
            )
            return

        # Check if all files already exist in the target directory
        if all(os.path.exists(os.path.join(target_path, item)) for item in source_files):
            log.info(f"DeltaTalk files already exist in {target_path}")
            gui.messageBox(
                _("The DeltaTalk files are already present in the target directory ({target_path}). "
                  "Installation will proceed without copying new files.").format(target_path=target_path),
                _("Information"),
                wx.OK | wx.ICON_INFORMATION,
                gui.mainFrame
            )
            return

        # Check if we need elevation
        need_elevation = not test_write_permission(target_path)
        
        log.info(f"Elevation needed: {need_elevation}")
        
        # Confirmation message
        if need_elevation:
            message = _(
                "This add-on requires copying DeltaTalk files to the NVDA program directory ({target_path}).\n\n"
                "Administrator permission (UAC) will be required to complete this operation.\n\n"
                "If the files are not copied, the DeltaTalk synthesizer may not work.\n\n"
                "Do you want to proceed with the installation?"
            ).format(target_path=target_path)
        else:
            message = _(
                "This add-on requires copying DeltaTalk files to the NVDA program directory({target_path}).\n\n"
                "If the files are not copied, the DeltaTalk synthesizer may not work.\n\n"
                "Do you want to proceed with the installation?"
            ).format(target_path=target_path)

        result = gui.messageBox(
            message,
            _("Installation Confirmation"),
            wx.YES_NO | wx.ICON_QUESTION,
            gui.mainFrame
        )

        if result != wx.YES:
            log.info("File copy canceled by user")
            gui.messageBox(
                _("The copy of the files has been canceled. The synthesizer will try to copy the files before it is loaded for the first time.\n\n"
                "If this fails, the synthesizer may not work correctly."),
                _("File copy canceled"),
                wx.OK | wx.ICON_INFORMATION,
                gui.mainFrame
            )
            return  # Don't raise exception, just return

        # Perform the copy operation
        success = False
        
        if need_elevation:
            log.info("Attempting to copy files with elevated permissions")
            success = copyDeltaTalkFilesElevated(addon_path, target_path)
        else:
            log.info("Copying files with normal permissions")
            success = copy_files_normal(addon_path, target_path)

        if success:
            log.info(f"DeltaTalk files successfully copied to {target_path}")
            gui.messageBox(
                _("DeltaTalk files successfully copied to:\n{target_path}\n\n"
                  "The DeltaTalk synthesizer is now ready to use.\n\n"
                  "You can now select MicroPower DeltaTalk TTS as your synthesizer in NVDA settings.").format(target_path=target_path),
                _("Installation Completed"),
                wx.OK | wx.ICON_INFORMATION,
                gui.mainFrame
            )
        else:
            log.warning("Failed to copy DeltaTalk files")
            gui.messageBox(
                _("Failed to copy DeltaTalk files to the target directory.\n\n"
                  "The synthesizer will try to copy the files before it is loaded for the first time. If this fails, you may need to:\n"
                  "1. Run NVDA as administrator and reinstall the add-on, or\n"
                  "2. Manually copy the files from the add-on directory to the NVDA program folder.\n\n"
                  "Please check the NVDA log for more details."),
                _("Installation Warning"),
                wx.OK | wx.ICON_WARNING,
                gui.mainFrame
            )
            # Don't raise exception to allow installation to continue

    except Exception as e:
        log.error(f"Error during DeltaTalk add-on installation: {e}")
        gui.messageBox(
            _("Error during installation: {error}\n\n"
              "Please check the NVDA log for more details.").format(error=str(e)),
            _("Installation Error"),
            wx.OK | wx.ICON_ERROR,
            gui.mainFrame
        )
        # Re-raise to prevent installation
        raise