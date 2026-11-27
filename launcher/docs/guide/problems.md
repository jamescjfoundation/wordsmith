# When something goes wrong

The launcher says what went wrong in red, under the app's name. These are the messages and what
to do.

| The message | What happened | What to do |
| --- | --- | --- |
| The newest release could not be read. | GitHub did not answer, or this computer is offline. GitHub also limits how often a computer may ask in an hour | Check the connection and choose **Check Now**. Apps that are installed still open |
| *(the app)* is running. Close it and try again. | An app is not replaced or removed while it runs | Close the app, then choose the button again |
| … is not the file the release lists … Nothing was installed. | The download's checksum is not the one in the release's list. The download was damaged on the way, or it is not the published file | Try again. If it happens twice, tell us ([getting help](https://wordsmithand.ink/wiki/start/help)) |
| The launcher did not install this copy of *(the app)*, so it leaves it alone. | The app was installed by hand, so the launcher has no record of what to remove | Remove it the way it was installed. On Linux: the `uninstall.sh` of its download |
| No release file of the Wordsmith apps is built for this system … | The apps are built for Linux and Windows on 64-bit Intel or AMD processors, and for Macs with Apple silicon | Nothing can be installed on this computer by the launcher |
| the package's install.sh failed … | The app's own install step stopped. The last lines it printed follow the message | Read them; a full disk and a folder that cannot be written are the usual causes |

## An app does not start on Linux

The apps need the C library of Ubuntu 24.04 (glibc 2.39) or a newer one. On an older system the
program is installed and does not start.

`~/.local/bin` must be on your `PATH` for the menu entry to find the program. Many systems add
it when the folder exists: log out and in again after the first install.

## macOS asks about the app

The apps are not signed with a publisher's certificate yet. If macOS does not open an app the
first time, open System Settings › Privacy & Security, find the line about the app and choose
Open Anyway.

## Starting over

The launcher's own folder holds its preferences and its records
([Installing and updating the launcher](installing.md#where-the-launcher-keeps-its-own-files)).
Deleting it resets the launcher. It removes no app; an app the launcher installed is then
treated as one you installed yourself.
