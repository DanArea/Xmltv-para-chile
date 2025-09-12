import re
import html
from datetime import datetime, timedelta

# Ruta a tu archivo M3U
M3U_FILE = "index.m3u"
XMLTV_FILE = "dummy.XMLTV"

def parse_m3u(m3u_file):
    channels = []
    with open(m3u_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith("#EXTINF"):
            tvg_id = re.search(r'tvg-id="([^"]*)"', line)
            tvg_logo = re.search(r'tvg-logo="([^"]*)"', line)
            group_title = re.search(r'group-title="([^"]*)"', line)
            name = line.split(",")[-1].strip()

            channel_info = {
                "id": tvg_id.group(1) if tvg_id else name.replace(" ", "_"),
                "name": name,
                "logo": tvg_logo.group(1) if tvg_logo else "",
                "group": group_title.group(1) if group_title else ""
            }
            channels.append(channel_info)
    return channels

def sanitize_display_name(name):
    # Quitar símbolos problemáticos: & * ( ) ^ % $ # @ !
    name = re.sub(r"[&*()^%$#@!]", "", name)
    # Escapar caracteres reservados XML (<, >, &)
    name = html.escape(name)
    return name.strip()

def generate_xmltv(channels, xml_file):
    now = datetime.utcnow()
    later = now + timedelta(hours=1)

    with open(xml_file, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<tv generator-info-name="Dummy-EPG">\n')

        for ch in channels:
            f.write(f'  <channel id="{ch["id"]}">\n')
            f.write(f'    <display-name>{sanitize_display_name(ch["name"])}</display-name>\n')
            if ch["logo"]:
                f.write(f'    <icon src="{ch["logo"]}"/>\n')
            f.write("  </channel>\n")

        # Programación dummy (1 hora genérica)
        for ch in channels:
            f.write(
                f'  <programme start="{now.strftime("%Y%m%d%H%M%S")} +0000" '
                f'stop="{later.strftime("%Y%m%d%H%M%S")} +0000" channel="{ch["id"]}">\n'
            )
            f.write('    <title lang="en">Sin EPG disponible</title>\n')
            f.write('    <desc lang="en">Este es un programa de relleno generado automáticamente.</desc>\n')
            f.write("  </programme>\n")

        f.write("</tv>\n")

if __name__ == "__main__":
    canales = parse_m3u(M3U_FILE)
    generate_xmltv(canales, XMLTV_FILE)
    print(f"✅ XMLTV generado con {len(canales)} canales en {XMLTV_FILE}")
