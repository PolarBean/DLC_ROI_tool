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
class SelectionObject:
    """ Widget to display a rectangular or circular area on given canvas defined by two points
        representing its diagonal (for rectangle) or defining the bounding box (for circle).
    """
    def __init__(self, canvas, select_opts, shape_type_var, dim1_entry, dim2_entry):
        # Create a selection objects for updating.
        self.canvas = canvas
        self.select_opts1 = select_opts
        self.width = int(self.canvas.cget('width'))
        self.height = int(self.canvas.cget('height'))
        self.shape_type_var = shape_type_var
        self.current_shape = None
        self.dimension_text = None
        self.dim1_entry = dim1_entry
        self.dim2_entry = dim2_entry

        # Store current shape coordinates for resizing
        self.current_x1 = None
        self.current_y1 = None
        self.current_x2 = None
        self.current_y2 = None


        # Options for areas outside selection.
        select_opts1 = self.select_opts1.copy()
        select_opts1.update({'state': tk.HIDDEN})  # Hide initially.
        # Separate options for area inside selection.
        select_opts2 = dict(dash=(2, 2), fill='', outline='white', state=tk.HIDDEN)

        self.outer_rects = (
            self.canvas.create_rectangle(0, 0, self.width, 1, **select_opts1),
            self.canvas.create_rectangle(0, 0, 1, self.height, **select_opts1),
            self.canvas.create_rectangle(self.width-1, 0, self.width, self.height, **select_opts1),
            self.canvas.create_rectangle(0, self.height-1, self.width, self.height, **select_opts1)
        )
        self.inner_shape = None # Initialize inner_shape to None

    def update(self, start, end, shape_type):
        self.hide() # Hide previous shape

        # Delete previous shape if it exists
        if self.inner_shape:
            self.canvas.delete(self.inner_shape)
            self.inner_shape = None

        # Options for the inner shape - include fill and stipple
        select_opts2 = dict(dash=(2, 2), fill='red', outline='white', stipple='gray25')

        if shape_type == "Rectangle":
            imin_x, imin_y,  imax_x, imax_y = self._get_coords(start, end)
            self.inner_shape = self.canvas.create_rectangle(imin_x, imin_y,  imax_x, imax_y, **select_opts2)

            # Store the coordinates
            self.current_x1 = imin_x
            self.current_y1 = imin_y
            self.current_x2 = imax_x
            self.current_y2 = imax_y

            # Hide outer rectangles for rectangle as fill is now on inner shape
            for rect in self.outer_rects:
                self.canvas.itemconfigure(rect, state=tk.HIDDEN)

            self._display_dimensions(imin_x, imin_y, imax_x, imax_y, shape_type)

        elif shape_type == "Circle":
            center_x = (start[0] + end[0]) / 2
            center_y = (start[1] + end[1]) / 2
            radius = max(abs(start[0] - end[0]), abs(start[1] - end[1])) / 2
            x1 = center_x - radius
            y1 = center_y - radius
            x2 = center_x + radius
            y2 = center_y + radius
            self.inner_shape = self.canvas.create_oval(x1, y1, x2, y2, **select_opts2)

            # Store the coordinates (bounding box)
            self.current_x1 = x1
            self.current_y1 = y1
            self.current_x2 = x2
            self.current_y2 = y2

            # Hide outer rectangles for circle (already done, but keep for clarity)
            for rect in self.outer_rects:
                self.canvas.itemconfigure(rect, state=tk.HIDDEN)

            self._display_dimensions(x1, y1, x2, y2, shape_type)

        self.canvas.update_idletasks() # Force canvas update


    def _get_coords(self, start, end):
        """ Determine coords of a polygon defined by the start and
            end points one of the diagonals of a rectangular area.
        """
        return (min((start[0], end[0])), min((start[1], end[1])),
                max((start[0], end[0])), max((start[1], end[1])))

    def _display_dimensions(self, x1, y1, x2, y2, shape_type):
        self.dim1_entry.delete(0, tk.END)
        self.dim2_entry.delete(0, tk.END)
        if shape_type == "Rectangle":
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            self.dim1_entry.insert(0, f"{width:.2f}")
            self.dim2_entry.insert(0, f"{height:.2f}")
        elif shape_type == "Circle":
            diameter = max(abs(x2 - x1), abs(y2 - y1))
            self.dim1_entry.insert(0, f"{diameter:.2f}")
            self.dim2_entry.insert(0, f"{diameter:.2f}") # Set height to diameter for circle


    def hide(self):
        if self.inner_shape: # Check if inner_shape exists before hiding
            self.canvas.itemconfigure(self.inner_shape, state=tk.HIDDEN)
        for rect in self.outer_rects:
            self.canvas.itemconfigure(rect, state=tk.HIDDEN)

    def reset_shape(self):
        self.hide()
        if self.inner_shape: # Delete shape on reset
            self.canvas.delete(self.inner_shape)
            self.inner_shape = None
        self.dim1_entry.delete(0, tk.END)
        self.dim2_entry.delete(0, tk.END)
        # Reset stored coordinates on shape reset
        self.current_x1 = None
        self.current_y1 = None
        self.current_x2 = None
        self.current_y2 = None


    def update_from_dimensions(self, dim1, dim2, shape_type):
        # Delete previous shape if it exists
        if self.inner_shape:
            self.canvas.delete(self.inner_shape)
            self.inner_shape = None

        # Options for the inner shape - include fill and stipple
        select_opts2 = dict(dash=(2, 2), fill='red', outline='white', stipple='gray25')

        # Use stored top-left coordinates as the anchor point
        new_x1 = self.current_x1 if self.current_x1 is not None else 0
        new_y1 = self.current_y1 if self.current_y1 is not None else 0

        if shape_type == "Rectangle":
            width = dim1
            height = dim2
            new_x2 = new_x1 + width
            new_y2 = new_y1 + height
            self.inner_shape = self.canvas.create_rectangle(new_x1, new_y1, new_x2, new_y2, **select_opts2)

            # Hide outer rectangles for rectangle as fill is now on inner shape
            for rect in self.outer_rects:
                self.canvas.itemconfigure(rect, state=tk.HIDDEN)

        elif shape_type == "Circle":
            diameter = dim1
            # For circle, dim2 should be equal to dim1 (diameter)
            if dim2 is None or dim2 == "": # If dim2 is not provided or empty, use dim1
                dim2 = dim1
            new_x2 = new_x1 + diameter
            new_y2 = new_y1 + diameter
            self.inner_shape = self.canvas.create_oval(new_x1, new_y1, new_x2, new_y2, **select_opts2)

        # Update stored coordinates after resizing
        self.current_x1 = new_x1
        self.current_y1 = new_y1
        self.current_x2 = new_x2
        self.current_y2 = new_y2

        self._display_dimensions(new_x1, new_y1, new_x2, new_y2, shape_type)
        self.canvas.update_idletasks() # Force canvas update
