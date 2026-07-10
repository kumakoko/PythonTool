import wx
import os


class FileDropTarget(wx.FileDropTarget):
    def __init__(self, listbox, dir_picker=None):
        super().__init__()
        self.listbox = listbox
        self.dir_picker = dir_picker

    def OnDropFiles(self, x, y, filenames):
        for file in filenames:
            self.listbox.Append(file)

        if filenames and self.dir_picker:
            first_file_path = filenames[0]
            dir_path = os.path.dirname(first_file_path)
            self.dir_picker.SetPath(dir_path)

        return True
