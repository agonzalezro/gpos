import os
import gtk

import gtk.glade
from gettext import gettext as _

import treefilebrowser


class Settings(object):
    glade = os.path.join(os.path.dirname(__file__), 'windows.glade')


class Gui(object):
    def __init__(self):
        print Settings.glade
        self.tree = self.get_glade_tree()
        self.connect_all_signals()
        self.build_main_window()
        self['main'].show()

    def __getitem__(self, item):
        return self.tree.get_widget(item)

    def build_main_window(self):
        self['hpaned'].pack2(self.get_file_browser(), resize=True, shrink=False)
        self['hpaned'].pack1(self.get_folder_browser(), resize=True, shrink=False)


    def get_folder_browser(self):
        folder_browser = treefilebrowser.TreeFileBrowser('/')
        folder_browser.connect('cursor-changed', self.on_path_changed)
        # self.file_browser.set_property('show-only-dirs', False)
        folder_browser.set_active_dir(os.path.join(os.environ['HOME'], 'Videos'))
        folder_browser.view.set_size_request(250, -1)
        return folder_browser.get_scrolled()

    def get_file_browser(self):
        self.liststore = gtk.ListStore(str, str, str, str, str)
        treeview = gtk.TreeView(self.liststore)
        textrenderer = gtk.CellRendererText()
        columns = (_('Download'), _('Language'), _('Rate'), _('Format'), _('Video'))
        for index, column in enumerate(columns):
            column = gtk.TreeViewColumn(column, textrenderer, text=index)
            column.set_sort_column_id(1)
            treeview.append_column(column)
        treeview.show()
        return treeview

    def fill_list(self, data):
        self.liststore.clear()
        for row in data:
            self.liststore.append([row[0], row[1], row[2], row[3], row[4]])

    def get_glade_tree(self):
        tree = gtk.glade.XML(Settings.glade)
        return tree

    def connect_all_signals(self):
        events = {'on_about_activate': self.on_about_activate,
                  'on_exit_activate': gtk.main_quit,
                  'on_main_destroy': gtk.main_quit}
        self.tree.signal_autoconnect(events)

    def on_path_changed(self, widget, path):
        files = Path.get_all_files(path)
        if files:
            data = list()
            for file in files:
                printable_file_name = os.path.basename(file)
                data.append((None, None, None, None, printable_file_name))
            self.fill_list(data)

    def on_about_activate(self, widget):
        response = self['aboutdialog'].run()
        if (response == gtk.RESPONSE_DELETE_EVENT or
            response == gtk.RESPONSE_CANCEL):
              self['aboutdialog'].hide()

    def test(self, *args, **kwargs):
        import ipdb;ipdb.set_trace()


class Path(object):
    supported_formats = ('3g2', '3gp', '3gp2', '3gpp', '60d', 'ajp', 'asf',
                         'asx', 'avchd', 'avi', 'bik', 'bix', 'box', 'cam',
                         'dat', 'divx', 'dmf', 'dv', 'dvr-ms', 'evo', 'flc',
                         'fli', 'flic', 'flv', 'flx', 'gvi', 'gvp', 'h264',
                         'm1v', 'm2p', 'm2ts', 'm2v', 'm4e', 'm4v', 'mjp',
                         'mjpeg', 'mjpg', 'mkv', 'moov', 'mov', 'movhd',
                         'movie', 'movx', 'mp4', 'mpe', 'mpeg', 'mpg', 'mpv',
                         'mpv2', 'mxf', 'nsv', 'nut', 'ogg', 'ogm', 'omf', 'ps',
                         'qt', 'ram', 'rm', 'rmvb', 'swf', 'ts', 'vfw', 'vid',
                         'video', 'viv', 'vivo', 'vob', 'vro', 'wm', 'wmv',
                         'wmx', 'wrap', 'wvx', 'wx', 'x264', 'xvid')

    @classmethod
    def is_compatible(cls, file_name):
        for format in cls.supported_formats:
            if file_name.endswith('.' + format):
                return True

    @classmethod
    def get_all_files(cls, path):
        files = os.listdir(path)
        result = list()
        for file in files:
            full_path = os.path.join(path, file)
            if os.path.isfile(full_path) and cls.is_compatible(file):
                result.append(full_path)
        return result

if __name__ == '__main__':
    gui = Gui()
    gtk.main()
