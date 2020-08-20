import wx
import wx.xrc


class MainFrame(wx.Frame):
 
    def __init__(self, parent):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"FACE RECOGNIZER", pos = wx.DefaultPosition, size = wx.Size( 500,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHints( wx.Size( 500,500 ), wx.DefaultSize )
        self.Colour()
        self.m_menubar = wx.MenuBar( 0 )
        self.m_menu_file = wx.Menu()
        self.m_menuItem_exit = wx.MenuItem( self.m_menu_file, wx.ID_ANY, u"Exit"+ u"\t" + u"F1", u"exit program", wx.ITEM_NORMAL )
        self.m_menu_file.Append( self.m_menuItem_exit )

        self.m_menubar.Append( self.m_menu_file, u"File" )

        self.m_menu_about = wx.Menu()
        self.m_menuItem_about = wx.MenuItem( self.m_menu_about, wx.ID_ANY, u"Tutorial", u"tutorial program", wx.ITEM_NORMAL )
        self.m_menu_about.Append( self.m_menuItem_about )

        self.m_menubar.Append( self.m_menu_about, u"Tutorial" )

        self.SetMenuBar( self.m_menubar )

        self.m_statusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
        bSizer = wx.BoxSizer( wx.VERTICAL )

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button_run = wx.Button( self, wx.ID_ANY, u"RUN", size=(100,100) )

        self.m_button_run.SetBitmapFocus( wx.NullBitmap )
        self.m_button_run.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_button_run.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.m_button_run.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )

        bSizer3.Add( self.m_button_run, 0, wx.ALL, 30 )

        self.m_button_train_dataset = wx.Button( self, wx.ID_ANY, u"TRAIN", size=(100, 100) )
        self.m_button_train_dataset.SetBitmapFocus( wx.NullBitmap )
        self.m_button_train_dataset.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_button_train_dataset.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.m_button_train_dataset.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )

        bSizer3.Add( self.m_button_train_dataset, 0, wx.ALL, 30 )

        self.m_button_create_dataset = wx.Button( self, wx.ID_ANY, u"CREATE", size=(100, 100) )
        self.m_button_create_dataset.SetBitmapFocus( wx.NullBitmap )
        self.m_button_create_dataset.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_button_create_dataset.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.m_button_create_dataset.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )

        bSizer3.Add( self.m_button_create_dataset, 0, wx.ALL, 30 )
        self.SetSizer(bSizer3)

        #connect events
        self.Bind( wx.EVT_MENU, self.m_menuItem_exitOnMenuSelection, id = self.m_menuItem_exit.GetId() )
        self.Bind( wx.EVT_MENU, self.m_menuItem_aboutOnMenuSelection, id = self.m_menuItem_about.GetId() )
        self.Bind( wx.EVT_CLOSE, self.mainframeOnClose )
        self.m_button_run.Bind( wx.EVT_BUTTON, self.m_button_runOnButtonClick )
        self.m_button_train_dataset.Bind( wx.EVT_BUTTON, self.m_button_train_datasetOnButtonClick )
        self.m_button_create_dataset.Bind( wx.EVT_BUTTON, self.m_button_create_datasetOnButtonClick )

    def m_menuItem_exitOnMenuSelection( self, event ):
        event.Skip()
    def m_menuItem_aboutOnMenuSelection( self, event ):
        event.Skip()
    def Colour(self):
        self.SetBackgroundColour('#EFFBFB')
    def __del__( self ):
        pass
    def mainframeOnClose( self, event ):
        event.Skip()
    def m_button_runOnButtonClick( self, event ):
        event.Skip()

    def m_button_train_datasetOnButtonClick( self, event ):
        event.Skip()

    def m_button_create_datasetOnButtonClick( self, event ):
        event.Skip()

class Getdata(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Thông Tin Cá nhân", pos = wx.DefaultPosition, size = wx.Size( 300,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHints( wx.Size(300,300 ), wx.DefaultSize )


        bSizer = wx.BoxSizer( wx.VERTICAL )

        #label id
        self.id_staticText = wx.StaticText(self, wx.ID_ANY, "ID:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.id_staticText.Wrap( -1 )
        bSizer.Add( self.id_staticText, 0, wx.LEFT, 50 )
        #input ID
        self.id_textCtrl = wx.TextCtrl( self, 0, wx.EmptyString, wx.DefaultPosition, wx.Size(150,20 ), 0 )
        bSizer.Add( self.id_textCtrl, 0, wx.LEFT, 70 )
        
        #label name
        self.name_staticText = wx.StaticText(self, wx.ID_ANY, "Name:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.name_staticText.Wrap( -1 )
        bSizer.Add( self.name_staticText, 0, wx.LEFT, 50 )
        #input name
        self.name_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(150,20 ), 0 )
        bSizer.Add( self.name_textCtrl, 0, wx.LEFT, 70 )

        self.gender_staticText = wx.StaticText(self, wx.ID_ANY, "Gender:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.gender_staticText.Wrap( -1 )
        bSizer.Add( self.gender_staticText, 0, wx.LEFT, 50 )
        self.gender_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(150,20 ), 0 )
        bSizer.Add( self.gender_textCtrl, 0, wx.LEFT, 70 )

        self.date_staticText = wx.StaticText(self, wx.ID_ANY, "Date of Birth:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.date_staticText.Wrap( -1 )
        bSizer.Add( self.date_staticText, 0, wx.LEFT, 50 )
        self.date_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(150,20 ), 0 )
        bSizer.Add( self.date_textCtrl, 0, wx.LEFT, 70 )

        self.phone_staticText = wx.StaticText(self, wx.ID_ANY, "Phone Number:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.phone_staticText.Wrap( -1 )
        bSizer.Add( self.phone_staticText, 0, wx.LEFT, 50 )
        self.phone_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(150,20 ), 0 )
        bSizer.Add( self.phone_textCtrl, 0, wx.LEFT, 70 )

        self.position_staticText = wx.StaticText(self, wx.ID_ANY, "Posotion:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.position_staticText.Wrap( -1 )
        bSizer.Add( self.position_staticText, 0, wx.LEFT, 50 )
        self.position_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(150,20 ), 0 )
        bSizer.Add( self.position_textCtrl, 0, wx.LEFT, 70 )

        self.salary_staticText = wx.StaticText(self, wx.ID_ANY, "Salary:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.salary_staticText.Wrap( -1 )
        bSizer.Add( self.salary_staticText, 0, wx.LEFT, 50 )
        self.salary_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(150,20 ), 0 )
        bSizer.Add( self.salary_textCtrl, 0, wx.LEFT, 70 )


		
        m_sdbSizer = wx.StdDialogButtonSizer()
        self.m_sdbSizerOK = wx.Button( self, wx.ID_OK, size = (50,30) )
        m_sdbSizer.AddButton( self.m_sdbSizerOK )
        self.m_sdbSizerCancel = wx.Button( self, wx.ID_CANCEL, size = (50,30) )
        m_sdbSizer.AddButton( self.m_sdbSizerCancel )
        m_sdbSizer.Realize()

        bSizer.Add( m_sdbSizer, 1, wx.EXPAND, 5 )
        self.SetSizer( bSizer )
        self.Layout()
        bSizer.Fit( self )

        self.Centre( wx.BOTH )  

		# Connect Events
        self.m_sdbSizerCancel.Bind( wx.EVT_BUTTON, self.m_sdbSizerOnCancelButtonClick )
        self.m_sdbSizerOK.Bind( wx.EVT_BUTTON, self.m_sdbSizerOnOKButtonClick )

    def __del__( self ):
        pass

	# Virtual event handlers, overide them in your derived class
    def m_sdbSizerOnCancelButtonClick( self, event ):
        event.Skip()

    def m_sdbSizerOnOKButtonClick( self, event ):
        event.Skip()