![notification](screenshots/example1.jpg)


# cmus_notify
cmus_notify is a python script which sends a notification on song change using notify-send.


# Installation

### Requirements

- pylast
- stagger

### Instructions

```bash
mkdir -p ~/.config/cmus/scripts
cd ~/.config/cmus/scripts
git clone git@github.com:wdog/cmus_notify.git
cd cmus_notify
pip install -r requirements.txt
chmod +x songChange.py
chmod +x run.sh
# optional step for LastFM
cp secret.example.json secret.json
```

Fill the file `secret.json` with your LastFM api key, secret, username and
password

Once you have requirements installed, just add this line to your `~/.config/cmus/rc`.

```
set status_display_program=~/.config/cmus/scripts/cmus_notify/run.sh

```

# Help

change options on `run.sh` script file

```
usage: songChange.py [-h] [-l] [-s]

optional arguments:
  -h, --help       show this help message and exit
  -l, --lastFm     Enable LastFm cover
  -s, --scrobbing  Enable LastFm scrobbing
```


