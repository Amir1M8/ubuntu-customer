### List of dconf UUID:
dconf list /org/gnome/terminal/legacy/profiles:/

### Extract dconf UUID Name:
dconf read /org/gnome/terminal/legacy/profiles:/`:UUID`/visible-name

### Export dconf Settings to File:
dconf dump /org/gnome/terminal/legacy/profiles:/`:UUID`/ > profile.dconf

### Import dconf Settings:
dconf load /org/gnome/terminal/legacy/profiles:/`:NEW-PROFILE-NAME`/ < profile.dconf

### ONE-Line Command for Extract All dconf Names and Export Them:
cat dconf-list.txt | while read line; do cname=$(dconf read /org/gnome/terminal/legacy/profiles:/$line/visible-name) ; dconf dump /org/gnome/terminal/legacy/profiles:/$line/ > ./$cname.dconf; done

### Set dconf as Default:
gsettings set org.gnome.Terminal.ProfilesList list "['UUID']"

example:
gsettings set org.gnome.Terminal.ProfilesList list "['b1dcc9dd-5262-4d8d-a863-c897e6d979b9']"

### Generate UUID:
uuidgen
