
Debian
====================
This directory contains files used to package cryptotarget100Md/cryptotarget100M-qt
for Debian-based Linux systems. If you compile cryptotarget100Md/cryptotarget100M-qt yourself, there are some useful files here.

## cryptotarget100M: URI support ##


cryptotarget100M-qt.desktop  (Gnome / Open Desktop)
To install:

	sudo desktop-file-install cryptotarget100M-qt.desktop
	sudo update-desktop-database

If you build yourself, you will either need to modify the paths in
the .desktop file or copy or symlink your cryptotarget100M-qt binary to `/usr/bin`
and the `../../share/pixmaps/cryptotarget100M128.png` to `/usr/share/pixmaps`

cryptotarget100M-qt.protocol (KDE)

