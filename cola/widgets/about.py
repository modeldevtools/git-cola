from __future__ import division, absolute_import, unicode_literals

from qtpy import QtGui
from qtpy import QtWidgets
from qtpy.QtCore import Qt

from .. import core
from .. import resources
from .. import hotkeys
from .. import icons
from .. import qtutils
from .. import version
from ..i18n import N_
from . import defs
from .text import MonoTextView


def about_dialog():
    """Launches the Help -> About dialog"""
    view = AboutView(qtutils.active_window())
    view.set_version(version.version())
    view.show()
    return view


COPYRIGHT = """git-cola: The highly caffeinated git GUI v$VERSION

Copyright (C) 2007-2016 David Aguilar and contributors

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License
version 2 as published by the Free Software Foundation.

This program is distributed in the hope that it will
be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.

You should have received a copy of the
GNU General Public License along with this program.
If not, see http://www.gnu.org/licenses/.

"""


class AboutView(QtWidgets.QDialog):
    """Provides the git-cola 'About' dialog"""

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.setWindowTitle(N_('About git-cola'))
        self.setWindowModality(Qt.WindowModal)

        self.pixmap = QtGui.QPixmap(icons.name_from_basename('logo-top.png'))
        self.label = QtWidgets.QLabel()
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignTop)

        palette = self.label.palette()
        palette.setColor(QtGui.QPalette.Window, Qt.black)
        self.label.setAutoFillBackground(True)
        self.label.setPalette(palette)

        self.text = MonoTextView(self)
        self.text.setReadOnly(True)
        self.text.setPlainText(COPYRIGHT)

        self.close_button = qtutils.close_button()
        self.close_button.setDefault(True)

        self.button_layout = qtutils.hbox(defs.spacing, defs.margin,
                                          qtutils.STRETCH, self.close_button)

        self.main_layout = qtutils.vbox(defs.no_margin, defs.spacing,
                                        self.label, self.text,
                                        self.button_layout)
        self.setLayout(self.main_layout)

        self.resize(666, 420)

        qtutils.connect_button(self.close_button, self.accept)

    def set_version(self, version):
        """Sets the version field in the 'about' dialog"""
        text = self.text.toPlainText().replace('$VERSION', version)
        self.text.setPlainText(text)


def show_shortcuts():
    try:
        from qtpy import QtWebEngineWidgets
    except ImportError:
        # redhat disabled QtWebKit in their qt build but don't punish the
        # users
        qtutils.critical(N_('This PyQt4 does not include QtWebKit.\n'
                            'The keyboard shortcuts feature is unavailable.'))
        return

    hotkeys_html = resources.doc(N_('hotkeys.html'))
    html = core.read(hotkeys_html)

    parent = qtutils.active_window()
    widget = QtWidgets.QDialog()
    widget.setWindowModality(Qt.WindowModal)
    widget.setWindowTitle(N_('Shortcuts'))

    web = QtWebEngineWidgets.QWebEngineView(parent)
    web.setHtml(html)

    layout = qtutils.hbox(defs.no_margin, defs.spacing, web)
    widget.setLayout(layout)
    widget.resize(800, min(parent.height(), 600))
    qtutils.add_action(widget, N_('Close'), widget.accept,
                       hotkeys.QUESTION, *hotkeys.ACCEPT)
    widget.show()
    widget.exec_()
