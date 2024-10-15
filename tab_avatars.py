# tab_avatars.py

import tkinter as tk
from tkinter import ttk
from tkinter import VERTICAL, RIGHT, LEFT, Y, StringVar, IntVar, messagebox

class AvatarsTab:
    def __init__(self, notebook, avatars_list, command_manager):
        self.notebook = notebook
        self.avatars_list = avatars_list
        self.command_manager = command_manager

        self.frame = ttk.Frame(notebook)
        self.init_tab()

    def init_tab(self):
        # Create sub-tabs
        self.sub_notebook = ttk.Notebook(self.frame)
        self.sub_notebook.pack(fill=tk.BOTH, expand=True)

        # Create 'Lineup & Properties' tab
        self.create_lineup_properties_tab()

        # Create 'Give' tab (this can be implemented later)
        # self.create_give_tab()

    def create_lineup_properties_tab(self):
        tab_frame = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(tab_frame, text='Lineup & Properties')

        

        # Main frame
        main_frame = tk.Frame(tab_frame)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame for Lineup section
        lineup_frame = tk.Frame(main_frame)
        lineup_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right frame for Properties section
        properties_frame = tk.Frame(main_frame)
        properties_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Lineup Section
        self.create_lineup_section(lineup_frame)

        # Properties Section
        self.create_properties_section(properties_frame)

    def create_lineup_section(self, parent_frame):
        # Title
        lineup_label = tk.Label(parent_frame, text="Lineup", font=("Arial", 12, "bold"))
        lineup_label.pack(pady=5)

        # Warning label
        warning_label = tk.Label(parent_frame, text="USE AT YOUR OWN RISK", fg="red", font=("Arial", 14, "bold"))
        warning_label.pack(pady=5)

        # Search functionality
        search_var = StringVar()
        search_label = tk.Label(parent_frame, text="Search:")
        search_label.pack()
        search_entry = tk.Entry(parent_frame, textvariable=search_var)
        search_entry.pack()
        search_var.trace('w', lambda *args: update_avatar_list())

        # Avatar listbox
        avatar_frame = tk.Frame(parent_frame)
        avatar_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(avatar_frame, orient=VERTICAL)
        avatar_listbox = tk.Listbox(avatar_frame, width=30, height=15, yscrollcommand=scrollbar.set, exportselection=False)
        scrollbar.config(command=avatar_listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        avatar_listbox.pack(side=LEFT, fill=tk.BOTH, expand=True)

        # Lineup listbox
        lineup_list_label = tk.Label(parent_frame, text="Lineup List:")
        lineup_list_label.pack(pady=5)
        lineup_listbox = tk.Listbox(parent_frame, width=30, height=10, exportselection=False)
        lineup_listbox.pack(fill=tk.BOTH, expand=True)

        # Buttons
        buttons_frame = tk.Frame(parent_frame)
        buttons_frame.pack(pady=5)
        add_button = tk.Button(buttons_frame, text="Add", command=lambda: add_to_lineup())
        add_button.pack(side=LEFT, padx=5)
        remove_button = tk.Button(buttons_frame, text="Remove", command=lambda: remove_from_lineup())
        remove_button.pack(side=LEFT, padx=5)
        clear_button = tk.Button(buttons_frame, text="Clear", command=lambda: clear_lineup())
        clear_button.pack(side=LEFT, padx=5)

        # Initialize variables
        selected_avatar_id = None
        lineup_ids = []

        # Function to update avatar list based on search
        def update_avatar_list():
            search_text = search_var.get().lower()

            # Clear the listbox
            avatar_listbox.delete(0, tk.END)

            # Populate the listbox
            for entry in self.avatars_list:
                display_text = f"{entry['name']} ({entry['id']})"
                if search_text in entry['name'].lower() or search_text in entry['id']:
                    avatar_listbox.insert(tk.END, display_text)

        # Bind selection event
        def on_avatar_select(event):
            nonlocal selected_avatar_id
            selected_indices = avatar_listbox.curselection()
            if selected_indices:
                index = selected_indices[0]
                selected_avatar = avatar_listbox.get(index)
                if '(' in selected_avatar and ')' in selected_avatar:
                    id_str = selected_avatar.split('(')[-1].split(')')[0]
                    selected_avatar_id = id_str
                else:
                    selected_avatar_id = None
            else:
                selected_avatar_id = None

        avatar_listbox.bind('<<ListboxSelect>>', on_avatar_select)

        # Function to add selected avatar to lineup
        def add_to_lineup():
            if selected_avatar_id:
                #if selected_avatar_id not in lineup_ids:
                lineup_ids.append(selected_avatar_id)
                lineup_listbox.insert(tk.END, selected_avatar_id)
                update_lineup_command()
                #else:
                    #messagebox.showinfo("Info", "Avatar already in lineup.")
            else:
                messagebox.showwarning("Warning", "No avatar selected.")

        # Function to remove selected avatar from lineup
        def remove_from_lineup():
            selected_indices = lineup_listbox.curselection()
            if selected_indices:
                index = selected_indices[0]
                avatar_id = lineup_listbox.get(index)
                lineup_listbox.delete(index)
                lineup_ids.remove(avatar_id)
                update_lineup_command()
            else:
                messagebox.showwarning("Warning", "No avatar selected in lineup.")

        # Function to clear the lineup
        def clear_lineup():
            lineup_listbox.delete(0, tk.END)
            lineup_ids.clear()
            update_lineup_command()

        # Function to update the lineup command
        def update_lineup_command():
            if lineup_ids:
                command = f"/lineup {' '.join(lineup_ids)}"
                self.command_manager.update_command(command)
            else:
                self.command_manager.update_command('')

        # Initialize the avatar list
        update_avatar_list()

    def create_properties_section(self, parent_frame):
        # Title
        properties_label = tk.Label(parent_frame, text="Properties", font=("Arial", 12, "bold"))
        properties_label.pack(pady=5)

        # Target selection
        target_label = tk.Label(parent_frame, text="Target:")
        target_label.pack()
        target_var = StringVar(value='cur')
        target_options = ['cur', 'all', 'lineup']
        target_menu = ttk.OptionMenu(parent_frame, target_var, target_options[0], *target_options, command=lambda _: update_properties_command())
        target_menu.pack()

        # Level
        level_label = tk.Label(parent_frame, text="Level (1-80):")
        level_label.pack()
        level_var = StringVar(value='1')
        level_entry = tk.Entry(parent_frame, textvariable=level_var)
        level_entry.pack()
        level_var.trace('w', lambda *args: update_properties_command())

        # Ascension
        ascension_label = tk.Label(parent_frame, text="Ascension (0-6):")
        ascension_label.pack()
        ascension_var = StringVar(value='0')
        ascension_entry = tk.Entry(parent_frame, textvariable=ascension_var)
        ascension_entry.pack()
        ascension_var.trace('w', lambda *args: update_properties_command())

        # Eidolon
        eidolon_label = tk.Label(parent_frame, text="Eidolon (0-6):")
        eidolon_label.pack()
        eidolon_var = StringVar(value='0')
        eidolon_entry = tk.Entry(parent_frame, textvariable=eidolon_var)
        eidolon_entry.pack()
        eidolon_var.trace('w', lambda *args: update_properties_command())

        # Skill Levels
        skill_label = tk.Label(parent_frame, text="Skill Levels (1-12):")
        skill_label.pack()
        skill_var = StringVar(value='1')
        skill_entry = tk.Entry(parent_frame, textvariable=skill_var)
        skill_entry.pack()
        skill_var.trace('w', lambda *args: update_properties_command())

        # Function to update the properties command
        def update_properties_command():
            target = target_var.get()
            level = level_var.get()
            ascension = ascension_var.get()
            eidolon = eidolon_var.get()
            skill = skill_var.get()

            # Validate inputs
            if not level.isdigit() or not (1 <= int(level) <= 80):
                self.command_manager.update_command('')
                return
            if not ascension.isdigit() or not (0 <= int(ascension) <= 6):
                self.command_manager.update_command('')
                return
            if not eidolon.isdigit() or not (0 <= int(eidolon) <= 6):
                self.command_manager.update_command('')
                return
            if not skill.isdigit() or not (1 <= int(skill) <= 12):
                self.command_manager.update_command('')
                return

            command = f"/avatar {target} lv{level} p{ascension} e{eidolon} s{skill}"
            self.command_manager.update_command(command)

        # Initialize the properties command
        update_properties_command()

    # Placeholder for 'Give' tab (can be implemented as needed)
    # def create_give_tab(self):
    #     pass