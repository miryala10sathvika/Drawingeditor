import tkinter as tk
import tkinter.simpledialog as sd
import tkinter.messagebox as messagebox
from tkinter import *
import sys

class DrawingApp:
    @staticmethod
    def round_rectangle(self,x1, y1, x2, y2, radius=25, **kwargs):
            
        points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2, # pos 19, 20     
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]

        return self.canvas.create_polygon(points, **kwargs, smooth=True)
    def __init__(self, master):
        self.master = master
        self.master.title("Drawing Application")

        self.canvas = tk.Canvas(self.master, width=800, height=800, bg="white")
        self.canvas.pack()
        
        if file_name:
            self.load_file(file_name)
        self.groups = []  # List to store coordinates of grouped rectang
        self.rectangle_type = {}
        self.selected_objects = []  # List to store IDs of selected objects
        self.start_x = None
        self.start_y = None
        self.selection_rect = None
        self.select_mode = False  # Flag to indicate selection mode
        self.move_mode = False # Flag to indicate move mode
        self.move_offset_x = 0  # Offset for moving objects
        self.move_offset_y = 0
        self.toggle_view=0
        self.create_menu()
        self.create_toolbar()
        self.objlist=[]
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.finish_drawing)

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        object_menu = tk.Menu(menubar, tearoff=0)
        object_menu.add_command(label="Line", command=self.select_line)
        object_menu.add_command(label="Rectangle", command=self.select_rectangle)
        object_menu.add_separator()
        object_menu.add_command(label="Print Object Coordinates", command=self.print_object_coordinates)  # New menu item
        object_menu.add_separator()
        object_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="Objects", menu=object_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Delete", command=self.delete_objects)
        edit_menu.add_command(label="Move", command=self.toggle_move_mode)
        edit_menu.add_command(label="Copy", command=self.copy_objects)
        edit_menu.add_command(label="Paste", command=self.paste_objects)
        edit_menu.add_command(label="Edit Properties", command=self.edit_object_properties)
        menubar.add_cascade(label="Operations", menu=edit_menu)
        
        saveExport_menu = tk.Menu(menubar, tearoff=0)
        saveExport_menu.add_command(label="Save", command=self.save_file)
        saveExport_menu.add_command(label="Load file", command=self.load_file)
        saveExport_menu.add_command(label="Export", command=self.xmlExport)
        menubar.add_cascade(label="File", menu=saveExport_menu)

    def create_toolbar(self):
        toolbar = tk.Frame(self.master, relief=tk.RAISED, bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        select_button = tk.Button(toolbar, text="Select", command=self.toggle_select_mode)
        select_button.pack(side=tk.LEFT, padx=2, pady=2)

        line_button = tk.Button(toolbar, text="Line", command=self.select_line)
        line_button.pack(side=tk.LEFT, padx=2, pady=2)

        rectangle_button = tk.Button(toolbar, text="Rectangle", command=self.select_rectangle)
        rectangle_button.pack(side=tk.LEFT, padx=2, pady=2)

        delete_button = tk.Button(toolbar, text="Delete", command=self.delete_objects)
        delete_button.pack(side=tk.LEFT, padx=2, pady=2)

        move_button = tk.Button(toolbar, text="Move", command=self.toggle_move_mode)
        move_button.pack(side=tk.LEFT, padx=2, pady=2)

        copy_button = tk.Button(toolbar, text="Copy", command=self.copy_objects)
        copy_button.pack(side=tk.LEFT, padx=2, pady=2)

        paste_button = tk.Button(toolbar, text="Paste", command=self.paste_objects)
        paste_button.pack(side=tk.LEFT, padx=2, pady=2)

        edit_button = tk.Button(toolbar, text="Edit", command=self.edit_object_properties)
        edit_button.pack(side=tk.LEFT, padx=2, pady=2)

        group_button = tk.Button(toolbar, text="Group", command=self.group_objects)
        group_button.pack(side=tk.LEFT, padx=2, pady=2)

        save_button = tk.Button(toolbar, text="Save", command=self.save_file)
        save_button.pack(side=tk.LEFT, padx=2, pady=2)

        ungroup_button = tk.Button(toolbar, text="UngroupAll", command=self.ungroupall_objects)
        ungroup_button.pack(side=tk.LEFT, padx=2, pady=2)

        ungroup_button = tk.Button(toolbar, text="Ungroup", command=self.ungroup_objects)
        ungroup_button.pack(side=tk.LEFT, padx=2, pady=2)

    def ungroupall_objects(self):
        if self.selected_objects:
            if self.selection_rect != None:
                coords = self.canvas.coords(self.selection_rect)
                # Find the group(s) inside the selection box
                groups_to_remove = []
                # for i, group_coords in enumerate(self.groups):
                #     if (group_coords[0] >= coords[0] and group_coords[1] >= coords[1] and
                #         group_coords[2] <= coords[2] and group_coords[3] <= coords[3]):
                #         groups_to_remove.append(i)
        # Check if any group is present within the selection rectangle
                objs_in_selection = self.canvas.find_overlapping(coords[0], coords[1], coords[2], coords[3])
                for i,group_coords in enumerate(self.groups):
                    # find objs in group
                    items_in_group = self.canvas.find_overlapping(group_coords[0], group_coords[1], group_coords[2], group_coords[3])
                    intersection = [value for value in items_in_group if value in objs_in_selection]
                    if len(intersection) > 0:
                        groups_to_remove.append(i)
                # Remove the identified group(s) from self.groups
                for index in sorted(groups_to_remove, reverse=True):
                    del self.groups[index]
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None
            for obj_id in self.objlist:
                    self.canvas.delete(obj_id)
    def ungroup_objects(self):
        if self.selected_objects:
            if self.selection_rect:
                coords = self.canvas.coords(self.selection_rect)
                # Find the group(s) inside the selection box
                groups_to_remove = []
                objs_in_selection = self.canvas.find_overlapping(coords[0], coords[1], coords[2], coords[3])
                for u,group_coords in enumerate(self.groups):
                    # find objs in group
                    items_in_group = self.canvas.find_overlapping(group_coords[0], group_coords[1], group_coords[2], group_coords[3])
                    intersection = [value for value in items_in_group if value in objs_in_selection]
                    if len(intersection) > 0:
                        groups_to_remove.append(u)
                # Iterate through all possible non-intersecting super groups
                for i in range(len(groups_to_remove)):
                    for j in range(len(groups_to_remove)):
                        if i!=j and groups_to_remove[i]!=-9999 and groups_to_remove[j]!=-9999:
                            group1 = groups_to_remove[i]
                            group2 = groups_to_remove[j]
                            print(group1,group2)
                            # Check if group2 is fully contained within group1
                            if (self.groups[group1][0] <= self.groups[group2][0] and self.groups[group1][1] <= self.groups[group2][1] and
                                self.groups[group1][2] >= self.groups[group2][2] and self.groups[group1][3] >= self.groups[group2][3]):
                                groups_to_remove[j]=-9999
                            # Check if group1 is fully contained within group2
                            elif (self.groups[group1][0] >= self.groups[group2][0] and self.groups[group1][1] >= self.groups[group2][1] and
                                self.groups[group1][2] <= self.groups[group2][2] and self.groups[group1][3] <= self.groups[group2][3]):
                                groups_to_remove[i]=-9999
                print(groups_to_remove,self.groups)
                # Remove the identified group(s) from self.groups
                for index in sorted(groups_to_remove, reverse=True):
                    if index!=-9999:
                        # print("i\n",groups_to_remove[index])
                        del self.groups[index]
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None
            for obj_id in self.objlist:
                    self.canvas.delete(obj_id)


    def toggle_move_mode(self):
        self.move_mode = True
        if self.move_mode:
            self.canvas.bind("<Button-1>", self.start_move)
            self.canvas.bind("<B1-Motion>", self.move_objects)
            self.canvas.bind("<ButtonRelease-1>", self.end_move)
        else:
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            if self.selection_rect:
                self.canvas.delete(self.selection_rect)
            self.selection_rect = None

    def toggle_select_mode(self):
        self.select_mode = True
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None
            for obj_id in self.objlist:
                    self.canvas.delete(obj_id)
                    print(f"hai: {obj_id}")
        if self.select_mode:
            self.selected_objects = []  # Clear selected objects list
            self.selection_rect = None
            self.canvas.bind("<Button-1>", self.start_selection)
            self.canvas.bind("<B1-Motion>", self.draw_selection_rectangle)
            self.canvas.bind("<ButtonRelease-1>", self.end_selection)
        else:
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            if self.selection_rect:
                self.canvas.delete(self.selection_rect)
                self.selection_rect = None
        print(self.selected_objects)
                

    def start_selection(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def draw_selection_rectangle(self, event):
        self.objlist=[]
        x, y = event.x, event.y
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
            for obj_id in self.objlist:
                self.canvas.delete(obj_id)
                print(f"hai: {obj_id}")
        self.selection_rect = self.canvas.create_rectangle(self.start_x, self.start_y, x, y, outline="blue", dash=(4, 4))
        # Check if any group is present within the selection rectangle
        objs_in_selection = self.canvas.find_overlapping(self.start_x, self.start_y, x, y)
        for i,group_coords in enumerate(self.groups):
            self.canvas.delete(str(i)+"view_rectangle")
            # find objs in group
            items_in_group = self.canvas.find_overlapping(group_coords[0], group_coords[1], group_coords[2], group_coords[3])
            intersection = [value for value in items_in_group if value in objs_in_selection]
            if len(intersection) > 0:
                obj=self.canvas.create_rectangle(group_coords[0], group_coords[1], group_coords[2], group_coords[3], outline="pink", dash=(4, 4),tags=str(i)+"view_rectangle")
                self.objlist.append(obj)
        # for i,group_coords in enumerate(self.groups):
        #     if (group_coords[0] >= self.start_x and group_coords[1] >= self.start_y and
        #         group_coords[2] <= x and group_coords[3] <= y):
        #         # Draw a pink dashed rectangle around the group
        #         obj=self.canvas.create_rectangle(group_coords[0], group_coords[1], group_coords[2], group_coords[3], outline="pink", dash=(4, 4),tags=str(i)+"view_rectangle")
        #         self.objlist.append(obj)
        #     elif (group_coords[0] >= x and group_coords[1] >= y and
        #         group_coords[2] <= self.start_x and group_coords[3] <= self.start_y):
        #         # Draw a pink dashed rectangle around the group
                


    # def group_view_objects(self):
    #     for group_coords in self.groups:
    #         obj=self.canvas.create_rectangle(group_coords[0], group_coords[1], group_coords[2], group_coords[3], outline="pink", dash=(4, 4))


    def end_selection(self, event):
        x, y = event.x, event.y
        items_in_selection = self.canvas.find_overlapping(self.start_x, self.start_y, x, y)
        self.selected_objects = list(items_in_selection)
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.finish_drawing)
        self.select_mode = False
        

    def start_move(self, event):
        if self.selected_objects:
            self.start_x = event.x
            self.start_y = event.y
            self.move_offset_x = 0
            self.move_offset_y = 0

    def move_objects(self, event):
        if self.selected_objects:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            if dx != 0 or dy != 0:
                move_list = []
                for obj_id in self.selected_objects:
                    # add condition to check for group. and then move the group also
                    # iterate through list of groups and check if the object is present in the group
                    for group_coords in self.groups:
                        # find the obj_id in the group and move all of them
                        items_in_group = self.canvas.find_overlapping(group_coords[0], group_coords[1], group_coords[2], group_coords[3])
                        if obj_id in items_in_group:
                            for groupobj_id in items_in_group:
                                if groupobj_id not in self.selected_objects:
                                    move_list.append(groupobj_id)
                    move_list.append(obj_id)
                self.selected_objects = move_list
                for obj_id in move_list:
                    self.canvas.move(obj_id, dx - self.move_offset_x, dy - self.move_offset_y)
                for obj_id in self.selected_objects:
                    for group_coords in self.groups:
                        if obj_id in items_in_group:
                            self.groups[self.groups.index(group_coords)] = (group_coords[0] + dx - self.move_offset_x, group_coords[1] + dy - self.move_offset_y, group_coords[2] + dx - self.move_offset_x, group_coords[3] + dy - self.move_offset_y)
                self.move_offset_x = dx
                self.move_offset_y = dy

    def end_move(self, event):
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None
        self.move_offset_x = 0
        self.move_offset_y = 0
        self.selected_objects = []
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.finish_drawing)
        self.move_mode = False

    def select_line(self):
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None
        self.selected_objects = []  # Clear selected objects list
        self.selected_objects.append("line")

    def select_rectangle(self):
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None
        self.selected_objects = []  # Clear selected objects list
        self.selected_objects.append("rectangle")

    def start_drawing(self, event):
        if not self.select_mode:
            self.start_x = event.x
            self.start_y = event.y

    def draw(self, event):
        if "line" in self.selected_objects:
            self.canvas.delete("temp_line")
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, tags="temp_line")
        elif "rectangle" in self.selected_objects:
            self.canvas.delete("temp_rectangle")
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="black", tags="temp_rectangle")
            

    def finish_drawing(self, event):
        if "line" in self.selected_objects:
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y)
        elif "rectangle" in self.selected_objects:
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="black")
            self.rectangle_type[str(self.canvas.find_all()[-1])] = "square"
            print(self.rectangle_type)

        # add code here to remove the duplicates present in the list 
        obj_list = self.canvas.find_all()
        # first check if in select mode
        if self.selection_rect:
            obj_list = obj_list[:-1]
        for obj_id in obj_list:
            if (int(obj_id) + 1 in obj_list and
                self.canvas.coords(obj_id) == self.canvas.coords(int(obj_id) + 1) and
                self.canvas.type(obj_id) == self.canvas.type(int(obj_id) + 1)):
                self.canvas.delete(obj_id)

    def delete_objects(self):
        for obj_id in self.selected_objects:
            # add condition to check for group. and then move the group also
            # iterate through list of groups and check if the object is present in the group
            for group_coords in self.groups:
                # find the obj_id in the group and move all of them
                items_in_group = self.canvas.find_overlapping(group_coords[0], group_coords[1], group_coords[2], group_coords[3])
                print("items_in_group",items_in_group)
                if obj_id in items_in_group:
                    for groupobj_id in items_in_group:
                        if groupobj_id not in self.selected_objects:
                            self.canvas.delete(groupobj_id)
            self.canvas.delete(obj_id)
        # In case you just select a group and no objects in it (and what if that group has a group inside it)
        self.selected_objects = []
        self.canvas.delete(self.selection_rect)

    def copy_objects(self):
        selected_objs = self.selected_objects.copy()
        for obj_id in self.selected_objects:
            for group_coords in self.groups:
                # find the obj_id in the group and move all of them
                items_in_group = self.canvas.find_overlapping(group_coords[0], group_coords[1], group_coords[2], group_coords[3])
                if obj_id in items_in_group:
                    for groupobj_id in items_in_group:
                        if groupobj_id not in self.selected_objects:
                            selected_objs.append(groupobj_id)
        if self.selection_rect:
            print("i")
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None

    def paste_objects(self):
        if self.copied_objects:
            # Calculate offset based on mouse position
            mouse_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
            mouse_y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
            dx = mouse_x - self.start_x
            dy = mouse_y - self.start_y
            for obj_id in self.copied_objects:
                # Get original coordinates of copied object
                x1, y1, x2, y2 = self.canvas.coords(obj_id)
                # Create copy at new position
                new_obj_id = None
                if self.canvas.type(obj_id) == "line":
                    new_obj_id = self.canvas.create_line(x1 + dx, y1 + dy, x2 + dx, y2 + dy)
                elif self.canvas.type(obj_id) == "rectangle":
                    new_obj_id = self.canvas.create_rectangle(x1 + dx, y1 + dy, x2 + dx, y2 + dy, outline="black")

    def group_objects(self):
        if self.selected_objects:
            if self.selection_rect !=None:
                coords = self.canvas.coords(self.selection_rect)
                items_in_group = self.canvas.find_overlapping(coords[0], coords[1], coords[2], coords[3])
                if len(list(items_in_group))>2:
                    self.groups.append(list(coords))
                    print(len(list(items_in_group)))
                else:
                    messagebox.showinfo("Single object is selected", "Please select an more than 1 object")
        self.canvas.delete(self.selection_rect)
        print(self.groups)

    def print_object_coordinates(self):
        print("Object Details:")
        for obj_id in self.canvas.find_all():
            obj_type = self.canvas.type(obj_id)  # Get the type of the object
            coordinates = self.canvas.coords(obj_id)
            print(f"Object ID: {obj_id}, Type: {obj_type}, Coordinates: {coordinates}")
        for obj_id in self.objlist:
                self.canvas.delete(obj_id)
                print(f"hai: {obj_id}")
    
    def save_file(self):
        # Define the file path where you want to store the data
        file_name = sd.askstring("Enter File Name", "Enter the file name (without extension):")
        added_objs = []
        if file_name:
            file_path = f"{file_name}.txt"
            with open(file_path, 'w') as file:
                for group_coords in self.groups:
                    items_in_group = self.canvas.find_overlapping(group_coords[0], group_coords[1], group_coords[2], group_coords[3]) 
                    if len(items_in_group) < 2:
                       continue
                    file.write("begin\n")
                    for item_group in items_in_group:
                        added_objs.append(item_group)
                        obj_type = self.canvas.type(obj_id)
                        coordinates = self.canvas.coords(obj_id)
                        coordinates_str = ' '.join(map(str, coordinates))
                        if obj_type == 'rectangle':
                            obj_type = 'rect'
                            round = self.rectangle_type.get(str(obj_id))
                            color = self.canvas.itemcget(obj_id, "outline")
                            file.write(f"{obj_type} {coordinates_str} {color} {round}\n")
                        elif obj_type == 'polygon':
                            coordinates = self.canvas.coords(obj_id)
                            coords = [coordinates[19], coordinates[20], coordinates[-2], coordinates[-1]]
                            coordinates_str = ' '.join(map(str, coords))
                            obj_type = 'rect'
                            round = self.rectangle_type.get(str(obj_id))
                            color = self.canvas.itemcget(obj_id, "outline")
                            file.write(f"{obj_type} {coordinates_str} {color} {round}\n")
                        elif obj_type == 'line':
                            color = self.canvas.itemcget(obj_id, "fill")
                            file.write(f"{obj_type} {coordinates_str} {color}\n")
                    file.write("end\n")
                        
                for obj_id in self.canvas.find_all():
                    obj_type = self.canvas.type(obj_id)
                    coordinates = self.canvas.coords(obj_id)
                    coordinates_str = ' '.join(map(str, coordinates))
                    if obj_type == 'rectangle':
                        obj_type = 'rect'
                        round = self.rectangle_type.get(str(obj_id))
                        color = self.canvas.itemcget(obj_id, "outline")
                        file.write(f"{obj_type} {coordinates_str} {color} {round}\n")
                    elif obj_type == 'polygon':
                        coordinates = self.canvas.coords(obj_id)
                        coords = [coordinates[19], coordinates[20], coordinates[-2], coordinates[-1]]
                        coordinates_str = ' '.join(map(str, coords))
                        obj_type = 'rect'
                        round = self.rectangle_type.get(str(obj_id))
                        color = self.canvas.itemcget(obj_id, "outline")
                        file.write(f"{obj_type} {coordinates_str} {color} {round}\n")
                    elif obj_type == 'line':
                        color = self.canvas.itemcget(obj_id, "fill")
                        file.write(f"{obj_type} {coordinates_str} {color}\n")
            

            print(f"Data written to '{file_path}' successfully.")
            
    def load_file(self,file_name=None):
        # Define the file path where you want to store the data
        if file_name:
            if file_name.endswith(".txt"):
                file_path = file_name
                self.canvas.delete("all")
                with open(file_path, 'r') as file:
                    for line in file:
                        data = line.split(" ")
                        if data[0] == 'line':
                            self.canvas.create_line(data[1], data[2], data[3], data[4])
                        elif data[0] == 'rect':
                            self.canvas.create_rectangle(data[1], data[2], data[3], data[4])

                print(f"Data loaded from '{file_path}' successfully.")
        else:
            file_name = sd.askstring("Enter File Name", "Enter the file name (with extension) (must be .txt):")
            if file_name and file_name.endswith(".txt"):
                self.load_file(file_name)
            
    def xmlExport(self):
        # Define the file path where you want to store the data
        file_name = sd.askstring("Enter File Name", "Enter the file name (without extension):")
        if file_name:
            file_path = f"{file_name}.xml"
            num_indents = 0
            indents = ''
            with open(file_path, 'w') as file:
                for obj_id in self.canvas.find_all():
                    obj_type = self.canvas.type(obj_id)
                    coordinates = self.canvas.coords(obj_id)
                    if obj_type == 'line':
                        for _ in range(num_indents):
                            indents += '\t'
                        file.write(indents + "<line>\n")
                        file.write(indents + "\t<begin>\n")
                        file.write(indents + f"\t\t<x>{coordinates[0]}</x>\n")
                        file.write(indents + f"\t\t<y>{coordinates[1]}</y>\n")
                        file.write(indents + "\t</begin>\n")
                        file.write(indents + "\t<end>\n")
                        file.write(indents + f"\t\t<x>{coordinates[2]}</x>\n")
                        file.write(indents + f"\t\t<y>{coordinates[3]}</y>\n")
                        file.write(indents + "\t</end>\n")
                        file.write(indents + "</line>\n")
                        indents = ''
                        
                    elif obj_type == 'rectangle':
                        for _ in range(num_indents):
                            indents += '\t'
                        file.write(indents + "<rectangle>\n")
                        file.write(indents + "\t<upper-left>\n")
                        file.write(indents + f"\t\t<x>{coordinates[0]}</x>\n")
                        file.write(indents + f"\t\t<y>{coordinates[1]}</y>\n")
                        file.write(indents + "\t</upper-left>\n")
                        file.write(indents + "\t<lower-right>\n")
                        file.write(indents + f"\t\t<x>{coordinates[2]}</x>\n")
                        file.write(indents + f"\t\t<y>{coordinates[3]}</y>\n")
                        file.write(indents + "\t</lower-right>\n")
                        file.write(indents + "</rectangle>\n")
                        indents = ''

            print(f"Data written to '{file_path}' successfully.")
    
    
    def edit_object_properties(self):
        if self.selected_objects:
            coords = self.canvas.coords(self.selection_rect)
                # Find the group(s) inside the selection box
            objs_in_selection = self.canvas.find_overlapping(coords[0], coords[1], coords[2], coords[3])
            for u,group_coords in enumerate(self.groups):
                # find objs in group
                items_in_group = self.canvas.find_overlapping(group_coords[0], group_coords[1], group_coords[2], group_coords[3])
                intersection = [value for value in items_in_group if value in objs_in_selection]
                if len(intersection) > 0:
                    messagebox.showinfo("Group is Selected", "Please select an object without group to edit.")
                    return
            for obj_id in self.selected_objects:
                if obj_id == self.selection_rect:
                    continue
                obj_type = self.canvas.type(obj_id)
                if obj_type == "line":
                    new_color = sd.askstring("Change Color", "Enter Line color (black, red, green, or blue):", initialvalue="black")
                    if new_color in ["black", "red", "green", "blue"]:
                        self.canvas.itemconfig(obj_id, fill=new_color)
                elif obj_type == "rectangle":
                    new_color = sd.askstring("Change Color", "Enter Rectangle color (black, red, green, or blue):", initialvalue="black")
                    if new_color in ["black", "red", "green", "blue"]:
                        self.canvas.itemconfig(obj_id, outline=new_color)

                    rounded_edges = sd.askstring("Rounded Edges", "Do you want rounded edges? (yes or no):", initialvalue="no")
                    if rounded_edges.lower() == "yes":
                        coords = self.canvas.coords(obj_id)
                        self.canvas.delete(obj_id)
                        self.selected_objects.remove(obj_id)  # Remove the old object ID
                        self.rectangle_type.pop(f'{obj_id}')
                        print(self.rectangle_type)
                        new_rectangle = self.round_rectangle(self,coords[0], coords[1], coords[2], coords[3], radius=25, outline=new_color, fill="")
                        self.rectangle_type[str(self.canvas.find_all()[-1])] = "rounded"
                        print(self.rectangle_type)
                        #self.selected_objects.append(new_rectangle)  # Add the new object ID
                
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None
        else:
            messagebox.showinfo("No Object Selected", "Please select an object to edit.")

if __name__ == "__main__":
    file_name = None
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()