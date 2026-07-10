# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainDialog
###########################################################################

class MainDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"ImageWizard--图片处理百宝箱", pos = wx.DefaultPosition, size = wx.Size( 1039,751 ), style = wx.DEFAULT_DIALOG_STYLE|wx.MINIMIZE_BOX )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetExtraStyle( wx.DIALOG_EX_METAL )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook5 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0|wx.TAB_TRAVERSAL )
		self.m_panelBatchConvert = wx.Panel( self.m_notebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText6 = wx.StaticText( self.m_panelBatchConvert, wx.ID_ANY, u"要转换的源文件列表", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		bSizer9.Add( self.m_staticText6, 0, wx.ALL, 5 )

		m_listBoxSrcImageChoices = []
		self.m_listBoxSrcImage = wx.ListBox( self.m_panelBatchConvert, wx.ID_ANY, wx.DefaultPosition, wx.Size( 1000,200 ), m_listBoxSrcImageChoices, wx.LB_HSCROLL|wx.LB_MULTIPLE )
		bSizer9.Add( self.m_listBoxSrcImage, 0, wx.ALL, 5 )

		self.m_dirPickerOutputDir = wx.DirPickerCtrl( self.m_panelBatchConvert, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.Size( 1000,-1 ), wx.DIRP_DEFAULT_STYLE )
		bSizer9.Add( self.m_dirPickerOutputDir, 0, wx.ALL, 5 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3 = wx.StaticText( self.m_panelBatchConvert, wx.ID_ANY, u"选择透明色", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer11.Add( self.m_staticText3, 0, wx.ALL, 5 )

		self.m_colourPickerTransparent = wx.ColourPickerCtrl( self.m_panelBatchConvert, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		bSizer11.Add( self.m_colourPickerTransparent, 0, wx.ALL, 5 )

		self.m_checkBoxUseTransparentColor = wx.CheckBox( self.m_panelBatchConvert, wx.ID_ANY, u"启用透明色", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxUseTransparentColor.SetValue(True)
		bSizer11.Add( self.m_checkBoxUseTransparentColor, 0, wx.ALL, 5 )

		self.m_staticText4 = wx.StaticText( self.m_panelBatchConvert, wx.ID_ANY, u"设置输出放大倍数", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer11.Add( self.m_staticText4, 0, wx.ALL, 5 )

		self.m_textCtrlScale = wx.TextCtrl( self.m_panelBatchConvert, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.m_textCtrlScale, 0, wx.ALL, 5 )

		self.m_staticText5 = wx.StaticText( self.m_panelBatchConvert, wx.ID_ANY, u"输出格式", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer11.Add( self.m_staticText5, 0, wx.ALL, 5 )

		m_comboBoxSuffixChoices = []
		self.m_comboBoxSuffix = wx.ComboBox( self.m_panelBatchConvert, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_comboBoxSuffixChoices, 0 )
		bSizer11.Add( self.m_comboBoxSuffix, 0, wx.ALL, 5 )


		bSizer9.Add( bSizer11, 1, wx.EXPAND, 5 )

		self.m_staticText1 = wx.StaticText( self.m_panelBatchConvert, wx.ID_ANY, u"转换后的生成文件列表", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		bSizer9.Add( self.m_staticText1, 0, wx.ALL, 5 )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		m_listBoxOutputFilesChoices = []
		self.m_listBoxOutputFiles = wx.ListBox( self.m_panelBatchConvert, wx.ID_ANY, wx.DefaultPosition, wx.Size( 440,100 ), m_listBoxOutputFilesChoices, wx.LB_HSCROLL )
		bSizer8.Add( self.m_listBoxOutputFiles, 0, wx.ALL, 5 )

		bSizer92 = wx.BoxSizer( wx.VERTICAL )

		self.m_buttonAddProcessFiles = wx.Button( self.m_panelBatchConvert, wx.ID_ANY, u"<-添加已处理的图片", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer92.Add( self.m_buttonAddProcessFiles, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_buttonLoadClipInfoFile = wx.Button( self.m_panelBatchConvert, wx.ID_ANY, u"打开图片裁切信息文件->", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer92.Add( self.m_buttonLoadClipInfoFile, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer191 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText20 = wx.StaticText( self.m_panelBatchConvert, wx.ID_ANY, u"切片类型", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )

		bSizer191.Add( self.m_staticText20, 0, wx.ALL, 5 )

		m_comboBoxClipInfoChoices = []
		self.m_comboBoxClipInfo = wx.ComboBox( self.m_panelBatchConvert, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_comboBoxClipInfoChoices, 0 )
		bSizer191.Add( self.m_comboBoxClipInfo, 0, wx.ALL, 5 )


		bSizer92.Add( bSizer191, 1, wx.EXPAND, 5 )

		self.m_buttonDoClip = wx.Button( self.m_panelBatchConvert, wx.ID_ANY, u"执行切片", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer92.Add( self.m_buttonDoClip, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer8.Add( bSizer92, 1, wx.EXPAND, 5 )

		self.m_listCtrlClipInfo = wx.ListCtrl( self.m_panelBatchConvert, wx.ID_ANY, wx.DefaultPosition, wx.Size( 390,100 ), wx.LC_REPORT|wx.VSCROLL )
		bSizer8.Add( self.m_listCtrlClipInfo, 0, wx.ALL, 5 )


		bSizer9.Add( bSizer8, 1, wx.EXPAND, 5 )

		self.m_staticText2 = wx.StaticText( self.m_panelBatchConvert, wx.ID_ANY, u"输出信息", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer9.Add( self.m_staticText2, 0, wx.ALL, 5 )

		self.m_textCtrlOutputMessage = wx.TextCtrl( self.m_panelBatchConvert, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 1000,100 ), 0 )
		bSizer9.Add( self.m_textCtrlOutputMessage, 0, wx.ALL, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_buttonGenerate = wx.Button( self.m_panelBatchConvert, wx.ID_ANY, u"转换并生成文件", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_buttonGenerate, 0, wx.ALL, 5 )

		self.m_buttonClearSrcImageListBox = wx.Button( self.m_panelBatchConvert, wx.ID_ANY, u"清空源图文件名", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_buttonClearSrcImageListBox, 0, wx.ALL, 5 )

		self.m_buttonClearOutputFileListBox = wx.Button( self.m_panelBatchConvert, wx.ID_ANY, u"清空输出文件名", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_buttonClearOutputFileListBox, 0, wx.ALL, 5 )

		self.m_buttonClearOutputMessage = wx.Button( self.m_panelBatchConvert, wx.ID_ANY, u"清空输出消息", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_buttonClearOutputMessage, 0, wx.ALL, 5 )


		bSizer9.Add( bSizer4, 1, wx.EXPAND, 5 )


		self.m_panelBatchConvert.SetSizer( bSizer9 )
		self.m_panelBatchConvert.Layout()
		bSizer9.Fit( self.m_panelBatchConvert )
		self.m_notebook5.AddPage( self.m_panelBatchConvert, u"批量转换", True )
		self.m_panelImageViewAndGrid = wx.Panel( self.m_notebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer91 = wx.BoxSizer( wx.VERTICAL )

		self.m_scrolledWindowImageViewAndGrid = wx.ScrolledWindow( self.m_panelImageViewAndGrid, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,480 ), wx.BORDER_RAISED|wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindowImageViewAndGrid.SetScrollRate( 5, 5 )
		bSizer91.Add( self.m_scrolledWindowImageViewAndGrid, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_filePickerLoadImageForViewAndGrid = wx.FilePickerCtrl( self.m_panelImageViewAndGrid, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 500,-1 ), wx.FLP_DEFAULT_STYLE|wx.BORDER_SUNKEN )
		bSizer91.Add( self.m_filePickerLoadImageForViewAndGrid, 0, wx.ALL, 5 )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText7 = wx.StaticText( self.m_panelImageViewAndGrid, wx.ID_ANY, u"网格宽：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer6.Add( self.m_staticText7, 0, wx.ALL, 5 )

		self.m_textCtrlViewGridWidth = wx.TextCtrl( self.m_panelImageViewAndGrid, wx.ID_ANY, u"16", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB )
		bSizer6.Add( self.m_textCtrlViewGridWidth, 0, wx.ALL, 5 )

		self.m_staticText8 = wx.StaticText( self.m_panelImageViewAndGrid, wx.ID_ANY, u"网格高：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		bSizer6.Add( self.m_staticText8, 0, wx.ALL, 5 )

		self.m_textCtrlViewGridHeight = wx.TextCtrl( self.m_panelImageViewAndGrid, wx.ID_ANY, u"16", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB )
		bSizer6.Add( self.m_textCtrlViewGridHeight, 0, wx.ALL, 5 )

		self.m_checkBoxDrawViewGrid = wx.CheckBox( self.m_panelImageViewAndGrid, wx.ID_ANY, u"画网格线", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxDrawViewGrid.SetValue(True)
		bSizer6.Add( self.m_checkBoxDrawViewGrid, 0, wx.ALL, 5 )

		self.m_colourPickerGridLine = wx.ColourPickerCtrl( self.m_panelImageViewAndGrid, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		bSizer6.Add( self.m_colourPickerGridLine, 0, wx.ALL, 5 )


		bSizer91.Add( bSizer6, 1, wx.EXPAND, 5 )

		self.m_dirPickerSplitImagePath = wx.DirPickerCtrl( self.m_panelImageViewAndGrid, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.Size( 500,-1 ), wx.DIRP_DEFAULT_STYLE )
		bSizer91.Add( self.m_dirPickerSplitImagePath, 0, wx.ALL, 5 )

		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText71 = wx.StaticText( self.m_panelImageViewAndGrid, wx.ID_ANY, u"单片图宽：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText71.Wrap( -1 )

		bSizer61.Add( self.m_staticText71, 0, wx.ALL, 5 )

		self.m_textCtrlSplitCellWidth = wx.TextCtrl( self.m_panelImageViewAndGrid, wx.ID_ANY, u"16", wx.DefaultPosition, wx.Size( 20,-1 ), wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB )
		bSizer61.Add( self.m_textCtrlSplitCellWidth, 0, wx.ALL, 5 )

		self.m_staticText81 = wx.StaticText( self.m_panelImageViewAndGrid, wx.ID_ANY, u"单片图高：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText81.Wrap( -1 )

		bSizer61.Add( self.m_staticText81, 0, wx.ALL, 5 )

		self.m_textCtrlSplitCellHeight = wx.TextCtrl( self.m_panelImageViewAndGrid, wx.ID_ANY, u"16", wx.DefaultPosition, wx.Size( 25,-1 ), wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB )
		bSizer61.Add( self.m_textCtrlSplitCellHeight, 0, wx.ALL, 5 )

		self.m_staticText811 = wx.StaticText( self.m_panelImageViewAndGrid, wx.ID_ANY, u"输出缩放比例", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText811.Wrap( -1 )

		bSizer61.Add( self.m_staticText811, 0, wx.ALL, 5 )

		self.m_textCtrlCellOutputScale = wx.TextCtrl( self.m_panelImageViewAndGrid, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 25,-1 ), wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB )
		bSizer61.Add( self.m_textCtrlCellOutputScale, 0, wx.ALL, 5 )

		self.m_staticText711 = wx.StaticText( self.m_panelImageViewAndGrid, wx.ID_ANY, u"单片图名前缀", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText711.Wrap( -1 )

		bSizer61.Add( self.m_staticText711, 0, wx.ALL, 5 )

		self.m_textCtrlSplitCellName = wx.TextCtrl( self.m_panelImageViewAndGrid, wx.ID_ANY, u"32", wx.DefaultPosition, wx.Size( 50,-1 ), wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB )
		bSizer61.Add( self.m_textCtrlSplitCellName, 0, wx.ALL, 5 )

		self.m_buttonSplitImage = wx.Button( self.m_panelImageViewAndGrid, wx.ID_ANY, u"切割图片", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer61.Add( self.m_buttonSplitImage, 0, wx.ALL, 5 )


		bSizer91.Add( bSizer61, 1, wx.EXPAND, 5 )


		self.m_panelImageViewAndGrid.SetSizer( bSizer91 )
		self.m_panelImageViewAndGrid.Layout()
		bSizer91.Fit( self.m_panelImageViewAndGrid )
		self.m_notebook5.AddPage( self.m_panelImageViewAndGrid, u"预览图片和网格", False )
		self.m_panelTextImageGenerator = wx.Panel( self.m_notebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer29 = wx.BoxSizer( wx.VERTICAL )

		m_sizerTextImageWH = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText14 = wx.StaticText( self.m_panelTextImageGenerator, wx.ID_ANY, u"图片高度", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )

		m_sizerTextImageWH.Add( self.m_staticText14, 0, wx.ALL, 5 )

		self.m_TextImageHeight = wx.TextCtrl( self.m_panelTextImageGenerator, wx.ID_ANY, u"96", wx.DefaultPosition, wx.DefaultSize, 0 )
		m_sizerTextImageWH.Add( self.m_TextImageHeight, 0, wx.ALL, 5 )

		self.m_staticText15 = wx.StaticText( self.m_panelTextImageGenerator, wx.ID_ANY, u"图片宽度", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )

		m_sizerTextImageWH.Add( self.m_staticText15, 0, wx.ALL, 5 )

		self.m_TextImageWidth = wx.TextCtrl( self.m_panelTextImageGenerator, wx.ID_ANY, u"96", wx.DefaultPosition, wx.DefaultSize, 0 )
		m_sizerTextImageWH.Add( self.m_TextImageWidth, 0, wx.ALL, 5 )

		self.m_staticText26 = wx.StaticText( self.m_panelTextImageGenerator, wx.ID_ANY, u"字号", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )

		m_sizerTextImageWH.Add( self.m_staticText26, 0, wx.ALL, 5 )

		self.m_textFontSize = wx.TextCtrl( self.m_panelTextImageGenerator, wx.ID_ANY, u"12", wx.DefaultPosition, wx.DefaultSize, 0 )
		m_sizerTextImageWH.Add( self.m_textFontSize, 0, wx.ALL, 5 )


		bSizer29.Add( m_sizerTextImageWH, 1, wx.EXPAND, 5 )

		m_sizerTextImageAlign = wx.BoxSizer( wx.HORIZONTAL )

		m_radioTextImageAlignHChoices = [ u"靠左", u"居中", u"靠右" ]
		self.m_radioTextImageAlignH = wx.RadioBox( self.m_panelTextImageGenerator, wx.ID_ANY, u"文字水平方向对齐", wx.DefaultPosition, wx.DefaultSize, m_radioTextImageAlignHChoices, 1, wx.RA_SPECIFY_COLS )
		self.m_radioTextImageAlignH.SetSelection( 0 )
		m_sizerTextImageAlign.Add( self.m_radioTextImageAlignH, 0, wx.ALL, 5 )

		m_radioTextImageAlignWChoices = [ u"靠上", u"居中", u"靠下" ]
		self.m_radioTextImageAlignW = wx.RadioBox( self.m_panelTextImageGenerator, wx.ID_ANY, u"文字垂直方向对齐", wx.DefaultPosition, wx.DefaultSize, m_radioTextImageAlignWChoices, 1, wx.RA_SPECIFY_COLS )
		self.m_radioTextImageAlignW.SetSelection( 0 )
		m_sizerTextImageAlign.Add( self.m_radioTextImageAlignW, 0, wx.ALL, 5 )


		bSizer29.Add( m_sizerTextImageAlign, 1, wx.EXPAND, 5 )

		bSizer19 = wx.BoxSizer( wx.VERTICAL )

		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText16 = wx.StaticText( self.m_panelTextImageGenerator, wx.ID_ANY, u"输入文字内容", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )

		bSizer17.Add( self.m_staticText16, 0, wx.ALL, 5 )

		self.m_textSingleTextContent = wx.TextCtrl( self.m_panelTextImageGenerator, wx.ID_ANY, u"碧血照丹心", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.m_textSingleTextContent, 0, wx.ALL, 5 )

		self.m_btnGenerateSingleTextImage = wx.Button( self.m_panelTextImageGenerator, wx.ID_ANY, u"生成单张文字图片", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.m_btnGenerateSingleTextImage, 0, wx.ALL, 5 )


		bSizer19.Add( bSizer17, 1, wx.EXPAND, 5 )

		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText17 = wx.StaticText( self.m_panelTextImageGenerator, wx.ID_ANY, u"指定输出目录和文件名", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )

		bSizer18.Add( self.m_staticText17, 0, wx.ALL, 5 )

		self.m_filePickerOutputSingleTextImage = wx.FilePickerCtrl( self.m_panelTextImageGenerator, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		bSizer18.Add( self.m_filePickerOutputSingleTextImage, 0, wx.ALL, 5 )


		bSizer19.Add( bSizer18, 1, wx.EXPAND, 5 )

		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText18 = wx.StaticText( self.m_panelTextImageGenerator, wx.ID_ANY, u"选择图片背景颜色", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )

		bSizer20.Add( self.m_staticText18, 0, wx.ALL, 5 )

		self.m_colourPickerImageBG = wx.ColourPickerCtrl( self.m_panelTextImageGenerator, wx.ID_ANY, wx.Colour( 255, 255, 255 ), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		bSizer20.Add( self.m_colourPickerImageBG, 0, wx.ALL, 5 )

		self.m_staticText19 = wx.StaticText( self.m_panelTextImageGenerator, wx.ID_ANY, u"选择文字颜色", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )

		bSizer20.Add( self.m_staticText19, 0, wx.ALL, 5 )

		self.m_colourPickerTextColor = wx.ColourPickerCtrl( self.m_panelTextImageGenerator, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		bSizer20.Add( self.m_colourPickerTextColor, 0, wx.ALL, 5 )


		bSizer19.Add( bSizer20, 1, wx.EXPAND, 5 )


		bSizer29.Add( bSizer19, 1, wx.EXPAND, 5 )


		bSizer10.Add( bSizer29, 1, wx.EXPAND, 5 )

		bSizer30 = wx.BoxSizer( wx.VERTICAL )

		m_listBox3Choices = []
		self.m_listBox3 = wx.ListBox( self.m_panelTextImageGenerator, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox3Choices, 0 )
		bSizer30.Add( self.m_listBox3, 0, wx.ALL, 5 )


		bSizer10.Add( bSizer30, 1, wx.EXPAND, 5 )


		self.m_panelTextImageGenerator.SetSizer( bSizer10 )
		self.m_panelTextImageGenerator.Layout()
		bSizer10.Fit( self.m_panelTextImageGenerator )
		self.m_notebook5.AddPage( self.m_panelTextImageGenerator, u"文字图片生成器", False )

		bSizer3.Add( self.m_notebook5, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer3 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_checkBoxUseTransparentColor.Bind( wx.EVT_CHECKBOX, self.OnUseTransparentsChecked )
		self.m_buttonAddProcessFiles.Bind( wx.EVT_BUTTON, self.OnButtonAddProcessFilesClicked )
		self.m_buttonLoadClipInfoFile.Bind( wx.EVT_BUTTON, self.OnButtonLoadClipInfoFileClicked )
		self.m_buttonDoClip.Bind( wx.EVT_BUTTON, self.OnButtonDoClipClicked )
		self.m_buttonGenerate.Bind( wx.EVT_BUTTON, self.OnButtonGenerateClicked )
		self.m_buttonClearSrcImageListBox.Bind( wx.EVT_BUTTON, self.OnButtonClearSrcImageListBoxClicked )
		self.m_buttonClearOutputFileListBox.Bind( wx.EVT_BUTTON, self.OnButtonClearOutputFileListBoxClicked )
		self.m_buttonClearOutputMessage.Bind( wx.EVT_BUTTON, self.OnButtonClearSrcOutputMessageClicked )
		self.m_filePickerLoadImageForViewAndGrid.Bind( wx.EVT_FILEPICKER_CHANGED, self.OnImageViewAndGridFileChanged )
		self.m_textCtrlViewGridWidth.Bind( wx.EVT_TEXT_ENTER, self.OnTextCtrlViewGridWidthTextEnter )
		self.m_textCtrlViewGridHeight.Bind( wx.EVT_TEXT_ENTER, self.OnTextCtrlViewGridHeightTextEnter )
		self.m_checkBoxDrawViewGrid.Bind( wx.EVT_CHECKBOX, self.OnCheckBoxViewAndGrid )
		self.m_colourPickerGridLine.Bind( wx.EVT_COLOURPICKER_CHANGED, self.OnImageViewGridLineColorChanged )
		self.m_textCtrlSplitCellWidth.Bind( wx.EVT_TEXT_ENTER, self.OnTextCtrlViewGridWidthTextEnter )
		self.m_textCtrlSplitCellHeight.Bind( wx.EVT_TEXT_ENTER, self.OnTextCtrlViewGridHeightTextEnter )
		self.m_textCtrlCellOutputScale.Bind( wx.EVT_TEXT_ENTER, self.OnTextCtrlViewGridHeightTextEnter )
		self.m_textCtrlSplitCellName.Bind( wx.EVT_TEXT_ENTER, self.OnTextCtrlViewGridWidthTextEnter )
		self.m_buttonSplitImage.Bind( wx.EVT_BUTTON, self.OnButtonSplitImageClicked )
		self.m_btnGenerateSingleTextImage.Bind( wx.EVT_BUTTON, self.OnButtonClickGenerateSingleTextImage )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def OnUseTransparentsChecked( self, event ):
		event.Skip()

	def OnButtonAddProcessFilesClicked( self, event ):
		event.Skip()

	def OnButtonLoadClipInfoFileClicked( self, event ):
		event.Skip()

	def OnButtonDoClipClicked( self, event ):
		event.Skip()

	def OnButtonGenerateClicked( self, event ):
		event.Skip()

	def OnButtonClearSrcImageListBoxClicked( self, event ):
		event.Skip()

	def OnButtonClearOutputFileListBoxClicked( self, event ):
		event.Skip()

	def OnButtonClearSrcOutputMessageClicked( self, event ):
		event.Skip()

	def OnImageViewAndGridFileChanged( self, event ):
		event.Skip()

	def OnTextCtrlViewGridWidthTextEnter( self, event ):
		event.Skip()

	def OnTextCtrlViewGridHeightTextEnter( self, event ):
		event.Skip()

	def OnCheckBoxViewAndGrid( self, event ):
		event.Skip()

	def OnImageViewGridLineColorChanged( self, event ):
		event.Skip()





	def OnButtonSplitImageClicked( self, event ):
		event.Skip()

	def OnButtonClickGenerateSingleTextImage( self, event ):
		event.Skip()


