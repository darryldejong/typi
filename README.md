# Typi
Typi is an automated typing application built using Python's tkinter library, allowing users to type predefined messages automatically at a set interval.
(My in-game name is psz, which is why it's in the title of the GUI.)

![Readmeimage](images/GUI.png)

## Features
- Add, Edit, and Delete Sentences: Manage a list of sentences to be typed automatically.
- Custom Time Delay: Set a delay (in seconds) between typing messages.
- Hotkey Support: Stop the typing process with the F12 key.

### Overview & Usage
Overview
1. Add messages to the list using the input field or Enter key.
2. Adjust the typing delay using the spinner.
3. Start or stop the automatic typing process using the "Start Typing" button or the F12 hotkey.
4. Sentences will be typed sequentially with the specified delay.

Usage
- Adding Sentences: Type a message in the input field and press Enter to add it to the list.
- Editing Sentences: Right-click on a sentence in the list and choose "Edit" from the context menu.
- Deleting Sentences: Right-click on a sentence and select "Delete" from the context menu.

##### Clarification
The script will wait for 3 seconds after starting before typing begins, allowing you to focus on the target window.
To prevent accidental actions, the input field is disabled while typing is active.

##### License
This project is open-source and available under the MIT License.
