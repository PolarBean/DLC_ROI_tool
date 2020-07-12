import pickle
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
from SelectionObject import SelectionObject
class MousePositionTracker(tk.Frame):
    """ Tkinter Canvas mouse position widget. """
    
    def __init__(self, canvas,imwidth,imheight,text,my_imo, fps):
        self.text = text
        self.fps = fps
        self.canvas = canvas
        self.reset()
        self.canv_width = self.canvas.cget('width')
        self.canv_height = self.canvas.cget('height')
        self.im_height=imheight
        self.im_width=imwidth
        print(self.im_width)
        self.my_imo = my_imo
        self.im_list=[]
        self.SELECT_OPTS = dict(dash=(2, 2), stipple='gray25', fill='red',
                          outline='')
        # Create canvas cross-hair lines.
        xhair_opts = dict(dash=(3, 2), fill='white', state=tk.HIDDEN)
        self.lines = (self.canvas.create_line(0, 0, 0, self.canv_height, **xhair_opts),
                      self.canvas.create_line(0, 0, self.canv_width,  0, **xhair_opts))
   
    def cur_selection(self):
        return (self.start, self.end)
    def track(self):
                self.posn_tracker = MousePositionTracker(self.canvas,  self.im_width, self.im_height,self.text,self.my_imo, self.fps)
                self.selection_obj = SelectionObject(self.canvas, self.SELECT_OPTS)

    def begin(self, event):
        self.hide()
        self.start = (event.x, event.y)# Remember position (no drawing).
        self.top_left_X=(event.x)
        self.top_left_Y=(event.y)
        print("top_left_X",self.top_left_X)
        print("im_width",self.im_width)
        self.TLX=self.top_left_X*(self.im_width/640)
        self.TLY=self.top_left_Y*(self.im_height/420)
        
    def endclick(self, event):
        self.hide()
        self.bottom_right_X=(event.x)
        self.bottom_right_Y=(event.y)
        self.BRX=self.bottom_right_X*(self.im_width/640)
        self.BRY=self.bottom_right_Y*(self.im_height/420)
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
            'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
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
            'saddle brown', 'sandy brown',
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
      
        colour=random.choice(COLOURS)
        USER_INP = simpledialog.askstring(title="ROI name",
                                  prompt="ROI name:")
        self.text.insert(tk.INSERT,("\nThe ROI {} is set and coloured {}".format(USER_INP, colour)))
        Current_ROI=pd.DataFrame({'ROI':USER_INP,'TLX':min(self.TLX,self.BRX),
                                      'TLY':min(self.TLY,self.BRY),'BRX':max(self.TLX,self.BRX),
                                      'BRY':max(self.TLY,self.BRY)},index=[0])
        self.ALL_ROIs=self.ALL_ROIs.append(Current_ROI)
#         img2 = img.crop([ left, upper, right, lower])
        self.canvas.create_rectangle(self.top_left_X,self.top_left_Y,self.bottom_right_X,self.bottom_right_Y,outline=colour,width=5)
        img = ImageTk.PhotoImage(self.my_imo.crop((min(self.top_left_X,self.bottom_right_X),min(self.top_left_Y,self.bottom_right_Y),max(self.top_left_X,self.bottom_right_X),max(self.top_left_Y,self.bottom_right_Y))))
        self.im_list.append(img)
        self.image_on_canvas=self.canvas.create_image(min(self.top_left_X,self.bottom_right_X),min(self.top_left_Y,self.bottom_right_Y), image=img, anchor=tk.NW)
        self.track()

    def bodyparts_to_ROI(self):
        # get the index of X columns
        ind_X=['x' in i for i in self.data.columns]
        X_data=self.data[self.data.columns[ind_X]]
        # get the index of Y columns
        ind_Y=['y' in i for i in self.data.columns]
        Y_data=self.data[self.data.columns[ind_Y]]
        X_data=np.array(X_data)
        Y_data=np.array(Y_data)
        if self.cropping == True:
            X_data += self.crop_params[0]
            Y_data += self.crop_params[2]
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

    def read_pickle(self, filename):
        """ Read the pickle file """
        with open(filename, "rb") as handle:
            return pickle.load(handle)

    def load_video_metadata(self,file):
            metadata = os.path.splitext(file)[0]
            metadata = glob.glob("{}*.pickle".format(metadata))
            if len(metadata) == 0:
                self.text.insert(tk.INSERT,
                            "\n\nno pickle file was found for {}, this means if you cropped your video in dlc our program will not be accurate\n\n")
                return None
            metadata = self.read_pickle(metadata[0])
            return metadata

    def load_deeplab_Coords(self):
        path=filedialog.askopenfilename(filetypes = ([("h5 and csv files",".h5 .csv")]))
        if path.endswith('.h5'):
            self.data=pd.read_hdf(path)
        else:
            self.data=pd.read_csv(path, header=[0,1,2])
        self.data.columns=self.data.columns.droplevel()
        self.data=self.data.drop('likelihood', axis=1, level=1)
        metadata = self.load_video_metadata(path)
        if metadata == None:
            self.cropping = False
            return
        self.cropping =    metadata["data"]["cropping"]
        self.crop_params = [x1, x2, y1, y2] = metadata["data"]["cropping_parameters"]

    def load_ROI_file(self):
        path=filedialog.askopenfilename()
        self.ALL_ROIs = pd.read_csv(path)
        self.fps = self.ALL_ROIs['FPS'][0]

        
    def Analyse_ROI(self):        
        counts=self.bp_data['Majority'].value_counts().to_dict()
        
        
        
    def quit(self, event):
        self.hide()  # Hide cross-hairs.
        self.reset()
    def save_All_ROIs(self):
        USER_INP = simpledialog.askstring(title="File name",
                                  prompt="ROI File name:")
        self.ALL_ROIs['FPS']=self.fps
        self.ALL_ROIs.to_csv(USER_INP+".csv")
        self.text.insert(tk.INSERT,"\n saved as {}.csv".format(USER_INP))
    def detect_entries(self):
        start_time = simpledialog.askinteger(title="Start time in seconds",
                                  prompt="Start(s):")
        end_time = simpledialog.askinteger(title="End time in seconds",
                                  prompt="End(s):")
        bucket_len = simpledialog.askinteger(title="Length of buckets in seconds",
                          prompt="bucket length(s):")
        data_analysis=pd.DataFrame()
#         (ALL_ROIs.columns.insert(0,"BINS")+" time spent").append(ALL_ROIs.columns.insert(0,"BINS")+" entries")
        start_time*=self.fps
        end_time*=self.fps
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
        


        data_analysis['BIN']=(pd.DataFrame({"BIN":"total_time"}, index=[0]))
        for entry in entry_dict:
            self.text.insert(tk.INSERT,"\n animal entered {} {} times".format(entry,entry_dict[entry]))
            data_analysis[entry+" entries"]=pd.DataFrame({entry+" entries":entry_dict[entry]}, index=[0])
          
        for entryfrom in entry_from_dict:
            self.text.insert(tk.INSERT,"\n animal entered {} {} times".format(entryfrom,entry_from_dict[entryfrom]))
            data_analysis[entryfrom]=pd.DataFrame({entryfrom:entry_from_dict[entryfrom]}, index=[0])
          
#         self.bp_data.to_csv("entries.csv")
        time_spent_dict=self.bp_data.Majority[start_time:end_time].value_counts().to_dict()
        for roi in time_spent_dict:
                secs_spent=int(time_spent_dict[roi])/self.fps
                self.text.insert(tk.INSERT,"\n time spent in {} is {} seconds".format(roi,secs_spent))
                data_analysis[roi+" time spent"]=pd.DataFrame({roi+" time spent":time_spent_dict[roi]}, index=[0])
        data_analysis.to_csv(self.save_path+'entries_and_time_spent.csv')
