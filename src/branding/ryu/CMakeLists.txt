# === This file is part of Ryū Installer, based on Calamares ===
#
#   SPDX-FileCopyrightText: 2026 David Kendig
#   SPDX-License-Identifier: GPL-3.0-or-later
#
# The Ryū OS branding component: the boot menu's aurora colours, the Ryū dragon logo,
# the welcome picture and the slideshow shown while the system is copied.
# branding.desc gets the Ryū OS version filled in; everything else installs as it is.

set(RYU_VERSION "0.1.26" CACHE STRING "Ryū OS version shown by the installer")
set(RYU_CODENAME "Beta" CACHE STRING "Ryū OS release name shown by the installer")

set(_ryu_branding_files
    stylesheet.qss
    logo.png
    icon.png
    welcome.png
    slide1.png
    slide2.png
    slide3.png
    arrow-down.png
)

# Also copied into the build directory, so `calamares -d` finds the branding there.
configure_file(branding.desc.in ${CMAKE_CURRENT_BINARY_DIR}/branding.desc @ONLY)
foreach(_f ${_ryu_branding_files})
    configure_file(${_f} ${CMAKE_CURRENT_BINARY_DIR}/${_f} COPYONLY)
endforeach()

list(TRANSFORM _ryu_branding_files PREPEND ${CMAKE_CURRENT_SOURCE_DIR}/)
install(
    FILES ${CMAKE_CURRENT_BINARY_DIR}/branding.desc ${_ryu_branding_files}
    DESTINATION share/calamares/branding/ryu
)
message(STATUS "Ryū OS branding component: version ${RYU_VERSION} (${RYU_CODENAME})")
