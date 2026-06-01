import subprocess
import os
from colorama import Fore

RESET   = "\x1b[0m"
BOLD    = "\x1b[1m"
DIM     = "\x1b[2m"
ITALIC  = "\x1b[3m"

FG_GRAY    = "\x1b[38;5;245m"
FG_BLUE    = "\x1b[38;5;39m"
FG_CYAN    = Fore.CYAN
FG_GREEN   = Fore.GREEN
FG_YELLOW  = Fore.YELLOW
FG_RED     = Fore.RED
FG_MAGENTA = "\x1b[38;5;177m"
FG_PURPLE  = "\x1b[38;5;141m"
FG_TEAL    = "\x1b[38;5;80m"
FG_ORANGE  = "\x1b[38;5;208m"

message = ""

def banner(subtitle):
    title = "Theme Designer"
    version_tag = "v.1.0"

    left = f" {title} "
    center = f" {subtitle} "
    right = f" {version_tag} "
    inner_width = max(68, len(left) + len(center) + len(right) + 2)

    gap = inner_width - (len(left) + len(center) + len(right))
    left_gap = gap // 2
    right_gap = gap - left_gap

    top = "╭" + ("─" * inner_width) + "╮"
    mid = "│" + left + (" " * left_gap) + center + (" " * right_gap) + right + "│"
    bot = "╰" + ("─" * inner_width) + "╯"

    top = f"{DIM}{FG_GRAY}{top}{RESET}"
    bot = f"{DIM}{FG_GRAY}{bot}{RESET}"
    mid = (
        f"{DIM}{FG_GRAY}│{RESET}"
        f"{BOLD}{FG_RED}{left}{RESET}"
        f"{' ' * left_gap}"
        f"{FG_GRAY}{center}{RESET}"
        f"{' ' * right_gap}"
        f"{BOLD}{FG_YELLOW}{right}{RESET}"
        f"{DIM}{FG_GRAY}│{RESET}"
    )

    print(top)
    print(mid)
    print(bot)

def changeTheme():
    UUID = ""
    isUUID = True
    try:
        open(os.path.expanduser("~/.ubuntu-customer/setting/uuid.ini"), "+x")
        isUUID = False
    except:
        setting = open(os.path.expanduser("~/.ubuntu-customer/setting/uuid.ini"), "r")
        UUID = setting.read()
        setting.close()

    themes = [
        "blue-theme",
        "dark-blue-theme",
        "forest-theme",
        "nigth-theme",
        "spring-theme",
        "winter-theme",
        "autumn-theme",
        "spring-forest-theme"
    ]

    path = "~/.ubuntu-customer/dconf/"

    global message
    message = "Terminal Theme"

    while True:
        os.system("clear")
        banner(message)

        counter = 0
        for theme in themes:
            counter += 1
            print(f"{FG_YELLOW}[{counter}{FG_YELLOW}]{FG_GREEN} {theme}{RESET}")
        print(f"{FG_YELLOW}[{counter+1}{FG_YELLOW}]{FG_GREEN} Home{RESET}")

        selected_theme = int(input(f"{FG_CYAN}\n[Theme]: {RESET}"))
        if selected_theme == counter+1:
            break
        else:
            selected_theme = selected_theme - 1
            user_theme = path+themes[selected_theme]+".dconf"

        UUID = UUID.replace("\n","")

        if isUUID == True:
            dconf_list = subprocess.check_output(['dconf', 'list', '/org/gnome/terminal/legacy/profiles:/'], text=True)
            if UUID == "":
                generate_uuid = subprocess.check_output(['uuidgen'], text=True)
                with open(os.path.expanduser("~/.ubuntu-customer/setting/uuid.ini"), "w") as write_uuid:
                    write_uuid.write(generate_uuid)
                    UUID = generate_uuid
            elif UUID in dconf_list: # Edit UUID in dconf
                pass
            else: # Create UUID in dconf
                generate_uuid = subprocess.check_output(['uuidgen'], text=True)
                with open(os.path.expanduser("~/.ubuntu-customer/setting/uuid.ini"), "w") as write_uuid:
                    write_uuid.write(generate_uuid)
                    UUID = generate_uuid
        else: # Create UUID in dconf
            generate_uuid = subprocess.check_output(['uuidgen'], text=True)
            with open(os.path.expanduser("~/.ubuntu-customer/setting/uuid.ini"), "w") as write_uuid:
                write_uuid.write(generate_uuid)
                UUID = generate_uuid

        UUID = UUID.replace("\n", "")
        print(f"Theme UUID: {UUID}")

        command = f'dconf load /org/gnome/terminal/legacy/profiles:/:{UUID}/ < {user_theme}'
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            message = f"Theme: {themes[selected_theme].upper()}"

            set_as_defualt = f'gsettings set org.gnome.Terminal.ProfilesList list "[\'{UUID}\']"'
            command_result = subprocess.run(
                set_as_defualt,
                shell=True,
                capture_output=True,
                text=True
            )

            if command_result.returncode == 0:
                # print(f"[+] {themes[selected_theme]} set as Default theme successfuly.")
                # input("[!] Press `Enter` to continue...")
                continue
            else:
                print(f"[!] Error in set theme as Default...")
                input("[!] Press `Enter` to continue...")

        else:
            print(f"[!] Error in loading dconf...")
            input("[!] Press `Enter` to continue...")

def gtk_css():
    gtks = [
        "blue-gtk",
        "dark-blue-gtk",
        "forest-gtk",
        "nigth-gtk",
        "spring-gtk",
        "winter-gtk",
        "autumn-gtk",
        "spring-forest-gtk"
    ]

    path = "~/.ubuntu-customer/gtk/"

    global message
    message = "GTK Style"

    while True:
        os.system("clear")
        banner(message)

        counter = 0
        for gtk in gtks:
            counter += 1
            print(f"{FG_YELLOW}[{counter}{FG_YELLOW}]{FG_GREEN} {gtk}{RESET}")
        print(f"{FG_YELLOW}[{counter+1}{FG_YELLOW}]{FG_GREEN} Manual Setting{RESET}")
        print(f"{FG_YELLOW}[{counter+2}{FG_YELLOW}]{FG_GREEN} Home{RESET}")


        selected_gtk = int(input(f"{FG_CYAN}\n[GTK]: {RESET}"))

        if selected_gtk == counter+1:
            pass
        elif selected_gtk == counter+2:
            break
        else:
            selected_gtk = selected_gtk - 1
            gtk_theme = path+gtks[selected_gtk]+".css"


        gtk_backup = f'cp ~/.config/gtk-3.0/gtk.css ~/.config/gtk-3.0/gtk-backup.css'
        gtk_backup_result = subprocess.run(
            gtk_backup,
            shell=True,
            capture_output=True,
            text=True
        )

        gtk = f'cp {gtk_theme} ~/.config/gtk-3.0/gtk.css'
        gtk_result = subprocess.run(
            gtk,
            shell=True,
            capture_output=True,
            text=True
        )

        if gtk_result.returncode == 0:
            message = f"GTK: {gtks[selected_gtk].upper()}"
            continue
        else:
            print(f"[!] Error in set theme as Default...")
            input("[!] Press `Enter` to continue...")

def wallpaper_ch():
    wallpapers = [
        "alone-winter-theme",
        "forest-road-theme",
        "forest-theme",
        "green-theme",
        "nigth-theme",
        "rainy-theme",
        "road-theme",
        "winter-theme",
        "spring-theme",
        "winter-forest",
        "autumn-forest",
        "spring-forest"
    ]
    global message
    message = "Desktop Wallpaper"

    while True:
        os.system("clear")
        banner(message)

        counter = 0
        for wallpaper in wallpapers:
            counter += 1
            print(f"{FG_YELLOW}[{counter}{FG_YELLOW}]{FG_GREEN} {wallpaper}{RESET}")
        print(f"{FG_YELLOW}[{counter+1}{FG_YELLOW}]{FG_GREEN} Home{RESET}")

        selected_wallpaper = int(input(f"{FG_CYAN}\n[WALLPAPER]: {RESET}"))

        if selected_wallpaper == counter+1:
            break
        else:
            selected_wallpaper = selected_wallpaper - 1
            path = os.path.expanduser(f"~/.ubuntu-customer/wallpapers/{wallpapers[selected_wallpaper]+".jpg"}")

        wall_theme = f'gsettings set org.gnome.desktop.background picture-uri-dark "file:///{path}"'
        wall_result = subprocess.run(
            wall_theme,
            shell=True,
            capture_output=True,
            text=True
        )

        if wall_result.returncode == 0:
            message = f"Wallpaper: {wallpapers[selected_wallpaper].upper()}"
            continue
        else:
            print(f"[!] Error in set theme as Default...")
            input("[!] Press `Enter` to continue...")

def autoset():
    UUID = ""
    isUUID = True
    try:
        open(os.path.expanduser("~/.ubuntu-customer/setting/uuid.ini"), "+x")
        isUUID = False
    except:
        setting = open(os.path.expanduser("~/.ubuntu-customer/setting/uuid.ini"), "r")
        UUID = setting.read()
        setting.close()

    themes = {
        "1": ["alone-winter-theme", "winter-gtk", "winter-theme"],
        "2": ["forest-road-theme", "forest-gtk", "forest-theme"],
        "3": ["forest-theme", "forest-gtk", "forest-theme"],
        "4": ["green-theme", "forest-gtk", "forest-theme"],
        "5": ["nigth-theme", "nigth-gtk", "nigth-theme"],
        "6": ["rainy-theme", "winter-gtk", "winter-theme"],
        "7": ["road-theme", "forest-gtk", "forest-theme"],
        "8": ["winter-theme", "winter-gtk", "winter-theme"],
        "9": ["spring-theme", "spring-gtk", "spring-theme"],
        "10": ["winter-forest", "winter-gtk", "winter-theme"],
        "11": ["autumn-forest", "autumn-gtk", "autumn-theme"],
        "12": ["spring-forest", "spring-forest-gtk", "spring-forest-theme"],
    }

    global message
    message = "Ubuntu Theme"
    os.system("clear")
    banner(message)
    dconf_path = "~/.ubuntu-customer/dconf/"
    gtk_path = "~/.ubuntu-customer/gtk/"

    counter = 0
    for theme in themes.keys():
        counter += 1
        print(f"{FG_YELLOW}[{counter}{FG_YELLOW}]{FG_GREEN} {themes[theme][0]}{RESET}")
    print(f"{FG_YELLOW}[{counter+1}{FG_YELLOW}]{FG_GREEN} Home{RESET}")


    user_theme = int(input(f"{FG_CYAN}\n[THEME]: {RESET}"))

    if user_theme == counter+1:
        return None

    wallpaper_path = os.path.expanduser(f"~/.ubuntu-customer/wallpapers/{themes[str(user_theme)][0]+".jpg"}")
    wall_theme = f'gsettings set org.gnome.desktop.background picture-uri-dark "file:///{wallpaper_path}"'

    wall_result = subprocess.run(
        wall_theme,
        shell=True,
        capture_output=True,
        text=True
    )

    if wall_result.returncode == 0:
        message = f"Wallpaper: {themes[str(user_theme)][0].upper()}"
    else:
        print(f"[!] Error in set theme as Default...")
        input("[!] Press `Enter` to continue...")
        return None

    gtk_theme = gtk_path+themes[str(user_theme)][1]+".css"

    gtk = f'cp {gtk_theme} ~/.config/gtk-3.0/gtk.css'
    gtk_result = subprocess.run(
        gtk,
        shell=True,
        capture_output=True,
        text=True
    )

    if gtk_result.returncode == 0:
        message = f"GTK: {themes[str(user_theme)][2].upper()}"
        
    else:
        print(f"[!] Error in set theme as Default...")
        input("[!] Press `Enter` to continue...")
        return None

    dconf_theme = dconf_path+themes[str(user_theme)][2]+".dconf"
    UUID = UUID.replace("\n","")

    if isUUID == True:
        dconf_list = subprocess.check_output(['dconf', 'list', '/org/gnome/terminal/legacy/profiles:/'], text=True)
        if UUID == "":
            generate_uuid = subprocess.check_output(['uuidgen'], text=True)
            with open(os.path.expanduser("~/.ubuntu-customer/setting/uuid.ini"), "w") as write_uuid:
                write_uuid.write(generate_uuid)
                UUID = generate_uuid
        elif UUID in dconf_list: # Edit UUID in dconf
            pass
        else: # Create UUID in dconf
            generate_uuid = subprocess.check_output(['uuidgen'], text=True)
            with open(os.path.expanduser("~/.ubuntu-customer/setting/uuid.ini"), "w") as write_uuid:
                write_uuid.write(generate_uuid)
                UUID = generate_uuid
    else: # Create UUID in dconf
        generate_uuid = subprocess.check_output(['uuidgen'], text=True)
        with open(os.path.expanduser("~/.ubuntu-customer/setting/uuid.ini"), "w") as write_uuid:
            write_uuid.write(generate_uuid)
            UUID = generate_uuid

    UUID = UUID.replace("\n", "")
    print(f"Theme UUID: {UUID}")

    command = f'dconf load /org/gnome/terminal/legacy/profiles:/:{UUID}/ < {dconf_theme}'
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"Theme: {themes[str(user_theme)][2].upper()}")

        set_as_defualt = f'gsettings set org.gnome.Terminal.ProfilesList list "[\'{UUID}\']"'
        command_result = subprocess.run(
            set_as_defualt,
            shell=True,
            capture_output=True,
            text=True
        )

        if command_result.returncode == 0:
            # print(f"[+] {themes[selected_theme]} set as Default theme successfuly.")
            # input("[!] Press `Enter` to continue...")
            pass
        else:
            print(f"[!] Error in set theme as Default...")
            input("[!] Press `Enter` to continue...")
            return None

    else:
        print(f"[!] Error in loading dconf...")
        input("[!] Press `Enter` to continue...")
        return None
    input("[!] Press `Enter` to continue...")



while True:
    os.system("clear")
    message = "Home"
    banner(message)
    print(f"{FG_YELLOW}[1{FG_YELLOW}]{FG_GREEN} Terminal Theme{RESET}")
    print(f"{FG_YELLOW}[2{FG_YELLOW}]{FG_GREEN} Terminal GTK CSS{RESET}")
    print(f"{FG_YELLOW}[3{FG_YELLOW}]{FG_GREEN} Desktop Wallpaper{RESET}")
    print(f"{FG_YELLOW}[4{FG_YELLOW}]{FG_GREEN} Theme{RESET}")
    print(f"{FG_YELLOW}[5{FG_YELLOW}]{FG_GREEN} Exit{RESET}\n")
    choice = int(input(f"{FG_CYAN}[OPTION]: {RESET}"))

    if choice == 1:
        os.system("clear")
        changeTheme()
    
    elif choice == 2:
        os.system("clear")
        gtk_css()
    
    elif choice == 3:
        os.system("clear")
        wallpaper_ch()

    elif choice == 4:
        os.system("clear")
        autoset()

    else:
        break