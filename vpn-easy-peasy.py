import os
import glob
import curses
import subprocess


def get_ovpn_file_name():
    files = glob.glob('*.ovpn')
    if files:
        ovpn_file = files[0]
        return os.path.basename(ovpn_file)
    else:
        return None


def start_vpn(ovpn_file_name):
    command = f'openvpn3 session-start --config {ovpn_file_name}'
    subprocess.call(command, shell=True)


def stop_vpn(ovpn_file_name):
    command = f'openvpn3 session-manage --config {ovpn_file_name} --disconnect'
    subprocess.call(command, shell=True)


def session():
    command = "openvpn3 sessions-list"
    subprocess.call(command, shell=True)


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    stdscr.addstr(1, 0, " ____ ____ ____ _   _    ___  ____ ____ ____ _   _    _  _ ___  _  _ ")
    stdscr.addstr(2, 0, " |___ |__| [__   \_/     |__] |___ |__| [__   \_/     |  | |__] |\ | ")
    stdscr.addstr(3, 0, " |___ |  | ___]   |      |    |___ |  | ___]   |       \/  |    | \| ")
    stdscr.addstr(4, 0, "                         https://github.com/alanvianaa/easy-peasy-vpn")

    ovpn_file_name = get_ovpn_file_name()
    if ovpn_file_name:
        stdscr.addstr(6, 0, f'Open VPN file config: {ovpn_file_name}')
    else:
        stdscr.addstr(6, 0, 'Open VPN file config not found (.ovpn)')

    options = ["Start VPN", "Stop VPN"]
    current_option = 0

    line = 10
    while True:
        for i, option in enumerate(options):
            if i == current_option:
                stdscr.addstr(i + line, 0, "[x] " + option)
            else:
                stdscr.addstr(i + line, 0, "[ ] " + option)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            current_option = (current_option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            current_option = (current_option + 1) % len(options)
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            if current_option == 0:
                start_vpn(ovpn_file_name)
            elif current_option == 1:
                stop_vpn(ovpn_file_name)

            stdscr.refresh()
            stdscr.getch()
            break

        stdscr.refresh()


curses.wrapper(main)
