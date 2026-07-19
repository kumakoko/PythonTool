"""
Google Play 上架检查工具 - 主程序入口

本工具用于检查 Android 应用的 .so 文件是否符合 Google Play 的 16KB 对齐要求。
主要功能：
1. 配置 readelf 程序路径
2. 支持拖拽添加 .so 文件
3. 检查 .so 文件的 LOAD Segment 是否满足 16KB(0x4000) 对齐要求
4. 将检查结果输出到界面，通过和未通过的文件分别列出，未通过的用红色字体标出
"""

import wx
import sys
import io
import os

from MainDialog import MainDialog
from config_manager import ConfigManager
from checker import check_so_align


class OutputRedirector(io.StringIO):
    """
    控制台输出重定向器
    
    将标准输出(stdout)重定向到指定的 wx.ListBox 控件，
    使程序的 print 输出能够显示在界面上。
    """
    
    def __init__(self, listbox):
        """
        初始化输出重定向器
        
        Args:
            listbox: wx.ListBox 控件实例，用于显示输出内容
        """
        super().__init__()
        self.listbox = listbox

    def write(self, text):
        """
        重写 write 方法，将输出内容追加到 ListBox
        
        Args:
            text: 要输出的文本内容
        """
        super().write(text)
        # 将文本按换行符分割，逐行添加到 ListBox
        lines = text.strip().split('\n')
        for line in lines:
            if line.strip():
                # 使用 wx.CallAfter 确保在 GUI 线程中更新控件
                wx.CallAfter(self.listbox.Append, line.strip())


class GooglePlayChecker(MainDialog):
    """
    Google Play 检查工具主类
    
    继承自 wxFormBuilder 生成的 MainDialog，实现所有业务逻辑。
    """
    
    def __init__(self, parent):
        """
        初始化主窗口
        
        Args:
            parent: 父窗口实例，通常为 None
        """
        super().__init__(parent)
        # 初始化配置管理器
        self.config_manager = ConfigManager()
        # 初始化界面状态
        self._setup_ui()
        # 绑定事件处理函数
        self._setup_events()
        # 重定向控制台输出
        self._redirect_output()

    def _setup_ui(self):
        """
        设置界面初始状态
        
        从配置文件中读取上次保存的 readelf 路径，并设置到文件选择器中。
        """
        readelf_path = self.config_manager.get_readelf_path()
        if readelf_path:
            self.m_pickerReadElfFilePath.SetPath(readelf_path)

    def _setup_events(self):
        """
        绑定事件处理函数
        
        为各个控件绑定相应的事件处理方法：
        - 文件选择器变化事件
        - ListBox 文件拖放事件
        - 窗口关闭事件
        """
        # 绑定 readelf 路径选择器的变化事件
        self.m_pickerReadElfFilePath.Bind(wx.EVT_FILEPICKER_CHANGED, self.OnReadElfPathChanged)
        # 设置 ListBox 的拖放目标
        self.m_listBoxCheckedSoFiles.SetDropTarget(FileDropTarget(self))
        # 绑定窗口关闭事件，确保程序正确退出
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def _redirect_output(self):
        """
        重定向控制台输出
        
        将 sys.stdout 重定向到 OutputRedirector，
        使 print 语句的输出能够显示在界面的输出信息 ListBox 中。
        """
        self.original_stdout = sys.stdout
        self.output_redirector = OutputRedirector(self.m_listBoxOutputMesages)
        sys.stdout = self.output_redirector

    def OnClose(self, event):
        """
        窗口关闭事件处理
        
        确保程序退出时恢复标准输出，并正确退出Python解释器。
        
        Args:
            event: wx.CloseEvent 事件对象
        """
        # 恢复标准输出
        sys.stdout = self.original_stdout
        # 销毁对话框
        self.Destroy()
        # 确保Python解释器退出
        wx.Exit()

    def OnReadElfPathChanged(self, event):
        """
        readelf 路径变化事件处理
        
        当用户选择了新的 readelf 程序路径时，将路径保存到配置文件中。
        
        Args:
            event: wx.FilePickerEvent 事件对象
        """
        path = self.m_pickerReadElfFilePath.GetPath()
        self.config_manager.set_readelf_path(path)

    def OnFilesDropped(self, filenames):
        """
        文件拖放事件处理
        
        当用户将文件拖放到 ListBox 时，过滤出 .so 文件并添加到列表中。
        
        Args:
            filenames: 拖放的文件路径列表
        """
        for file in filenames:
            # 只处理 .so 文件
            if file.endswith('.so'):
                self.m_listBoxCheckedSoFiles.Append(file)

    def OnButtonGenerateClicked(self, event):
        """
        "转换并生成文件"按钮点击事件处理
        
        执行 .so 文件的 16KB 对齐检查，调用 readelf 程序检查每个 LOAD Segment 的对齐值。
        检查完成后，分别列出通过和未通过的文件，未通过的用红色字体标出。
        
        Args:
            event: wx.CommandEvent 事件对象
        """
        try:
            # 获取 readelf 程序路径
            readelf_path = self.m_pickerReadElfFilePath.GetPath()
            if not readelf_path:
                wx.MessageBox("请先选择readelf程序路径", "错误", wx.OK | wx.ICON_ERROR)
                return

            # 获取待检查的 so 文件列表
            so_files = [self.m_listBoxCheckedSoFiles.GetString(i) for i in range(self.m_listBoxCheckedSoFiles.GetCount())]
            if not so_files:
                wx.MessageBox("请先添加要检查的so文件", "错误", wx.OK | wx.ICON_ERROR)
                return

            # 输出检查开始信息
            print("开始检查so文件对齐...")
            print("-" * 60)

            # 保存通过和未通过的文件列表
            passed_files = []
            failed_files = []

            # 逐个检查 so 文件
            for so_file in so_files:
                passed, results = check_so_align(readelf_path, so_file)
                # 将检查结果输出到界面
                for result in results:
                    print(result)
                
                # 记录检查结果
                if passed:
                    passed_files.append(so_file)
                else:
                    failed_files.append(so_file)
                print()

            # 输出汇总结果
            print("=" * 60)
            print("检查结果汇总：")
            print("=" * 60)

            # 输出通过的文件列表
            if passed_files:
                print(f"\n通过检查的文件 ({len(passed_files)}个)：")
                print("-" * 40)
                for idx, file in enumerate(passed_files, 1):
                    print(f"  {idx}. {os.path.basename(file)}")

            # 输出未通过的文件列表（红色字体）
            if failed_files:
                print(f"\n未通过检查的文件 ({len(failed_files)}个)：")
                print("-" * 40)
                for idx, file in enumerate(failed_files, 1):
                    # 使用 ANSI 转义序列输出红色文本
                    print(f"  {idx}. \033[91m{os.path.basename(file)}\033[0m")

            # 输出最终检查结果
            print("\n" + "=" * 60)
            if not failed_files:
                print("所有文件检查通过！")
            else:
                print(f"共 {len(so_files)} 个文件，{len(passed_files)} 个通过，{len(failed_files)} 个未通过！")

        except Exception as e:
            # 捕获异常并弹出消息框通知用户
            wx.MessageBox(f"检查过程中发生错误: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def OnButtonClearSrcImageListBoxClicked(self, event):
        """
        "清空源图文件名"按钮点击事件处理
        
        清空待检查 so 文件列表。
        
        Args:
            event: wx.CommandEvent 事件对象
        """
        self.m_listBoxCheckedSoFiles.Clear()

    def OnButtonClearSrcOutputMessageClicked(self, event):
        """
        "清空输出消息"按钮点击事件处理
        
        清空输出信息列表。
        
        Args:
            event: wx.CommandEvent 事件对象
        """
        self.m_listBoxOutputMesages.Clear()


class FileDropTarget(wx.FileDropTarget):
    """
    文件拖放目标类
    
    继承自 wx.FileDropTarget，实现文件拖放功能。
    """
    
    def __init__(self, window):
        """
        初始化拖放目标
        
        Args:
            window: 主窗口实例，用于调用其 OnFilesDropped 方法
        """
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        """
        文件拖放事件处理
        
        当文件被拖放到控件上时，调用主窗口的 OnFilesDropped 方法处理。
        
        Args:
            x: 拖放位置的 x 坐标
            y: 拖放位置的 y 坐标
            filenames: 拖放的文件路径列表
            
        Returns:
            bool: True 表示接受拖放，False 表示拒绝
        """
        # 直接传递文件名列表给主窗口处理，不再创建 DropFilesEvent
        self.window.OnFilesDropped(filenames)
        return True


if __name__ == "__main__":
    """
    程序入口
    
    创建 wx.App 实例和主窗口，启动事件循环。
    """
    app = wx.App(False)
    dialog = GooglePlayChecker(None)
    dialog.Show(True)
    app.MainLoop()

    # 恢复标准输出并退出
    sys.stdout = dialog.original_stdout
    sys.exit(0)