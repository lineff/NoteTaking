import wx
import os

class MyFrame(wx.Frame):
    
    def __init__(self, file_folder, fresh):
        wx.Frame.__init__(self)
        self.file_folder = file_folder
        self.fresh = fresh
        self.OnCloseMe()
         
    def OnCloseMe(self):
        dlg = wx.TextEntryDialog(None, u"file name:", u"New File", u"temp.txt")
        if dlg.ShowModal() == wx.ID_OK:
            # print("ok")
            message = dlg.GetValue() #获取文本框中输入的值
            new_msg = "None"
            create_flag = True
            if "." not in message:
                message = message + ".txt"
            if ".txt" not in message:
                new_msg = "unsupport file type:%s" % message
                create_flag = False
            else:
                new_msg = "file:%s add successfully!" % os.path.join(self.file_folder, message)
            if create_flag:
                file_path = os.path.join(self.file_folder, message)
                self.create_new_file(file_path)
                self.fresh()
            dlg_tip = wx.MessageDialog(None, new_msg, u"Result", wx.OK | wx.ICON_INFORMATION)
            if dlg_tip.ShowModal() == wx.ID_OK:
                self.Close(True)
            dlg_tip.Destroy()
        else:
            self.Close(True)
        dlg.Destroy()    

    def create_new_file(self, file_path):
        print("create_new_file:")
        print(file_path)
        try:
            f = open(file_path, "w", encoding="utf-8")
            f.close()
        except FileExistsError:
            print("file alreay exists")


class FolderFrame(wx.Frame):
    
    def __init__(self, file_folder, fresh):
        wx.Frame.__init__(self)
        self.file_folder = file_folder
        self.fresh = fresh
        self.OnCloseMe()
         
    def OnCloseMe(self):
        dlg = wx.TextEntryDialog(None, u"folder name:", u"New Folder", u"temp")
        if dlg.ShowModal() == wx.ID_OK:
            # print("ok")
            message = dlg.GetValue() #获取文本框中输入的值
            new_msg = "None"
            create_flag = True
            if len(message) > 15:
                new_msg = "name too long:%s" % message
                create_flag = False
            else:
                new_msg = "folder:%s add successfully!" % os.path.join(self.file_folder, message)
            if create_flag:
                self.file_folder = os.path.join(self.file_folder, message)
                self.create_folder(self.file_folder)
                self.fresh()
            dlg_tip = wx.MessageDialog(None, new_msg, u"Result", wx.OK | wx.ICON_INFORMATION)
            if dlg_tip.ShowModal() == wx.ID_OK:
                self.Close(True)
            dlg_tip.Destroy()
        else:
            self.Close(True)
        dlg.Destroy()

    def create_folder(self, folder_path):
        print("ceate folder:")
        print(folder_path)
        try:
            os.mkdir(folder_path)
        except Exception as e:
            print('create folder fail:%s' % e)

def new_file_win(folder_path, fresh):
    app = wx.App()
    MyFrame(folder_path, fresh)
    app.MainLoop()

def new_folder_win(folder_path, fresh):
    app = wx.App()
    FolderFrame(folder_path, fresh)
    app.MainLoop()  

class WinFactory(object):
    @staticmethod
    def open_win(*args):
        t = args[0]
        folder_path = args[1]
        fresh = args[2]
        if t == "folder":
            new_folder_win(folder_path, fresh)
        elif t == "file":
            new_file_win(folder_path, fresh)
        else:
            print("unkonwn type:%s" % t)

            
# if __name__ == '__main__':
#     WinFactory.open_win("file", "E:\\PyProjects\\Notepad\\test", None)
#     new_file_win("E:\\PyProjects\\Notepad\\test")