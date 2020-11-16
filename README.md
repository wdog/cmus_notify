![notification](screenshots/example1.jpg)


# cmus_notify
cmus_notify is a python script which sends a notification on song change using notify-send.


# Installation

You must have stagger in your path.
You can install it using pip.

```
$ pip install --user stagger
$ mkdir -p ~/.config/cmus/scripts
$ curl -o ~/.config/cmus/scripts/songChange.py https://raw.githubusercontent.com/wdog/cmus_notify/main/songChange.py
$ chmod +x ~/.config/cmus/scripts/songChange.py

```

Once you have stagger installed, just add this line to your `~/.config/cmus/rc` or `~/.config/cmus/autosave`.

```
set status_display_program=~/.config/cmus/scripts/songChange.py

```
