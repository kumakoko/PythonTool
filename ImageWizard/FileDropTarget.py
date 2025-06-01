import wx


class FileDropTarget(wx.FileDropTarget):
    def __init__(self, listbox):
        super().__init__()
        self.listbox = listbox  # 关联的 ListBox

    # OnDropFiles 是核心方法，参数 filenames 是拖放的文件路径列表。
    def OnDropFiles(self, x, y, filenames):
        for file in filenames:
            self.listbox.Append(file)  # 将文件路径添加到 ListBox
        return True  # 返回 True 表示处理成功
