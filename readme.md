# DeltaTalk TTS add-on for NVDA#

Authors: Patrick Barboza <patrickbarboza774@gmail.com> and Wendrill Aksenow Brandão <wendrillaksenow@gmail.com>

## Description

DeltaTalk is the first high-quality speech synthesizer available for the Portuguese language. It was created by the Brazilian company MicroPower Software, specifically for the Virtual Vision screen reader, in 1997.

This add-on is a prototype still in its early stages, which implements NVDA compatibility with this synthesizer.

## Features

- Supports voice, speed, pitch and volume settings.

- Supports changing the Capital pitch change percentage

- It is very lightweight and responsive

- It has better control of voice features, such as speed and pitch, compared to the Sapi 4 version.

- Reading is more accurate, without glitches, slowdowns or interruptions.

## Installation and Usage

To install the add-on, double-click the "deltaTalk-0.1.nvda-addon" file.

During installation, the add-on will attempt to copy the DeltaTalk files to the NVDA program folder and may ask for administrator access if you are using an installed copy of NVDA.

If this is not possible, or if you choose not to copy the files during installation, the add-on will attempt to copy them before loading the synthesizer for the first time, and may ask for administrator access again.

If the copy fails, the synthesizer will not work correctly and will attempt to copy the files again the next time it is loaded.

After installation, go to NVDA's voice settings (NVDA + Ctrl + V), press the "Change" button, and select the MicroPower DeltaTalk TTS synthesizer.

You can also quickly access the "Select Synthesizer" dialog with the shortcut NVDA+CTRL+S.

## Known issues

- The synthesizer is limited to 3 instances at a time. If you use NVDA with a configuration profile with different voices, after the third change the synthesizer will lock and will not load until NVDA is restarted.

- Similarly, if you manually switch to another synthesizer and then switch back to DeltaTalk, it will lock after the third change until NVDA is restarted.

- The ability to lower the volume of other sounds while NVDA is speaking (NVDA + CTRL + D) is currently not supported unless it is set to "Always lower".

- Using a secondary audio device is also not supported unless it is set as the default audio device.

- During continuous reading, the system cursor does not follow the synthesizer. Instead, it jumps straight to the end of the text.

- In some cases, the synthesizer may crash completely and remain unvoiced until NVDA is restarted.

## Future development

This add-on is an early prototype, but is already fully functional. Future versions may include:

- Standalone operation, without the need to copy DeltaTalk voice files to the NVDA program folder

- Dedicated configuration interface in NVDA, with various options to customize the synthesizer reading

- Unlimited synthesizer instances, allowing you to use different voice profiles and freely change the synthesizer

- Integration of the "Pausing Information" add-on functionality, providing a more detailed and paused reading of control and state information when the focus changes.

## Acknowledgements

This project was made possible thanks to the support of the artificial intelligence tools Claude, Grok and ChatGPT, which contributed at different stages of the technical and conceptual development of the add-on.

The authors would also like to thank the friends who contributed during the closed testing phase with suggestions and bug reports.

Likewise, the authors would like to thank everyone who tries this add-on from now on and ask that any bugs be reported using the contact details provided at the beginning of this document.

## Change history

### Version 0.2

- This is the first public release, with some important bug fixes.

- The routines that copy DeltaTalk data files to the NVDA program folder have been corrected so that administrative access is only requested when necessary. This eliminates the need to run NVDA as an administrator when installing the add-on.

- The "installTasks.py" file now supports internationalization to maintain consistency with the main synthesizer code.

- More log messages have been added to the main synthesizer code to make it easier to debug and identify possible problems.

- The documentation for the add-on (which was previously just an initial draft) has been rewritten and updated.

- The old codes were removed from the add-on because they didn't work and were obsolete.

- Translations into Brazilian and european Portuguese have been added for the add-on messages.

### Version 0.1

- First private test version, with several bug fixes that prevented the synthesizer from working.

- A routine has been created that copies the DeltaTalk data files to the NVDA program folder during the installation of the add-on, which eliminates the need to keep the Sapi 4 version installed.

    - A logic has also been added that checks for the presence of these files in the NVDA program folder before loading the synthesizer, and copies them again if they are missing.

    - Note that for this to work, NVDA must be run as administrator.

- Initial support for internationalization has been added to the main synthesizer code.