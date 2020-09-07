import win32con
import win32gui
import win32api
import time
import os
import subprocess

qingtian_name="书签获取小工具2015.05.05  【晴天软件】"
target_dir=r"D:\All_SS_bookmarks"
qingtian_path=r"D:\qtrj.exe"

def get_hd_from_child_hds(father_hd,some_idx,expect_name):
    child_hds=[]
    win32gui.EnumChildWindows(father_hd,lambda hwnd, param: param.append(hwnd),child_hds)

    names=[win32gui.GetWindowText(each) for each in child_hds]
    hds=[hex(each) for each in child_hds]
    print("ChildName List:",names)
    print("Child Hds List:",hds)

    name=names[some_idx]
    hd=hds[some_idx]

    print("The {} Child.".format(some_idx))
    print("The Name:{}".format(name))
    print("The HD:{}".format(hd))

    if name==expect_name:
        return child_hds[some_idx]
    else:
        print("窗口不对！")
        return None

def save_catalog_from_ss(ss):
    os.startfile(qingtian_path)
    time.sleep(1)
    ori_ss=ss
    qingtian_hd=win32gui.FindWindowEx(None,0,0,qingtian_name)
    feedSS_hd=get_hd_from_child_hds(qingtian_hd,6,'')
    win32gui.SendMessage(feedSS_hd,win32con.WM_SETTEXT,0,ss)
    print("gg")
    time.sleep(0.5)
    # huoquzhong_hd=get_hd_from_child_hds(qingtian_hd,5,"获取")
    # cnt=0
    # while cnt!=5:
    bookmark_hd=get_hd_from_child_hds(qingtian_hd,1,'')
    # time.sleep(0.5)
        # cnt+=1
        # time.sleep(0.5)
    # https: // blog.csdn.net / qq_41928442 / article / details / 88937337
    length = win32gui.SendMessage(bookmark_hd, win32con.WM_GETTEXTLENGTH)*3
    # length = win32gui.SendMessage(bookmark_hd, win32con.WM_GETTEXTLENGTH)*1
    time.sleep(0.5)
    buf = win32gui.PyMakeBuffer(length)
    #发送获取文本请求
    win32api.SendMessage(bookmark_hd, win32con.WM_GETTEXT, length, buf)
    time.sleep(0.5)
    #下面应该是将内存读取文本
    address, length = win32gui.PyGetBufferAddressAndLen(buf[:-1])
    # time.sleep(0.5)
    text = win32gui.PyGetString(address, length)
    # time.sleep(0.5)
    error_line="没有查询到此SS的书签！"
    if error_line in text:
        ss="error_"+ss
    try:
        with open(target_dir+os.sep+ss+".txt","w",encoding="utf-8") as f:
            f.write(text)
        with open(target_dir+os.sep+"already_save.txt","a",encoding="utf-8") as f:
            f.write(ori_ss+"\n")
    except Exception:
        pass
    win32gui.PostMessage(qingtian_hd,win32con.WM_CLOSE,0,0)
    time.sleep(1)


def main():
    # SW_MINIMIZE = 6
    # info = subprocess.STARTUPINFO()
    # info.dwFlags = subprocess.STARTF_USESHOWWINDOW
    # info.wShowWindow = SW_MINIMIZE
    # subprocess.Popen(qingtian_path, startupinfo=info)
    if os.path.exists(target_dir+os.sep+"already_save.txt"):
        with open(target_dir+os.sep+"already_save.txt","r",encoding="utf-8") as f:
            start_val=int(f.readlines()[-1].replace("\n",""))
    else:
        start_val=10**7
    # some_ss=[10400487,12527673,12205452,12790775,12866829]
    # some_ss2=[some_ss[0]]
    for each in range(start_val,10**8):
        if isinstance(each,int):
            ss=str(each)
        save_catalog_from_ss(ss)
        print("one done")

        # os.system("taskkill /F {}".format(qingtian_path))
        time.sleep(2)
    print("all done.")

if __name__ == '__main__':
    main()


