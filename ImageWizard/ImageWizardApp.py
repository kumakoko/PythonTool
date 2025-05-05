import wx
import ImageWizardMainDialog


class ImageWizardApp(wx.App):
    def OnInit(self):
        frame = ImageWizardMainDialog.ImageWizardMainDialog(None)  # 初始化应用程序
        frame.Show()
        return True


def main_win():
    app = ImageWizardApp()
    app.MainLoop()


if __name__ == "__main__":
    main_win()
