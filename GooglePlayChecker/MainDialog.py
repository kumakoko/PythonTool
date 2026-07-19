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
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"上架GooglePlay检查工具", pos = wx.DefaultPosition, size = wx.Size( 1039,717 ), style = wx.DEFAULT_DIALOG_STYLE|wx.MINIMIZE_BOX )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetExtraStyle( wx.DIALOG_EX_METAL )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook5 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0|wx.TAB_TRAVERSAL )
		self.m_panel16KbAlignedChecker = wx.Panel( self.m_notebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText21 = wx.StaticText( self.m_panel16KbAlignedChecker, wx.ID_ANY, u"ReadElf程序路径", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		bSizer20.Add( self.m_staticText21, 0, wx.ALL, 5 )

		self.m_pickerReadElfFilePath = wx.FilePickerCtrl( self.m_panel16KbAlignedChecker, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 900,-1 ), wx.FLP_DEFAULT_STYLE )
		bSizer20.Add( self.m_pickerReadElfFilePath, 0, wx.ALL, 5 )


		bSizer9.Add( bSizer20, 1, wx.EXPAND, 5 )

		self.m_staticText6 = wx.StaticText( self.m_panel16KbAlignedChecker, wx.ID_ANY, u"要转换的so文件列表", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		bSizer9.Add( self.m_staticText6, 0, wx.ALL, 5 )

		m_listBoxCheckedSoFilesChoices = []
		self.m_listBoxCheckedSoFiles = wx.ListBox( self.m_panel16KbAlignedChecker, wx.ID_ANY, wx.DefaultPosition, wx.Size( 1000,200 ), m_listBoxCheckedSoFilesChoices, wx.LB_HSCROLL|wx.LB_MULTIPLE )
		bSizer9.Add( self.m_listBoxCheckedSoFiles, 0, wx.ALL, 5 )

		self.m_staticText2 = wx.StaticText( self.m_panel16KbAlignedChecker, wx.ID_ANY, u"输出信息", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer9.Add( self.m_staticText2, 0, wx.ALL, 5 )

		m_listBoxOutputMesagesChoices = []
		self.m_listBoxOutputMesages = wx.ListBox( self.m_panel16KbAlignedChecker, wx.ID_ANY, wx.DefaultPosition, wx.Size( 1000,300 ), m_listBoxOutputMesagesChoices, 0 )
		bSizer9.Add( self.m_listBoxOutputMesages, 0, wx.ALL, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_buttonCheck16KbAligned = wx.Button( self.m_panel16KbAlignedChecker, wx.ID_ANY, u"检查so文件对齐", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_buttonCheck16KbAligned, 0, wx.ALL, 5 )

		self.m_buttonClearCheckedSoFilesPath = wx.Button( self.m_panel16KbAlignedChecker, wx.ID_ANY, u"清空待检查的so文件列表", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_buttonClearCheckedSoFilesPath, 0, wx.ALL, 5 )

		self.m_buttonClearOutputMessage = wx.Button( self.m_panel16KbAlignedChecker, wx.ID_ANY, u"清空输出消息", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_buttonClearOutputMessage, 0, wx.ALL, 5 )


		bSizer9.Add( bSizer4, 1, wx.EXPAND, 5 )


		self.m_panel16KbAlignedChecker.SetSizer( bSizer9 )
		self.m_panel16KbAlignedChecker.Layout()
		bSizer9.Fit( self.m_panel16KbAlignedChecker )
		self.m_notebook5.AddPage( self.m_panel16KbAlignedChecker, u"so文件16KB对齐检查", True )
		self.m_panelZipAlignedCheck = wx.Panel( self.m_notebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer91 = wx.BoxSizer( wx.VERTICAL )


		self.m_panelZipAlignedCheck.SetSizer( bSizer91 )
		self.m_panelZipAlignedCheck.Layout()
		bSizer91.Fit( self.m_panelZipAlignedCheck )
		self.m_notebook5.AddPage( self.m_panelZipAlignedCheck, u"包体检查对齐", False )

		bSizer3.Add( self.m_notebook5, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer3 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_buttonCheck16KbAligned.Bind( wx.EVT_BUTTON, self.OnButtonGenerateClicked )
		self.m_buttonClearCheckedSoFilesPath.Bind( wx.EVT_BUTTON, self.OnButtonClearSrcImageListBoxClicked )
		self.m_buttonClearOutputMessage.Bind( wx.EVT_BUTTON, self.OnButtonClearSrcOutputMessageClicked )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def OnButtonGenerateClicked( self, event ):
		event.Skip()

	def OnButtonClearSrcImageListBoxClicked( self, event ):
		event.Skip()

	def OnButtonClearSrcOutputMessageClicked( self, event ):
		event.Skip()


