import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import Button
import pandas as pd
from tkinter import filedialog
import cv2
import os
import numpy as np
import random
import glob
from tkinter import simpledialog
from MousePositionTracker import MousePositionTracker
from SelectionObject import SelectionObject







class Application(tk.Frame):



    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        def frame_from_video():
            video=filedialog.askopenfilename()
            vidcap = cv2.VideoCapture(video)
            count = 0
            frames= int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = vidcap.get(cv2.CAP_PROP_FPS) 
            self.text.insert(tk.INSERT,"\nVideo was recorded at {} FPS!".format(self.fps))
            # Default selection object options.
            self.SELECT_OPTS = dict(dash=(2, 2), stipple='gray25', fill='red',
                          outline='')
            while vidcap.isOpened():
                success, self.my_im = vidcap.read()
                if success:
                    count += 1
               
                if count>frames*(np.random.randint(99)*0.01):
                    self.my_im=Image.fromarray(self.my_im)
                    self.im_height=self.my_im.height
                    self.im_width=self.my_im.width
                    print('test{}'.format(self.im_width))
                    height_factor=420/self.my_im.height
                    width_factor=640/self.my_im.width
                    self.my_imo=self.my_im.resize((int(self.my_im.width*width_factor),int(self.my_im.height*height_factor)))
                    self.my_im = ImageTk.PhotoImage(self.my_imo)
                    self.posn_tracker = MousePositionTracker(self.canvas, self.im_width, self.im_height, self.text,self.my_imo, self.fps)
                    self.canvas.create_image(0, 0, image=self.my_im, anchor=tk.NW)
                    self.canvas.img = self.my_im
                    self.selection_obj = SelectionObject(self.canvas, self.SELECT_OPTS)

                    
                    break
            cv2.destroyAllWindows()
            vidcap.release()
 

 

        
        self.text = tk.Text(root,height=14)


        self.text.insert(tk.INSERT, 'First, load the video you want to draw an ROI on with \"Load Video Frame for ROI selection\"\nThen, Drag the box around your first ROI \n once you are happy with this ROI click \"set and name\" \n To Create a new ROI repeat this process. \n Once you have set and named all of your ROIs. click \"Save ROIs to File\"\n if you have Saved your ROIs in the future you can load them and skip the \n previous steps. next load a deeplabcut h5 or csv coordinate file \n with the \"Load DeepLabCut File\" button, Clicking \"Bodypart to ROI\" will \n output a csv of the region for each frame which you can quickly analyse \n with \"detect entries and time spent\"')
        self.text.pack(side='bottom',expand=True)
        
        self.canvas = tk.Canvas(root, width=640, height=420,
                                borderwidth=0, highlightthickness=0)
        frame_from_video()
        self.posn_tracker = MousePositionTracker(self.canvas, self.im_width, self.im_height, self.text, self.my_imo, self.fps)
        button_frame = tk.Frame(root)
        button_frame.place(relx=0.5, rely=0.6, anchor='center')
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        button_frame.columnconfigure(3, weight=1)
        button_frame.columnconfigure(4, weight=1)
        button_frame.columnconfigure(5, weight=1)
        button_frame.columnconfigure(6, weight=1)
        button_frame.columnconfigure(7, weight=1)
        self.canvas.pack(expand=True, side='top')
        self.SetandNameButton = Button(button_frame, text="Set & Name",height=1,command=self.posn_tracker.set_and_name)
        self.SaveROItoFile = Button(button_frame, text="Save ROIs to File",height=1,command=self.posn_tracker.save_All_ROIs)
        self.LoadROIfromFile = Button(button_frame, text="Load ROI from File",height=1,command=self.posn_tracker.load_ROI_file)
        self.LoadDeepLabfromFile = Button(button_frame, text="Load DeepLabCut File",height=1,command=self.posn_tracker.load_deeplab_Coords)
        self.LoadVid = Button(button_frame, text="Load Video Frame for ROI selection",height=1,command=frame_from_video)
        self.bodyparts_to_ROI_button= Button(button_frame, text="Bodypart to ROI",height=1,command=self.posn_tracker.bodyparts_to_ROI)
        self.detect_entries_button= Button(button_frame, text="detect entries and time spent",height=1,command=self.posn_tracker.detect_entries)
#         self.time_spent_button= Button(button_frame, text="time spent",height=1,command=self.posn_tracker.time_spent)
        #         self.quitButton.pack(expand=True)
#         self.SetandNameButton.pack(expand=True)
        
        self.canvas.create_image(0, 0, image=self.my_im, anchor=tk.NW)
        self.canvas.img = self.my_im  # Keep reference.
        self.LoadVid.grid(column=0,row=4)
        self.SetandNameButton.grid(column=1,row=4)
        self.LoadROIfromFile.grid(column=2,row=4)
        self.SaveROItoFile.grid(column=3,row=4)
        self.LoadDeepLabfromFile.grid(column=0,row=5)
        self.bodyparts_to_ROI_button.grid(column=1,row=5)
        self.detect_entries_button.grid(column=2, row=5)
#         self.time_spent_button.grid(column=7, row=4)

        
        # Create selection object to show current selection boundaries.
        self.selection_obj = SelectionObject(self.canvas, self.SELECT_OPTS)

        # Callback function to update it given two points of its diagonal.
        def on_drag(start, end, **kwarg):  # Must accept these arguments.
            self.selection_obj.update(start, end)

        # Create mouse position tracker that uses the function.
        
        self.posn_tracker.autodraw(command=on_drag)  # Enable callbacks.



if __name__ == '__main__':

    WIDTH, HEIGHT = 900, 900
    BACKGROUND = 'grey'
    TITLE = 'ROI tool'

    root = tk.Tk()
    root.title(TITLE)
    root.geometry('%sx%s' % (WIDTH, HEIGHT))
    root.configure(background=BACKGROUND)

    app = Application(root, background=BACKGROUND)
    app.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
    app.mainloop()
