#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio
from gi.repository.GdkPixbuf import Pixbuf

class Gtk_Dialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Gtk Theme", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.widget_name = []
        self.icons = []

        vbox_all = Gtk.VBox()

        settings_gtk = Gio.Settings.new("org.mate.interface")
        current_theme = settings_gtk.get_string("gtk-theme")

        for theme_widget in os.listdir("/usr/share/themes/" + current_theme + "/gtk-2.0"):
            if os.path.isdir(os.path.join("/usr/share/themes/", current_theme + "/gtk-2.0/" + theme_widget)):
                self.widget_name.append(theme_widget)

        self.widget_name.sort()

        for item in self.widget_name:
            file_path = os.path.join("/usr/share/themes/", current_theme + "/gtk-2.0/" + item)
            for file_name in os.listdir(file_path):
                full_name = file_path + "/" + file_name
                if os.path.isfile(full_name):
                    self.icons.append(full_name)

            liststore = Gtk.ListStore(Pixbuf, str)
            iconview = Gtk.IconView.new()
            iconview.set_model(liststore)
            iconview.set_pixbuf_column(0)
            iconview.set_text_column(1)

            for icon in self.icons:
                pixbuf = Gdk.pixbuf_new_from_file(icon)
                liststore.append([pixbuf, "Label"])

            vbox_all.pack_start(iconview, True, True, 0)

        box = self.get_content_area()
        box.add(vbox_all)
        self.show_all()
