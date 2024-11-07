import os
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
import random


class Home:

    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry('800x800')
        self.root.title('Home')

        self.menu = tk.Menu(self.root)
        help_menu = tk.Menu(self.menu, tearoff=0)
        help_menu.add_command(label="About...", command=self.get_about)
        self.menu.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=self.menu)

        f = open("welcome.txt", "r")
        self.label = tk.Label(
            self.root,
            text=f.read(),
            font=('Arial', 15))
        self.label.pack(padx=10, pady=10)
        f.close()

        self.button = tk.Button(
            self.root, text="New Character", font=('Arial', 15), command=self.create_character
        )
        self.button.pack(padx=10, pady=10)

        self.button = tk.Button(
            self.root, text="View Characters", font=('Arial', 15), command=self.get_characters
        )
        self.button.pack(padx=10, pady=10)

        self.button = tk.Button(
            self.root, text="Manage Characters", font=('Arial', 15), command=self.manage_characters
        )
        self.button.pack(padx=10, pady=10)

        self.options_chosen = {
            "class": '',
            "race" : ''
        }


        self.root.mainloop()

    def create_character(self):

        self.clear_frame()

        # Character popup window:
        self.root.title("New Character")
        self.root.geometry("800x800")

        # Class options
        class_label = tk.Label(self.root, text="Choose a class")
        class_label.pack(padx=10, pady=10)

        class_drop = Combobox(
            state="readonly",
            values=["Fighter", "Wizard"],
        )
        class_drop.pack(padx=10, pady=10)

        # Race options - set initial chosen
        race_label = tk.Label(self.root, text="Choose a race")
        race_label.pack(padx=10, pady=10)

        race_drop = Combobox(
            state="readonly",
            values=["Human", "Elf"],
        )
        race_drop.pack(padx=10, pady=10)

        # Create a back button:
        back_btn = tk.Button(
            self.root, text="Back", font=('Arial', 15),
            command=lambda: self.go_home()
        )

        back_btn.pack(padx=10, pady=10)

        # Create a next button:
        nxt_btn = tk.Button(
            self.root, text="Next", font=('Arial', 15),
            command=lambda: self.char_p2(class_drop.get(), race_drop.get())
        )
        nxt_btn.pack(padx=10, pady=10)

    def go_home(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to go back? Info will not be saved"):
            self.reset_window()


    def char_p2(self, class_choice, race_choice):

        # Store the chosen options
        self.options_chosen["class"] = class_choice
        self.options_chosen["race"] = race_choice

        # Only continue if required options are selected
        for option in self.options_chosen:
            if self.options_chosen[option] == '':
                messagebox.showinfo(option, f'Please choose {option}')
                return

        # Then set the page to next page
        self.clear_frame()

        # Character information from prev page
        char_label = tk.Label(
            self.root, text=f'{self.options_chosen["race"]} {self.options_chosen["class"]}'
        )
        char_label.pack(padx=10, pady=10)

        # Name
        name_label = tk.Label(self.root, text="Enter a name for your character")
        name_label.pack(padx=10, pady=10)
        name_entry = tk.Entry(self.root)
        name_entry.pack(padx=10, pady=10)

        # Stat options
        stat_label = tk.Label(
            self.root,
            text="Enter your character stats manually or click the roll button to roll for you"
        )
        stat_label.pack(padx=10, pady=10)
        stats = {
            "str": None,
            "dex": None,
            "con": None,
            "int": None,
            "wis": None,
            "cha": None
        }
        for stat in stats:
            stat_label = tk.Label(self.root, text=stat)
            stat_label.pack(padx=1, pady=1)
            stats[stat] = tk.Entry(self.root, width=5)
            stats[stat].pack(padx=1, pady=1)
            if race_choice == "Human":
                mod_label = tk.Label(self.root, text="(+1)")
                mod_label.pack(padx=1, pady=1)
            if race_choice == "Elf" and stat == "dex":
                mod_label = tk.Label(self.root, text="(+2)")
                mod_label.pack(padx=1, pady=1)

        # Create a roll button:
        roll_btn = tk.Button(
            self.root,
            text="Roll",
            font=('Arial', 15),
            command=lambda: self.roll(stats)
        )
        roll_btn.pack(padx=10, pady=10)

        # Create a back button:
        back_btn = tk.Button(
            self.root, text="Back", font=('Arial', 15), command=self.create_character
        )
        back_btn.pack(padx=10, pady=10)

        # Create a submit button
        submit_btn = tk.Button(
            self.root, text="Done", font=('Arial', 15),
            command=lambda: self.finish_character(
                name_entry.get(),
                self.options_chosen["race"],
                self.options_chosen["class"],
                stats
            )
        )
        submit_btn.pack(padx=10, pady=10)

    def roll(self, stats):
        for stat in stats:
            stats[stat].delete(0, tk.END)
            stats[stat].insert(0, str(
                random.randint(1, 6)+random.randint(1, 6)+random.randint(1, 6)
            ))

    def finish_character(self, name, race, char_class, stats):
        f = open(f'characters/{name}.txt', 'w')
        f.write(f'Character Sheet\n'
                f'Name: {name}\n'
                f'Race: {race}\n'
                f'Class: {char_class}\n'
                )

        if race == "Human":
            for stat in stats:
                f.write(f'{stat}: {int(stats[stat].get())+1}\n')

        if race == "Elf":
            for stat in stats:
                if stat == "dex":
                    f.write(f'{stat}: {int(stats[stat].get()) + 2}\n')
                else:
                    f.write(f'{stat}: {stats[stat].get()}\n')

        f.close()

        self.reset_window()

    def get_characters(self):
        for filename in os.listdir('characters'):
            f = open('characters/' + filename, 'r')
            char_window = tk.Toplevel(self.root)
            char_window.geometry('800x800')
            char_window.title(filename[0:(len(filename)-4)])
            char_label = tk.Label(char_window, text=f.read())
            char_label.pack(padx=10, pady=10)
            f.close()

    def clear_frame(self):
        for child in self.root.winfo_children():
            if child != self.menu:
                child.destroy()

    def reset_window(self):
        self.root.destroy()
        self.root = Home()

    def manage_characters(self):
        char_window = tk.Toplevel(self.root)
        label = tk.Label(char_window, text="Delete characters below:")
        label.pack(padx=10, pady=10)

        for filename in os.listdir('characters'):
            btn = tk.Button(
                char_window,
                text=f"delete {filename[0:(len(filename) - 4)]}",
                font=('Arial', 15),
                command=lambda: self.delete_character(filename, btn)
            )
            btn.pack(padx=10, pady=10)

    def delete_character(self, filename, btn):
        os.remove(f'characters/{filename}')
        btn.destroy()

    def get_about(self):
        about_window = tk.Toplevel(self.root)
        f = open("about.txt", 'r')
        info_label = tk.Label(about_window, text=f.read())
        info_label.pack(padx=10, pady=10)
        f.close()


Home()