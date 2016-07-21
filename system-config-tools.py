#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
 
from gi.repository import Gtk, GdkPixbuf, Gdk, GObject, Gio
import os

class MainWindow( object ):
    """This is the main class for the application"""

    def __init__(self):
        
        builder = Gtk.Builder()
        builder.add_from_file("system-config-tools.glade")
        builder.connect_signals(self)
        self.window = builder.get_object("window_main")
        self.set_gtk = builder.get_object("set_gtk")
        self.set_gtk.connect("changed", self.on_gtk_combo_changed)
        self.set_window = builder.get_object("set_window")
        self.set_window.connect("changed", self.on_window_combo_changed)
        self.set_icon = builder.get_object("set_icon")
        self.set_icon.connect("changed", self.on_icon_combo_changed)
        self.set_cursor = builder.get_object("set_cursor")
        self.set_cursor.connect("changed", self.on_cursor_combo_changed)
        self.theme_list = []
        self.window_list = []
        self.icon_list = []
        self.cursor_list = []
        self.constructCombo()
        self.window.connect("delete-event", Gtk.main_quit)
        self.settings_gtk = Gio.Settings.new("org.mate.interface")
        self.settings_marco = Gio.Settings.new("org.mate.Marco.general")
        self.settings_cursor = Gio.Settings.new("org.mate.peripherals-mouse")
        self.settings_gtk.connect( "changed::gtk-theme", self.loadSettings )
        self.loadSettings()
        self.window.show_all()
        Gtk.main()

    def constructCombo( self ):
        for theme in os.listdir("/usr/share/themes"):
            themedir = os.path.join("/usr/share/themes", theme)
            themefile = os.path.join(themedir, "gtk-2.0/gtkrc")
            if os.path.isfile(themefile):
                self.theme_list.append(theme)
        self.theme_list.sort()
        for item in self.theme_list:
            self.set_gtk.append_text(item)

        for theme in os.listdir("/usr/share/themes"):
            themedir = os.path.join("/usr/share/themes", theme)
            themefile = os.path.join(themedir, "metacity-1/metacity-theme-1.xml")
            if os.path.isfile(themefile):
                self.window_list.append(theme)
        self.window_list.sort()
        for item in self.window_list:
            self.set_window.append_text(item)

        for theme in os.listdir("/usr/share/icons"):
            themedir = os.path.join("/usr/share/icons", theme)
            themefile = os.path.join(themedir, "index.theme")
            if os.path.isfile(themefile):
                self.icon_list.append(theme)
        self.icon_list.remove("default")
        self.icon_list.remove("hicolor")
        self.icon_list.sort()
        for item in self.icon_list:
            self.set_icon.append_text(item)

        for theme in os.listdir("/usr/share/icons"):
            themedir = os.path.join("/usr/share/icons", theme)
            themefile = os.path.join(themedir, "cursors")
            if os.path.isdir(themefile):
                self.cursor_list.append(theme)
        self.cursor_list.append("default")
        self.cursor_list.sort()
        for item in self.cursor_list:
            self.set_cursor.append_text(item)

    def loadSettings( self, *args, **kargs ):
        self.gtk_theme   =  self.settings_gtk.get_string( "gtk-theme" )
        self.window_theme =  self.settings_marco.get_string( "theme" )
        self.icon_theme =  self.settings_gtk.get_string( "icon-theme" )
        self.cursor_theme =  self.settings_cursor.get_string( "cursor-theme" )
        self.set_gtk.set_active(self.theme_list.index(self.gtk_theme))
        self.set_window.set_active(self.window_list.index(self.window_theme))
        self.set_icon.set_active(self.icon_list.index(self.icon_theme))
        self.set_cursor.set_active(self.cursor_list.index(self.cursor_theme))

    def on_gtk_combo_changed(self, combo):
        iter = combo.get_active()
        self.settings_gtk.set_string( "gtk-theme", self.theme_list[iter] )

    def on_window_combo_changed(self, combo):
        iter = combo.get_active()
        self.settings_marco.set_string( "theme", self.window_list[iter] )

    def on_icon_combo_changed(self, combo):
        iter = combo.get_active()
        self.settings_gtk.set_string( "icon-theme", self.icon_list[iter] )

    def on_cursor_combo_changed(self, combo):
        iter = combo.get_active()
        self.settings_cursor.set_string( "cursor-theme", self.cursor_list[iter] )

if __name__ == '__main__':
    main_window = MainWindow()
