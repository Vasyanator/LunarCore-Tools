# main.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import os

from process_handbook import process_handbook

# Import tab classes
import tab_planars_gen
import tab_items 
import tab_spawn 
import tab_mazes
import tab_avatars
import tab_commands
import tab_opencommand

program_name = "LunarCore Tools"
program_version = "1.1"

def main():
    # Check if file exists
    filename = "Lunar Core Handbook.txt"
    while True:
        if not os.path.exists(filename):
            # Prompt user to select a file
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            messagebox.showwarning("File Not Found", f"File '{filename}' not found. Please select a file.")
            filename = filedialog.askopenfilename(title="Select Data File",
                                                  filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
            if not filename:
                messagebox.showerror("No File Selected", "No file selected. Exiting.")
                return
            root.destroy()
        # Read the first line of the file
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
            # Additional check to ensure file is not empty
            if not first_line:
                raise Exception("Empty File")
        except Exception as e:
            # Could not read the file, prompt again
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("File Error", f"Could not read file '{filename}'. Please select another file.")
            filename = filedialog.askopenfilename(title="Select Data File",
                                                  filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
            if not filename:
                messagebox.showerror("No File Selected", "No file selected. Exiting.")
                return
            root.destroy()
            continue

        # Check if first line starts with "# Lunar Core" and ends with "Handbook"
        if first_line.startswith("# Lunar Core") and "Handbook" in first_line:
            # Extract version
            handbook_version = first_line[len("# Lunar Core"):].strip()
            if handbook_version.endswith("Handbook"):
                handbook_version = handbook_version[:-len("Handbook")].strip()
            break
        else:
            # First line does not match, prompt user to select another file
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Invalid File", f"The selected file '{filename}' is not a valid Lunar Core Handbook. Please select another file.")
            filename = filedialog.askopenfilename(title="Select Data File",
                                                  filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
            if not filename:
                messagebox.showerror("No File Selected", "No file selected. Exiting.")
                return
            root.destroy()

    # Process the file
    # items = process_handbook(filename)
    # data = process_handbook.data
    handbook_data = process_handbook(filename)
    avatars_list = handbook_data.avatars_list
    relics_list = handbook_data.relics_list
    props_list = handbook_data.props_list
    npc_monsters_list = handbook_data.npc_monsters_list
    battle_stages = handbook_data.battle_stages
    battle_monsters_list = handbook_data.battle_monsters_list
    mazes_list = handbook_data.mazes_list
    lightcones_list = handbook_data.lightcones_list
    materials_list = handbook_data.materials_list
    base_materials_list = handbook_data.base_materials_list
    unknown_items_list = handbook_data.unknown_items_list
    other_items_list = handbook_data.other_items_list

    # Create main application window
    root = tk.Tk()
    root.title(f"{program_name} {program_version} - With {handbook_version} Handbook")
    root.state('zoomed')

    # Initialize shared variables
    give_command = tk.StringVar()
    autocopy_var = tk.BooleanVar()

    # Create the notebook
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Create a CommandManager or similar to handle command updates
    command_manager = CommandManager(root, give_command, autocopy_var)

    # Create and add tabs
    tabs = []
    # Relic Generation Tab
    planars_tab = tab_planars_gen.PlanarsTab(notebook, relics_list, command_manager)
    notebook.add(planars_tab.frame, text="Relic Generation")
    tabs.append(planars_tab)

    # Items Tab
    items_tab = tab_items.ItemsTab(
    notebook,
    base_materials=base_materials_list,
    lightcones=lightcones_list,
    materials=materials_list,
    other_items=other_items_list,
    unknown_items=unknown_items_list,
    command_manager=command_manager
    )
    notebook.add(items_tab.frame, text="Items")
    tabs.append(items_tab)

    # Spawn Tab
    spawn_tab = tab_spawn.SpawnTab(
    notebook,
    props_list=props_list,
    npc_monsters_list=npc_monsters_list,
    battle_stages=battle_stages,
    battle_monsters_list=battle_monsters_list,
    command_manager=command_manager
    )
    notebook.add(spawn_tab.frame, text="Spawn")
    tabs.append(spawn_tab)

    # Mazes Tab
    mazes_tab = tab_mazes.MazesTab(notebook, mazes_list, command_manager)
    notebook.add(mazes_tab.frame, text="Mazes")
    tabs.append(mazes_tab)

    # Avatars Tab
    avatars_tab = tab_avatars.AvatarsTab(notebook, avatars_list, command_manager)
    notebook.add(avatars_tab.frame, text="Avatars")
    tabs.append(avatars_tab)

    # Commands Tab
    commands_tab = tab_commands.CommandsTab(notebook, command_manager=command_manager)
    notebook.add(commands_tab.frame, text="Commands")
    tabs.append(commands_tab)

    # OpenCommand Tab
    opencommand_tab = tab_opencommand.OpenCommandTab(notebook)
    notebook.add(opencommand_tab.frame, text="OpenCommand Plugin")
    tabs.append(opencommand_tab)

    # Command Entry and copy button
    command_frame = tk.Frame(root)
    command_frame.pack(side=tk.BOTTOM, pady=10)

    command_entry = tk.Entry(command_frame, textvariable=give_command, font=('Arial', 12), width=50)
    command_entry.pack()

    # Autocopy checkbox
    autocopy_check = tk.Checkbutton(command_frame, text="Autocopy", variable=autocopy_var)
    autocopy_check.pack()

    # Copy button
    copy_button = tk.Button(command_frame, text="Copy", command=command_manager.copy_to_clipboard)
    copy_button.pack()

    root.mainloop()

class CommandManager:
    def __init__(self, root, give_command_var, autocopy_var):
        self.root = root
        self.give_command = give_command_var
        self.autocopy_var = autocopy_var

    def update_command(self, command):
        self.give_command.set(command)
        if self.autocopy_var.get():
            self.copy_to_clipboard()

    def copy_to_clipboard(self):
        command = self.give_command.get()
        if command:
            self.root.clipboard_clear()
            self.root.clipboard_append(command)
            self.root.update()  # Now it stays on the clipboard after the window is closed
            if not self.autocopy_var.get():
                messagebox.showinfo("Copied", "Command copied to clipboard.")
        else:
            if not self.autocopy_var.get():
                messagebox.showwarning("No Command", "No command to copy.")

if __name__ == '__main__':
    main()
