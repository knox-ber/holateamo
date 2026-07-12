#!/usr/bin/env python3
"""
~/.config/apply-colors.py  (chmod +x)

Fuente única de verdad: ~/.config/colors.json
Este script la traduce a los formatos nativos de cada programa:

  ~/.config/alacritty/colors.toml   (importado por alacritty.toml)
  ~/.config/polybar/colors.ini      (incluido por config.ini)
  ~/.config/cava/config             (generado completo)

Flujo: editas colors.json -> corres este script -> relanzas polybar
(alacritty recarga solo). Ranger no necesita hex: usa los 16 colores
del terminal, que Alacritty deriva de este mismo JSON.

NO edites a mano los archivos generados: se sobreescriben.
"""

import json
from pathlib import Path

CONFIG = Path.home() / ".config"
C = json.loads((CONFIG / "colors.json").read_text())

BAR_ALPHA = "E6"  # transparencia del fondo de polybar (00-FF)


def a(name: str, alpha: str = BAR_ALPHA) -> str:
    """Color con canal alfa al estilo polybar: #AARRGGBB."""
    return "#" + alpha + C[name].lstrip("#")


# ---------------------------------------------------------------
# Alacritty -> ~/.config/alacritty/colors.toml
# ---------------------------------------------------------------
alacritty = f"""# GENERADO por ~/.config/apply-colors.py — no editar a mano.
# Fuente: ~/.config/colors.json

[colors.primary]
background = "{C['Background']}"
foreground = "{C['Foreground']}"

[colors.cursor]
text = "{C['Background']}"
cursor = "{C['Foreground']}"

[colors.vi_mode_cursor]
text = "{C['Background']}"
cursor = "{C['Foreground']}"

[colors.selection]
text = "CellForeground"
background = "{C['Selection']}"

[colors.search.matches]
foreground = "CellBackground"
background = "{C['AccentPrimary']}"

[colors.footer_bar]
foreground = "{C['Background']}"
background = "{C['Foreground']}"

[colors.normal]
black   = "{C['BackgroundAlt']}"
red     = "{C['Error']}"
green   = "{C['Success']}"
yellow  = "{C['Warning']}"
blue    = "{C['AccentTertiary']}"
magenta = "{C['Media']}"
cyan    = "{C['AccentPrimary']}"
white   = "{C['ForegroundSoft']}"

[colors.bright]
black   = "{C['Selection']}"
red     = "{C['Error']}"
green   = "{C['Success']}"
yellow  = "{C['Warning']}"
blue    = "{C['AccentTertiary']}"
magenta = "{C['Media']}"
cyan    = "{C['AccentSecondary']}"
white   = "{C['ForegroundBright']}"
"""

# ---------------------------------------------------------------
# Polybar -> ~/.config/polybar/colors.ini
# ---------------------------------------------------------------
polybar = f"""; GENERADO por ~/.config/apply-colors.py — no editar a mano.
; Fuente: ~/.config/colors.json

[colors]
background        = {a('Background')}
background-solid  = {C['Background']}
background-alt    = {C['BackgroundAlt']}
surface           = {C['Surface']}
selection         = {C['Selection']}
foreground        = {C['Foreground']}
foreground-soft   = {C['ForegroundSoft']}
foreground-bright = {C['ForegroundBright']}
accent-primary    = {C['AccentPrimary']}
accent-secondary  = {C['AccentSecondary']}
accent-tertiary   = {C['AccentTertiary']}
accent-deep       = {C['AccentDeep']}
error             = {C['Error']}
orange            = {C['Orange']}
warning           = {C['Warning']}
success           = {C['Success']}
media             = {C['Media']}
"""

# ---------------------------------------------------------------
# Cava -> ~/.config/cava/config  (archivo completo)
# ---------------------------------------------------------------
cava = f"""# GENERADO por ~/.config/apply-colors.py — no editar a mano.
# Fuente: ~/.config/colors.json

[general]
framerate = 60
bars = 0
bar_width = 3
bar_spacing = 1

[input]
method = pulse
source = auto

[output]
method = ncurses

[color]
background = default
foreground = '{C['AccentSecondary']}'

[smoothing]
monstercat = 1
waves = 0
gravity = 100
"""

targets = {
    CONFIG / "alacritty" / "colors.toml": alacritty,
    CONFIG / "polybar" / "colors.ini": polybar,
    CONFIG / "cava" / "config": cava,
}

for path, content in targets.items():
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"  escrito  {path}")

print("Listo. Relanza polybar (~/.config/polybar/launch.sh); alacritty recarga solo.")
