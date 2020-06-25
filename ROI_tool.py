import tkinter as tk
from tkinter import *
import math
from PIL import Image, ImageTk
from tkinter import Button
import pandas as pd
from tkinter import filedialog
import cv2
import os
import numpy as np
import random

from tkinter import simpledialog
class MousePositionTracker(tk.Frame):
    """ Tkinter Canvas mouse position widget. """
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.reset()
        self.canv_width = self.canvas.cget('width')
        self.canv_height = self.canvas.cget('height')
        

        # Create canvas cross-hair lines.
        xhair_opts = dict(dash=(3, 2), fill='white', state=tk.HIDDEN)
        self.lines = (self.canvas.create_line(0, 0, 0, self.canv_height, **xhair_opts),
                      self.canvas.create_line(0, 0, self.canv_width,  0, **xhair_opts))
   
    def cur_selection(self):
        return (self.start, self.end)

    def begin(self, event):
        self.hide()
        self.start = (event.x, event.y)# Remember position (no drawing).
        self.top_left_X=(event.x)
        self.top_left_Y=(event.y)
        print("top_left_X",self.top_left_X)
        print("im_width",im_width)
        self.TLX=self.top_left_X*(im_width/640)
        self.TLY=self.top_left_Y*(im_height/420)
        
    def endclick(self, event):
        self.hide()
        self.bottom_right_X=(event.x)
        self.bottom_right_Y=(event.y)
        self.BRX=self.bottom_right_X*(im_width/640)
        self.BRY=self.bottom_right_Y*(im_height/420)
    def update(self, event):
        self.end = (event.x, event.y)
        self._update(event)
        self._command(self.start, (event.x, event.y))  # User callback.
        

    def _update(self, event):
        # Update cross-hair lines.
        self.canvas.coords(self.lines[0], event.x, 0, event.x, self.canv_height)
        self.canvas.coords(self.lines[1], 0, event.y, self.canv_width, event.y)
        self.show()


    def reset(self):
        self.start = self.end = None

    def hide(self):
        self.canvas.itemconfigure(self.lines[0], state=tk.HIDDEN)
        self.canvas.itemconfigure(self.lines[1], state=tk.HIDDEN)

    def show(self):
        self.canvas.itemconfigure(self.lines[0], state=tk.NORMAL)
        self.canvas.itemconfigure(self.lines[1], state=tk.NORMAL)

    def autodraw(self,command=lambda *args: None):
        """Setup automatic drawing; supports command option"""
        self.reset()
        self.ALL_ROIs=pd.DataFrame(columns=['ROI','TLX','TLY','BRX','BRY','FPS'])
        self._command = command
        self.canvas.bind("<Button-1>", self.begin)
        self.canvas.bind("<B1-Motion>", self.update)
        self.canvas.bind("<ButtonRelease-1>", self.quit)
        self.canvas.bind("<ButtonRelease-1>", self.endclick)

    def set_and_name(self):
        COLOURS = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
            'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
            'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
            'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
            'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
            'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
            'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
            'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
            'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
            'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
            'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
            'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
            'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
            'indian red', 'saddle brown', 'sandy brown',
            'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
            'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
            'pale violet red', 'maroon', 'medium violet red', 'violet red',
            'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
            'thistle', 'snow2', 'snow3',
            'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
            'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
            'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
            'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
            'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
            'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
            'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
            'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
            'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
            'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
            'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
            'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
            'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
            'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
            'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
            'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
            'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
            'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
            'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
            'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
            'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
            'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
            'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
            'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
            'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
            'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
            'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
            'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
            'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
            'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
            'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
            'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
            'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
            'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
            'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
            'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
            'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
            'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
            'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
            'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
            'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
            'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
            'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
            'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
            'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
            'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4']
        global im_list, track
        colour=random.choice(COLOURS)
        USER_INP = simpledialog.askstring(title="ROI name",
                                  prompt="ROI name:")
        text.insert(tk.INSERT,("\nThe ROI {} is set and coloured {}".format(USER_INP, colour)))
        Current_ROI=pd.DataFrame({'ROI':USER_INP,'TLX':min(self.TLX,self.BRX),
                                      'TLY':min(self.TLY,self.BRY),'BRX':max(self.TLX,self.BRX),
                                      'BRY':max(self.TLY,self.BRY)},index=[0])
        self.ALL_ROIs=self.ALL_ROIs.append(Current_ROI)
#         img2 = img.crop([ left, upper, right, lower])
        self.canvas.create_rectangle(self.top_left_X,self.top_left_Y,self.bottom_right_X,self.bottom_right_Y,outline=colour,width=5)
        img = ImageTk.PhotoImage(my_imo.crop((min(self.top_left_X,self.bottom_right_X),min(self.top_left_Y,self.bottom_right_Y),max(self.top_left_X,self.bottom_right_X),max(self.top_left_Y,self.bottom_right_Y))))
        im_list.append(img)
        self.image_on_canvas=self.canvas.create_image(min(self.top_left_X,self.bottom_right_X),min(self.top_left_Y,self.bottom_right_Y), image=img, anchor=tk.NW)
        track()
#         self.canvas.img = img


#         self.canvas.pack(expand=True, side='top')
    def bodyparts_to_ROI(self):
        # get the index of X columns
        ind_X=['x' in i for i in self.data.columns]
        X_data=self.data[self.data.columns[ind_X]]
        # get the index of Y columns
        ind_Y=['y' in i for i in self.data.columns]
        Y_data=self.data[self.data.columns[ind_Y]]
        X_data=np.array(X_data)
        Y_data=np.array(Y_data)
        mylist=self.data.columns.get_level_values(0)
        mylist = list( dict.fromkeys(mylist) )
        My_ROI_df=pd.DataFrame(np.zeros(X_data.shape),columns=mylist)
        for ROI in self.ALL_ROIs.iterrows():
            truth_array=((Y_data>ROI[1]['TLY'])&(Y_data<ROI[1]['BRY'])&(X_data>ROI[1]['TLX'])&(X_data<ROI[1]['BRX']))  
            My_ROI_df[truth_array]=ROI[1]['ROI']
        self.save_path= simpledialog.askstring(title="Save bodypart data",
                                  prompt="File name:")
        My_ROI_df=My_ROI_df.replace(0,"Nothing")
        My_ROI_df['Majority']=My_ROI_df.mode(axis=1).iloc[:,0]
        My_ROI_df.to_csv(self.save_path+".csv")
        self.bp_data=My_ROI_df
        
    def load_deeplab_Coords(self):
        path=filedialog.askopenfilename(filetypes = ([("h5 and csv files",".h5 .csv")]))
        if path.endswith('.h5'):
            self.data=pd.read_hdf(path)
        else:
            self.data=pd.read_csv(path, header=[0,1,2])
        self.data.columns=self.data.columns.droplevel()
        self.data=self.data.drop('likelihood', axis=1, level=1)
    def load_ROI_file(self):
        global fps
        path=filedialog.askopenfilename()
        self.ALL_ROIs=pd.read_csv(path)
        fps=self.ALL_ROIs['FPS'][0]

        
    def Analyse_ROI(self):        
        counts=self.bp_data['Majority'].value_counts().to_dict()
        
        
        
    def quit(self, event):
        self.hide()  # Hide cross-hairs.
        self.reset()
    def save_All_ROIs(self):
        USER_INP = simpledialog.askstring(title="File name",
                                  prompt="ROI File name:")
        self.ALL_ROIs['FPS']=fps
        self.ALL_ROIs.to_csv(USER_INP+".csv")
        text.insert(tk.INSERT,"\n saved as {}.csv".format(USER_INP))
    def detect_entries(self):
        start_time = simpledialog.askinteger(title="Start time in seconds",
                                  prompt="Start(s):")
        end_time = simpledialog.askinteger(title="End time in seconds",
                                  prompt="End(s):")
        bucket_len = simpledialog.askinteger(title="Length of buckets in seconds",
                          prompt="bucket length(s):")
        data_analysis=pd.DataFrame()
#         (ALL_ROIs.columns.insert(0,"BINS")+" time spent").append(ALL_ROIs.columns.insert(0,"BINS")+" entries")
        start_time*=fps
        end_time*=fps
        start_time=int(start_time)
        end_time=int(end_time)
        ##shift region names down one value and check difference to original region names
        entries=(self.bp_data.Majority.ne(self.bp_data.Majority.shift())).astype(int)
        ##set value one to zero as this is not a region entry
        entries.iloc[0]=0
        #multiply region entries by roi names to get the region being entered
        self.bp_data['entries']=entries*self.bp_data.Majority
        self.bp_data['enteredFrom']=self.bp_data['entries']+' from '+self.bp_data['Majority'].shift()
        self.bp_data['enteredFrom']*=entries
        self.bp_data.fillna('')
        entry_dict=self.bp_data['entries'][start_time:end_time].value_counts().to_dict()
        entry_dict.pop('')
        entry_from_dict=self.bp_data['enteredFrom'][start_time:end_time].value_counts().to_dict()
        entry_from_dict.pop('')
        data_len=self.bp_data['entries'][start_time:end_time].shape[0]
        
#         for i in range(int(math.ceil(data_len/bucket_len))):

        data_analysis['BIN']=(pd.DataFrame({"BIN":"total_time"}, index=[0]))
        for entry in entry_dict:
            text.insert(tk.INSERT,"\n animal entered {} {} times".format(entry,entry_dict[entry]))
            data_analysis[entry+" entries"]=pd.DataFrame({entry+" entries":entry_dict[entry]}, index=[0])
          
        for entryfrom in entry_from_dict:
            text.insert(tk.INSERT,"\n animal entered {} {} times".format(entryfrom,entry_from_dict[entryfrom]))
            data_analysis[entryfrom]=pd.DataFrame({entryfrom:entry_from_dict[entryfrom]}, index=[0])
          
#         self.bp_data.to_csv("entries.csv")
        time_spent_dict=self.bp_data.Majority[start_time:end_time].value_counts().to_dict()
        for roi in time_spent_dict:
                secs_spent=int(time_spent_dict[roi])/fps
                text.insert(tk.INSERT,"\n time spent in {} is {} seconds".format(roi,secs_spent))
                data_analysis[roi+" time spent"]=pd.DataFrame({roi+" time spent":time_spent_dict[roi]}, index=[0])
    
        print(data_analysis)
        data_analysis.to_csv(self.save_path+'entries_and_time_spent.csv')


        

class SelectionObject:
    """ Widget to display a rectangular area on given canvas defined by two points
        representing its diagonal.
    """
    def __init__(self, canvas, select_opts):
        # Create a selection objects for updating.
        self.canvas = canvas
        self.select_opts1 = select_opts
        self.width = self.canvas.cget('width')
        self.height = self.canvas.cget('height')

        # Options for areas outside rectanglar selection.
        select_opts1 = self.select_opts1.copy()
        select_opts1.update({'state': tk.HIDDEN})  # Hide initially.
        # Separate options for area inside rectanglar selection.
        select_opts2 = dict(dash=(2, 2), fill='', outline='white', state=tk.HIDDEN)

        # Initial extrema of inner and outer rectangles.
        imin_x, imin_y,  imax_x, imax_y = 0, 0,  1, 1
        omin_x, omin_y,  omax_x, omax_y = 0, 0,  self.width, self.height

        self.rects = (
            # Area *outside* selection (inner) rectangle.
            self.canvas.create_rectangle(omin_x, omin_y,  omax_x, imin_y, **select_opts1),
            self.canvas.create_rectangle(omin_x, imin_y,  imin_x, imax_y, **select_opts1),
            self.canvas.create_rectangle(imax_x, imin_y,  omax_x, imax_y, **select_opts1),
            self.canvas.create_rectangle(omin_x, imax_y,  omax_x, omax_y, **select_opts1),
            # Inner rectangle.
            self.canvas.create_rectangle(imin_x, imin_y,  imax_x, imax_y, **select_opts2)
        )

    def update(self, start, end):
        # Current extrema of inner and outer rectangles.
        imin_x, imin_y,  imax_x, imax_y = self._get_coords(start, end)
        omin_x, omin_y,  omax_x, omax_y = 0, 0,  self.width, self.height

        # Update coords of all rectangles based on these extrema.
        self.canvas.coords(self.rects[0], omin_x, omin_y,  omax_x, imin_y),
        self.canvas.coords(self.rects[1], omin_x, imin_y,  imin_x, imax_y),
        self.canvas.coords(self.rects[2], imax_x, imin_y,  omax_x, imax_y),
        self.canvas.coords(self.rects[3], omin_x, imax_y,  omax_x, omax_y),
        self.canvas.coords(self.rects[4], imin_x, imin_y,  imax_x, imax_y),

        for rect in self.rects:  # Make sure all are now visible.
            self.canvas.itemconfigure(rect, state=tk.NORMAL)

    def _get_coords(self, start, end):
        """ Determine coords of a polygon defined by the start and
            end points one of the diagonals of a rectangular area.
        """
        return (min((start[0], end[0])), min((start[1], end[1])),
                max((start[0], end[0])), max((start[1], end[1])))

    def hide(self):
        for rect in self.rects:
            self.canvas.itemconfigure(rect, state=tk.NORMAL)




class Application(tk.Frame):

    # Default selection object options.
    SELECT_OPTS = dict(dash=(2, 2), stipple='gray25', fill='red',
                          outline='')

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        def frame_from_video():
            global fps
            global my_im
            global my_imo
            global im_height
            global im_width
            video=filedialog.askopenfilename()
            vidcap = cv2.VideoCapture(video)
            count = 0
            frames= int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
            print(frames)
            fps = vidcap.get(cv2.CAP_PROP_FPS) 
            text.insert(tk.INSERT,"\nVideo was recorded at {} FPS!".format(fps))
      
            while vidcap.isOpened():
                success, my_im = vidcap.read()
                if success:
                    count += 1
               
                if count>frames*(np.random.randint(99)*0.01):
                    my_im=Image.fromarray(my_im)
                    im_height=my_im.height
                    im_width=my_im.width
                    height_factor=420/my_im.height
                    width_factor=640/my_im.width
                    my_imo=my_im.resize((int(my_im.width*width_factor),int(my_im.height*height_factor)))
                    my_im = ImageTk.PhotoImage(my_imo)
                    self.posn_tracker = MousePositionTracker(self.canvas)
                    self.canvas.create_image(0, 0, image=my_im, anchor=tk.NW)
                    self.canvas.img = my_im
                    self.selection_obj = SelectionObject(self.canvas, self.SELECT_OPTS)

                    
                    break
            cv2.destroyAllWindows()
            vidcap.release()
        global track 
        def track():
                self.posn_tracker = MousePositionTracker(self.canvas)
                self.selection_obj = SelectionObject(self.canvas, self.SELECT_OPTS)
        global im_list
        global my_im
        global my_imo
        global fps
        fps=1
        global text
        global im_height
        global im_width
        im_list=[]
        text = tk.Text(root,height=14)


        text.insert(tk.INSERT, 'First, load the video you want to draw an ROI on with \"Load Video Frame for ROI selection\"\nThen, Drag the box around your first ROI \n once you are happy with this ROI click \"set and name\" \n To Create a new ROI repeat this process. \n Once you have set and named all of your ROIs. click \"Save ROIs to File\"\n if you have Saved your ROIs in the future you can load them and skip the \n previous steps. next load a deeplabcut h5 or csv coordinate file \n with the \"Load DeepLabCut File\" button, Clicking \"Bodypart to ROI\" will \n output a csv of the region for each frame which you can quickly analyse \n with \"detect entries and time spent\"')
        text.pack(side='bottom',expand=True)
        
        self.canvas = tk.Canvas(root, width=640, height=420,
                                borderwidth=0, highlightthickness=0)
        frame_from_video()
        self.posn_tracker = MousePositionTracker(self.canvas)
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
        
        self.canvas.create_image(0, 0, image=my_im, anchor=tk.NW)
        self.canvas.img = my_im  # Keep reference.
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
