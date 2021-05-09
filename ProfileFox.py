import tkinter as tk
import os
import sys
import copy
import subprocess
import admin
from time import sleep
import math

def get_profiles():
    directory = os.path.join(os.environ["LOCALAPPDATA"], 'Mozilla', 'Firefox', 'Profiles')
    #print(directory)
    files = os.listdir(directory)
    #print(files)
    files = list(filter(lambda x: os.path.isdir(os.path.join(directory, x)), files))
    #print(files)
    files = list(map(lambda x: x.split('.')[-1], files))
    #files = list(range(30)) # inject "profiles"
    #print(files)
    return files

def center(win):
    #Sto... taken from https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
    # answer by Honest Abe. Asssumed to be under a public license
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    #win.deiconify()

def build_gui(profiles):
    root = tk.Tk()
    scaling = 2
    root.tk.call('tk', 'scaling', scaling)
    root.title("Pick a profile to run")
    
    var1 = tk.IntVar(master=root, value=1)
    text = ''
    if len(sys.argv) > 1:
        text = 'Opening URL: ' + sys.argv[1]
    else:
        text = 'Opening firefox'
    tk.Label(root, 
              justify=tk.CENTER,
              padx = 10,
              pady = 20,
              text=text).pack(side="top")
    #scroll = tk.Scrollbar(root)
    #scroll.pack(side=tk.LEFT, fill=tk.Y)
    #frame = tk.Canvas(root, yscrollcommand=scroll.set)
    frame = tk.Frame(root)
    frame.pack(side="top",
               padx=20)

    #NOTE: hardcoded values.
    #NOTE: Past avihay managed to fox it from the root window, but now this is hardcoded here
    window_static_height = 150 * scaling
    per_line_height = 27 * scaling
    #scroll.config(command=frame.yview)
    rowPerCol = int((root.winfo_screenheight() -
                 window_static_height) / per_line_height)
    for pro, index in zip(profiles, range(len(profiles))):
        #print(pro)
        def h(name):
            def i():
                run_profile(name)
                if var1.get() == 1:
                    root.destroy()
            return i
        def j(name):
            def i():
                subprocess.run(["cmd", "/c", "taskkill", '/F', '/IM', 'FF_' + name + '.exe'])
            return i
        vcol = int(index/rowPerCol) # the supercolumn number of the the two columns of the buttons
        vrow = int(index%rowPerCol)
        tk.Button(frame,
                    text='☠',
                    padx = 5,
                    pady = 5,
                  command=j(pro)).grid(row=vrow, column=vcol*3+0)
        tk.Button(frame,
                    text=pro,
                    padx = 5,
                    pady = 5,
                  command=h(pro)).grid(sticky=tk.W, row=vrow, column=vcol*3+1)
    for index in range(math.ceil(len(profiles)/rowPerCol)-1): # -1 == no need for space after first column
        frame.grid_columnconfigure(index*3+2, minsize=20)
    quit = tk.Button(root,
                    text="Q\u0332uit",
                    padx = 5,
                    pady = 5,
                    command = root.destroy)
    quit.pack(side="top",
                fill=tk.X,
                padx=25,
                pady=5)
    tk.Checkbutton(root, text="Close after selecting profile", variable=var1).pack(side="top",
                fill=tk.X,
                padx=25,
                pady=1)
    root.bind('<q>', lambda x: root.destroy())
    center(root)
    root.update()
    #frame.config(scrollregion=(0, 0, 1000, 1000))
    raise_above_all(root)
    #root.update()
    #root.grab_set()
    #root.focus()
    root.focus_set()
    #root.focus_force()
    #root.update()
    root.after(3000,root.focus_set)
    #root.after_idle(root.after, 1, root.wm_deiconify)
    root.mainloop()

def raise_above_all(window):
    window.attributes('-topmost', True)
    window.after_idle(window.attributes,'-topmost',False)

def run_profile(profile):
    # admin.run_as_admin(
    #     ['cmd', '/C', 'echo', 'ff fullname', '&', 'timeout', '5', '&&', 'exit'], debug=True) #exec test

    def makecopy(ff, filename):
        admin.run_as_admin(
            ['cmd', '/C', 'copy', ff, fullname, '&', 'timeout', '5','&&', 'taskkill', '-f', '-im', 'profilefox.exe','&&', 'exit'], debug=True)
        sleep(5000)
    directory = os.getcwd()
    # if not os.path.exists(directory):
    #     os.mkdir(directory)
    ff = os.path.join(directory, 'Firefox.exe')
    filename = 'FF_' + profile + '.exe'
    fullname = os.path.join(directory, filename)
    print(fullname)
    if not os.path.exists(fullname) or os.path.getmtime(fullname) < os.path.getmtime(ff):
        makecopy(ff, filename)
    
    subprocess.run([fullname, '-P', profile, '-foreground', '--no-remote'] + sys.argv[1:])

if __name__ == "__main__":
    profiles = get_profiles()
    profiles.sort()   
    build_gui(profiles)
    pass
