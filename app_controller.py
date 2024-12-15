# app_controller.py

from model.flight_model import FlightModel
from view.flight_view import FlightView
from tkinter import messagebox
from settings import API_KEY, API_SECRET
from view.seat_selection import SeatSelectionView
from view.passenger_info_view import PassengerInfoView
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from settings import SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD
from datetime import datetime, date
import json
import folium
import webbrowser
from geopy.geocoders import Nominatim
import hashlib
from view.login_register_view import LoginRegisterView
from view.historic_view import HistoryView


class AppController:
    def __init__(self, root):
        self.root = root
        self.model = FlightModel(API_KEY, API_SECRET)

        # Start with the login/register view
        self.open_login_register()

        try:
            self.destinations = self.model.get_destinations()
            self.airlines = self.model.get_airlines()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching data: {e}")
            self.destinations = []
            self.airlines = []

    def search_flights(self, data):
        """Busca voos com base nos dados fornecidos e os exibe."""
        try:
            filters = data["filters"]
            # Normalize and sanitize filter keys
            filters["nonStop"] = bool(filters.pop("non_stop", False))

            flights, dictionaries = self.model.search_flights(
                origin=data["origin"],
                destination=data["destination"],
                departure=data["departure_date"],
                return_date=data["return_date"],
                passengers=data["passengers"],
                filters=filters
            )
            if flights:

                # Logar a busca no histórico
                self.log_history(
                    user_email=self.current_user,
                    entry_type="search",
                    origin=data["origin"],
                    destination=data["destination"],
                    passengers=data["passengers"],
                    price_max=filters.get("price_max", "N/A")
                )
                self.view.display_flights(flights, dictionaries)
                self.save_search_history(data, flights)
            else:
                messagebox.showinfo("No Flights", "No flights were found for the selected criteria.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def select_flight(self, flight):
        """Armazena o voo selecionado e avança para a próxima etapa."""
        # Salva o voo selecionado
        self.selected_flight = flight

        # Mostra uma mensagem de confirmação
        messagebox.showinfo("Flight Selected", "You have selected a flight!")

        # Avança para a próxima etapa: Seleção de assentos
        self.open_seat_selection()

    def open_seat_selection(self):
        """Abre a janela de seleção de assentos."""
        # Número de passageiros com base na pesquisa inicial
        num_passengers = self.view.passenger_var.get()
        self.selected_passengers = num_passengers
        SeatSelectionView(self.view.root, self, self.selected_flight, num_passengers)

    def confirm_seat_selection(self, selected_seats):
        """Lida com a confirmação da seleção de assentos."""
        self.selected_seats = selected_seats
        messagebox.showinfo(
            "Seats Confirmed",
            f"Seats {', '.join(self.selected_seats)} have been confirmed!"
        )
        # Avançar para a próxima etapa: informações dos passageiros
        self.open_passenger_info()

    def open_passenger_info(self):
        """Abre a janela para coletar informações dos passageiros."""
        PassengerInfoView(
            self.view.root,
            self,
            self.selected_flight,
            self.selected_seats,
            self.view.passenger_var.get()  # Pega o número de passageiros do formulário principal
        )

    def send_email(recipient, subject, body):
        try:
            # Configurar o e-mail
            msg = MIMEMultipart()
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = recipient
            msg["Subject"] = subject

            # Adicionar corpo do e-mail
            msg.attach(MIMEText(body, "plain"))

            # Configurar servidor SMTP
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()  # Iniciar conexão segura
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Login
                server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())  # Enviar e-mail

            print(f"E-mail enviado com sucesso para {recipient}")

        except Exception as e:
            print(f"Erro ao enviar e-mail para {recipient}: {e}")
            raise Exception(f"Failed to send email: {e}")

    def reset_form(self):
        """Reinicia os campos do formulário principal."""
        # Define valores padrão
        self.view.origin_var.set("LIS - Lisbon")
        self.view.destination_var.set("JFK - New York")
        self.view.passenger_var.set(1)
        self.view.max_price_var.set("")
        self.view.non_stop_var.set(False)
        self.view.airline_var.set("")

        # Define a data atual para os widgets DateEntry
        today = date.today()
        self.view.departure_date_entry.set_date(today)  # Ajuste no DateEntry
        self.view.return_date_entry.set_date(today)  # Ajuste no DateEntry

        # Remove resultados antigos
        if hasattr(self.view, "results_canvas"):
            self.view.results_canvas.destroy()

        if hasattr(self.view, "scrollbar"):
            self.view.scrollbar.destroy()
            del self.view.scrollbar

        messagebox.showinfo("Form Reset", "The form has been reset successfully!")

    def save_search_history(self, search_data, results):
        with open("search_history.json", "a") as file:
            history = {"search": search_data, "results": results}
            file.write(json.dumps(history) + "\n")

    def generate_route_map(self, origin_code, destination_code):
        """Cria um mapa interativo mostrando a rota entre o aeroporto de origem e o de destino."""
        try:
            geolocator = Nominatim(user_agent="flight_app")

            # Obter localizações dos aeroportos
            origin_location = geolocator.geocode(origin_code)
            destination_location = geolocator.geocode(destination_code)

            if not origin_location or not destination_location:
                raise ValueError("Não foi possível localizar os aeroportos especificados.")

            # Coordenadas
            origin_coords = (origin_location.latitude, origin_location.longitude)
            destination_coords = (destination_location.latitude, destination_location.longitude)

            # Criar mapa
            route_map = folium.Map(location=origin_coords, zoom_start=6)
            folium.Marker(origin_coords, tooltip="Origem", icon=folium.Icon(color="green")).add_to(route_map)
            folium.Marker(destination_coords, tooltip="Destino", icon=folium.Icon(color="red")).add_to(route_map)
            folium.PolyLine([origin_coords, destination_coords], color="blue", weight=2.5).add_to(route_map)

            # Salvar e abrir o mapa
            map_file = "route_map.html"
            route_map.save(map_file)
            webbrowser.open(map_file)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate route map: {e}")

    def calculate_carbon_emissions(self, origin_code, destination_code, passengers):
        """
        Calcula a pegada de carbono para um voo com base na distância entre origem e destino.
        """
        try:
            geolocator = Nominatim(user_agent="flight_app")

            # Obter coordenadas dos aeroportos
            origin_location = geolocator.geocode(origin_code)
            destination_location = geolocator.geocode(destination_code)

            if not origin_location or not destination_location:
                raise ValueError("Não foi possível localizar os aeroportos especificados.")

            # Coordenadas
            origin_coords = (origin_location.latitude, origin_location.longitude)
            destination_coords = (destination_location.latitude, destination_location.longitude)

            # Calcular distância em km
            from geopy.distance import geodesic
            distance_km = geodesic(origin_coords, destination_coords).kilometers

            # Fórmula básica de emissões (média aproximada por km por passageiro)
            carbon_per_km = 0.115  # Toneladas de CO2 por passageiro por km (média global)
            total_emissions = distance_km * carbon_per_km * passengers

            # Mostrar resultado
            messagebox.showinfo(
                "Carbon Emissions",
                f"Total carbon emissions for this flight:\n"
                f"{total_emissions:.2f} kg CO2 for {passengers} passenger(s)."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate carbon emissions: {e}")

    def open_login_register(self):
        """Displays the login/register view."""
        self.clear_frame()
        from view.login_register_view import LoginRegisterView
        self.login_register_view = LoginRegisterView(self.root, self)

    def handle_login(self, email, password):
        """Lida com o login do usuário."""
        try:
            with open("users.json", "r") as file:
                users = json.load(file)

            hashed_password = self.hash_password(password)
            if users.get(email) == hashed_password:
                messagebox.showinfo("Success", "Login successful!")
                self.open_main_form()
            else:
                messagebox.showerror("Error", "Invalid email or password.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No users registered yet.")

    def handle_register(self, email, password):
        """Lida com o registro de um novo usuário."""
        try:
            with open("users.json", "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            users = {}

        if email in users:
            messagebox.showerror("Error", "Email already registered.")
            return

        hashed_password = self.hash_password(password)
        users[email] = hashed_password

        with open("users.json", "w") as file:
            json.dump(users, file)

        messagebox.showinfo("Success", "Registration successful! You can now log in.")
        self.open_login_register()

    def open_main_form(self):
        """Abre o formulário principal após login bem-sucedido."""
        self.clear_frame()  # Limpa todos os widgets anteriores

        # Recria o FlightView
        try:
            self.destinations = self.model.get_destinations()
            self.view = FlightView(self.root, self, self.destinations)

            # Mostrar mensagem de boas-vindas com o usuário logado
            if hasattr(self, "current_user"):
                self.view.display_logged_in_user(self.current_user)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load main form: {e}")

    def clear_frame(self):
        """Clears all widgets from the current root window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    @staticmethod
    def hash_password(password):
        """Converte a senha para um hash SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def login_user(self, email, password):
        """Handles user login."""
        try:
            if self.model.validate_login(email, password):
                messagebox.showinfo("Login Successful", f"Welcome, {email}!")
                self.current_user = email  # Store the logged-in user's email
                self.open_flight_search()  # Transition to flight search
            else:
                messagebox.showerror("Login Failed", "Invalid email or password.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during login: {e}")

    def register_user(self, email, password):
        """Handles user registration."""
        try:
            if self.model.register_user(email, password):
                messagebox.showinfo("Registration Successful", "You can now log in.")
                self.open_login_register()  # Transition back to login
            else:
                messagebox.showerror("Registration Failed", "Email is already registered.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during registration: {e}")

    def open_flight_search(self):
        """Displays the flight search view."""
        self.clear_frame()
        self.view = FlightView(self.root, self, self.destinations)
        if hasattr(self, "current_user"):
            self.view.display_logged_in_user(self.current_user)

    def open_history_view(self):
        """Opens the history view for the logged-in user."""
        if not hasattr(self, "current_user"):
            messagebox.showerror("Error", "No user is logged in.")
            return

        self.clear_frame()
        HistoryView(self.root, self, self.current_user)

        def log_history(self, user_email, entry):
            """Logs a search or booking to the user's history."""
            try:
                history = {}
                try:
                    with open("history.json", "r") as file:
                        history = json.load(file)
                except FileNotFoundError:
                    pass

                if user_email not in history:
                    history[user_email] = []

                history[user_email].append(entry)

                with open("history.json", "w") as file:
                    json.dump(history, file, indent=4)

            except Exception as e:
                print(f"Failed to log history: {e}")

    def log_history(self, user_email, entry_type, origin=None, destination=None, passengers=None, price_max=None):
        """Logs a search or booking to the user's history."""
        try:
            history = {}
            # Carregar histórico existente
            try:
                with open("history.json", "r") as file:
                    history = json.load(file)
            except FileNotFoundError:
                pass

            # Novo registro com detalhes
            entry = {
                "type": entry_type,
                "details": {
                    "origin": origin if origin else "N/A",
                    "destination": destination if destination else "N/A",
                    "passengers": passengers if passengers else "N/A",
                    "price_max": price_max if price_max else "N/A"
                },
                "date": datetime.now().isoformat()
            }

            # Adicionar ao histórico
            history.setdefault(user_email, []).append(entry)

            # Salvar no JSON
            with open("history.json", "w") as file:
                json.dump(history, file, indent=4)

        except Exception as e:
            print(f"Error logging history: {e}")

























