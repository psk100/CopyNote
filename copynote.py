"""
This program add copy text or clipboard txt to textbox 
and  you can copy the text from  textbox when you click on it
you can also update the if you modify the textbox note then it will modify automaticaly

Author:PSK100

"""


import pandas as pd
import os.path
import subprocess
from tkinter import *
import time
#this varible declaration global store the value 
#this all we used in the update csv file if any changes made in the text box

global clp,inp,clicks,n
clp="a"
#this is for new updated variable
inp="a"
n=0
clicks=0
#class for scroll bar the screen
#remove padding from text note field 
class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
                

		

        canvas = Canvas(self)
        #this command activate the scrolling with mouse drag event to go up and down
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set,width=280,height=740,bg="white")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
##        scrollbar.config(command=main.yview)

        
def copy():
    #this fuction add copy text to note pad and store for later used
    print("you add text success full")
    na=main.clipboard_get()     
    
    
    addt=na 
    
    
    ##merge two data frame to add new note
    df=pd.read_csv("n1.csv")
    df2=pd.DataFrame({'Notes':[addt]})
    df=pd.concat([df, df2], 
                          ignore_index = True)
    df.to_csv("n1.csv",index=False)
    #this reload funtion is used for update the indexing after adding new element
    reload()
    
    readf()
    #pass

def reload():
##    rewrite the append with new text
    global notes
    df=pd.read_csv("n1.csv")
    notes=list(df['Notes'])
    notes=notes[::-1]
##    print(".................",notes[42],len(notes))

r=0
    
def closed():
## in is for the scrole bar that is adding continuesly same items
##  every time that run
    print(r)
    if r==1:
        mainf.destroy()
        print("close")


        
def readf():
    ##if r is 0 then this is just start and closed function 
    ## if r is 1 then the program is alrady running 
    closed()
    global textname,fs,r,mainf
    mainf=ScrollableFrame(main,bg="white")
    mainf.configure(bg="white")
    mainf.pack()
    #update index if any new element if add in the data frame 
    reload()
    sr=0
    r=1
    #return r
    print(r)
    textname=['!text']
    for bname in notes[:]:
        
        
        fs="f"+str(sr)
        txts=bname[:5]
        print(txts)
        fs=Text(mainf.scrollable_frame,height = 5,width = 34)
        fs.pack()#pady=5)
        
        fs.insert(END,bname)
        fs.bind('<Button-1>',paste)
        fs.bind('<Enter>',enter_in)
        fs.bind('<Leave>',leave_out)
        sr=sr+1
        tx="!text"+str(sr)
        textname.append(tx)

        print(fs.get("1.0",'end-1c'))
    print(textname[:])
    return r



##this variable for the store old note
oldw=0
##textcolorlist=[]

def paste(events):
    #this fuction copy the selected tect from this button
    global textname,oldw,w,clp,inp,n,clicks
    #this code for latter used and select random color combination for the bg and fg
    # and also and feedback option that monitor if user like it or not
    textcolorlist=[]
    n=0
    if oldw != 0:
        print("old w",oldw)
        oldw.configure(bg="white",fg="black")
    w = events.widget
    
    print('sname'+w._name)
    aa=str(w._name)
##    your changing the color of the text box when we click
    w.configure(bg='purple',fg='white')
    clicks=1
    print(w)
    oldw=w
##    oldw.configure(bg=None,fg=None)
    print("old just assign",oldw)

    
    for ne in textname[:]:
        #msg=notes[n]
        print(ne)
        if ne==aa:
            if n >1:
                clp=notes[n-1]
                
                main.clipboard_clear()
                main.clipboard_append(clp)

                break
                
            else:
                clp=notes[n]
                inp = w.get(1.0, "end-1c")
                main.clipboard_clear()
                main.clipboard_append(clp)
                break
##                
                

        n=n+1
   

     
    
    pass
## hover methods
def enter_in(events):
    global w ,oldw,clp,inp
    w = events.widget
    w.configure(bg="green",fg="white")
def leave_out(events):
      global clp,inp,n,clicks
      reload()
      w.configure(bg="white",fg="black")
      if oldw != 0:
          oldw.configure(bg='purple',fg='white')
      if clicks==1:
          print("clicks",clicks)
          clicks=0
          inp = w.get(1.0, "end-1c")
          if clp!=inp:
                  valueupdate(inp)
                  print(clp," to ",inp)
                  notesn=notes[::-1]
                  print(notesn[1])
                  df=pd.DataFrame({'Notes':notesn})
                  df.to_csv("n1.csv",index=False)
                  



## file cheking is present or not
if os.path.exists("n1.csv"):
    print("exist")
 
         
    
else:
    print("not exist")
    df = pd.DataFrame({'Notes':[' ']})
    df.to_csv("n1.csv",index=False)
    
def valueupdate(inp):
    

    # upddating the change if any  in text box
    notes[n-1]=inp
    aa=str(w._name)
    print("all in",n,notes[n-1])
    

main=Tk()
main.configure(bg="white")
main.title("CopyPad")
main.geometry('300x750+1050+0')
main.resizable(False,False)
topframe=Frame(main)
topframe.pack()
##bload=RoundedButton(main, 10, 10, 50, 2, 'red', 'white', command=readf)
bload=Button(topframe,text="Load",command=readf,bg="light green",fg="white")
bload.pack(side="right")
bcopy=Button(topframe,text="Add Copy text",command=copy,bg="light green",fg="white")
##bcopy=RoundedButton(main, 100, 50, 50, 2, 'red', 'white', command=copy)
bcopy.pack(side="left")
readf()
mainloop()
