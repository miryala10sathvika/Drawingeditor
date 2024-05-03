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
        menubar.add_cascade(label="Edit", menu=edit_menu)

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

    def toggle_select_mode(self):
        self.select_mode = True
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
        self.selected_objects = items_in_selection
        self.selection_rect = None
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.finish_drawing)
        self.select_mode = False

    def select_line(self):
        self.selected_objects = []  # Clear selected objects list
        self.selected_objects.append("line")

    def select_rectangle(self):
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

    def delete_objects(self):
        for obj_id in self.selected_objects:
            self.canvas.delete(obj_id)
        self.selected_objects = []
        self.canvas.delete(self.selection_rect)
        


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()