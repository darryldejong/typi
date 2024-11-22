import tkinter as tk
from tkinter import simpledialog, messagebox
import pyautogui
import threading
import time
import keyboard
import os

class AutoTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap(os.path.join('images', 'favicon.ico'))
        self.root.title("Auto Typer by psz")
        self.root.geometry("600x400")
        self.root.resizable(True, True)

        self.is_typing_event = threading.Event()
        self.sentences = []
        self.message_rate = 0.03

        self.sentences_listbox = tk.Listbox(
            root, bg="#f5edf3", fg="black", font=("Arial", 12), selectmode=tk.SINGLE
        )
        self.sentences_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))

        self.input_field = tk.Entry(
            root, font=("Arial", 12), fg="black", bg="#f5edf3", relief="solid", bd=2
        )
        self.input_field.insert(0, "Type your message here")
        self.input_field.bind("<FocusIn>", self.on_focus_in)
        self.input_field.bind("<FocusOut>", self.on_focus_out)
        self.input_field.bind("<Return>", self.add_sentence_popup)
        self.input_field.pack(padx=10, pady=(10, 5), fill=tk.X)

        self.top_frame = tk.Frame(root, bg="#f5edf3")
        self.top_frame.pack(fill=tk.X, pady=10)

        self.button_frame = tk.Frame(self.top_frame, bg="#f5edf3")
        self.button_frame.pack(side="top", fill=tk.X, padx=10, pady=5)

        self.start_stop_button = tk.Button(self.button_frame, text="Start Typing", width=15, font=("Arial", 12), command=self.toggle_typing)
        self.start_stop_button.pack(side="left", padx=10)

        self.stop_hotkey_label = tk.Label(self.button_frame, text="F12 Stop", bg="#f5edf3", font=("Arial", 10))
        self.stop_hotkey_label.pack(side="left", padx=10)

        self.table_frame = tk.Frame(self.button_frame, bg="#f5edf3")
        self.table_frame.pack(side="right", padx=20, pady=10)

        tk.Label(self.table_frame, text="Time Delay:", bg="#f5edf3", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.delay_entry = tk.Spinbox(self.table_frame, from_=1, to=10, width=5, font=("Arial", 10), justify="center", increment=1, state="readonly")
        self.delay_entry.grid(row=0, column=1, padx=5, pady=5)
        self.delay_entry.insert(0, "1")
        tk.Label(self.table_frame, text="Sec", bg="#f5edf3", font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.edit_sentence_popup)
        self.context_menu.add_command(label="Delete", command=self.delete_sentence)
        
        self.sentences_listbox.bind("<Button-3>", self.show_context_menu)

        self.hotkey_thread = threading.Thread(target=self.check_hotkey_once)
        self.hotkey_thread.daemon = True
        self.hotkey_thread.start()

    def show_context_menu(self, event):
        try:
            index = self.sentences_listbox.nearest(event.y)
            self.sentences_listbox.select_set(index)
            self.context_menu.post(event.x_root, event.y_root)
        except IndexError:
            pass

    def add_sentence_popup(self, event=None):
        sentence = self.input_field.get()
        if sentence and sentence != "Type your message here":
            self.sentences.append(sentence)
            self.sentences_listbox.insert(tk.END, sentence)
            self.input_field.delete(0, tk.END)

    def edit_sentence_popup(self):
        try:
            index = self.sentences_listbox.curselection()[0]
            old_sentence = self.sentences[index]
            new_sentence = simpledialog.askstring("Edit Sentence", f"Edit sentence:", initialvalue=old_sentence)
            if new_sentence:
                self.sentences[index] = new_sentence
                self.sentences_listbox.delete(index)
                self.sentences_listbox.insert(index, new_sentence)
        except IndexError:
            messagebox.showwarning("No Selection", "Select a sentence to edit first.")

    def delete_sentence(self):
        try:
            index = self.sentences_listbox.curselection()[0]
            self.sentences_listbox.delete(index)
            del self.sentences[index]
        except IndexError:
            messagebox.showwarning("No Selection", "Select a sentence to delete first.")

    def toggle_typing(self, event=None):
        if not self.is_typing_event.is_set():
            self.start_typing()
        else:
            self.stop_typing()

    def start_typing(self):
        if not self.is_typing_event.is_set():
            self.is_typing_event.set()
            typing_thread = threading.Thread(target=self.type_text)
            typing_thread.daemon = True
            typing_thread.start()
            self.start_stop_button.config(text="Stop Typing")
            self.input_field.config(state="disabled")
            self.sentences_listbox.config(state="disabled")
            self.start_stop_button.config(state="normal")

    def stop_typing(self):
        self.is_typing_event.clear()
        self.start_stop_button.config(text="Start Typing")
        self.input_field.config(state="normal")
        self.sentences_listbox.config(state="normal")
        self.start_stop_button.config(state="normal")

    def type_text(self):
        time.sleep(3)
        sentences_to_type = self.sentences.copy()
        while self.is_typing_event.is_set():
            for sentence in sentences_to_type:
                if not self.is_typing_event.is_set():
                    return
                pyautogui.write(sentence + "\n", interval=0.01)
                time_delay = int(self.delay_entry.get())  
                time.sleep(time_delay)  

    def on_focus_in(self, event):
        if self.input_field.get() == "Type your message here":
            self.input_field.delete(0, tk.END)

    def on_focus_out(self, event):
        if not self.input_field.get():
            self.input_field.insert(0, "Type your message here")

    def check_hotkey_once(self):
        while True:
            event = keyboard.read_event(suppress=False)
            if event.name == 'f12' and event.event_type == keyboard.KEY_DOWN:
                self.toggle_typing()
                time.sleep(0.5)

root = tk.Tk()
app = AutoTyperApp(root)
root.mainloop()
