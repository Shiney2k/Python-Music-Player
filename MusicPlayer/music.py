#importing libraries 
import tkinter as tk
from typing import Pattern
from pygame import Color, mixer
from tkinter import *
import tkinter.font as font
from tkinter import filedialog
import fnmatch
import os

# Create the node class
class Node:
   def __init__(self, data):
      self.data = data
      self.next = None
      self.prev = None

# Create the doubly linked list class
class song_list:
   def __init__(self):
      self.head = None
      self.tail = None
      self.current = None
      self.tailIndex=-1
      self.currIndex = 0

# Define the append method to add elements at the end
   def append(self, NewVal):
      new = Node(NewVal)
      if(self.tail is None):
         self.head = self.tail = new
         self.tailIndex+=1
      else:
         self.tail.next = new
         new.prev=self.tail
         self.tail = new
         self.tailIndex+=1
         self.tail.next=self.head
         self.head.prev=self.tail

   def currSong(self, song):
  
      #1. create a temp node pointing to head
      temp = self.head
  
      #2. create two variables: found - to track
      #   search, idx - to track current index
      found = 0
      i = -1

  #3. if the temp node is not null check the
  #   node value with searchValue, if found 
  #   update variables and break the loop, else
  #   continue searching till temp node is not null 
      if(temp != None):
         while (temp != None):
            i += 1
            if(temp.data == song):
               found += 1
               break
            temp = temp.next
         if(found == 1):
            self.currIndex=i
            print(song,"is current song found at index =", self.currIndex)
            self.current= temp
            
         else:
            print(song,"is not found in the list.")

      else:    
         print("The list is empty.")


   def nextSong(self):
      if(self.current != self.tail):
         self.current=self.current.next
         self.currIndex+=1
         print(self.current.data ,"is playing as next @ index= ", self.currIndex)
      else:
         self.current=self.head
         self.currIndex=0
         print(self.current.data ,"is playing as next @ index= ", self.currIndex)


   def prevSong(self):
      if(self.current != self.head):
         self.current=self.current.prev
         self.currIndex-=1
         print(self.current.data ,"is playing as prev @ index= ", self.currIndex)
      else:
         self.current=self.tail
         self.currIndex=self.tailIndex
         print(self.current.data ,"is playing as prev @ index= ", self.currIndex)
      

# Define the method to print
   def listprint(self, node):
      i=0
      while (i<=self.tailIndex):
         print(node.data)
         listbox.insert('end', node.data)
         node = node.next
         i+=1
    

#create song_list ibject
songlist = song_list()


canvas = tk.Tk()
canvas.title("Music Player")
canvas.geometry("350x480")
canvas.config(bg='black')

rootpath = "E:\\Songs"
Pattern = "*.mp3"

mixer.init()

prev_img = tk.PhotoImage(file="prev_img.png")
stop_img = tk.PhotoImage(file="stop_img.png")
play_img = tk.PhotoImage(file="play_img.png")
pause_img = tk.PhotoImage(file="pause_img.png")
next_img = tk.PhotoImage(file="next_img.png")

def select():
   songlist.currSong(listbox.get("anchor"))
   label.config(text=songlist.current.data)
   mixer.music.load(rootpath + "\\" + songlist.current.data)
   mixer.music.play()

def stop():
   mixer.music.stop()
   listbox.select_clear('active')

def play_next():
   songlist.nextSong()
   next_song_name= listbox.get(songlist.currIndex)
   label.config(text=songlist.current.data)
   mixer.music.load(rootpath + "\\" + songlist.current.data)
   mixer.music.play()
   listbox.select_clear(0, 'end')
   listbox.activate(songlist.currIndex)
   listbox.select_set(songlist.currIndex)

def play_prev():
   songlist.prevSong()
   label.config(text=songlist.current.data)
   mixer.music.load(rootpath + "\\" + songlist.current.data)
   mixer.music.play()
   listbox.select_clear(0, 'end')
   listbox.activate(songlist.currIndex)
   listbox.select_set(songlist.currIndex)

def pause_song():
   if pauseButton["text"]=="Pause":
      mixer.music.pause()
      pauseButton["text"]=="Play"
   else:
      mixer.music.unpause()
      pauseButton["text"]=="Pause"
      

listbox = tk.Listbox(canvas, fg = "cyan", bg = "black", width = 100, font =('ds-digital',12))
listbox.pack(padx=15, pady=15)

label = tk.Label(canvas, text='', bg= 'black', fg='yellow', font=('ds-digital',14))
label.pack(pady=15)

top = tk.Frame(canvas, bg="black")
top.pack(padx=1, pady=5, anchor='center')

prevButton = tk.Button(canvas, text="Prev", image=prev_img, bg='black', borderwidth=0, command=play_prev)
prevButton.pack(pady=15, in_=top, side='left')

stopButton = tk.Button(canvas, text="Stop", image=stop_img, bg='black', borderwidth=0, command=stop)
stopButton.pack(pady=15, in_=top, side='left')

playButton = tk.Button(canvas, text="Play", image=play_img, bg='black', borderwidth=0, command=select)
playButton.pack(pady=15, in_=top, side='left')

pauseButton = tk.Button(canvas, text="Pause", image=pause_img, bg='black', borderwidth=0, command=pause_song)
pauseButton.pack(pady=15, in_=top, side='left')

nextButton = tk.Button(canvas, text="Next", image=next_img, bg='black', borderwidth=0, command=play_next)
nextButton.pack(pady=15, in_=top, side='left')

songlist = song_list()
for root, dirs, files in os.walk(rootpath):
    for filename in fnmatch.filter(files, Pattern):
        songlist.append(filename)
songlist.listprint(songlist.head)
canvas.mainloop()