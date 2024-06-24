import tkinter as tk
from tkinter import ttk, messagebox

class ExpressionValidator:
    def __init__(self):
        self.stack = []
        self.state = 'q0'
        self.accepted = False
        self.has_error = False
        self.paren_count = 0  
        self.last_char = ''  

    def transition(self, char):
        if self.state == 'q0':
            if char.isdigit():
                self.state = 'q1'
            elif char == '(':
                self.stack.append('(')
                self.paren_count += 1
                self.state = 'q0'
            else:
                self.state = 'qe'  
        elif self.state == 'q1':
            if char.isdigit():
                self.state = 'q1'
            elif char in '+-*/':
                self.state = 'q2'
            elif char == ')':
                if self.stack and self.stack[-1] == '(':
                    self.stack.pop()
                    self.paren_count -= 1
                    self.state = 'q1'
                else:
                    self.state = 'qe'
            elif char == '(':
                self.stack.append('(')
                self.paren_count += 1
                self.state = 'q0'
            else:
                self.state = 'qe'
        elif self.state == 'q2':
            if char.isdigit():
                if char == '0' and self.last_char == '/':
                    self.has_error = True
                self.state = 'q1'
            elif char == '(':
                self.stack.append('(')
                self.paren_count += 1
                self.state = 'q0'
            else:
                self.state = 'qe'
        else:
            self.state = 'qe'  

        self.last_char = char

    def process(self, input_string):
        self.last_char = ''  
        for char in input_string:
            self.transition(char)
            if self.state == 'qe':
                break

        if self.state == 'q1' and not self.stack and not self.has_error and self.paren_count == 0:
            self.accepted = True

        return self.accepted

def check_syntax(input_string):
    pda = ExpressionValidator()
    input_without_spaces = input_string.replace(' ', '')
    return pda.process(input_without_spaces)

def check_expression():
    user_input = entry.get()
    result = check_syntax(user_input)
    add_to_history(user_input, result)
    if result:
        messagebox.showinfo("Sonuç", f"'{user_input}' ifadesi geçerlidir.")
    else:
        messagebox.showinfo("Sonuç", f"'{user_input}' ifadesi geçersizdir.")

def clear_entry():
    entry.delete(0, tk.END)

def insert_sample_expression():
    entry.insert(0, "12 + ((3 - 2) * 4) / 2")

def add_to_history(expression, result):
    history_list.insert(tk.END, f"{expression} - {'Geçerli' if result else 'Geçersiz'}")

def show_help():
    help_text = (
        "Bu uygulama, girilen matematiksel ifadelerin geçerli olup olmadığını kontrol eder.\n"
        "Geçerli ifadeler:\n"
        "- Sayılar: 0-9\n"
        "- Operatörler: +, -, *, /\n"
        "- Parantezler: ()\n"
        "Örnek ifadeler: \n"
        "12 + ((3 - 2) * 4) / 2\n"
        "5 * (6 + 3)"
    )
    messagebox.showinfo("Yardım", help_text)

def append_to_entry(text):
    current_text = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current_text + text)

app = tk.Tk()
app.title("Matematiksel İfade Denetleyici ve Hesap Makinesi")
app.geometry("600x750")
app.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')  # Use a modern theme
style.configure('TFrame', background='#f0f0f0')
style.configure('TButton', font=('Helvetica', 12), padding=10, background="#007acc", foreground="#ffffff")
style.map('TButton', background=[('active', '#005f99')], foreground=[('active', '#ffffff')])
style.configure('TLabel', font=('Helvetica', 14), background='#f0f0f0')
style.configure('TListbox', font=('Helvetica', 12), background='#ffffff', foreground='#000000')

background_frame = ttk.Frame(app, style='TFrame')
background_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(background_frame, width=600, height=750)
canvas.pack(fill=tk.BOTH, expand=True)

gradient = canvas.create_rectangle(0, 0, 600, 750, fill='#ffffff', outline='')
canvas.create_rectangle(0, 0, 600, 750, fill='', outline='')

main_frame = ttk.Frame(canvas, style='TFrame')
canvas.create_window(300, 375, window=main_frame)

label = ttk.Label(main_frame, text="Matematiksel bir ifade girin:", style='TLabel')
label.pack(pady=10)

entry = ttk.Entry(main_frame, width=50, font=("Helvetica", 14), foreground="#333333", background="#e6e6e6")
entry.pack(pady=10)

button_frame = ttk.Frame(main_frame, style='TFrame')
button_frame.pack(pady=10)

check_button = ttk.Button(button_frame, text="Kontrol Et", command=check_expression, style='TButton')
check_button.grid(row=0, column=0, padx=5, pady=5)

clear_button = ttk.Button(button_frame, text="Temizle", command=clear_entry, style='TButton')
clear_button.grid(row=0, column=1, padx=5, pady=5)

sample_button = ttk.Button(button_frame, text="Örnek Doldur", command=insert_sample_expression, style='TButton')
sample_button.grid(row=0, column=2, padx=5, pady=5)

history_label = ttk.Label(main_frame, text="Geçmiş:", style='TLabel')
history_label.pack(pady=10)

history_list = tk.Listbox(main_frame, height=10, width=50, font=("Helvetica", 12), background='#ffffff', foreground='#000000')
history_list.pack(pady=10)

calc_frame = ttk.Frame(main_frame, style='TFrame')
calc_frame.pack(pady=10)

buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('(', 4, 2), (')', 4, 3),
    ('+', 5, 0), ('=', 5, 1), ('C', 5, 2), ('Exit', 5, 3),
]

for (text, row, col) in buttons:
    if text == 'Exit':
        btn = ttk.Button(calc_frame, text=text, command=app.quit, style='TButton')
    elif text == 'C':
        btn = ttk.Button(calc_frame, text=text, command=clear_entry, style='TButton')
    elif text == '=':
        btn = ttk.Button(calc_frame, text=text, command=check_expression, style='TButton')
    else:
        btn = ttk.Button(calc_frame, text=text, command=lambda t=text: append_to_entry(t), style='TButton')
    btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

for i in range(6):
    calc_frame.rowconfigure(i, weight=1)
    calc_frame.columnconfigure(i, weight=1)

help_button = ttk.Button(main_frame, text="Yardım", command=show_help, style='TButton')
help_button.pack(pady=10)

app.mainloop()
