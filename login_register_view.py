# login_register_view.py

import tkinter as tk
from tkinter import ttk, messagebox
import re
from settings import  BACKGROUND_COLOR_2, WIDGET_COLOR_2, BUTTON_COLOR_2, FONT_LARGE, FONT_MEDIUM, FONT_SMALL

class LoginRegisterView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.configure(bg="#1F2833")  # Cor de fundo geral

        # Frame principal para Login/Register
        self.main_frame = tk.Frame(self.root, bg="#1F2833", bd=2, relief="solid")
        self.main_frame.pack(expand=True, fill="both", padx=50, pady=50)

        # Notebook (abas para Login e Register)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill="both")

        # Frames para Login e Registro
        self.login_frame = tk.Frame(self.notebook, bg="#1F2833")
        self.register_frame = tk.Frame(self.notebook, bg="#1F2833")

        # Adiciona as abas
        self.notebook.add(self.login_frame, text="Login")
        self.notebook.add(self.register_frame, text="Register")

        # Criar widgets para Login e Registro
        self.create_login_widgets()
        self.create_register_widgets()

    def create_login_widgets(self):
        """Cria widgets para a aba de Login."""
        title = tk.Label(self.login_frame, text="Login", fg="#66FCF1", bg="#1F2833", font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(self.login_frame, text="Email:", fg="#C5C6C7", bg="#1F2833", font=("Arial", 12)).grid(
            row=1, column=0, pady=10, padx=10, sticky="e")
        self.login_email_entry = tk.Entry(self.login_frame, font=("Arial", 12), width=30)
        self.login_email_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(self.login_frame, text="Password:", fg="#C5C6C7", bg="#1F2833", font=("Arial", 12)).grid(
            row=2, column=0, pady=10, padx=10, sticky="e")
        self.login_password_entry = tk.Entry(self.login_frame, font=("Arial", 12), width=30, show="*")
        self.login_password_entry.grid(row=2, column=1, pady=10, padx=10)

        tk.Button(self.login_frame, text="Login", bg="#66FCF1", fg="#1F2833", font=("Arial", 12, "bold"),
                  command=self.handle_login).grid(row=3, column=0, columnspan=2, pady=20)

    def create_register_widgets(self):
        """Cria widgets para a aba de Registro."""
        title = tk.Label(self.register_frame, text="Register", fg="#66FCF1", bg="#1F2833", font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(self.register_frame, text="Email:", fg="#C5C6C7", bg="#1F2833", font=("Arial", 12)).grid(
            row=1, column=0, pady=10, padx=10, sticky="e")
        self.email_entry = tk.Entry(self.register_frame, font=("Arial", 12), width=30)
        self.email_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(self.register_frame, text="Password:", fg="#C5C6C7", bg="#1F2833", font=("Arial", 12)).grid(
            row=2, column=0, pady=10, padx=10, sticky="e")
        self.password_entry = tk.Entry(self.register_frame, font=("Arial", 12), width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=10, padx=10)

        tk.Button(self.register_frame, text="Register", bg="#66FCF1", fg="#1F2833", font=("Arial", 12, "bold"),
                  command=self.handle_register).grid(row=3, column=0, columnspan=2, pady=20)

    def is_valid_email(self, email):
        """Valida o formato do email usando regex."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email)

    def handle_register(self):
        """Lida com o processo de registro."""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showerror("Error", "Email and password cannot be empty.")
            return

        if not self.is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            return

        try:
            success = self.controller.register_user(email, password)
            if success:
                messagebox.showinfo("Success", "Registration successful! Redirecting to login.")
                self.notebook.select(self.login_frame)  # Redireciona para a aba de login
            else:
                #messagebox.showerror("Error", "Email already exists.")
                pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register: {e}")

    def handle_login(self):
        """Lida com o processo de login."""
        email = self.login_email_entry.get().strip()
        password = self.login_password_entry.get().strip()

        if not email or not password:
            messagebox.showerror("Error", "Email and password cannot be empty.")
            return

        try:
            success = self.controller.login_user(email, password)
            if success:
                messagebox.showinfo("Success", "Login successful!")
                self.controller.open_main_view()
            else:
                #messagebox.showerror("Error", "Invalid email or password.")
                pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to login: {e}")
