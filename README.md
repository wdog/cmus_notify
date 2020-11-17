![notification](screenshots/example1.jpg)


# cmus_notify
cmus_notify is a python script which sends a notification on song change using notify-send.


# Installation

You must have stagger in your path.
You can install it using pip.

```
$ mkdir -p ~/.config/cmus/script
$ git clone git@github.com:wdog/cmus_notify.git
$ cd cmus_notify
$ pip install -r requirements.txt
$ chmod +x ~/.config/cmus/scripts/cmus_notify/songChange.py

```

Once you have stagger installed, just add this line to your `~/.config/cmus/rc` or `~/.config/cmus/autosave`.

```
set status_display_program=~/.config/cmus/scripts/cmus_notify/songChange.py

```
