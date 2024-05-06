import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import threading
import time

class Teleprompter:
    def __init__(self, root):
        self.root = root
        self.root.title("Teleprompter")
        self.current_font_size = 18

        # Text display area
        self.text_display = ScrolledText(root, font=('Arial', self.current_font_size), wrap='word', height=10)
        self.text_display.pack(padx=10, pady=10, fill='both', expand=True)

        # Controls frame
        controls_frame = tk.Frame(root)
        controls_frame.pack(fill='x', padx=10, pady=10)

        # Load button
        load_button = tk.Button(controls_frame, text="Load Text", command=self.load_text)
        load_button.pack(side='left')

        # Speed slider
        self.speed_slider = tk.Scale(controls_frame, from_=1, to=100, orient='horizontal', label='Speed')
        self.speed_slider.set(20)  # Default to a moderate speed
        self.speed_slider.pack(side='left', fill='x', expand=True)

        # Start button
        start_button = tk.Button(controls_frame, text="Start", command=self.start_scrolling)
        start_button.pack(side='left')

        # Font size controls
        font_smaller_button = tk.Button(controls_frame, text="A-", command=lambda: self.adjust_font_size(-2))
        font_smaller_button.pack(side='right')

        font_larger_button = tk.Button(controls_frame, text="A+", command=lambda: self.adjust_font_size(2))
        font_larger_button.pack(side='right')

    def load_text(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, 'r') as file:
                self.text = file.readlines()  # Store as list of lines
            self.text_display.delete('1.0', 'end')
            self.text_display.insert('1.0', ''.join(self.text))  # Insert text as a single joined string
            self.text_display.yview_moveto(1)  # Scroll to the bottom to prepare for teleprompter-like scrolling

    def start_scrolling(self):
        threading.Thread(target=self.scroll_text, daemon=True).start()

    def scroll_text(self):
        """ Scroll text at a speed based on the slider's value. """
        self.text_display.yview_moveto(0)  # Start scrolling from the top
        total_lines = int(self.text_display.index('end-1c').split('.')[0])
        line = 1
        speed = self.speed_slider.get()
        while line < total_lines:
            self.text_display.yview_scroll(1, 'units')
            line += 1
            self.root.update()
            time.sleep(100.0 / speed)

    def adjust_font_size(self, delta):
        self.current_font_size += delta
        self.current_font_size = max(8, self.current_font_size)  # Set minimum font size to 8
        self.text_display.config(font=('Arial', self.current_font_size))
        self.text_display.pack_configure(padx=10, pady=10, fill='both', expand=True)  # Ensure the text area resizes

if __name__ == "__main__":
    root = tk.Tk()
    app = Teleprompter(root)
    root.mainloop()
