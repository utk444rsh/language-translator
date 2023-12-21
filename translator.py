from tkinter import *
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
import sqlite3

# Database connection and table creation
conn = sqlite3.connect('trans.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS history (
        froml TEXT NOT NULL,
        text_trans TEXT NOT NULL,
        tol TEXT NOT NULL,
        transl TEXT NOT NULL
    )
''')

conn.commit()

def translate_text():
    translator = Translator()
    input_text_value = input_text.get()
    dest_lang_value = dest_lang.get()

    # Check if input_text and dest_lang are not empty
    if input_text_value and dest_lang_value:
        translated = translator.translate(text=input_text_value, dest=dest_lang_value)
        output_text.delete(1.0, END)
        output_text.insert(END, translated.text)

        # Save translation history to the database
        cursor.execute('''
            INSERT INTO history (froml, text_trans, tol, transl)
            VALUES (?, ?, ?, ?)
        ''', ("English", input_text_value, dest_lang_value, translated.text))

        conn.commit()

    else:
        messagebox.showwarning("Warning", "Please enter text and choose a language")

def display_history():
    cursor.execute('SELECT * FROM history')
    entries = cursor.fetchall()

    if entries:
        history_text.delete(1.0, END)
        for entry in entries:
            history_text.insert(END, f"From: {entry[0]}\nText: {entry[1]}\nTo: {entry[2]}\nTranslation: {entry[3]}\n\n")
    else:
        history_text.delete(1.0, END)
        history_text.insert(END, "No history entries found.")

# Create main window
root = Tk()
root.geometry('1200x700')  # Increased width and height
root.resizable(0, 0)
root['bg'] = 'skyblue'
root.title('Language Translator')

# Labels and input widgets
Label(root, text='Language Translator', font="Arial 20 bold").pack()

Label(root, text="Enter Text", font='arial 13 bold', bg='white smoke').place(x=165, y=95)
input_text = Entry(root, width=60)
input_text.place(x=30, y=130)

Label(root, text="Output", font='arial 13 bold', bg='white smoke').place(x=700, y=90)
output_text = Text(root, font='arial 10', height=5, wrap=WORD, padx=5, pady=5, width=50)
output_text.place(x=600, y=130)

language = list(LANGUAGES.values())
dest_lang = ttk.Combobox(root, values=language, width=22)
dest_lang.place(x=130, y=180)
dest_lang.set('Choose Language')

# Buttons with commands
trans_btn = Button(root, text='Translate', font='arial 13 bold', pady=5, command=translate_text, bg='Orange',
                   activebackground='green')
trans_btn.place(x=445, y=225)

clear_button = Button(root, text="Clear", font=('Corbel', 15, 'bold'), command=lambda: [input_text.delete(0, END), output_text.delete(1.0, END)], bg="#ffffff")
clear_button.place(x=370, y=225)

copy_button = Button(root, text="Copy", font=('Corbel', 15, 'bold'), command=lambda: root.clipboard_append(output_text.get(1.0, END)), bg="#ffffff")
copy_button.place(x=300, y=225)

# New display button
display_button = Button(root, text="Display History", font=('Corbel', 15, 'bold'), command=display_history, bg="#ffffff")
display_button.place(x=200, y=400)

# Textbox to display history
history_text = Text(root, font='arial 10', height=20, wrap=WORD, padx=5, pady=5, width=100)
history_text.place(x=30, y=500)

root.mainloop()
