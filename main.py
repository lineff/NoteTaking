import wx
import os
from widget.file_op import WinFactory

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600))
        self.SetBackgroundColour("#006400")
        self.current_folder = ""

        # 创建一个垂直布局的主容器，并将其设置为窗体的主布局管理器
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_sizer)

        # 创建一个水平布局的容器，用于将树状组件和预览窗格放置在同一行
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        butbox = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(hbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        # 创建按钮，用于打开文件夹选择对话框
        button = wx.Button(self, wx.ID_ANY, "Open Folder")
        butbox.Add(button, proportion=0, flag=wx.ALL|wx.CENTER, border=5)
        new_folder_btn = wx.Button(self, wx.ID_ANY, "New Folder")
        butbox.Add(new_folder_btn, proportion=0, flag=wx.ALL|wx.CENTER, border=5)
        button2 = wx.Button(self, wx.ID_ANY, "New File")
        butbox.Add(button2, proportion=0, flag=wx.ALL|wx.CENTER, border=5)
        button1 = wx.Button(self, wx.ID_ANY, "Save File")
        button1.SetBackgroundColour("#FF0000")
        butbox.Add(button1, proportion=0, flag=wx.ALL|wx.CENTER, border=5)
        refresh_btn = wx.Button(self, wx.ID_ANY, "Reload")
        butbox.Add(refresh_btn, proportion=0, flag=wx.ALL|wx.CENTER, border=5)
        hbox.Add(butbox, proportion=0, flag=wx.ALL, border=5)

        # 创建一个树状组件，用于显示指定目录中的所有文件
        self.tree = wx.TreeCtrl(self, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
        self.root = self.tree.AddRoot("Root")
        hbox.Add(self.tree, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        # hbox.Add(butbox, proportion=0, flag=wx.ALL, border=5)


        # 创建一个预览窗格，用于显示选定的图像文件
        # self.preview = wx.StaticBitmap(self, wx.ID_ANY, wx.NullBitmap)
        self.preview = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.HSCROLL)
        # 设置字体大小
        font = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL)  # 12是字体大小
        self.preview.SetFont(font)
        self.preview.SetForegroundColour("#006400")
        hbox.Add(self.preview, proportion=4, flag=wx.EXPAND | wx.ALL, border=5)

        # 将按钮的单击事件绑定到处理函数self.on_open_folder()上
        button.Bind(wx.EVT_BUTTON, self.on_open_folder)
        button1.Bind(wx.EVT_BUTTON, self.on_save_file)
        button2.Bind(wx.EVT_BUTTON, self.on_new_file)
        new_folder_btn.Bind(wx.EVT_BUTTON, self.on_new_folder)
        refresh_btn.Bind(wx.EVT_BUTTON, self.refresh_tree)
        

        # 将树状组件的选中事件绑定到处理函数self.on_tree_select()上
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_tree_select, self.tree)

        # 显示窗体
        self.Centre()
        self.Show(True)

    def create_tree(self, parent, path):
        # 递归地向树状组件中添加指定目录中的所有文件和子目录
        for item in os.listdir(path):
            fullpath = os.path.join(path, item)
            # print("item:%s" % item)
            if os.path.isdir(fullpath):
                node = self.tree.AppendItem(parent, item)
                self.tree.SetItemTextColour(node, "#006400")
                self.create_tree(node, fullpath)
            else:
                ext = os.path.splitext(fullpath)[1].lower()
                if ext in [".txt", ".bat"]:
                    self.tree.AppendItem(parent, item, data=fullpath)

    def on_open_folder(self, event):
        # 处理打开文件夹按钮的单击事件，打开文件夹选择对话框并更新树状组件
        dialog = wx.DirDialog(self, "Select a folder")
        if dialog.ShowModal() == wx.ID_OK:
            self.tree.DeleteChildren(self.root)
            self.create_tree(self.root, dialog.GetPath())
        # print("root-----------")
        # print(dialog.GetPath())
        self.SetTitle(dialog.GetPath())
        self.current_folder = dialog.GetPath()
        self.root_path = dialog.GetPath()
        dialog.Destroy()

    def on_save_file(self, event):
        print("current file:%s" % self.filepath)
        text = self.preview.GetValue()
        print("input text: %s " % text)
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(text)

    def on_new_file(self, event):
        print("current folder:%s" % self.current_folder)
        WinFactory.open_win("file", self.current_folder, self.fresh)

    def on_new_folder(self, event):
        print("----------new folder")
        print("current folder:%s" % self.current_folder)
        WinFactory.open_win("folder", self.current_folder, self.fresh)

    def refresh_tree(self, event):
        self.fresh()

    def fresh(self):
        print("call fresh=============")
        self.tree.DeleteChildren(self.root)
        self.create_tree(self.root, self.root_path)
        


    def on_tree_select(self, event):
        # 处理树状组件的选中事件，更新预览窗格中的图像文件
        item = event.GetItem()
        if item:
            self.filepath = self.tree.GetItemData(item)
            name = self.tree.GetItemText(item)
            # print("name:%s current_folder:%s" % (name, self.current_folder))
            if os.path.isdir(os.path.join(self.root_path, name)):
                self.current_folder = os.path.join(self.root_path, name)
                print("+++current folder:%s" % self.current_folder)
            if self.filepath:
                print("current file:%s" % self.filepath)
                # self.current_folder = os.path.dirname(self.filepath)
                with open(self.filepath, 'r', encoding="utf-8") as file:
                    self.preview.SetValue(file.read())
                    self.SetTitle(self.filepath)
                # image = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
                # self.preview.SetBitmap(wx.Bitmap(image))
            # else:
            #     # file_f = wx.Frame(None, title="test", size=(300, 200))
            #     # file_text = wx.TextCtrl(file_f)
            #     # file_f.Show()
            #     print("click folder")

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame(None, "Study Hard")
    app.MainLoop()
