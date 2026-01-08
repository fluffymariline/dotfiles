#!/usr/bin/env python3
import argparse
import io
import os
import sys
from ctypes import CDLL
from os import path
from subprocess import call

CDLL("libgtk4-layer-shell.so")

import gi

gi.require_foreign("cairo")
gi.require_version("Gio", "2.0")
gi.require_version("Gly", "2")
gi.require_version("GlyGtk4", "2")
gi.require_version("Gdk", "4.0")
gi.require_version("Gtk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")

import tempfile

import cairo
from gi.repository import Gdk, Gio, Gly, GlyGtk4, Gtk
from gi.repository import Gtk4LayerShell as LayerShell

scriptdir = path.realpath(path.dirname(__file__))

wallpaper = None
"""
loader = gly_loader_new (file);
image = gly_loader_load (loader, NULL);
if (image)
  {
    frame = gly_image_next_frame (image, NULL);
    if (frame)
      {
        texture = gly_gtk_frame_get_texture (frame);
        g_print ("Image height: %d\n", gdk_texture_get_height (texture));
        image_widget = gtk_image_new_from_paintable (GDK_PAINTABLE (texture));
      }
  }
  """


def on_activate(app) -> None:
    provider = Gtk.CssProvider()
    provider.load_from_path(path.join(scriptdir, "main.css"))
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    window = Gtk.Window(application=app)
    window.set_resizable(True)
    window.maximize()
    window.set_default_size(400, 70)

    LayerShell.init_for_window(window)
    LayerShell.set_anchor(window, LayerShell.Edge.BOTTOM, True)
    LayerShell.set_anchor(window, LayerShell.Edge.TOP, True)
    LayerShell.set_anchor(window, LayerShell.Edge.LEFT, True)
    LayerShell.set_anchor(window, LayerShell.Edge.RIGHT, True)
    LayerShell.set_exclusive_zone(window, -1)
    LayerShell.set_layer(window, LayerShell.Layer.BACKGROUND)
    LayerShell.set_keyboard_mode(window, LayerShell.KeyboardMode.NONE)
    settings: Gio.Settings = Gio.Settings(schema="org.gnome.desktop.background")
    area = Gtk.Picture()
    file = Gio.File.new_for_uri(settings.get_string("picture-uri"))
    area.set_file(file)
    area.set_content_fit(Gtk.ContentFit.COVER)

    window.set_child(area)
    window.present()


def run_wallpaper_ui() -> None:
    app = Gtk.Application(application_id="com.github.wmww.gtk4-layer-shell.py-example")
    app.connect("activate", on_activate)
    app.run(None)


if __name__ == "__main__":
    run_wallpaper_ui()
