import tkinter as tk
from tkinter import messagebox, font
from password_generator import PasswordGenerator
from collections import deque

WINDOW_TITLE = "Secure Password Generator"
WINDOW_BG = "#2D2D2D"
PRIMARY_TEXT = "white"
ACCENT_GREEN = "#00FF00"
ACCENT_BLUE = "#1E90FF"
ACCENT_RED = "#8B0000"
BUTTON_GREEN = "#006600"
BUTTON_GREEN_ACTIVE = "#009900"
BUTTON_BLUE_ACTIVE = "#4169E1"
BUTTON_RED_ACTIVE = "#FF0000"
DARK_INPUT_BG = "#1C1C1C"
STATUS_CLEAR_TIME = 2000

generator = PasswordGenerator()
password_history = deque(maxlen=10)

def get_char_type_counts(password: str) -> dict:
    import string
    return {
        'lowercase': sum(1 for c in password if c in string.ascii_lowercase),
        'uppercase': sum(1 for c in password if c in string.ascii_uppercase),
        'digits': sum(1 for c in password if c in string.digits),
        'special': sum(1 for c in password if c in generator.special),
    }

def on_generate():
    try:
        length = int(length_spinbox.get())
        if length < 4:
            messagebox.showerror("Error", "Minimum password length is 4 characters")
            return
        if length > 1024:
            messagebox.showerror("Error", "Maximum password length is 1024 characters")
            return

        use_lower = lower_var.get()
        use_upper = upper_var.get()
        use_digits = digit_var.get()
        use_special = special_var.get()

        if not any([use_lower, use_upper, use_digits, use_special]):
            messagebox.showerror("Error", "Select at least one character type")
            return

        password = generator.generate(
            length,
            use_lowercase=use_lower,
            use_uppercase=use_upper,
            use_digits=use_digits,
            use_special=use_special,
            exclude_ambiguous=ambiguous_var.get()
        )

        result_var.set(password)
        password_history.append(password)
        update_strength_indicator(password)
        update_history_display()
        clear_status()

    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def on_key_generate(event):
    if event.keysym == 'Return':
        on_generate()

def copy_to_clipboard():
    password = result_var.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        status_label.config(text="✓ Copied to clipboard", fg="#00FF00")
        root.after(STATUS_CLEAR_TIME, clear_status)
    else:
        status_label.config(text="No password to copy", fg=ACCENT_RED)
        root.after(STATUS_CLEAR_TIME, clear_status)

def clear_result():
    result_var.set("")
    update_strength_indicator("")
    clear_status()

def clear_status():
    status_label.config(text="")

def update_strength_indicator(password: str):
    if not password:
        strength_canvas.delete("all")
        strength_label.config(text="")
        return

    score, strength_text = generator.calculate_strength(password)
    colors = {1: "#FF4444", 2: "#FFAA00", 3: "#AAFF00", 4: "#00FF00"}
    color = colors.get(score, "#FF4444")

    strength_canvas.delete("all")
    bar_width = (score / 4) * 200
    strength_canvas.create_rectangle(0, 0, bar_width, 15, fill=color, outline=color)
    strength_canvas.create_rectangle(0, 0, 200, 15, outline=PRIMARY_TEXT, width=2)

    strength_label.config(text=f"Strength: {strength_text}", fg=color)

def update_history_display():
    history_text.config(state=tk.NORMAL)
    history_text.delete(1.0, tk.END)
    for i, pwd in enumerate(reversed(list(password_history)), 1):
        history_text.insert(tk.END, f"{i}. {pwd}\n")
    history_text.config(state=tk.DISABLED)

def select_history_password(event):
    try:
        index = int(history_text.index(tk.CURRENT).split('.')[0]) - 1
        passwords_list = list(reversed(list(password_history)))
        if 0 <= index < len(passwords_list):
            result_var.set(passwords_list[index])
            update_strength_indicator(passwords_list[index])
            status_label.config(text="✓ Password selected from history", fg="#00FF00")
            root.after(STATUS_CLEAR_TIME, clear_status)
    except:
        pass

root = tk.Tk()
root.title(WINDOW_TITLE)
root.configure(bg=WINDOW_BG)
root.resizable(False, False)
root.geometry("500x800")

main_frame = tk.Frame(root, bg=WINDOW_BG, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

title_label = tk.Label(
    main_frame,
    text="Secure Password Generator",
    font=("Arial", 18, "bold"),
    bg=WINDOW_BG,
    fg=ACCENT_GREEN
)
title_label.pack(pady=10)

length_frame = tk.Frame(main_frame, bg=WINDOW_BG)
length_frame.pack(fill=tk.X, pady=10)

tk.Label(length_frame, text="Length:", bg=WINDOW_BG, fg=PRIMARY_TEXT, font=("Arial", 11)).pack(side=tk.LEFT)

length_spinbox = tk.Spinbox(
    length_frame,
    from_=4,
    to=1024,
    width=6,
    font=("Arial", 11),
    justify="center"
)
length_spinbox.set(16)
length_spinbox.pack(side=tk.LEFT, padx=10)

tk.Label(length_frame, text="(Recommended: 16+)", bg=WINDOW_BG, fg="#888888", font=("Arial", 9)).pack(side=tk.LEFT)

options_frame = tk.LabelFrame(
    main_frame,
    text="Character Types",
    bg=WINDOW_BG,
    fg=PRIMARY_TEXT,
    font=("Arial", 10),
    padx=10,
    pady=8
)
options_frame.pack(fill=tk.X, pady=10)

lower_var = tk.BooleanVar(value=True)
upper_var = tk.BooleanVar(value=True)
digit_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)
ambiguous_var = tk.BooleanVar(value=False)

tk.Checkbutton(
    options_frame,
    text="Lowercase (a-z)",
    variable=lower_var,
    bg=WINDOW_BG,
    fg=PRIMARY_TEXT,
    selectcolor=WINDOW_BG,
    activebackground=WINDOW_BG,
    activeforeground=ACCENT_GREEN
).pack(anchor=tk.W)

tk.Checkbutton(
    options_frame,
    text="Uppercase (A-Z)",
    variable=upper_var,
    bg=WINDOW_BG,
    fg=PRIMARY_TEXT,
    selectcolor=WINDOW_BG,
    activebackground=WINDOW_BG,
    activeforeground=ACCENT_GREEN
).pack(anchor=tk.W)

tk.Checkbutton(
    options_frame,
    text="Digits (0-9)",
    variable=digit_var,
    bg=WINDOW_BG,
    fg=PRIMARY_TEXT,
    selectcolor=WINDOW_BG,
    activebackground=WINDOW_BG,
    activeforeground=ACCENT_GREEN
).pack(anchor=tk.W)

tk.Checkbutton(
    options_frame,
    text="Special characters (!@#$%...)",
    variable=special_var,
    bg=WINDOW_BG,
    fg=PRIMARY_TEXT,
    selectcolor=WINDOW_BG,
    activebackground=WINDOW_BG,
    activeforeground=ACCENT_GREEN
).pack(anchor=tk.W)

tk.Checkbutton(
    options_frame,
    text="Exclude ambiguous characters (0, O, 1, l, I)",
    variable=ambiguous_var,
    bg=WINDOW_BG,
    fg=PRIMARY_TEXT,
    selectcolor=WINDOW_BG,
    activebackground=WINDOW_BG,
    activeforeground=ACCENT_GREEN
).pack(anchor=tk.W)

button_frame = tk.Frame(main_frame, bg=WINDOW_BG)
button_frame.pack(fill=tk.X, pady=10)

generate_btn = tk.Button(
    button_frame,
    text="Generate Password",
    command=on_generate,
    bg=BUTTON_GREEN,
    fg="white",
    font=("Arial", 11, "bold"),
    activebackground=BUTTON_GREEN_ACTIVE,
    activeforeground="white",
    padx=10
)
generate_btn.pack(side=tk.LEFT, padx=5)
generate_btn.bind('<Return>', on_key_generate)

root.bind('<Return>', on_key_generate)

result_var = tk.StringVar()
result_entry = tk.Entry(
    main_frame,
    textvariable=result_var,
    font=("Courier", 13),
    bg=DARK_INPUT_BG,
    fg=ACCENT_GREEN,
    width=40,
    borderwidth=2,
    relief="flat",
    justify="center",
    state="readonly"
)
result_entry.pack(pady=10)

copy_clear_frame = tk.Frame(main_frame, bg=WINDOW_BG)
copy_clear_frame.pack(fill=tk.X, pady=5)

copy_btn = tk.Button(
    copy_clear_frame,
    text="Copy",
    command=copy_to_clipboard,
    bg=ACCENT_BLUE,
    fg="white",
    font=("Arial", 10, "bold"),
    activebackground=BUTTON_BLUE_ACTIVE,
    activeforeground="white",
    width=12
)
copy_btn.pack(side=tk.LEFT, padx=5)

clear_btn = tk.Button(
    copy_clear_frame,
    text="Clear",
    command=clear_result,
    bg="#555555",
    fg="white",
    font=("Arial", 10, "bold"),
    activebackground="#777777",
    activeforeground="white",
    width=12
)
clear_btn.pack(side=tk.LEFT, padx=5)

strength_label = tk.Label(main_frame, text="", bg=WINDOW_BG, font=("Arial", 10))
strength_label.pack(pady=5)

strength_canvas = tk.Canvas(main_frame, bg=DARK_INPUT_BG, height=15, width=200, highlightthickness=0)
strength_canvas.pack(pady=5)

status_label = tk.Label(main_frame, text="", bg=WINDOW_BG, font=("Arial", 9))
status_label.pack(pady=5)

history_label = tk.Label(
    main_frame,
    text="Recent Passwords (Click to select)",
    bg=WINDOW_BG,
    fg=PRIMARY_TEXT,
    font=("Arial", 10, "bold")
)
history_label.pack(pady=(15, 5))

history_text = tk.Text(
    main_frame,
    height=6,
    width=45,
    bg=DARK_INPUT_BG,
    fg=ACCENT_GREEN,
    font=("Courier", 9),
    borderwidth=1,
    relief="solid",
    state=tk.DISABLED
)
history_text.pack(pady=5)
history_text.bind("<Button-1>", select_history_password)

exit_btn = tk.Button(
    main_frame,
    text="Exit",
    command=root.destroy,
    bg=ACCENT_RED,
    fg="white",
    font=("Arial", 11, "bold"),
    activebackground=BUTTON_RED_ACTIVE,
    activeforeground="white",
    width=20
)
exit_btn.pack(pady=10)

root.mainloop()
