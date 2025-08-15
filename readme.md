# MicroPower DeltaTalk TTS - add-on for NVDA

Authors: Patrick Barboza [patrickbarboza774@gmail.com](mailto:patrickbarboza774@gmail.com) and Wendrill Aksenow Brandão [wendrillaksenow@gmail.com](mailto:wendrillaksenow@gmail.com)

This add-on implements NVDA compatibility with the MicroPower DeltaTalk synthesizer. It includes two integrated modules, which will be described in detail below

## DeltaTalk Synthesizer

### Description

DeltaTalk is the first high-quality speech synthesizer available for the Portuguese language. It was created by the Brazilian company MicroPower Software, specifically for the Virtual Vision screen reader, in 1997.

### Features

- Supports voice, speed, pitch and volume settings.
- Supports changing the Capital pitch change percentage
- It is very lightweight and responsive
- It has better control of voice features, such as speed and pitch, compared to the Sapi 4 version.
- Reading is more accurate, without glitches, slowdowns or interruptions.

### Installation and Usage

The add-on can be downloaded and installed from the NVDA add-on store. Just search for "MicroPower DeltaTalk TTS".

After installation, go to NVDA's speech settings (NVDA+Ctrl+V), press the "Change" button, and select the MicroPower DeltaTalk TTS synthesizer.

You can also quickly access the "Select Synthesizer" dialog with the shortcut NVDA+CTRL+S.

As of version 0.4, it is no longer necessary to copy the DeltaTalk data files to the NVDA program folder. These will be loaded from the folder of the add-on itself.

Although we can't guarantee it, some of the problems reported by certain users are supposedly solved with this solution. However, some more specific problems may persist.

Because it is an old component (almost 30 years old), the synthesizer can be unstable or have problems that make it difficult or even impossible to operate on more modern computers. We recently discovered this and all we can do is ask users to be patient and avoid using it at full speed, which might alleviate these problems a little.

### Pronunciation and Symbol Dictionaries

DeltaTalk includes its own symbol dictionary, which is activated automatically when the add-on is loaded.

Due to the architecture of the NVDA screen reader, this symbol dictionary is shared with other compatible synthesizers, such as Eloquence and eSpeak.

If you only want to use the default symbol dictionary provided by NVDA, you can deactivate the "DeltaTalk Symbol Dictionary". To do this, go to the NVDA settings and, in the "Speech" category, uncheck the corresponding item in the list of extra dictionaries for character and symbol processing.

Please note that this setting will be automatically reverted if, when restarting NVDA, DeltaTalk is set as the default synthesizer (which will cause the dictionary to be reactivated).

In addition, DeltaTalk includes an internal pronunciation dictionary, which contains more than 100,000 pronunciation rules for Portuguese language words. This dictionary is included in the add-on package and is essential for the synthesizer to work. It will be updated regularly with new pronunciation rules as the add-on is updated.

### Secondary audio devices and audio ducking mode

As of version 0.3, the add-on includes initial support for audio ducking mode (Shift+NVDA+D) and secondary audio devices.

Please note that this feature is still in the experimental phase and may present problems, so it is disabled by default.

See the "Change history" section below to find out how you can activate this feature and get more information.

### Virtual Vision mode

The functionality of the "Pausing Information" add-on is now integrated into DeltaTalk as "Virtual Vision Mode".

See more about this feature in the "Virtual Vision Mode" section below.

### Configuration options

DeltaTalk now includes a category in the NVDA settings dialog that allows you to adjust some of the add-on's operating options.

Initially, only an option to enable or disable the experimental use of NVWave mode for audio playback and a button to adjust the options for the new "Virtual Vision Mode" are available. In the future, more options will be added that will allow you to adjust the reading mode and the operation of the synthesizer itself.

### Known issues

- The synthesizer is limited to 3 instances at a time. This limitation is imposed by the DeltaTalk DLL and cannot be circumvented, at least not yet.

    - If you use NVDA with a configuration profile with different voices, after the third change, the synthesizer will lock and will not load until NVDA is restarted.
    - Likewise, if you manually switch to another synthesizer and then back to DeltaTalk, it will lock after the third switch until NVDA is restarted.

- During continuous reading, the system cursor does not follow the synthesizer. Instead, it jumps straight to the end of the text.
- In some cases, the synthesizer may crash completely and remain unvoiced until NVDA is restarted.

### Future development

This add-on is an early prototype, but is already fully functional. Future versions may include:

- Unlimited synthesizer instances, allowing you to use different voice profiles and freely change the synthesizer
- Configuration options that will allow you to control the internal workings of the synthesizer

### Acknowledgements

This project was made possible thanks to the support of the artificial intelligence tools Claude, Grok and ChatGPT, which contributed at different stages of the technical and conceptual development of the add-on.

The authors would also like to thank the friends who contributed during the closed testing phase with suggestions and bug reports.

Likewise, the authors would like to thank everyone who tries this add-on from now on and ask that any bugs be reported using the contact details provided at the beginning of this document.

Last but not least, here are our deepest thanks to Denis Renato da Costa and MicroPower Software, who kindly provided us with the DeltaTalk SDK and its development APIs, without which none of this would be possible.

### Change history

#### Version 0.4.1

- This version only fixes a problem where the synthesizer couldn't be loaded because one of the main files was missing.

#### Version 0.4

- The functionality of the old "Pausing Information" add-on was integrated into DeltaTalk as a global plugin called "Virtual Vision Mode".

    - The current version is identical to the last version of the original add-on, but will be updated regularly.
    - The installTasks.py file now includes a routine that checks for the presence of the old add-on and removes it if it is installed.

- A new settings panel has been created for DeltaTalk and added to the NVDA settings dialog. This panel will be expanded with new configuration options over time.
- The add-on now works completely independently, eliminating the need to copy the DeltaTalk data files to the NVDA program folder.

    - The corresponding routines for copying and removing these files have been removed from the main code of add-on and from the installTasks.py file.
    - This should solve most of the problems reported by some users, but we cannot guarantee that they will actually be solved.

#### Version 0.3

- A logic has been implemented that checks the synthesizer's internal pronunciation dictionary (Brport.lng) and automatically copies it to the NVDA program folder if changes to the original file included in the add-on package are detected.
- An integrated symbol dictionary has been included for DeltaTalk, allowing it to interpret punctuation marks in it's own way.
- The add-on now uses "log" (imported from "logHandler") instead of "logging", for better integration with NVDA.
- Experimental support has been included for audio playback using the "nvwave" system, with audio generation in multiple blocks and asynchronous playback.

    - This activates initial support for secondary audio devices and audio ducking mode (Shift+NVDA+D).
    - This feature is still disabled by default and can be activated for testing via the new option "Use NVWave for audio playback" in the NVDA settings dialog, on the "DeltaTalk" category.

- DeltaTalk's error messages now use friendlier translations, in addition to the DLL's internal error codes.
- Routines have been implemented to remove the DeltaTalk data files from the NVDA program folder if the add-on is uninstalled. Note that administrator privileges may be required.

#### Version 0.2

- This is the first public release, with some important bug fixes.
- The routines that copy DeltaTalk data files to the NVDA program folder have been corrected so that administrative access is only requested when necessary. This eliminates the need to run NVDA as an administrator when installing the add-on.
- The "installTasks.py" file now supports internationalization to maintain consistency with the main synthesizer code.
- More log messages have been added to the main synthesizer code to make it easier to debug and identify possible problems.
- The documentation for the add-on (which was previously just an initial draft) has been rewritten and updated.
- The old codes were removed from the add-on because they didn't work and were obsolete.
- Translations into Brazilian and european Portuguese have been added for the add-on messages.

#### Version 0.1

- First private test version, with several bug fixes that prevented the synthesizer from working.
- A routine has been created that copies the DeltaTalk data files to the NVDA program folder during the installation of the add-on, which eliminates the need to keep the Sapi 4 version installed.

    - A logic has also been added that checks for the presence of these files in the NVDA program folder before loading the synthesizer, and copies them again if they are missing.
    - Note that for this to work, NVDA must be run as administrator.

- Initial support for internationalization has been added to the main synthesizer code.

## Virtual Vision Mode

### Description

Virtual Vision mode (originally "Pausing Information") is an extension that inserts pauses during the reading of control information, providing a more detailed and paused reading of control and status information when the focus switches between interface elements.

This feature was inspired by the Brazilian screen reader "Virtual Vision", known for its paused way of announcing information, improving user comprehension.

This module is integrated with DeltaTalk to guarantee a complete reading experience similar to that of Virtual Vision.

If you want to use it with other synthesizers, you can install the old "Pausing Information" add-on, which is perfectly compatible with any synthesizer being used by NVDA. Note that, for compatibility reasons, it is not recommended to keep both add-ons installed.

You should also remember that the old "Pausing Information" add-on has been discontinued and will not receive future updates, so it may lose compatibility with new versions of NVDA.

### Important note

Paused reading is based exclusively on the symbol level. Hyphens are added to pause the reading of information. If the symbol level is set to anything above "some", the hyphens will be read aloud.

Likewise, if the symbols (specifically the hyphen) are not correctly adjusted in the punctuation/symbol pronunciation dialog, the pauses may not occur.

To ensure that pauses work as expected, go to the punctuation/symbol pronunciation dialog and make sure that the hyphen is set to be sent to the synthesizer when it is below the symbol level.

### Features

- Announcement of control types and states: The extension announces the type of control (e.g. "checkbox", "Radio button", "menu", "edit box") and its status (e.g. "checked", "pressed", "unavailable", "busy").
- The announcement is made in a paused manner, similar to what was done by the Virtual Vision screen reader.

### Use

After installing the MicroPower DeltaTalk add-on for NVDA, Virtual Vision Mode works automatically, allowing a more detailed and paused reading of information about the types and states of controls, as long as the DeltaTalk synthesizer is active. No additional configuration is required.

### Configuration options

As mentioned, no additional configuration is required when using this extension. The default settings and integration with the DeltaTalk synthesizer provide a screen reading and navigation experience in Windows very similar to that of Virtual Vision.

However, various configuration options are available, allowing you to adjust the operation of the extension to your liking or needs.

To access the Virtual Vision Mode settings, open the NVDA settings dialog, go to the "DeltaTalk" category and press the "Virtual Vision Mode..." button. The following options are available:

- Enable Virtual Vision Mode: If you uncheck this option, the extension will be completely disabled and all other configuration options will be unavailable. You can also activate/deactivate Virtual Vision  Mode using the NVDA+Shift+V shortcut. This shortcut can be modified from NVDA's "Input gestures" dialog, in the "DeltaTalk" category. Note that the add-on will automatically disable Virtual Vision Mode when you switch to another synthesizer and will enable it again when you switch back to DeltaTalk.
- Allow custom translations for the names of control types and states: If this option is checked, the extension will use an internal dictionary to translate the names of the types and states of the controls. Otherwise, NVDA's internal translations will be used.
Note: For now, this option only has a major impact on Portuguese languages. In English, there are no significant differences.
- Message Extension: This group of radio buttons controls the amount of information to be spoken.
    - Short: Only essential NVDA navigation information will be spoken.
    - Medium: In addition to NVDA's essential navigation information, the extension will add some more information. For example, when an object has a shortcut key associated with it, you will hear the information "shortcut" before the shortcut key is announced. You will also hear the "value" information before announcing the value of the sliders and scroll bars.
    - Long: The extension will add another set of information in addition to the above. When you navigate through the items in a list, tree view or menus, you will hear the corresponding information according to the type of item. The extension will also warn you whenever a window is activated. This is the default setting.
    - Custom: With this option, you can individually control all the information announced by the extension.

#### Settings for the custom level

By setting the message extension level to "Custom", you can individually adjust all the information announced, for example, you can deactivate the information you don't want or don't need to be announced. You can do this via the "Configure" button. This button is only available when the custom message extension level is selected. Clicking this button opens a configuration dialog for the custom level, with the following options:

- Select the controls to be announced: In this list, you can activate or deactivate all the control types supported by Virtual Vision Mode. For deactivated controls, only the name and status (if applicable) will be announced.

- Other additional messages: This group of controls contains the following options:
    - Announce active windows: Announces whenever a window is activated.
    - Announce shortcut before object shortcut keys: When an object has an associated shortcut key, it announces the "shortcut" information before the corresponding shortcut key is announced.
    - Announce value before slider and scrollbar values: When focusing on a slider or scroll bar, it announces the "value" information before the value is announced.

### Known issues

- On web pages, paused reading only works when NVDA's focus mode is activated. Otherwise, navigating with the arrows causes the controls to be read using NVDA's native methods.
- In some cases, the announcement of states may fail or be incorrect.
    - When a checkbox is checked, unchecking it causes the "checked" state to be announced incorrectly.
    - When a toggle button is pressed or a list item is selected, deactivating the button or deselecting the item does not announce them.
    - This fault only occurs the first time you uncheck a checkbox, deactivate a toggle button or deselect a list item with the Spacebar or Control+Spacebar.
    - To be sure, you can use the NVDA+Tab shortcut to have the information repeated by NVDA. In this case, the status will be announced correctly.
- Some types of menus, such as those in Thunderbird, read a little strangelly. The informations "submenu" and "unavailable" are announced several times, even when it is not necessary. In these cases, when navigating through Thunderbird menus and other similar menus, it is recommended that Virtual Vision Mode is temporarily disabled (via the shortcut key) until a solution to this problem is found.
- In some types of dialog boxes that do not have an associated title, their content is not read automatically. In these cases, you can use NVDA's object navigation mode to explore the dialog box or have NVDA try to read it using the NVDA+Tab shortcut.
- The announcement of active windows, in certain cases, causes this information to be announced incorrectly, for example, when opening a combo box with the Alt+Down Arrow shortcut or when opening a context menu such as the one in Google Chrome.
- At certain times, occasional errors may appear in the NVDA log, but they do not interfere with operation. These errors will be corrected in the next updates.

### Change history (Pausing Information)

#### Version 1.5

- The "internal_link" status (which identifies links to the same page) has been added to the list of states to be announced.
- A few more controls have also been added to the list of control types to be announced.
- A logic has been created that checks for the presence of the old version of the add-on and removes it before installing this new version.
- Fixed an issue where Settings for the custom message extension level were lost when NVDA was restarted or when its language was changed.
- The code of the add-on has been simplified and unnecessary and repeated parts have been removed to make it easier to maintain.
- The add-on is now available in the NVDA add-ons store. Just search for "Pausing Information".
- The add-on functionality has been integrated into DeltaTalk as "Virtual Vision Mode", so this will be the last stand-alone version.

#### Version 1.4

- Fixed an error with the announcement of active windows that caused the first item not to be announced when focusing on the taskbar or switching between tasks with the Alt+Tab shortcut. This problem also affected some items in normal windows, which were ignored.

#### Version 1.3

- First official release version.
- A customized message extension level has been implemented, which allows you to individually control all the information announced by the add-on.
- A new configuration option has been created to completely disable the add-on.
- An enable/disable shortcut key has also been adedd, which is especially useful for temporarily disabling the add-on in certain cases.

#### Version 1.2

- Private test version, initially released as 1.1 and later updated to 1.2.
- A new configuration option has been created that allows you to choose whether or not the add-on should translate the names of the types and states of the controls.
- A logic of message extension levels has been implemented - long, medium and short. At the long level (default), all possible information will be spoken. At the medium level, some information will be suppressed and at the short level, only the essential information will be spoken.

#### Version 1.1

- New methods of reading control states were created to correct a problem in which certain states were not read.
- A new interface has been created for the add-on, with the first concept of configuration options.
- An error has been fixed in which the description of certain objects and the contents of some dialog boxes were not read.
- Fixed a bug where the value of progress bars was not read automatically.
- Fixed a bug where links contained in e-mail messages and web pages could not be focused correctly.
- A problem with reading Excel cells has been fixed.
- A logic has been created to check whether the read-only status is relevant, in order to avoid unnecessary announcements.

#### Version 1.0

- Completely rewritten version from the initial prototype, with several error corrections.
- A complete dictionary has been created with the names of the control types and states, with their respective translations, which will be updated as necessary.
- The documentation has been rewritten and updated.

#### Version 0.1

- Initial prototype, created with very few resources and not yet very functional.
- Creation of the initial documentation.