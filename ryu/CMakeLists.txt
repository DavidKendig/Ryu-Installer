# === This file is part of Ryū Installer, based on Calamares ===
#
#   SPDX-FileCopyrightText: 2026 David Kendig
#   SPDX-License-Identifier: GPL-3.0-or-later
#
# Ryū OS's installer configuration: settings.conf (which pages and steps run, and the
# "ryu" branding) and the module configs. They install to /etc/calamares, the first place
# Calamares looks, so the upstream examples (INSTALL_CONFIG) are not needed.

option(INSTALL_RYU_CONFIG "Install Ryū OS's settings.conf and module configs to /etc/calamares" ON)

if(INSTALL_RYU_CONFIG)
    file(GLOB _ryu_module_configs ${CMAKE_CURRENT_SOURCE_DIR}/modules/*.conf)
    install(FILES settings.conf DESTINATION ${CMAKE_INSTALL_FULL_SYSCONFDIR}/calamares)
    install(FILES ${_ryu_module_configs} DESTINATION ${CMAKE_INSTALL_FULL_SYSCONFDIR}/calamares/modules)
endif()
