import wx


class ImageViewAndGrid:
    """图片查看器（组合模式，直接操作wx.ScrolledWindow）"""

    def __init__(self, scrolled_win, w_interval=32, h_interval=32):
        # 创建内部的 ScrolledWindow（不再依赖wx.Panel）
        self.scrolled_win = scrolled_win
        self.scrolled_win.SetScrollRate(10, 10)  # 设置滚动步长
        self.w_interval = 50
        self.h_interval = 50
        self.m_Bitmap = None
        self.isDrawViewGrid = True
        self.m_GridLineColor = wx.RED
        self.m_wxImageContent = None

        # 绑定事件
        self.scrolled_win.Bind(wx.EVT_PAINT, self.on_paint)

    def set_w_interval(self,w_interval):
        self.w_interval = w_interval

    def set_h_interval(self, h_interval):
        self.h_interval = h_interval

    def SetIsDrawViewGrid(self,draw):
        self.isDrawViewGrid = draw

    def GetIsDrawViewGrid(self):
        return self.isDrawViewGrid

    def RefreshWindow(self):
        self.scrolled_win.Refresh()

    def SetGridLineColor(self,c):
        self.m_GridLineColor = c

    def load_image(self, path):
        """加载图片并更新滚动区域"""
        self.m_wxImageContent = wx.Image(path)
        if not self.m_wxImageContent.IsOk():
            self.m_wxImageContent = None
            wx.MessageBox("无法加载图片！", "错误", wx.OK | wx.ICON_ERROR)
            return

        self.m_Bitmap = wx.Bitmap(self.m_wxImageContent)
        self.scrolled_win.SetVirtualSize(self.m_Bitmap.GetSize())
        self.scrolled_win.Refresh()

    def on_paint(self, event):
        """绘制图片和网格线"""
        dc = wx.PaintDC(self.scrolled_win)
        self.scrolled_win.DoPrepareDC(dc)  # 处理滚动偏移

        if not self.m_Bitmap:
            return

        # 绘制图片
        dc.DrawBitmap(self.m_Bitmap, 0, 0, True)

        if not self.isDrawViewGrid:
            return

        # 设置网格线样式
        dc.SetPen(wx.Pen(wx.RED, 1))
        width, height = self.m_Bitmap.GetWidth(), self.m_Bitmap.GetHeight()

        # 绘制垂直线（每隔w_interval像素）
        for x in range(0, width, self.w_interval):
            dc.DrawLine(x, 0, x, height)

        # 绘制水平线（每隔h_interval像素）
        for y in range(0, height, self.h_interval):
            dc.DrawLine(0, y, width, y)