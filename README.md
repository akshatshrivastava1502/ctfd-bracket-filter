# CTFd Bracket Filter Plugin

This plugin filters challenges shown to users based on their bracket.

## Logic
- Users in the **Basic** bracket see challenges whose names start with `B -`.
- Users in the **Advanced** bracket see challenges whose names start with `A -`.

## Installation
1. Copy the folder into `CTFd/plugins/bracket_filter/`.
2. Restart your CTFd instance.
3. Ensure brackets named **Basic** and **Advanced** exist.
4. Prefix challenge names accordingly:
   - `B - Reverse 1`
   - `A - Web Exploit`
