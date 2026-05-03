import tkinter as tk
from tkinter import ttk # Import ttk
from PIL import Image, ImageTk
from tkinter import Button # Keep for now, might replace with ttk.Button
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
from tkinter.scrolledtext import ScrolledText # For the introductory text


class Application(ttk.Frame): # Change to ttk.Frame



    def __init__(self, parent, *args, **kwargs):

        super().__init__(parent, *args, **kwargs)

        # Create a style object for custom styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background='#2e2e2e', foreground='white') # Global background and font
        style.configure('TFrame', background='#2e2e2e')
        style.configure('TLabel', background='#2e2e2e', foreground='white')
        style.configure('TButton', background='#2b2b2b', foreground='white', relief='flat', borderwidth=0) # Dark grey buttons
        style.map('TButton',
                  background=[('active', '#4a4a4a')], # Slightly lighter grey on hover
                  foreground=[('active', 'white')])
        style.configure('TEntry', fieldbackground='#3a3a3a', foreground='white', insertbackground='white')
        style.configure('TCombobox', fieldbackground='#3a3a3a', foreground='white', selectbackground='#3a3a3a', selectforeground='white')
        style.map('TCombobox',
                  background=[('readonly', '#3a3a3a')],
                  fieldbackground=[('readonly', '#3a3a3a')],
                  selectbackground=[('readonly', '#3a3a3a')],
                  selectforeground=[('readonly', 'white')])
        
        # Define section colors
        SECTION_BG_COLOR_SOBER = '#3a3a3a'

        style.configure('Section1.TLabelframe', background=SECTION_BG_COLOR_SOBER, bordercolor=SECTION_BG_COLOR_SOBER, relief='solid', borderwidth=1)
        style.configure('Section1.TLabelframe.Label', background=SECTION_BG_COLOR_SOBER, foreground='white')
        style.configure('Section2.TLabelframe', background=SECTION_BG_COLOR_SOBER, bordercolor=SECTION_BG_COLOR_SOBER, relief='solid', borderwidth=1)
        style.configure('Section2.TLabelframe.Label', background=SECTION_BG_COLOR_SOBER, foreground='white')
        style.configure('Section3.TLabelframe', background=SECTION_BG_COLOR_SOBER, bordercolor=SECTION_BG_COLOR_SOBER, relief='solid', borderwidth=1)
        style.configure('Section3.TLabelframe.Label', background=SECTION_BG_COLOR_SOBER, foreground='white')
        style.configure('Section4.TLabelframe', background=SECTION_BG_COLOR_SOBER, bordercolor=SECTION_BG_COLOR_SOBER, relief='solid', borderwidth=1)
        style.configure('Section4.TLabelframe.Label', background=SECTION_BG_COLOR_SOBER, foreground='white')
        style.configure('Section5.TLabelframe', background=SECTION_BG_COLOR_SOBER, bordercolor=SECTION_BG_COLOR_SOBER, relief='solid', borderwidth=1)
        style.configure('Section5.TLabelframe.Label', background=SECTION_BG_COLOR_SOBER, foreground='white')


        # Main layout frame
        main_frame = ttk.Frame(self, padding="10 10 10 10")
        main_frame.pack(fill="both", expand=True)

        # Introductory Text Section
        text_frame = ttk.LabelFrame(main_frame, text="Instructions", padding="10 10 10 10", style='Section1.TLabelframe')
        text_frame.pack(side='bottom', fill='x', padx=10, pady=10)
        self.text = ScrolledText(text_frame, height=8, wrap=tk.WORD, bg=SECTION_BG_COLOR_SOBER, fg='white', insertbackground='white')
        self.text.insert(tk.INSERT, 'First, load the video you want to draw an ROI on with \"Load Video Frame for ROI selection\"\nThen, Drag the box around your first ROI \n once you are happy with this ROI click \"set and name\" \n To Create a new ROI repeat this process. \n Once you have set and named all of your ROIs. click \"Save ROIs to File\"\n if you have Saved your ROIs in the future you can load them and skip the \n previous steps. next load a deeplabcut h5 or csv coordinate file \n with the \"Load DeepLabCut File\" button, Clicking \"Bodypart to ROI\" will \n output a csv of the region for each frame which you can quickly analyse \n with \"detect entries and time spent\"')
        self.text.config(state=tk.DISABLED)
        self.text.pack(expand=True, fill='both')

        # Create a frame to hold all control sections
        controls_frame = ttk.Frame(main_frame, padding="0 0 0 0") # No extra padding here, sections will have their own
        controls_frame.pack(side='bottom', fill='x', padx=10, pady=5) # Pack controls above the text frame

        # --- Load Video Frame ---
        video_load_frame = ttk.LabelFrame(controls_frame, text="Video Loading", padding="10 10 10 10", style='Section2.TLabelframe')
        video_load_frame.pack(fill='x', padx=0, pady=5) # padx=0 as controls_frame has padx=10
        self.LoadVid = ttk.Button(video_load_frame, text="Load Video Frame for ROI selection", command=self.frame_from_video)
        self.LoadVid.pack(pady=5, fill='x', expand=True)

        # --- Shape Options ---
        shape_options_frame = ttk.LabelFrame(controls_frame, text="Shape Options", padding="10 10 10 10", style='Section3.TLabelframe')
        shape_options_frame.pack(fill='x', padx=0, pady=5)
        
        shape_options_inner_frame = ttk.Frame(shape_options_frame)
        shape_options_inner_frame.pack(pady=5)
        shape_options_inner_frame.columnconfigure(0, weight=1)
        shape_options_inner_frame.columnconfigure(1, weight=1)
        shape_options_inner_frame.columnconfigure(2, weight=1)
        shape_options_inner_frame.columnconfigure(3, weight=1)
        shape_options_inner_frame.columnconfigure(4, weight=1)
        shape_options_inner_frame.columnconfigure(5, weight=1)

        ttk.Label(shape_options_inner_frame, text="Shape:").grid(column=0, row=0, padx=5, pady=5, sticky='w')
        self.shape_type = tk.StringVar(root)
        self.shape_type.set("Rectangle")
        self.shape_menu = ttk.Combobox(shape_options_inner_frame, textvariable=self.shape_type, values=["Rectangle", "Circle"], state="readonly", width=12)
        self.shape_menu.grid(column=1, row=0, padx=5, pady=5, sticky='ew')

        self.dim1_label = ttk.Label(shape_options_inner_frame, text="Width/Diameter (px):")
        self.dim1_label.grid(column=2, row=0, padx=5, pady=5, sticky='w')
        self.dim1_entry = ttk.Entry(shape_options_inner_frame, width=10)
        self.dim1_entry.grid(column=3, row=0, padx=5, pady=5, sticky='ew')
        self.dim2_label = ttk.Label(shape_options_inner_frame, text="Height (px):")
        self.dim2_label.grid(column=4, row=0, padx=5, pady=5, sticky='w')
        self.dim2_entry = ttk.Entry(shape_options_inner_frame, width=10)
        self.dim2_entry.grid(column=5, row=0, padx=5, pady=5, sticky='ew')

        # --- ROI Management ---
        roi_management_frame = ttk.LabelFrame(controls_frame, text="ROI Management", padding="10 10 10 10", style='Section4.TLabelframe')
        roi_management_frame.pack(fill='x', padx=0, pady=5)
        roi_management_frame.columnconfigure(0, weight=1)
        roi_management_frame.columnconfigure(1, weight=1)
        roi_management_frame.columnconfigure(2, weight=1)

        self.SetandNameButton = ttk.Button(roi_management_frame, text="Set & Name ROI", command=lambda: self.posn_tracker.set_and_name())
        self.SetandNameButton.grid(column=0, row=0, padx=5, pady=5, sticky="ew")
        self.SaveROItoFile = ttk.Button(roi_management_frame, text="Save ROIs to File", command=lambda: self.posn_tracker.save_All_ROIs())
        self.SaveROItoFile.grid(column=1, row=0, padx=5, pady=5, sticky="ew")
        self.LoadROIfromFile = ttk.Button(roi_management_frame, text="Load ROIs from File", command=lambda: self.posn_tracker.load_ROI_file())
        self.LoadROIfromFile.grid(column=2, row=0, padx=5, pady=5, sticky="ew")

        # --- DeepLabCut Analysis ---
        dlc_analysis_frame = ttk.LabelFrame(controls_frame, text="DeepLabCut Analysis", padding="10 10 10 10", style='Section5.TLabelframe')
        dlc_analysis_frame.pack(fill='x', padx=0, pady=5)
        dlc_analysis_frame.columnconfigure(0, weight=1)
        dlc_analysis_frame.columnconfigure(1, weight=1)
        dlc_analysis_frame.columnconfigure(2, weight=1)

        self.LoadDeepLabfromFile = ttk.Button(dlc_analysis_frame, text="Load DeepLabCut File", command=lambda: self.posn_tracker.load_deeplab_Coords())
        self.LoadDeepLabfromFile.grid(column=0, row=0, padx=5, pady=5, sticky="ew")
        self.bodyparts_to_ROI_button= ttk.Button(dlc_analysis_frame, text="Bodypart to ROI", command=lambda: self.posn_tracker.bodyparts_to_ROI())
        self.bodyparts_to_ROI_button.grid(column=1, row=0, padx=5, pady=5, sticky="ew")
        self.detect_entries_button= ttk.Button(dlc_analysis_frame, text="Detect Entries and Time Spent", command=lambda: self.posn_tracker.detect_entries())
        self.detect_entries_button.grid(column=2, row=0, padx=5, pady=5, sticky="ew")

        # --- Batch Processing ---
        batch_processing_frame = ttk.LabelFrame(controls_frame, text="Batch Processing", padding="10 10 10 10", style='Section1.TLabelframe') # Reusing Section1 style for consistency
        batch_processing_frame.pack(fill='x', padx=0, pady=5)
        self.ProcessBatchButton = ttk.Button(batch_processing_frame, text="Process Batch", command=self.process_batch_gui)
        self.ProcessBatchButton.pack(pady=5, fill='x', expand=True)

        # Canvas Section (packed last, takes remaining space)
        canvas_frame = ttk.Frame(main_frame, padding="10 10 10 10")
        canvas_frame.pack(side='top', fill='both', expand=True, padx=10, pady=10)
        self.canvas = tk.Canvas(canvas_frame, width=640, height=420,
                                borderwidth=0, highlightthickness=0, bg='black') # Darker canvas background
        self.canvas.pack(expand=True, fill='both')

        # Bind the canvas configure event to handle resizing
        self.canvas.bind("<Configure>", self.on_resize)

        # Bind dimension entry fields to update shape
        self.dim1_entry.bind("<Return>", self.update_shape_from_dimensions)
        self.dim2_entry.bind("<Return>", self.update_shape_from_dimensions)
        
    def frame_from_video(self):
        video=filedialog.askopenfilename()
        vidcap = cv2.VideoCapture(video)
        count = 0
        frames= int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = vidcap.get(cv2.CAP_PROP_FPS)
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.INSERT,"\nVideo was recorded at {} FPS!".format(self.fps))
        self.text.config(state=tk.DISABLED)
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
                self.my_imo_original = self.my_im.copy() # Store original PIL image for resizing
                print('test{}'.format(self.im_width))
                
                # Initial resize to fit canvas
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                
                original_aspect_ratio = self.im_width / self.im_height
                canvas_aspect_ratio = canvas_width / canvas_height

                if original_aspect_ratio > canvas_aspect_ratio:
                    displayed_width = canvas_width
                    displayed_height = int(canvas_width / original_aspect_ratio)
                else:
                    displayed_height = canvas_height
                    displayed_width = int(canvas_height * original_aspect_ratio)

                # Ensure dimensions are at least 1 pixel to avoid errors
                displayed_width = max(1, displayed_width)
                displayed_height = max(1, displayed_height)

                self.my_imo = self.my_imo_original.resize((displayed_width, displayed_height), Image.LANCZOS)
                self.my_im = ImageTk.PhotoImage(self.my_imo)
                self.selection_obj = SelectionObject(self.canvas, self.SELECT_OPTS, self.shape_type, self.dim1_entry, self.dim2_entry)
                
                # Center the image on the canvas
                image_x = (canvas_width - displayed_width) / 2
                image_y = (canvas_height - displayed_height) / 2
                self.canvas.create_image(image_x, image_y, image=self.my_im, anchor=tk.NW)
                self.canvas.img = self.my_im

                # Pass image offsets and displayed dimensions to MousePositionTracker
                self.posn_tracker = MousePositionTracker(self.canvas, self.im_width, self.im_height, self.text, self.my_imo, self.fps, shape_type_var=self.shape_type, selection_obj=self.selection_obj, image_offset_x=image_x, image_offset_y=image_y, displayed_im_width=displayed_width, displayed_im_height=displayed_height)

                def on_drag(start, end, **kwarg):
                    self.selection_obj.update(start, end, self.shape_type.get())

                break
        cv2.destroyAllWindows()
        vidcap.release()

        self.posn_tracker.autodraw(command=on_drag)

    def on_resize(self, event=None): # event=None for initial call if needed
        # Only proceed if a video has been loaded and original image is available
        if not hasattr(self, 'my_imo_original') or self.my_imo_original is None:
            return

        # Get current canvas dimensions
        new_canvas_width = self.canvas.winfo_width()
        new_canvas_height = self.canvas.winfo_height()

        # Avoid division by zero if canvas is too small
        if new_canvas_width <= 0 or new_canvas_height <= 0:
            return

        # Calculate scaling factors based on original image dimensions
        original_aspect_ratio = self.im_width / self.im_height
        canvas_aspect_ratio = new_canvas_width / new_canvas_height

        if original_aspect_ratio > canvas_aspect_ratio:
            # Image is wider than canvas, scale by width
            displayed_width = new_canvas_width
            displayed_height = int(new_canvas_width / original_aspect_ratio)
        else:
            # Image is taller than canvas, scale by height
            displayed_height = new_canvas_height
            displayed_width = int(new_canvas_height * original_aspect_ratio)

        # Ensure dimensions are at least 1 pixel to avoid errors
        displayed_width = max(1, displayed_width)
        displayed_height = max(1, displayed_height)

        # Resize the PIL image
        self.my_imo = self.my_imo_original.resize((displayed_width, displayed_height), Image.LANCZOS)
        self.my_im = ImageTk.PhotoImage(self.my_imo)

        # Clear existing image and draw the new one, centered
        self.canvas.delete("all") # Clear everything, including old ROIs and image
        
        image_x = (new_canvas_width - displayed_width) / 2
        image_y = (new_canvas_height - displayed_height) / 2
        self.canvas.create_image(image_x, image_y, image=self.my_im, anchor=tk.NW)
        self.canvas.img = self.my_im # Keep a reference to prevent garbage collection

        # Update MousePositionTracker with new displayed dimensions and offsets
        if hasattr(self, 'posn_tracker') and self.posn_tracker is not None:
            self.posn_tracker.displayed_im_width = displayed_width
            self.posn_tracker.displayed_im_height = displayed_height
            self.posn_tracker.image_offset_x = image_x
            self.posn_tracker.image_offset_y = image_y
            self.posn_tracker.canv_width = new_canvas_width # Update canvas dimensions for crosshairs
            self.posn_tracker.canv_height = new_canvas_height
            self.posn_tracker.draw_all_loaded_ROIs() # Redraw ROIs


    def update_shape_from_dimensions(self, event):
        if not hasattr(self, 'selection_obj') or self.selection_obj is None:
            print("Please load a video first.")
            return

        shape_type = self.shape_type.get()
        try:
            dim1 = float(self.dim1_entry.get())
            dim2 = float(self.dim2_entry.get()) if self.dim2_entry.get() else None
            self.selection_obj.update_from_dimensions(dim1, dim2, shape_type)
        except ValueError:
            print("Invalid dimension input.")

    def process_batch_gui(self):
        """ Prompts user for batch file and triggers batch processing. """
        batch_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if batch_file_path:
            batch_tracker = MousePositionTracker(
                canvas=None,
                imwidth=None,
                imheight=None,
                text=self.text,
                my_imo=None,
                fps=None,
                shape_type_var=self.shape_type
            )
            batch_tracker.process_batch(batch_file_path)


if __name__ == '__main__':

    WIDTH, HEIGHT = 900, 900
    TITLE = 'ROI tool'

    root = tk.Tk()
    root.title(TITLE)
    root.geometry('%sx%s' % (WIDTH, HEIGHT))

    # Initialize ttk.Style for a modern look
    style = ttk.Style()
    style.theme_use('clam')
    root.configure(bg='#2e2e2e')

    app = Application(root)
    app.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
    app.mainloop()
