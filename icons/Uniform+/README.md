Translate google

For this themes, created a modified script Hardcoded Icon Fixer to fix immutable icons.

Before using the script better compressed folder .local/share/applications /usr/share/applications /usr/share/icons /usr/share/pixmaps and save them as bakup for recovery.

How to fix a stubborn icons?

Take fix2.sh and tofix2.csv and place it in your home directory (this is the folder where Documents, Video, Images, etc.). 

Run the script in the terminal

sudo bash fix2.sh

Next, enter your password (it will be completely invisible) and hit Enter


How does the script?

The script looks at all the .desktop files in the system, and if he sees a path to the icon:

Icon=/usr/share/pixmaps/gcolor2/gcolor2.xpm

the fix it on here such:

Icon=gcolor2

In this case, any themes icons where there gcolor2 (any resolution .png, or .svg), shows a beautiful picture, rather than the standard and terrible gcolor2.xpm.

The script corrects only icons for installed programs. Ie If you install a new program and its icon is turned off themes, run the script again.

P.S. Under this script adapted several icon themes:

Snowy - https://yadi.sk/d/kVzafq1ptMV4R

Green triangles and Orange triangles - https://yadi.sk/d/mgw3OdwPtMUwb

Yellow square - https://www.gnome-look.org/p/1150789

Not superflat stickers  - https://www.gnome-look.org/p/1152410

Gears - http://gnome-look.org/content/show.php/Gears?content=168695

Shiny buttons - http://gnome-look.org/content/show.php/Shiny+buttons?content=169942

Glass of water - http://gnome-look.org/content/show.php/Glass+of+water?content=169389

White chips https://yadi.sk/d/DrytZyZUyZm9S

White chips 256 https://yadi.sk/d/PC4BiN55yZkzS

White chips heavy https://yadi.sk/d/R7ZQxb5q3EB2r6

P.S.S. To optimize the system, you can create an icon-cache themes. This will help in case of problems with applets in the MATE.

If the subject in the .icons

In the terminal:

gtk-update-icon-cache /home/*****/.icons/Uniform+

(***** instead of writing the name of your computer)

If the subject in the /usr/share/icons то

In the terminal:

sudo gtk-update-icon-cache /usr/share/icons/Uniform+

Translate google
