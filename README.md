# DLC_ROI_tool
A tool for drawing ROIs on videos and analysing deeplabcut videos.

# The DLC-ROI Process

## Step 1. Choose a video.
When you initially launch the application you will be asked to choose a video on which to draw your ROI.

## Step 2. Draw your ROIs. 
Click and drag to draw your ROIs and save them sequentially with "Set and Name"

## Step 3. Load DeepLabCut File.
Choose a scored deeplabcut file (this should work with either the csv or .h5 file, but i usually use the .h5).
This doesnt necessarily need to be the same video that you drew the ROI on, drawing the ROI set the XY coordinates of each ROI and it will apply these coordinates to any DLC file you choose. If your ROIs dont move from video to video this can be efficient. 

## Step 4. BodyPart to ROI. 
This is a necessary step and generates a csv with the ROI an animal was in for each frame of the scored DLC video. It uses a majority method to determine where the majority of the animal was in any given frame. This can take a long time especially with long or high fps videos so if the application is not responding just let it think for a minute or 3 :)

## Step 5. Detect Entries and Time Spent.
This will quickly generate you a csv file with basic stats on your videos, such as time spent and the number of entries into each ROI and between ROIs. 

## Optional. Save ROIs for future analysis
The Save ROIs to file allows you to save your defined ROIs to a csv file which can be loaded at a later date to allow for consistency and replication of your analysis.
