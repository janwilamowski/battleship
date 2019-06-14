# -*- coding: utf-8 -*-

import os
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, TEXT_COLOR, BASE_DIR
from AI import AI_Level
import pygame
from pygame.locals import MOUSEBUTTONDOWN
from pgu import gui


def load_image(filename, subdir=''):
    file = os.path.join(BASE_DIR, subdir, filename)
    return pygame.image.load(file).convert_alpha()


class AboutDialog(gui.Dialog):
    def __init__(self):
        title = gui.Label('About')
        space = title.style.font.size(' ')
        doc = gui.Document(width=400, height=300)
        doc.block(align=0)
        doc.add(gui.Label('BATTLESHIPS'))
        doc.br(space[1])
        doc.block(align=0)
        doc.add(gui.Label('Made by Jan Wilamowski'))
        doc.block(align=0)
        doc.br(space[1])
        doc.add(gui.Label('Graphics by Fabian Freiesleben'))
        doc.block(align=0)
        doc.add(gui.Label('License: GPLv3'))
        gui.Dialog.__init__(self, title, doc)


class Gui():
    def __init__(self, init_cb, set_ai_cb, font):
        self.app = gui.App()
        self.app.connect(gui.QUIT, self.app.quit, None)
        container = gui.Container(align=-1, valign=-1)
        self.font = font

        menus = gui.Menus([
            ('Game/New', init_cb, True),
            ('Game/Quit', self.quit, None),
            ('AI Level/Dumb', set_ai_cb, AI_Level.dumb),
            ('AI Level/Smart', set_ai_cb, AI_Level.smart),
            ('Help/About', self.open_about, None),
            ])
        menus.rect.w, menus.rect.h = menus.resize()
        self.doc = gui.Document(width=0, height=0) # TODO: vertical?
        self.log_box = gui.ScrollArea(self.doc, SCREEN_WIDTH, 100, hscrollbar=False)
        self.log("Welcome to Battleships!")

        container.add(menus, 0, 0)
        container.add(self.log_box, 0, SCREEN_HEIGHT-100)
        self.menus = menus
        self.elements = (menus, self.log_box)
        self.app.init(container)

        self.about_dlg = AboutDialog()

    def quit(self, args):
        self.app.quit()
        sys.exit()

    def open_about(self, args):
        self.about_dlg.open()

    def clear_log(self):
        self.doc.widgets = []

    def log(self, text, color=TEXT_COLOR):
        # insert on top to avoid scrolling problems
        self.doc.layout._widgets.reverse()
        self.doc.block(align=-1)
        self.doc.add(gui.Label(text, color=color))
        self.doc.layout._widgets.reverse()
        self.log_box.set_vertical_scroll(0)

    def update_ai_menu(self, level):
        # there might be a better way to access these
        ai_menu = self.menus._rows[0][1]['widget']
        dumb_label, smart_label = [r[0]['widget'].value for r in ai_menu.options._rows]
        if level == AI_Level.dumb:
            dumb_label.set_text('Dumb ✔')
            smart_label.set_text('Smart')
        elif level == AI_Level.smart:
            dumb_label.set_text('Dumb')
            smart_label.set_text('Smart ✔')
        dumb_label.resize()
        smart_label.resize()
        dumb_label.set_font(self.font)
        smart_label.set_font(self.font)

    def paint(self):
        self.app.paint()

    def handle(self, event):
        self.app.event(event)

    def is_active(self):
        """ Returns True if a menu or dialog is active (shown) and False otherwise. """
        return self.about_dlg.is_open() or any(menu['widget'].pcls for menu in self.menus._rows[0])

    def is_gui_click(self, event):
        """ Scrolling is also clicking """
        return event.type == MOUSEBUTTONDOWN and any(gui_el.rect.collidepoint(event.pos) for gui_el in self.elements)
