import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import VERTICAL, RIGHT, LEFT, Y, END

# Import characteristics from stats_id.py
from stats_id import substats, stats_3, stats_4, stats_5, stats_6

# Pre-defined dictionaries (lists in this case)
planars_2 = []
planars_3 = []
planars_4 = []
planars_5 = []
default_2 = []
default_3 = []
default_4 = []
default_5 = []

# Mapping of list names to the actual lists
list_dict = {
    'planars_2': planars_2,
    'planars_3': planars_3,
    'planars_4': planars_4,
    'planars_5': planars_5,
    'default_2': default_2,
    'default_3': default_3,
    'default_4': default_4,
    'default_5': default_5
}

# Placeholder for widgets that need to be accessed globally
item_listbox = None  # Will be assigned in main
root = None  # Will be assigned in main

def process_file(filename):
    # Read the file with UTF-8 encoding to handle names in any language
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Process each line
    for line in lines:
        # Remove any leading/trailing whitespace
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Split the line into id and name
        if ':' in line:
            id_part, name_part = line.split(':', 1)
        else:
            # Skip lines that don't have the correct format
            continue

        id_str = id_part.strip()
        name = name_part.strip()

        # Check if id is a 5-digit number
        if len(id_str) != 5 or not id_str.isdigit():
            continue

        # **New check: Skip IDs where the second digit is '0'**
        if id_str[1] == '0':
            continue

        # Get the first digit and check if it's between 3 and 6 inclusive
        first_digit = int(id_str[0])
        if first_digit < 3 or first_digit > 6:
            continue

        if 'null' in name.lower():
            continue

        # Determine the rarity based on the first digit minus 1
        rarity = first_digit - 1  # Rarity from 2 to 5

        # Determine the type based on the last digit
        last_digit = int(id_str[-1])
        if last_digit in [1, 2, 3, 4]:
            type_name = 'default'
        elif last_digit in [5, 6]:
            type_name = 'planars'
        else:
            continue  # Skip if last digit is not in the specified range

        # Construct the list name
        list_name = f"{type_name}_{rarity}"

        # Add the entry to the appropriate list
        if list_name in list_dict:
            list_dict[list_name].append({'id': id_str, 'title': name})


def update_item_list(*args):
    global type_var, rarity_var, search_var, item_listbox, give_command

    type_selected = type_var.get()
    rarity_selected = rarity_var.get()
    search_text = search_var.get().lower()

    list_name = f"{type_selected}_{rarity_selected}"

    items = list_dict.get(list_name, [])
    # Group items by id prefix (excluding last digit)
    groups = {}
    for item in items:
        id_prefix = item['id'][:-1]  # Exclude last digit
        if id_prefix not in groups:
            groups[id_prefix] = []
        groups[id_prefix].append(item)

    # Clear the listbox
    item_listbox.delete(0, tk.END)

    # Create the item list with groupings and separators
    for group in groups.values():
        group_items = []
        for item in group:
            display_text = f"{item['title']} ({item['id']})"
            if search_text in item['title'].lower() or search_text in item['id']:
                group_items.append(display_text)
        if group_items:
            for display_text in group_items:
                item_listbox.insert(tk.END, display_text)
            item_listbox.insert(tk.END, '---')  # Add a separator after each group

    if item_listbox.size() > 0:
        last_item = item_listbox.get(tk.END)
        if last_item == '---':
            item_listbox.delete(tk.END)  # Remove last separator

    # Clear the give command
    give_command.set('')

def on_item_select(event):
    global item_listbox, give_command, autocopy_var, main_stat_var, main_stat_options, main_stat_menu, main_stat_label, selected_item_id

    selected_indices = item_listbox.curselection()
    if selected_indices:
        index = selected_indices[0]
        selected_item = item_listbox.get(index)
        if selected_item != '---':
            # Extract the id from the selected item
            if '(' in selected_item and ')' in selected_item:
                id_str = selected_item.split('(')[-1].split(')')[0]
                selected_item_id = id_str
                last_digit = int(id_str[-1])

                # Update main_stat_options based on last_digit
                if last_digit in [1, 2]:
                    # Main stat is fixed and not specified in command
                    main_stat_label.config(text="Main Stat: Fixed")
                    main_stat_var.set("Fixed")
                    main_stat_menu['menu'].delete(0, 'end')
                    main_stat_menu.config(state='disabled')
                else:
                    # Enable main_stat_menu and populate options
                    main_stat_menu.config(state='normal')
                    main_stat_label.config(text="Select Main Stat:")
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
                    main_stat_options = list(main_stats.keys())
                    if main_stat_options:
                        main_stat_var.set(main_stat_options[0])
                        main_stat_menu['menu'].delete(0, 'end')
                        for option in main_stat_options:
                            main_stat_menu['menu'].add_command(label=option, command=tk._setit(main_stat_var, option, update_command))
                    else:
                        # Handle case where there are no main stats
                        main_stat_var.set("No Main Stats Available")
                        main_stat_menu['menu'].delete(0, 'end')
                        main_stat_menu['menu'].add_command(label="No Main Stats Available", command=tk._setit(main_stat_var, "No Main Stats Available", update_command))
                        main_stat_menu.config(state='disabled')

                # Do not clear additional stats; preserve them across item selections
                # Update the command
                update_command()
            else:
                give_command.set('')
        else:
            give_command.set('')
    else:
        give_command.set('')



def update_command(*args):
    global give_command, selected_item_id, main_stat_var, additional_stats, maxsteps_var, level_var

    if not selected_item_id:
        give_command.set('')
        return

    command_parts = [f"/give {selected_item_id}"]

    # Determine if main stat should be included
    last_digit = int(selected_item_id[-1])
    if last_digit not in [1, 2]:
        # Include main stat
        main_stat_name = main_stat_var.get()
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
    for stat_name, quantity in additional_stats.items():
        stat_id = substats.get(stat_name)
        if stat_id:
            command_parts.append(f"{stat_id}:{quantity}")

    # Add selected level
    level = level_var.get()
    command_parts.append(f"lv{level}")

    # Add '-maxsteps' if selected
    if maxsteps_var.get():
        command_parts.append("-maxsteps")

    # Set the command
    give_command.set(' '.join(command_parts))

    # Autocopy functionality
    if autocopy_var.get():
        copy_to_clipboard()


def copy_to_clipboard():
    global root, give_command, autocopy_var

    command = give_command.get()
    if command:
        root.clipboard_clear()
        root.clipboard_append(command)
        root.update()  # Now it stays on the clipboard after the window is closed
        if not autocopy_var.get():
            messagebox.showinfo("Copied", "Command copied to clipboard.")
    else:
        if not autocopy_var.get():
            messagebox.showwarning("No Command", "No command to copy.")

def add_additional_stat():
    global additional_stats_var, additional_quantity_var, additional_stats_listbox, additional_stats

    stat_name = additional_stats_var.get()
    quantity = additional_quantity_var.get()

    if not stat_name or not quantity.isdigit() or int(quantity) <= 0:
        messagebox.showwarning("Invalid Input", "Please select a valid stat and enter a positive quantity.")
        return

    # Add to the dictionary
    additional_stats[stat_name] = quantity

    # Update the listbox
    additional_stats_listbox.delete(0, tk.END)
    for stat, qty in additional_stats.items():
        additional_stats_listbox.insert(tk.END, f"{stat} x{qty}")

    # Update the command
    update_command()

def remove_additional_stat():
    global additional_stats_listbox, additional_stats

    selected_indices = additional_stats_listbox.curselection()
    if selected_indices:
        index = selected_indices[0]
        stat_entry = additional_stats_listbox.get(index)
        stat_name = stat_entry.split(' x')[0]
        # Remove from the dictionary
        if stat_name in additional_stats:
            del additional_stats[stat_name]
        # Update the listbox
        additional_stats_listbox.delete(index)
        # Update the command
        update_command()
    else:
        messagebox.showwarning("No Selection", "Please select a stat to remove.")

def clear_additional_stats():
    global additional_stats_listbox, additional_stats
    additional_stats.clear()
    additional_stats_listbox.delete(0, tk.END)
    # Update the command
    update_command()

def main():
    global item_listbox, root, type_var, rarity_var, give_command, search_var, autocopy_var
    global main_stat_var, main_stat_menu, main_stat_options, additional_stats_var, additional_quantity_var
    global additional_stats_listbox, additional_stats, main_stat_label, selected_item_id, maxsteps_var, level_var
    global remove_button

    root = tk.Tk()
    root.title("LC Relic Generator")

    # Initialize variables
    type_var = tk.StringVar(value='default')
    rarity_var = tk.StringVar(value='5')
    give_command = tk.StringVar()
    search_var = tk.StringVar()
    autocopy_var = tk.BooleanVar()
    main_stat_var = tk.StringVar()
    main_stat_options = ["Select an item first"]  # Placeholder option
    main_stat_var.set(main_stat_options[0])      # Set default value
    additional_stats_var = tk.StringVar()
    additional_quantity_var = tk.StringVar(value='9')
    additional_stats = {}  # Dictionary to hold added additional stats
    selected_item_id = None
    maxsteps_var = tk.BooleanVar()
    level_var = tk.StringVar(value='15')

    # Create main frame to hold left and right frames
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create left and right frames
    left_frame = tk.Frame(main_frame)
    left_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    right_frame = tk.Frame(main_frame)
    right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Right Frame (Selection Interface)
    # (Same as before)
    # Type selection
    type_label = tk.Label(right_frame, text="Select Type:")
    type_label.pack()

    type_frame = tk.Frame(right_frame)
    type_frame.pack()

    default_radio = tk.Radiobutton(type_frame, text="Default", variable=type_var, value='default', command=update_item_list)
    default_radio.pack(side=tk.LEFT)
    planars_radio = tk.Radiobutton(type_frame, text="Planars", variable=type_var, value='planars', command=update_item_list)
    planars_radio.pack(side=tk.LEFT)

    # Rarity selection
    rarity_label = tk.Label(right_frame, text="Select Rarity:")
    rarity_label.pack()

    rarity_combobox = ttk.Combobox(right_frame, textvariable=rarity_var, values=[str(i) for i in range(2, 6)], state='readonly')
    rarity_combobox.pack()
    rarity_combobox.bind('<<ComboboxSelected>>', update_item_list)

    # Search functionality
    search_label = tk.Label(right_frame, text="Search:")
    search_label.pack()

    search_entry = tk.Entry(right_frame, textvariable=search_var)
    search_entry.pack()
    search_var.trace('w', lambda *args: update_item_list())

    # Item selection with scrollbar
    item_frame = tk.Frame(right_frame)
    item_frame.pack(fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(item_frame, orient=VERTICAL)
    item_listbox = tk.Listbox(item_frame, width=50, height=15, yscrollcommand=scrollbar.set)
    scrollbar.config(command=item_listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    item_listbox.pack(side=LEFT, fill=tk.BOTH, expand=True)
    item_listbox.bind('<<ListboxSelect>>', on_item_select)

    # Left Frame (Characteristic Generation Interface)
    # Main Stat Selection
    main_stat_label = tk.Label(left_frame, text="Main Stat:")
    main_stat_label.pack()

    main_stat_menu = tk.OptionMenu(left_frame, main_stat_var, *main_stat_options)
    main_stat_menu.config(state='disabled')  # Disabled until an item is selected
    main_stat_menu.pack()

    # Level selection
    level_label = tk.Label(left_frame, text="Select Level:")
    level_label.pack()

    level_spinbox = tk.Spinbox(left_frame, from_=1, to=15, textvariable=level_var, width=5, command=update_command)
    level_spinbox.pack()
    level_var.trace('w', lambda *args: update_command())

    # Additional Stats Selection
    additional_label = tk.Label(left_frame, text="Add Additional Stat:")
    additional_label.pack()

    additional_frame = tk.Frame(left_frame)
    additional_frame.pack()

    additional_stats_var.set(next(iter(substats)))  # Default value

    additional_stats_menu = tk.OptionMenu(additional_frame, additional_stats_var, *substats.keys())
    additional_stats_menu.pack(side=tk.LEFT)

    additional_quantity_entry = tk.Entry(additional_frame, textvariable=additional_quantity_var, width=5)
    additional_quantity_entry.pack(side=tk.LEFT)
    additional_quantity_var.set('1')  # Default quantity

    add_button = tk.Button(additional_frame, text="Add", command=add_additional_stat)
    add_button.pack(side=tk.LEFT)

    # Remove and Clear buttons
    buttons_frame = tk.Frame(left_frame)
    buttons_frame.pack(pady=5)

    remove_button = tk.Button(buttons_frame, text="Remove Selected", command=remove_additional_stat)
    remove_button.pack(side=tk.LEFT, padx=5)

    clear_button = tk.Button(buttons_frame, text="Clear All", command=clear_additional_stats)
    clear_button.pack(side=tk.LEFT, padx=5)

    # Listbox to show added additional stats
    additional_stats_listbox = tk.Listbox(left_frame, width=30, height=5)
    additional_stats_listbox.pack()
    # Remove or comment out the following line
    # additional_stats_listbox.bind('<<ListboxSelect>>', on_additional_stat_select)

    # Maxsteps checkbox
    maxsteps_check = tk.Checkbutton(left_frame, text="Include -maxsteps", variable=maxsteps_var, command=update_command)
    maxsteps_check.pack()

    # Give command display as an editable Entry at the bottom center
    command_frame = tk.Frame(root)
    command_frame.pack(side=tk.BOTTOM, pady=10)

    command_entry = tk.Entry(command_frame, textvariable=give_command, font=('Arial', 12), width=50)
    command_entry.pack()

    # Autocopy checkbox
    autocopy_check = tk.Checkbutton(command_frame, text="Autocopy", variable=autocopy_var)
    autocopy_check.pack()

    # Copy button
    copy_button = tk.Button(command_frame, text="Copy", command=copy_to_clipboard)
    copy_button.pack()

    # Initialize the item list
    update_item_list()

    root.mainloop()

if __name__ == '__main__':
    # Call the function to process the file and fill the pre-defined lists
    #filename = 'data.txt'  # Ensure this is the correct path to your data file
    filename = "Lunar Core Handbook.txt"
    process_file(filename)
    main()
