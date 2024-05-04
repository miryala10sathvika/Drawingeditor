import tkinter as tk

class DrawingApp:
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
        object_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="Objects", menu=object_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Delete", command=self.delete_objects)
        edit_menu.add_command(label="Move", command=self.toggle_move_mode)
        edit_menu.add_command(label="Copy", command=self.copy_objects)
        edit_menu.add_command(label="Paste", command=self.paste_objects)
        menubar.add_cascade(label="Operations", menu=edit_menu)

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
        print("hai\n")

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

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()