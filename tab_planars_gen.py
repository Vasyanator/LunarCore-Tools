# tab_planars_gen.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import VERTICAL, RIGHT, LEFT, Y, END

# Import characteristics from stats_id.py
from stats_id import substats, stats_3, stats_4, stats_5, stats_6

class PlanarsTab:
    def __init__(self, notebook, items, command_manager):
        self.notebook = notebook
        self.items = items
        self.command_manager = command_manager

        self.frame = ttk.Frame(notebook)
        self.init_tab()

    def init_tab(self):
        # Initialize variables
        self.selected_item_id = None
        self.additional_stats = {}

        self.type_var = tk.StringVar(value='default')
        self.rarity_var = tk.StringVar(value='5')
        self.search_var = tk.StringVar()
        self.main_stat_var = tk.StringVar()
        self.main_stat_options = ["Select an item first"]  # Placeholder option
        self.main_stat_var.set(self.main_stat_options[0])      # Set default value
        self.additional_stats_var = tk.StringVar()
        self.additional_quantity_var = tk.StringVar(value='9')
        self.maxsteps_var = tk.BooleanVar()
        self.level_var = tk.StringVar(value='15')

        # Create main frame to hold left and right frames
        main_frame = tk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create left and right frames
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right Frame (Selection Interface)
        # Type selection
        type_label = tk.Label(right_frame, text="Select Type:")
        type_label.pack()

        type_frame = tk.Frame(right_frame)
        type_frame.pack()

        default_radio = tk.Radiobutton(type_frame, text="Default", variable=self.type_var, value='default', command=self.update_item_list)
        default_radio.pack(side=tk.LEFT)
        planars_radio = tk.Radiobutton(type_frame, text="Planars", variable=self.type_var, value='planars', command=self.update_item_list)
        planars_radio.pack(side=tk.LEFT)

        # Rarity selection
        rarity_label = tk.Label(right_frame, text="Select Rarity:")
        rarity_label.pack()

        rarity_combobox = ttk.Combobox(right_frame, textvariable=self.rarity_var, values=[str(i) for i in range(2, 6)], state='readonly')
        rarity_combobox.pack()
        rarity_combobox.bind('<<ComboboxSelected>>', self.update_item_list)

        # Search functionality
        search_label = tk.Label(right_frame, text="Search:")
        search_label.pack()

        search_entry = tk.Entry(right_frame, textvariable=self.search_var)
        search_entry.pack()
        self.search_var.trace('w', lambda *args: self.update_item_list())

        # Item selection with scrollbar
        item_frame = tk.Frame(right_frame)
        item_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(item_frame, orient=VERTICAL)
        self.item_listbox = tk.Listbox(item_frame, width=50, height=15, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.item_listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.item_listbox.pack(side=LEFT, fill=tk.BOTH, expand=True)
        self.item_listbox.bind('<<ListboxSelect>>', self.on_item_select)

        # Left Frame (Characteristic Generation Interface)
        # Main Stat Selection
        self.main_stat_label = tk.Label(left_frame, text="Main Stat:")
        self.main_stat_label.pack()

        self.main_stat_menu = tk.OptionMenu(left_frame, self.main_stat_var, *self.main_stat_options)
        self.main_stat_menu.config(state='disabled')  # Disabled until an item is selected
        self.main_stat_menu.pack()

        # Level selection
        level_label = tk.Label(left_frame, text="Select Level:")
        level_label.pack()

        level_spinbox = tk.Spinbox(left_frame, from_=1, to=15, textvariable=self.level_var, width=5, command=self.update_command)
        level_spinbox.pack()
        self.level_var.trace('w', lambda *args: self.update_command())

        # Additional Stats Selection
        additional_label = tk.Label(left_frame, text="Add Additional Stat:")
        additional_label.pack()

        additional_frame = tk.Frame(left_frame)
        additional_frame.pack()

        self.additional_stats_var.set(next(iter(substats)))  # Default value

        additional_stats_menu = tk.OptionMenu(additional_frame, self.additional_stats_var, *substats.keys())
        additional_stats_menu.pack(side=tk.LEFT)

        additional_quantity_entry = tk.Entry(additional_frame, textvariable=self.additional_quantity_var, width=5)
        additional_quantity_entry.pack(side=tk.LEFT)
        self.additional_quantity_var.set('1')  # Default quantity

        add_button = tk.Button(additional_frame, text="Add", command=self.add_additional_stat)
        add_button.pack(side=tk.LEFT)

        # Remove and Clear buttons
        buttons_frame = tk.Frame(left_frame)
        buttons_frame.pack(pady=5)

        remove_button = tk.Button(buttons_frame, text="Remove Selected", command=self.remove_additional_stat)
        remove_button.pack(side=tk.LEFT, padx=5)

        clear_button = tk.Button(buttons_frame, text="Clear All", command=self.clear_additional_stats)
        clear_button.pack(side=tk.LEFT, padx=5)

        # Listbox to show added additional stats
        self.additional_stats_listbox = tk.Listbox(left_frame, width=30, height=5)
        self.additional_stats_listbox.pack()

        # Maxsteps checkbox
        maxsteps_check = tk.Checkbutton(left_frame, text="Include -maxsteps", variable=self.maxsteps_var, command=self.update_command)
        maxsteps_check.pack()

        # Initialize the item list
        self.update_item_list()

        # Bind events
        self.main_stat_var.trace('w', self.update_command)
        self.level_var.trace('w', self.update_command)
        self.maxsteps_var.trace('w', self.update_command)

    def update_item_list(self, *args):
        # Update the item list based on the selected type and rarity
        type_selected = self.type_var.get()
        rarity_selected = self.rarity_var.get()
        search_text = self.search_var.get().lower()

        # Filter items based on type and rarity
        items = [item for item in self.items if item.type == type_selected and str(item.rarity) == rarity_selected]

        # Group items by id prefix (excluding last digit)
        groups = {}
        for item in items:
            id_prefix = item.id[:-1]  # Exclude last digit
            if id_prefix not in groups:
                groups[id_prefix] = []
            groups[id_prefix].append(item)

        # Clear the listbox
        self.item_listbox.delete(0, tk.END)

        # Create the item list with groupings and separators
        for group in groups.values():
            group_items = []
            for item in group:
                display_text = f"{item.title} ({item.id})"
                if search_text in item.title.lower() or search_text in item.id:
                    group_items.append(display_text)
            if group_items:
                for display_text in group_items:
                    self.item_listbox.insert(tk.END, display_text)
                self.item_listbox.insert(tk.END, '---')  # Add a separator after each group

        if self.item_listbox.size() > 0:
            last_item = self.item_listbox.get(tk.END)
            if last_item == '---':
                self.item_listbox.delete(tk.END)  # Remove last separator

        # Clear the command
        self.command_manager.update_command('')

    def on_item_select(self, event):
        selected_indices = self.item_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            selected_item = self.item_listbox.get(index)
            if selected_item != '---':
                # Extract the id from the selected item
                if '(' in selected_item and ')' in selected_item:
                    id_str = selected_item.split('(')[-1].split(')')[0]
                    self.selected_item_id = id_str
                    last_digit = int(id_str[-1])

                    # Update main_stat_options based on last_digit
                    if last_digit in [1, 2]:
                        # Main stat is fixed and not specified in command
                        self.main_stat_label.config(text="Main Stat: Fixed")
                        self.main_stat_var.set("Fixed")
                        self.main_stat_menu['menu'].delete(0, 'end')
                        self.main_stat_menu.config(state='disabled')
                    else:
                        # Enable main_stat_menu and populate options
                        self.main_stat_menu.config(state='normal')
                        self.main_stat_label.config(text="Select Main Stat:")
                        if last_digit == 3:
                            main_stats = stats_3
                        elif last_digit == 4:
                            main_stats = stats_4
                        elif last_digit == 5:
                            main_stats = stats_5
                        elif last_digit == 6:
                            main_stats = stats_6
                        else:
                            main_stats = {}
                        # Update main_stat_options
                        self.main_stat_options = list(main_stats.keys())
                        if self.main_stat_options:
                            self.main_stat_var.set(self.main_stat_options[0])
                            self.main_stat_menu['menu'].delete(0, 'end')
                            for option in self.main_stat_options:
                                self.main_stat_menu['menu'].add_command(label=option, command=tk._setit(self.main_stat_var, option, self.update_command))
                        else:
                            # Handle case where there are no main stats
                            self.main_stat_var.set("No Main Stats Available")
                            self.main_stat_menu['menu'].delete(0, 'end')
                            self.main_stat_menu['menu'].add_command(label="No Main Stats Available", command=tk._setit(self.main_stat_var, "No Main Stats Available", self.update_command))
                            self.main_stat_menu.config(state='disabled')

                    # Do not clear additional stats; preserve them across item selections
                    # Update the command
                    self.update_command()
                else:
                    self.command_manager.update_command('')
            else:
                self.command_manager.update_command('')
        else:
            self.command_manager.update_command('')

    def update_command(self, *args):
        if not self.selected_item_id:
            self.command_manager.update_command('')
            return

        command_parts = [f"/give {self.selected_item_id}"]

        # Determine if main stat should be included
        last_digit = int(self.selected_item_id[-1])
        if last_digit not in [1, 2]:
            # Include main stat
            main_stat_name = self.main_stat_var.get()
            if main_stat_name in ["Fixed", "No Main Stats Available"]:
                # Do not include main stat in command
                pass
            else:
                # Find the id of the main stat
                if last_digit == 3:
                    main_stats = stats_3
                elif last_digit == 4:
                    main_stats = stats_4
                elif last_digit == 5:
                    main_stats = stats_5
                elif last_digit == 6:
                    main_stats = stats_6
                else:
                    main_stats = {}
                main_stat_id = main_stats.get(main_stat_name)
                if main_stat_id:
                    command_parts.append(f"s{main_stat_id}")
        else:
            # For last digits 1 and 2, main stat is not included in command
            pass

        # Add additional stats
        for stat_name, quantity in self.additional_stats.items():
            stat_id = substats.get(stat_name)
            if stat_id:
                command_parts.append(f"{stat_id}:{quantity}")

        # Add selected level
        level = self.level_var.get()
        command_parts.append(f"lv{level}")

        # Add '-maxsteps' if selected
        if self.maxsteps_var.get():
            command_parts.append("-maxsteps")

        # Set the command
        command = ' '.join(command_parts)
        self.command_manager.update_command(command)

    def add_additional_stat(self):
        stat_name = self.additional_stats_var.get()
        quantity = self.additional_quantity_var.get()

        if not stat_name or not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showwarning("Invalid Input", "Please select a valid stat and enter a positive quantity.")
            return

        # Add to the dictionary
        self.additional_stats[stat_name] = quantity

        # Update the listbox
        self.additional_stats_listbox.delete(0, tk.END)
        for stat, qty in self.additional_stats.items():
            self.additional_stats_listbox.insert(tk.END, f"{stat} x{qty}")

        # Update the command
        self.update_command()

    def remove_additional_stat(self):
        selected_indices = self.additional_stats_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            stat_entry = self.additional_stats_listbox.get(index)
            stat_name = stat_entry.split(' x')[0]
            # Remove from the dictionary
            if stat_name in self.additional_stats:
                del self.additional_stats[stat_name]
            # Update the listbox
            self.additional_stats_listbox.delete(index)
            # Update the command
            self.update_command()
        else:
            messagebox.showwarning("No Selection", "Please select a stat to remove.")

    def clear_additional_stats(self):
        self.additional_stats.clear()
        self.additional_stats_listbox.delete(0, tk.END)
        # Update the command
        self.update_command()
