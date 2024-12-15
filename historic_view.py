# historic_view.py

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json



class HistoryView:
    def __init__(self, root, controller, user_email):
        """Initialize the history view window."""
        self.root = root
        self.controller = controller
        self.user_email = user_email

        # Criar uma nova janela para o histórico
        self.window = tk.Toplevel(self.root)
        self.window.title("User History")
        self.window.geometry("700x400")
        self.window.configure(bg="#1F2833")

        # Header
        tk.Label(self.window, text=f"History for {self.user_email}",
                 font=("Arial", 18, "bold"), fg="#66FCF1", bg="#1F2833").pack(pady=10)

        # Treeview para mostrar os dados do histórico
        self.history_list = ttk.Treeview(self.window)
        self.history_list["columns"] = ("Type", "Details", "Date")

        # Configurar colunas
        self.history_list.column("#0", width=0, stretch=tk.NO)  # Oculta a primeira coluna vazia
        self.history_list.column("Type", anchor=tk.W, width=100)
        self.history_list.column("Details", anchor=tk.W, width=400)
        self.history_list.column("Date", anchor=tk.W, width=150)

        self.history_list.heading("Type", text="Type", anchor=tk.W)
        self.history_list.heading("Details", text="Details", anchor=tk.W)
        self.history_list.heading("Date", text="Date", anchor=tk.W)

        self.history_list.pack(pady=20, fill="both", expand=True)

        # Botão de retorno
        tk.Button(self.window, text="Back to Main", font=("Arial", 12, "bold"),
                  bg="#66FCF1", fg="#1F2833", command=self.back_to_main).pack(pady=10)

        # Carregar histórico
        self.load_history()

    def load_history(self):
        """Load user history from the JSON file."""
        try:
            with open("history.json", "r") as file:
                data = json.load(file)

            user_history = data.get(self.user_email, [])
            for entry in user_history:
                entry_type = entry.get("type", "Unknown")
                details = entry.get("details", {})
                detail_text = (
                    f"From {details.get('origin', 'N/A')} to {details.get('destination', 'N/A')} | "
                    f"Passengers: {details.get('passengers', 'N/A')} | "
                    f"Max Price: {details.get('price_max', 'N/A')}"
                )
                date = entry.get("date", "Unknown")
                self.history_list.insert("", "end", values=(entry_type, detail_text, date))

        except FileNotFoundError:
            tk.messagebox.showinfo("No History", "No history found for this user.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to load history: {e}")

    def back_to_main(self):
        """Volta para o menu principal."""
        self.controller.open_main_form()







