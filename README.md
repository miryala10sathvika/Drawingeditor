# Drawingeditor

This is a basic drawing application built using Python's tkinter library. The application allows users to draw lines and rectangles, select, delete and move objects, and group objects for collective manipulation.


# Running the Application

- Open your terminal or command prompt.
- Type the command 'sudo apt install tk'
- Type the command 'sudo apt install python3-tk'
- Navigate to the directory where you saved draw.py.
- Run the script by typing 'python3 draw.py'

# Features

- Draw: Draw lines and rectangles with options from the toolbar.
- Selection and Movement: Select and move objects using the mouse.
- Editing: Change properties such as color or modify rectangles to have rounded edges.
- Grouping: Create groups to manage multiple objects as a single unit.
- Copy and Paste: Duplicate objects within the canvas.
- Save and Load: Save the current state of your canvas to a file and load it later.
- Export: Export the canvas data to an XML file for external use.
- View Group: Visual representation of grouped objects during selection.

# How to Use

- To Draw: Select a drawing tool from the toolbar and use the mouse to draw on the canvas.
- To Select: Click the 'Select' button and then drag over objects to form a selection rectangle.
- To Move: With objects selected, click the 'Move' button and then drag to reposition them.
- To Group: Use the 'Group' button after making a selection to group objects together.
- To Ungroup: Select a group and use the 'Ungroup' button to break it back into individual objects.
- To UngroupAll: Select a group and use 'Ungroup All' button to recursively ungroup all the objects in the group.
- To Copy/Paste: Select an object, click 'Copy', then 'Paste' to duplicate the object at a different location on the canvas.
- To Edit Properties: Select an object and choose 'Edit' to change its properties.
- To Save: Use the 'Save' option under the File menu to save your canvas.
- To Load: Use the 'Load file' option under the File menu to load a previously saved canvas.
- To Export: Use the 'Export' option under the File menu to generate an XML file of your canvas.

## Assumptions

- After grouping , if you add any object inside that grouping area , then it will be automatically added to group.
- To select a group , you should select atleast one object of the group. 
