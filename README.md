# Installation über PyOxidizer
https://gregoryszorc.com/docs/pyoxidizer/main/pyoxidizer_overview.html

# todo
- add cli for jg gremlin
- config handling
  - neuen Standard in config speichern
  - laden und schreiben
# Cave
in 32bit weil JG 32 bit läuft


## Nuitka
python -m nuitka --onefile --enable-plugin=tk-inter --windows-disable-console .\joy_switcher\js_gui.py