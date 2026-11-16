<!-- SPDX-FileCopyrightText: 2026 David Kendig
     SPDX-License-Identifier: GPL-3.0-or-later
-->

# Ryū Installer

<img src="src/branding/ryu/logo.png" alt="Ryū OS dragon" width="96" align="right">

The graphical installer of **Ryū OS**. It is [Calamares](https://calamares.io) 3.4.2 with Ryū OS's branding and configuration added. Calamares does all the work: partitioning, copying the system, creating the user and installing the boot loader.

From the live session's **Install Ryū OS** icon, it takes you through six pages: Welcome, Location, Keyboard, Partitions, Users and Summary. Then it copies the system while a slideshow plays. It is drawn in the colors of the Ryū OS boot menu: a deep indigo aurora, azure and violet buttons, and the Ryū dragon in the sidebar.

## What Ryū OS adds to Calamares

These are the changes from Calamares 3.4.2 (tag `v3.4.2`), made by David Kendig on 2026-11-16. Everything else is upstream Calamares, unchanged.

| Path | What it is |
|---|---|
| `src/branding/ryu/` | The **ryu** branding component, registered in `src/branding/CMakeLists.txt`: <ul><li>`stylesheet.qss`: the aurora colors.</li><li>`logo.png`: the dragon, from `art/logo.svg`.</li><li>`icon.png`: the window icon.</li><li>`welcome.png`, `slide1.png` to `slide3.png`: the welcome picture and the install slideshow.</li><li>`art/installer_art.py`: the script that drew the welcome picture and slides.</li></ul> |
| `ryu/` | Ryū OS's `settings.conf` and module configs, installed to `/etc/calamares` (`ryu/CMakeLists.txt`, added from the top-level `CMakeLists.txt`). |
| `.github/workflows/` | Removed: upstream's nightly CI builds, which target Calamares' own infrastructure. |
| `README.md`, `LICENSE` | This file and the GPL text. Upstream's README is kept as [README-Calamares.md](README-Calamares.md). |

### The configuration (`ryu/`)
* **Pages:** welcome, locale, keyboard, partition, users and summary, then finished.
* **Install steps:** partition, mount, unpackfs, machineid, fstab, locale, keyboard, localecfg, users, removeuser, hwclock, Ryū OS's post-install step (`shellprocess@ryupost`), bootloader, umount.
* **Disks:** "erase disk" is the default. File systems are ext4, btrfs or xfs, with an optional small swap partition. Ryū OS's initramfs mounts a plain root file system, so there is no LUKS encryption or LVM.
* **System:** the read-only live root (`/run/ryu/lower`) is copied as is, so changes made in the live session never reach the installed system.
* **Users:** the new account joins `wheel` for sudo; there is no root password. The live user `ryu` is removed.
* **Boot loader:** GRUB, BIOS or UEFI (EFI id `RyuOS`).
* **Requirements:** 7.5 GiB of disk and 1.5 GiB of RAM.

The configuration expects the Ryū OS live image around it:
* `/run/ryu/lower`, the squashfs root.
* `/usr/libexec/ryuos/post-install`, which removes the live-only files and starts the desktop session for the new user at boot, behind the login screen.
* A launcher that starts the system D-Bus and polkit first. Calamares partitions through kpmcore, whose helper is reached over D-Bus and authorized by polkit even when Calamares runs as root.

Those live in the Ryū OS repository, next to the image that uses them.

## Building

On Void Linux (the base of Ryū OS), install the build dependencies:

```sh
xbps-install -S cmake ninja gcc pkg-config qt6-base-devel qt6-svg-devel qt6-tools-devel \
    kf6-kcoreaddons-devel extra-cmake-modules yaml-cpp-devel kpmcore-devel python3-devel \
    libpwquality-devel polkit-qt6-devel gettext
```

Ryū OS builds only the modules it uses. The QML pages and systemd, dracut and package-manager modules are skipped:

```sh
skip="dracut dracutlukscfg initcpio initcpiocfg initramfs initramfscfg mkinitfs plymouthcfg plasmalnf
  services-systemd services-openrc netinstall packages packagechooser packagechooserq tracking zfs zfshostid
  luksbootkeyfile luksopenswaphookcfg openrcdmcryptcfg fsresizer interactiveterminal notesqml welcomeq localeq
  keyboardq usersq summaryq finishedq oemid rawfs dummycpp dummyprocess dummypython displaymanager
  contextualprocess grubcfg networkcfg license preservefiles unpackfsc"
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_INSTALL_LIBDIR=lib \
    -DWITH_QT6=ON -DWITH_QML=OFF -DBUILD_TESTING=OFF -DBUILD_SCHEMA_TESTING=OFF -DBUILD_CRASH_REPORTING=OFF \
    -DINSTALL_CONFIG=OFF -DINSTALL_POLKIT=OFF -DSKIP_MODULES="$(echo $skip)" \
    -DRYU_VERSION=0.1.26 -DRYU_CODENAME=Beta
ninja -C build
DESTDIR=/path/to/rootfs cmake --install build
```

* **Version:** `RYU_VERSION` and `RYU_CODENAME` set the Ryū OS version shown on the welcome page and in the window title.
* **Config:** `-DINSTALL_RYU_CONFIG=OFF` leaves out the `/etc/calamares` configuration.
* **Theme:** Ryū OS starts Calamares with `QT_STYLE_OVERRIDE=Fusion` and `QT_QPA_PLATFORMTHEME=gtk3` so Qt's palette is dark to match the stylesheet.

### Redrawing the pictures
`logo.png` is the dragon (`art/logo.svg`) at 256×256:

```sh
rsvg-convert -w 256 -h 256 src/branding/ryu/art/logo.svg -o src/branding/ryu/logo.png
```

The welcome picture and slides are drawn on the boot menu's aurora. That aurora comes from Ryū OS's compositor, RyūGlass, which `art/installer_art.py` runs. The script needs Pillow and the Inter font. Redraw them after a version change, because the welcome picture shows the version:

```sh
python3 src/branding/ryu/art/installer_art.py /path/to/ryuglass src/branding/ryu 0.1.26
```

## Updating to a newer Calamares

Upstream lives on Codeberg. Merge a release tag, then rebuild and test an install in a VM:

```sh
git remote add upstream https://codeberg.org/Calamares/calamares.git   # once
git fetch upstream --tags
git merge v3.4.3
```

## License

Ryū Installer is free software under the **GNU General Public License, version 3 or later** (GPL-3.0-or-later), the license of Calamares. See [LICENSE](LICENSE).

* Like Calamares, the repository follows [REUSE](https://reuse.software/). Each file states its own license in an SPDX header or in [.reuse/dep5](.reuse/dep5), and the license texts are in [LICENSES/](LICENSES).
* A few upstream files use licenses compatible with the GPL: BSD-2-Clause, LGPL, MIT, CC0 and CC-BY-4.0. The installer as a whole is GPL-3.0-or-later.
* **Calamares:** © its authors (see [AUTHORS](AUTHORS) and each file's header). Source: <https://codeberg.org/Calamares/calamares>.
* **Ryū OS's additions:** the branding, pictures, dragon logo and configuration are © 2026 David Kendig, licensed GPL-3.0-or-later.
