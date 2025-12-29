from pathlib import Path
from split_text_builder import SplitTextBuilder
import sys
import tkinter as tk


class MyWindow:
    OUTPUT_FILE_NAME = 'output.txt'

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Splits Generator v1.1')
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(fill='both', expand=True)

        self.add_input_text_box()
        self.add_checkboxes()
        self.add_generate_buttons()

        self.root.mainloop()

    def add_input_text_box(self):
        self.label1 = tk.Label(self.frame, text='must use the copy/paste hotkeys')
        self.label1.pack()

        self.input_text_box = tk.Text(self.frame, height=6, width=30, wrap='word')
        self.input_text_box.pack(pady=4)

        self.clear_button = tk.Button(self.frame, text='clear', width=10, command=self.clear_textbox)
        self.clear_button.pack()

    def add_checkboxes(self):
        tk.Frame(self.frame, height=30).pack()

        self.use_star_count = tk.BooleanVar()
        self.use_subsplits = tk.BooleanVar()
        self.swap_star_and_level_symbol = tk.BooleanVar()
        self.star_count_in_front = tk.BooleanVar()

        self.use_star_count.set(True)
        self.use_subsplits.set(False)
        self.swap_star_and_level_symbol.set(False)
        self.star_count_in_front.set(False)

        self.use_star_count_checkbox = tk.Checkbutton(self.frame, text='use star count', variable=self.use_star_count)
        self.use_subsplits_checkbox = tk.Checkbutton(self.frame, text='use subsplits', variable=self.use_subsplits)
        self.swap_star_and_level_symbol_checkbox = tk.Checkbutton(self.frame, text='swap star and level symbol', variable=self.swap_star_and_level_symbol)
        self.star_count_in_front_checkbox = tk.Checkbutton(self.frame, text='star count in front', variable=self.star_count_in_front)

        self.use_star_count_checkbox.pack()
        self.use_subsplits_checkbox.pack()
        self.swap_star_and_level_symbol_checkbox.pack()
        self.star_count_in_front_checkbox.pack()

    def add_generate_buttons(self):
        tk.Frame(self.frame, height=30).pack()

        self.output_to_file_button = tk.Button(self.frame, text='output to output.txt', command=self.output_to_file)
        self.copy_to_clipboard_button = tk.Button(self.frame, text='copy to clipboard', command=self.copy_to_clipboard)
        self.output_to_file_button.pack()
        self.copy_to_clipboard_button.pack()

    def clear_textbox(self):
        self.input_text_box.delete("1.0", "end")

    def output_to_file(self):
        text = self.get_text()

        if getattr(sys, 'frozen', False):
            script_folder = Path(sys.executable).parent
        else:
            script_folder = Path(__file__).parent

        output_path = script_folder / MyWindow.OUTPUT_FILE_NAME
        output_path.write_text(text)

    def copy_to_clipboard(self):
        text = self.get_text()
        
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()

    def get_text(self):
        lines = self.input_text_box.get("1.0", tk.END).splitlines()

        return SplitTextBuilder(
            lines                         = lines,
            use_star_count                = self.use_star_count.get(),
            use_subsplits                 = self.use_subsplits.get(),
            swap_star_and_level_symbol    = self.swap_star_and_level_symbol.get(),
            star_count_in_front           = self.star_count_in_front.get()
        ).get_text()
