import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import VERTICAL, RIGHT, LEFT, Y, END
from stats_id import substats, substats_levels, stats_3, stats_4, stats_5, stats_6

class PlanarsTab:

    def __init__(self, notebook, items, command_manager, localization):
        self.localization = localization
        
        self.localized_substats = self.localize_stat_keys(substats)
        self.localized_substats_levels = self.localize_stat_keys(substats_levels)
        self.localized_stats_3 = self.localize_stat_keys(stats_3)
        self.localized_stats_4 = self.localize_stat_keys(stats_4)
        self.localized_stats_5 = self.localize_stat_keys(stats_5)
        self.localized_stats_6 = self.localize_stat_keys(stats_6)
        self.notebook = notebook
        self.items = items
        self.command_manager = command_manager
        self.frame = ttk.Frame(notebook)
        self.init_tab()

    def init_tab(self):
        self.selected_item_id = None
        self.additional_stats = {}
        self.type_var = tk.StringVar(value='default')
        self.rarity_var = tk.StringVar(value='5')
        self.search_var = tk.StringVar()
        self.main_stat_var = tk.StringVar()
        self.main_stat_options = [self.localization['Select_an_item_first']]
        self.main_stat_var.set(self.main_stat_options[0])
        self.additional_stats_var = tk.StringVar()
        self.additional_quantity_var = tk.StringVar(value='1')
        self.maxsteps_var = tk.BooleanVar()
        self.level_var = tk.StringVar(value='15')
        self.additional_levels_var = tk.BooleanVar()
        self.additional_levels_var.set(True)
        self.additional_level_index_var = tk.IntVar(value=0)
        main_frame = tk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True)
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        type_label = tk.Label(right_frame, text=self.localization['Select_Type'])
        type_label.pack()
        type_frame = tk.Frame(right_frame)
        type_frame.pack()
        default_radio = tk.Radiobutton(type_frame, text=self.localization['Default'], variable=self.type_var, value='default', command=self.update_item_list)
        default_radio.pack(side=tk.LEFT)
        planars_radio = tk.Radiobutton(type_frame, text=self.localization['Planars'], variable=self.type_var, value='planars', command=self.update_item_list)
        planars_radio.pack(side=tk.LEFT)
        rarity_label = tk.Label(right_frame, text=self.localization['Select_Rarity:'])
        rarity_label.pack()
        rarity_combobox = ttk.Combobox(right_frame, textvariable=self.rarity_var, values=[str(i) for i in range(2, 6)], state='readonly')
        rarity_combobox.pack()
        rarity_combobox.bind('<<ComboboxSelected>>', self.update_item_list)
        search_label = tk.Label(right_frame, text=self.localization['Search:'])
        search_label.pack()
        search_entry = tk.Entry(right_frame, textvariable=self.search_var)
        search_entry.pack()
        self.search_var.trace('w', lambda *args: self.update_item_list())
        item_frame = tk.Frame(right_frame)
        item_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(item_frame, orient=VERTICAL)
        self.item_listbox = tk.Listbox(item_frame, width=50, height=15, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.item_listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.item_listbox.pack(side=LEFT, fill=tk.BOTH, expand=True)
        self.item_listbox.bind('<<ListboxSelect>>', self.on_item_select)
        self.main_stat_label = tk.Label(left_frame, text=self.localization['Main_Stat:'])
        self.main_stat_label.pack()
        self.main_stat_menu = tk.OptionMenu(left_frame, self.main_stat_var, *self.main_stat_options)
        self.main_stat_menu.config(state='disabled')
        self.main_stat_menu.pack()
        level_label = tk.Label(left_frame, text=self.localization['Select_Level:'])
        level_label.pack()
        level_spinbox = tk.Spinbox(left_frame, from_=1, to=15, textvariable=self.level_var, width=5, command=self.update_command)
        level_spinbox.pack()
        self.level_var.trace('w', lambda *args: self.update_command())
        additional_label = tk.Label(left_frame, text=self.localization['Additional_stats:'])
        additional_label.pack(pady=5)
        additional_stats_frame = tk.Frame(left_frame)
        additional_stats_frame.pack()
        select_stat_label = tk.Label(additional_stats_frame, text=self.localization['Select_stat:'])
        select_stat_label.grid(row=0, column=0, sticky='e')
        self.additional_stats_var.set(next(iter(self.localized_substats)))
        additional_stats_menu = tk.OptionMenu(additional_stats_frame, self.additional_stats_var, *self.localized_substats.keys())
        additional_stats_menu.grid(row=0, column=1, sticky='w')
        quantity_label = tk.Label(additional_stats_frame, text=self.localization['Quantity:'])
        quantity_label.grid(row=1, column=0, sticky='e')
        additional_quantity_entry = tk.Spinbox(additional_stats_frame, from_=1, to=15, textvariable=self.additional_quantity_var, width=5)
        additional_quantity_entry.grid(row=1, column=1, sticky='w')
        self.additional_quantity_var.set('1')
        self.level_label = tk.Label(additional_stats_frame, text=self.localization['Select_Value:'])
        self.level_label.grid(row=2, column=0, sticky='e')
        self.level_frame = tk.Frame(additional_stats_frame)
        self.level_frame.grid(row=2, column=1, sticky='w')
        self.additional_level_index_var = tk.IntVar(value=0)
        self.additional_stats_var.trace('w', self.update_level_options)
        add_button = tk.Button(additional_stats_frame, text=self.localization['Add'], command=self.add_additional_stat)
        add_button.grid(row=3, column=0, columnspan=2, pady=5)
        current_additional_label = tk.Label(left_frame, text=self.localization['Current_additional_stats:'])
        current_additional_label.pack()
        self.additional_stats_listbox = tk.Listbox(left_frame, width=30, height=5)
        self.additional_stats_listbox.pack()
        buttons_frame = tk.Frame(left_frame)
        buttons_frame.pack(pady=5)
        remove_button = tk.Button(buttons_frame, text=self.localization['Remove_Selected'], command=self.remove_additional_stat)
        remove_button.pack(side=tk.LEFT, padx=5)
        clear_button = tk.Button(buttons_frame, text=self.localization['Clear_All'], command=self.clear_additional_stats)
        clear_button.pack(side=tk.LEFT, padx=5)
        maxsteps_check = tk.Checkbutton(left_frame, text=self.localization['Include_-maxsteps'], variable=self.maxsteps_var, command=self.update_command)
        maxsteps_check.pack()
        levels_check = tk.Checkbutton(left_frame, text=self.localization['Levels_of_additional_stats'], variable=self.additional_levels_var, command=self.on_additional_levels_toggle)
        levels_check.pack()
        self.update_item_list()
        self.main_stat_var.trace('w', self.update_command)
        self.level_var.trace('w', self.update_command)
        self.maxsteps_var.trace('w', self.update_command())
        self.update_level_options()
    
    def localize_stat_keys(self, original_dict):
        return {
            self.localization['Stats'].get(key, key): value
            for key, value in original_dict.items()
        }

    def update_level_options(self, *args):
        # Clear existing radiobuttons
        for widget in self.level_frame.winfo_children():
            widget.destroy()
        stat_name = self.additional_stats_var.get()
        if stat_name in self.localized_substats_levels:
            level_values = self.localized_substats_levels[stat_name]
            for i, value in enumerate(level_values):
                # Round value to one decimal
                display_value = round(value, 1)
                rb = tk.Radiobutton(self.level_frame, text=str(display_value), variable=self.additional_level_index_var, value=i)
                rb.pack(side=tk.LEFT)
            # Set default selection
            self.additional_level_index_var.set(0)
        else:
            # No levels available
            self.additional_level_index_var.set(0)
            rb = tk.Radiobutton(self.level_frame, text='N/A', variable=self.additional_level_index_var, value=0, state='disabled')
            rb.pack(side=tk.LEFT)
        # Disable level selection if /give is used
        if not self.additional_levels_var.get():
            for widget in self.level_frame.winfo_children():
                widget.config(state='disabled')

    def on_additional_levels_toggle(self):
        if self.additional_levels_var.get():
            # Enable level selection
            for widget in self.level_frame.winfo_children():
                widget.config(state='normal')
        else:
            # Disable level selection
            for widget in self.level_frame.winfo_children():
                widget.config(state='disabled')
        self.update_command()

    def update_item_list(self, *args):
        type_selected = self.type_var.get()
        rarity_selected = self.rarity_var.get()
        search_text = self.search_var.get().lower()
        items = [item for item in self.items if item.type == type_selected and str(item.rarity) == rarity_selected]
        groups = {}
        for item in items:
            id_prefix = item.id[:-1]
            if id_prefix not in groups:
                groups[id_prefix] = []
            groups[id_prefix].append(item)
        self.item_listbox.delete(0, tk.END)
        for group in groups.values():
            group_items = []
            for item in group:
                display_text = f'{item.title} ({item.id})'
                if search_text in item.title.lower() or search_text in item.id:
                    group_items.append(display_text)
            if group_items:
                for display_text in group_items:
                    self.item_listbox.insert(tk.END, display_text)
                self.item_listbox.insert(tk.END, '---')
        if self.item_listbox.size() > 0:
            last_item = self.item_listbox.get(tk.END)
            if last_item == '---':
                self.item_listbox.delete(tk.END)
        self.command_manager.update_command('')

    def on_item_select(self, event):
        selected_indices = self.item_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            selected_item = self.item_listbox.get(index)
            if selected_item != '---':
                if '(' in selected_item and ')' in selected_item:
                    id_str = selected_item.split('(')[-1].split(')')[0]
                    self.selected_item_id = id_str
                    last_digit = int(id_str[-1])
                    if last_digit in [1, 2]:
                        self.main_stat_label.config(text=self.localization['Main_Stat:_Fixed'])
                        self.main_stat_var.set('Fixed')
                        self.main_stat_menu['menu'].delete(0, 'end')
                        self.main_stat_menu.config(state='disabled')
                    else:
                        self.main_stat_menu.config(state='normal')
                        self.main_stat_label.config(text=self.localization['Select_Main_Stat:'])
                        if last_digit == 3:
                            main_stats = self.localized_stats_3
                        elif last_digit == 4:
                            main_stats = self.localized_stats_4
                        elif last_digit == 5:
                            main_stats = self.localized_stats_5
                        elif last_digit == 6:
                            main_stats = self.localized_stats_6
                        else:
                            main_stats = {}
                        self.main_stat_options = list(main_stats.keys())
                        if self.main_stat_options:
                            self.main_stat_var.set(self.main_stat_options[0])
                            self.main_stat_menu['menu'].delete(0, 'end')
                            for option in self.main_stat_options:
                                self.main_stat_menu['menu'].add_command(label=option, command=tk._setit(self.main_stat_var, option, self.update_command))
                        else:
                            self.main_stat_var.set('No Main Stats Available')
                            self.main_stat_menu['menu'].delete(0, 'end')
                            self.main_stat_menu['menu'].add_command(label=self.localization['No_Main_Stats_Available'], command=tk._setit(self.main_stat_var, 'No Main Stats Available', self.update_command))
                            self.main_stat_menu.config(state='disabled')
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
        command_parts = []
        if self.additional_levels_var.get():
            command_parts.append(f'/relics {self.selected_item_id}')
        else:
            command_parts.append(f'/give {self.selected_item_id}')
        last_digit = int(self.selected_item_id[-1])
        if last_digit not in [1, 2]:
            main_stat_name = self.main_stat_var.get()
            if main_stat_name in ['Fixed', 'No Main Stats Available']:
                pass
            else:
                if last_digit == 3:
                    main_stats = self.localized_stats_3
                elif last_digit == 4:
                    main_stats = self.localized_stats_4
                elif last_digit == 5:
                    main_stats = self.localized_stats_5
                elif last_digit == 6:
                    main_stats = self.localized_stats_6
                else:
                    main_stats = {}
                main_stat_id = main_stats.get(main_stat_name)
                if main_stat_id:
                    command_parts.append(f's{main_stat_id}')
        else:
            pass
        for stat_name, (quantity, level_index) in self.additional_stats.items():
            stat_id = self.localized_substats.get(stat_name)
            if stat_id:
                if self.additional_levels_var.get() and level_index is not None:
                    level_in_command = level_index + 1  # Level is index + 1
                    command_parts.append(f'{stat_id}:{quantity}:{level_in_command}')
                else:
                    command_parts.append(f'{stat_id}:{quantity}')
        level = self.level_var.get()
        command_parts.append(f'lv{level}')
        if self.maxsteps_var.get():
            command_parts.append('-maxsteps')
        command = ' '.join(command_parts)
        self.command_manager.update_command(command)


    def add_additional_stat(self):
        stat_name = self.additional_stats_var.get()
        quantity = self.additional_quantity_var.get()
        if not stat_name or not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showwarning('Invalid Input', 'Please select a valid stat and enter a positive quantity.')
            return
        quantity = int(quantity)
        if self.additional_levels_var.get():
            level_index = self.additional_level_index_var.get()
            if stat_name in self.localized_substats_levels and 0 <= level_index <= 2:
                level_value = self.localized_substats_levels[stat_name][level_index]
            else:
                messagebox.showwarning('Invalid Input', 'Please select a valid level value.')
                return
        else:
            level_index = None
            level_value = None
        # Calculate total value
        if level_value is not None:
            total_value = quantity * level_value
            total_value = round(total_value, 1)
        else:
            total_value = None
        # Add to additional_stats dictionary
        self.additional_stats[stat_name] = (quantity, level_index)
        # Update the listbox
        self.additional_stats_listbox.delete(0, tk.END)
        for stat, (qty, lvl_idx) in self.additional_stats.items():
            if lvl_idx is not None:
                lvl_value = self.localized_substats_levels[stat][lvl_idx]
                total_val = qty * lvl_value
                total_val = round(total_val, 1)
                self.additional_stats_listbox.insert(tk.END, f'{stat} x{qty} ({total_val})')
            else:
                self.additional_stats_listbox.insert(tk.END, f'{stat} x{qty}')
        self.update_command()


    def remove_additional_stat(self):
        selected_indices = self.additional_stats_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            stat_entry = self.additional_stats_listbox.get(index)
            stat_name = stat_entry.split(' x')[0]
            if stat_name in self.additional_stats:
                del self.additional_stats[stat_name]
            self.additional_stats_listbox.delete(index)
            self.update_command()
        else:
            messagebox.showwarning('No Selection', 'Please select a stat to remove.')

    def clear_additional_stats(self):
        self.additional_stats.clear()
        self.additional_stats_listbox.delete(0, tk.END)
        self.update_command()
