import tkinter as tk
import os
import sys
import copy
import subprocess
import admin
from time import sleep

def get_profiles():
    directory = os.path.join(os.environ["LOCALAPPDATA"], 'Mozilla', 'Firefox', 'Profiles')
    #print(directory)
    files = os.listdir(directory)
    #print(files)
    files = list(filter(lambda x: os.path.isdir(os.path.join(directory, x)), files))
    #print(files)
    files = list(map(lambda x: x.split('.')[-1], files))
    #print(files)
    return files

def build_gui(profiles):
    root = tk.Tk()
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
              pady = 50,
              text=text).pack(side="top")
    for pro in profiles:
        #print(pro)
        def h(name):
            def i():
                run_profile(name)
                if var1.get() == 1:
                    root.destroy()
            return i

        tk.Button(root,
                    text=pro,
                    padx = 5,
                    pady = 5,
                    command = h(pro)).pack(side="top",
                                            fill=tk.X,
                                            padx=25,
                                            pady=5)
    quit = tk.Button(root,
                    text="Q\u0332uit",
                    padx = 5,
                    pady = 5,
                    command = root.destroy)
    quit.pack(side="top",
                fill=tk.X,
                padx=25,
                pady=25)
    tk.Checkbutton(root, text="Close after selecting profile", variable=var1).pack(side="top",
                fill=tk.X,
                padx=25,
                pady=25)
    root.bind('<q>', lambda x: root.destroy())
    root.mainloop()

def run_profile(profile):
    directory = os.path.join(os.environ["ProgramW6432"], 'Mozilla Firefox')
    # if not os.path.exists(directory):
    #     os.mkdir(directory)
    ff = os.path.join(directory, 'Firefox.exe')
    filename = 'FF_' + profile + '.exe'
    fullname = os.path.join(directory, filename)
    print(fullname)
    if not os.path.exists(fullname):
        # ff = os.path.join(os.environ["ProgramW6432"], 'Mozilla Firefox', 'Firefox.exe')
        #os.link(ff,fullname)
        #print (ff)
        #subprocess.run(['cmd','/K','mklink', '/H', f'{fullname}', f'{ff}'])
        #subprocess.run(['cmd','/K',f'echo /H "{fullname}" "{ff}"'])
        admin.run_as_admin(['cmd','/K','copy', f'{ff}', f'{fullname}'], debug=True)
        while not os.path.exists(fullname):
            sleep(1)
        #print('Created hardlink')
    
    subprocess.run([f'{fullname}','-P',f'{profile}','-foreground'] + sys.argv[1:])

if __name__ == "__main__":
    profiles = get_profiles()    
    build_gui(profiles)
    pass