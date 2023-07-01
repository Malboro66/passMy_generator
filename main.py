import random
import string
import tkinter as tk

def generate_password():
    length = 8
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_characters = "@#$%&"
    characters = lowercase + uppercase + digits + special_characters
    password = random.choice(lowercase) + random.choice(uppercase) + random.choice(digits) + random.choice(special_characters)
    while len(password) < length:
        char = random.choice(characters)
        if char not in password:
            if char in uppercase and password and password[-1] in uppercase:
                continue
            if char in lowercase and password and password[-1] in lowercase:
                continue
            if char in digits and password and password[-1] in digits:
                continue
            if char in lowercase and len(password) > 1 and password[-2:] in lowercase:
                continue
            if char in uppercase and len(password) > 1 and password[-2:] in uppercase:
                continue
            if char in digits and len(password) > 1 and password[-2:] in digits:
                continue
            password += char
    password = ''.join(random.sample(password, len(password)))
    return password

def on_generate():
    password = generate_password()
    result_label["text"] = f"Generated Password: {password}"

root = tk.Tk()
root.title("Password Generator")

generate_button = tk.Button(root, text="Generate Password", command=on_generate)
generate_button.pack()

result_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"))
result_label.pack()

quit_button = tk.Button(root, text="Quit", command=root.destroy)
quit_button.pack()

root.mainloop()