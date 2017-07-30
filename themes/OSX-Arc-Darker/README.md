# OSX-Arc Collection

OSX-Arc theme collection is a flat theme collection based on arc with transparent elements for GTK 3, GTK 2 and Gnome-Shell which supports GTK 3 and GTK 2 based desktop environments like Gnome, Unity, Budgie, Pantheon, XFCE, Mate, etc.

## 0SX-Arc Collection is available in three variants 

##### OSX-Arc-White

![A screenshot of the OSX-Arc-White theme](https://cn.pling.com/img/4/7/5/0/8c43c7300506520877db93f40e16f68005e8.png)

##### OSX-Arc-Darker

![A screenshot of the OSX-Arc-Darker theme](https://cn.pling.com/img/b/c/1/9/2663fe7724cdbe48087bf8ffb61ef33d9270.png)

##### OSX-Arc-Shadow

![A screenshot of the OSX-Arc-Shadow theme](https://cn.pling.com/img/4/e/e/e/7aa33dbf66b684e7ca882318e6b400acd1b5.png)

## Installation

### Packages


--

### Manual Installation

How To Install:

1. Download (https://www.gnome-look.org/p/1167049)

1a-. Extract to /usr/share/themes
or ~/.themes (create it (in your home folder) if necessary);

2. Alternatively click on the install button next to the theme
(follow instructions by clicking the question mark next to the install button)

3. Change via distribution specific tool.


**Note:** If your distribution doesn't ship separate development packages you just need GTK 3 instead of the `-dev` packages.

For the theme to function properly, install the following
* Gnome Shell, GTK 3.14 - 3.22
* The `gnome-themes-standard` package
* The murrine engine. This has different names depending on your distro.
  * `gtk-engine-murrine` (Arch Linux)
  * `gtk2-engines-murrine` (Debian, Ubuntu, elementary OS)
  * `gtk-murrine-engine` (Fedora)
  * `gtk2-engine-murrine` (openSUSE)
  * `gtk-engines-murrine` (Gentoo)


After the installation is complete you can activate the theme with `gnome-tweak-tool` or a similar program by selecting `OSX-Arc-White`, `OSX-Arc-Darker` or `OSX-Arc-Shadow` as Window/GTK+ theme and `OSX-Arc-White`, `OSX-Arc-Darker` or `OSX-Arc-Shadow` as Gnome Shell/Cinnamon theme.

## Uninstall

Run

    sudo rm -rf /usr/share/themes/{OSX-Arc-White,OSX-Arc-Darker,OSX-Arc-Shadow}

## Extras

### Arc Firefox theme
A theme for Firefox is available at https://github.com/horst3180/arc-firefox-theme

### Arc icon theme
The Arc icon theme is available at https://github.com/horst3180/arc-icon-theme

### Chrome/Chromium theme
To install the Chrome/Chromium theme go to the Extra folder and drag and drop the arc-theme.crx or arc-dark-theme.crx or arc-darker-theme.crx file into the Chrome/Chromium window. The source of the Chrome themes is located in the source folder "OSX-Arc-White > Extra folder > arc-theme.crx.

### Plank theme
To install the Plank theme, copy the `extra/Arc-Plank` folder to `~/.local/share/plank/themes` or to `/usr/share/plank/themes` for system-wide use.
Now open the Plank preferences window by executing `plank --preferences` from a terminal and select `Arc-Plank` as the theme.

### Arc-Dark for Ubuntu Software Center
The Arc Dark theme for the Ubuntu Software Center by [mervick](https://github.com/mervick) can be installed from [here](https://github.com/mervick/arc-dark-software-center). It solves readability issues with Arc Dark and the Ubuntu Software Center.

## Troubleshooting

If you have Ubuntu with a newer GTK/Gnome version than the one included by default (i.e Ubuntu 14.04 with GTK 3.14 or Ubuntu 15.04 with GTK 3.16, etc.) you have to install the theme manually as described above.
This is also true for other distros with a different GTK/Gnome version than the one included by default

--

If you get artifacts like black or invisible backgrounds under Unity, disable overlay scrollbars with

    gsettings set com.canonical.desktop.interface scrollbar-mode normal


## Bugs
bug page available soon.

## License
OSX-Arc Collection is available under the terms of the GPL-3.0. See `COPYING` for details.

## Full Preview

