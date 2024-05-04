import tkinter as tk
import tkinter.simpledialog as sd
import tkinter.messagebox as messagebox

from tkinter import *

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
                x2, y2,
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

        self.selected_objects = []  # List to store IDs of selected objects
        self.start_x = None
        self.start_y = None
        self.selection_rect = None
        self.select_mode = False  # Flag to indicate selection mode
        self.move_mode = False # Flag to indicate move mode
        self.move_offset_x = 0  # Offset for moving objects
        self.move_offset_y = 0

        self.create_menu()
        self.create_toolbar()

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
        menubar.add_cascade(label="Operations", menu=saveExport_menu)

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
        x, y = event.x, event.y
        if self.selection_rect:
            self.canvas.delete(self.selection_rect)
        self.selection_rect = self.canvas.create_rectangle(self.start_x, self.start_y, x, y, outline="blue", dash=(4, 4))

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
                for obj_id in self.selected_objects:
                    self.canvas.move(obj_id, dx - self.move_offset_x, dy - self.move_offset_y)
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
            self.canvas.delete(obj_id)
        self.selected_objects = []
        self.canvas.delete(self.selection_rect)

    def copy_objects(self):
        self.copied_objects = list(self.selected_objects)
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

    def print_object_coordinates(self):
        print("Object Details:")
        for obj_id in self.canvas.find_all():
            obj_type = self.canvas.type(obj_id)  # Get the type of the object
            coordinates = self.canvas.coords(obj_id)
            print(f"Object ID: {obj_id}, Type: {obj_type}, Coordinates: {coordinates}")
    
    def save_file(self):
        # Define the file path where you want to store the data
        file_name = sd.askstring("Enter File Name", "Enter the file name (without extension):")
        if file_name:
            file_path = f"{file_name}.txt"
            with open(file_path, 'w') as file:
                for obj_id in self.canvas.find_all():
                    obj_type = self.canvas.type(obj_id)
                    coordinates = self.canvas.coords(obj_id)
                    if obj_type == 'rectangle':
                        obj_type = 'rect'
                    coordinates_str = ' '.join(map(str, coordinates))
                    file.write(f"{obj_type} {coordinates_str}\n")

            print(f"Data written to '{file_path}' successfully.")
            
    def load_file(self):
        # Define the file path where you want to store the data
        file_name = sd.askstring("Enter File Name", "Enter the file name (with extension) (must be .txt):")
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
            for obj_id in self.selected_objects:
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
                        new_rectangle = self.round_rectangle(self,coords[0], coords[1], coords[2], coords[3], radius=25, outline=new_color, fill="")
                        self.canvas.delete(obj_id)
                        self.selected_objects.remove(obj_id)  # Remove the old object ID
                        self.selected_objects.append(new_rectangle)  # Add the new object ID
                
            self.canvas.delete(self.selection_rect)
        else:
            messagebox.showinfo("No Object Selected", "Please select an object to edit.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()