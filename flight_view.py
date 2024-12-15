# flight_view.py

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from settings import DEEP_FOREST, FOREST_GREEN, LEAF_GREEN, MOSS_YELLOW, BRIGHT_YELLOW
from settings import FONT_ENTRY, FONT_BOLD, FONT_TITLE, FONT_NORMAL, FONT_BUTTON, FONT_LABEL

class FlightView:
    def __init__(self, root, controller, destinations):
        self.root = root
        self.controller = controller
        self.destinations = destinations

        # State variables
        self.filters_visible = False
        self.origin_var = tk.StringVar(value="LIS - Lisbon")
        self.destination_var = tk.StringVar(value="JFK - New York")
        self.departure_date = tk.StringVar()
        self.return_date = tk.StringVar()
        self.passenger_var = tk.IntVar(value=1)
        self.max_price_var = tk.StringVar()
        self.non_stop_var = tk.BooleanVar(value=False)
        self.airline_var = tk.StringVar(value="")
        self.max_duration_var = tk.StringVar(value="")
        self.stops_var = tk.StringVar(value="Any")
        self.departure_time_var = tk.StringVar(value="")
        self.arrival_time_var = tk.StringVar(value="")
        self.layover_var = tk.StringVar(value="")

        # Configure root
        self.frame = tk.Frame(self.root, background=DEEP_FOREST)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        """Creates the main form widgets."""
        tk.Label(self.frame, text="Origin:", bg=DEEP_FOREST, fg=BRIGHT_YELLOW, font=FONT_LABEL).grid(
            row=0, column=0, sticky="e", pady=10, padx=10
        )
        self.origin_dropdown = ttk.Combobox(
            self.frame, textvariable=self.origin_var, font=FONT_ENTRY, width=30
        )
        self.origin_dropdown['values'] = sorted(self.destinations)
        self.origin_dropdown.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(self.frame, text="Destination:", bg=DEEP_FOREST, fg=BRIGHT_YELLOW, font=FONT_LABEL).grid(
            row=1, column=0, sticky="e", pady=10, padx=10
        )
        self.destination_dropdown = ttk.Combobox(
            self.frame, textvariable=self.destination_var, font=FONT_ENTRY, width=30
        )
        self.destination_dropdown['values'] = sorted(self.destinations)
        self.destination_dropdown.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(self.frame, text="Departure Date:", bg=DEEP_FOREST, fg=BRIGHT_YELLOW, font=FONT_LABEL).grid(
            row=2, column=0, sticky="e", pady=10, padx=10
        )
        self.departure_date_entry = DateEntry(self.frame, textvariable=self.departure_date, width=12, font=FONT_ENTRY)
        self.departure_date_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        tk.Label(self.frame, text="Return Date:", bg=DEEP_FOREST, fg=BRIGHT_YELLOW, font=FONT_LABEL).grid(
            row=3, column=0, sticky="e", pady=10, padx=10
        )
        self.return_date_entry = DateEntry(self.frame, textvariable=self.return_date, width=12, font=FONT_ENTRY)
        self.return_date_entry.grid(row=3, column=1, pady=10, padx=10, sticky="w")

        tk.Label(self.frame, text="Passengers:", bg=DEEP_FOREST, fg=BRIGHT_YELLOW, font=FONT_LABEL).grid(
            row=4, column=0, sticky="e", pady=10, padx=10
        )
        tk.Spinbox(
            self.frame, from_=1, to=10, textvariable=self.passenger_var, font=FONT_ENTRY, width=5
        ).grid(row=4, column=1, pady=10, padx=10, sticky="w")

        self.advanced_filter_button = tk.Button(
            self.frame,
            text="Advanced Filters",
            bg=LEAF_GREEN,
            fg=DEEP_FOREST,
            activebackground=MOSS_YELLOW,
            activeforeground=BRIGHT_YELLOW,
            font=("Arial", 10),
            command=self.toggle_filters
        )
        self.advanced_filter_button.grid(row=6, column=0, pady=10, padx=10, sticky="w")

        # Search button
        self.search_button = tk.Button(
            self.frame, text="Search Flights", bg=MOSS_YELLOW, fg=DEEP_FOREST,
            activebackground=BRIGHT_YELLOW, activeforeground=FOREST_GREEN, font=FONT_BUTTON,
            command=self.collect_search_data
        )
        self.search_button.grid(row=5, column=0,columnspan=2, pady=20)

        # Botão para mostrar rota
        self.route_button = tk.Button(
            self.frame, text="Show Route", bg=LEAF_GREEN, fg=DEEP_FOREST,
            activebackground=MOSS_YELLOW, activeforeground=BRIGHT_YELLOW,
            font=("Arial", 10), command=self.show_route
        )
        self.route_button.grid(row=7, column=0, columnspan=1, pady=10, padx=10, sticky="w")

        # Botão para calcular carbono
        self.carbon_button = tk.Button(
            self.frame, text="Calculate Carbon", bg=LEAF_GREEN, fg=DEEP_FOREST,
            activebackground=MOSS_YELLOW, activeforeground=BRIGHT_YELLOW,
            font=("Arial", 10), command=self.calculate_carbon
        )
        self.carbon_button.grid(row=7, column=1, columnspan=1, pady=10, padx=10, sticky="w")

        # Botão para mostrar historico
        tk.Button(
            self.frame,
            text="View History",
            command=self.controller.open_history_view,
            bg=LEAF_GREEN,
            fg=DEEP_FOREST,
            font=("Arial", 10),
            activebackground=MOSS_YELLOW,
            activeforeground=BRIGHT_YELLOW
        ).grid(row=6, column=1, columnspan=1, pady=10, padx=10, sticky="w")

    def toggle_filters(self):
        """Shows or hides the advanced filters section."""
        if not hasattr(self, "filters_frame"):
            self.filters_frame = tk.Frame(self.frame, bg=DEEP_FOREST)

            # Max Price
            tk.Label(self.filters_frame, text="Max Price (EUR):", bg=DEEP_FOREST, fg=BRIGHT_YELLOW,
                     font=FONT_LABEL).grid(row=0, column=0, sticky="e", pady=10, padx=10)
            tk.Entry(self.filters_frame, textvariable=self.max_price_var, font=FONT_ENTRY, width=15).grid(
                row=0, column=1, pady=10, padx=10, sticky="w")

            # Non-stop only
            tk.Label(self.filters_frame, text="Non-stop only:", bg=DEEP_FOREST, fg=BRIGHT_YELLOW,
                     font=FONT_LABEL).grid(row=1, column=0, sticky="e", pady=10, padx=10)
            tk.Checkbutton(self.filters_frame, variable=self.non_stop_var, bg=DEEP_FOREST).grid(
                row=1, column=1, pady=10, padx=10, sticky="w")

            # Airline filter
            tk.Label(self.filters_frame, text="Airline:", bg=DEEP_FOREST, fg=BRIGHT_YELLOW,
                     font=FONT_LABEL).grid(row=2, column=0, sticky="e", pady=10, padx=10)
            self.airline_dropdown = ttk.Combobox(
                self.filters_frame, textvariable=self.airline_var, font=FONT_ENTRY, width=30
            )
            self.airline_dropdown['values'] = [f"{code} - {name}" for code, name in self.controller.airlines.items()]
            self.airline_dropdown.grid(row=2, column=1, pady=10, padx=10, sticky="w")

            # Max Flight Duration
            tk.Label(self.filters_frame, text="Max Flight Duration (hrs):", bg=DEEP_FOREST, fg=BRIGHT_YELLOW,
                     font=FONT_LABEL).grid(row=3, column=0, sticky="e", pady=10, padx=10)
            tk.Entry(self.filters_frame, textvariable=self.max_duration_var, font=FONT_ENTRY, width=15).grid(
                row=3, column=1, pady=10, padx=10, sticky="w")

            # Number of Stops
            tk.Label(self.filters_frame, text="Number of Stops:", bg=DEEP_FOREST, fg=BRIGHT_YELLOW,
                     font=FONT_LABEL).grid(row=4, column=0, sticky="e", pady=10, padx=10)
            ttk.Combobox(
                self.filters_frame, textvariable=self.stops_var, font=FONT_ENTRY,
                values=["Any", "Non-stop", "1 Stop", "2+ Stops"], width=15
            ).grid(row=4, column=1, pady=10, padx=10, sticky="w")

            # Departure Time
            tk.Label(self.filters_frame, text="Departure Time (HH:MM):", bg=DEEP_FOREST, fg=BRIGHT_YELLOW,
                     font=FONT_LABEL).grid(row=5, column=0, sticky="e", pady=10, padx=10)
            tk.Entry(self.filters_frame, textvariable=self.departure_time_var, font=FONT_ENTRY, width=15).grid(
                row=5, column=1, pady=10, padx=10, sticky="w")

            # Arrival Time
            tk.Label(self.filters_frame, text="Arrival Time (HH:MM):", bg=DEEP_FOREST, fg=BRIGHT_YELLOW,
                     font=FONT_LABEL).grid(row=6, column=0, sticky="e", pady=10, padx=10)
            tk.Entry(self.filters_frame, textvariable=self.arrival_time_var, font=FONT_ENTRY, width=15).grid(
                row=6, column=1, pady=10, padx=10, sticky="w")

            # Layover Airport
            tk.Label(self.filters_frame, text="Layover Airport:", bg=DEEP_FOREST, fg=BRIGHT_YELLOW,
                     font=FONT_LABEL).grid(row=7, column=0, sticky="e", pady=10, padx=10)
            tk.Entry(self.filters_frame, textvariable=self.layover_var, font=FONT_ENTRY, width=30).grid(
                row=7, column=1, pady=10, padx=10, sticky="w")

        if self.filters_visible:
            self.filters_frame.grid_remove()
        else:
            self.filters_frame.grid(row=7, column=0, columnspan=2, pady=10)

        self.filters_visible = not self.filters_visible


    def collect_search_data(self):
        """Collects form data and sends it to the controller."""
        carrier = self.airline_var.get().split(" - ")[0] if self.airline_var.get() else ""
        try:
            data = {
                "origin": self.origin_var.get().split(" - ")[0],
                "destination": self.destination_var.get().split(" - ")[0],
                "departure_date": self.departure_date_entry.get_date().strftime("%Y-%m-%d"),
                "return_date": self.return_date_entry.get_date().strftime("%Y-%m-%d"),
                "passengers": self.passenger_var.get(),
                "filters": {
                    "price_max": self.max_price_var.get(),
                    "non_stop": self.non_stop_var.get(),
                    "carrier": carrier,
                    "max_duration": self.max_duration_var.get(),
                    "stops": self.stops_var.get(),
                    "departure_time": self.departure_time_var.get(),
                    "arrival_time": self.arrival_time_var.get(),
                    "layover_airport": self.layover_var.get(),
                }
            }
            self.controller.search_flights(data)
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to collect search data: {e}")

    def display_flights(self, flights, dictionaries):
        """Exibe os voos disponíveis no canvas usando grid."""
        # Remove widgets antigos do canvas
        if hasattr(self, "results_canvas"):
            self.results_canvas.destroy()

        if hasattr(self, "scrollbar"):
            self.scrollbar.destroy()
            del self.scrollbar

        # Remove duplicados
        seen_flights = set()
        unique_flights = []
        for flight in flights:
            flight_key = (
                flight["price"]["grandTotal"],
                flight["itineraries"][0]["duration"],
                tuple((segment["departure"]["iataCode"], segment["arrival"]["iataCode"]) for segment in
                      flight["itineraries"][0]["segments"]),
            )
            if flight_key not in seen_flights:
                seen_flights.add(flight_key)
                unique_flights.append(flight)

        # Cria um novo canvas para exibir os voos
        self.results_canvas = tk.Canvas(self.frame, bg=DEEP_FOREST, highlightthickness=0)
        self.results_canvas.grid(row=9, column=0, columnspan=3, sticky="nsew", pady=10)

        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.results_canvas.yview)
        scrollbar.grid(row=9, column=3, sticky="ns", pady=10)

        self.results_canvas.configure(yscrollcommand=scrollbar.set)
        self.results_frame = tk.Frame(self.results_canvas, bg=DEEP_FOREST)
        self.results_canvas.create_window((10, 10), window=self.results_frame, anchor="n")

        for i, flight in enumerate(unique_flights):
            frame = tk.Frame(self.results_frame, bg=FOREST_GREEN, bd=2, relief="solid")
            frame.pack(padx=10, pady=10, fill="x", expand=True)

            # Processa detalhes do voo
            price = flight["price"]
            traveler_pricing = flight["travelerPricings"][0]
            checked_bags = traveler_pricing["fareDetailsBySegment"][0].get("includedCheckedBags", {}).get("quantity", 0)

            amenities = traveler_pricing["fareDetailsBySegment"][0].get("amenities", [])
            services = "\n".join(
                [f"  - {amenity['description']}: {'Included' if not amenity['isChargeable'] else 'Paid'}" for amenity in
                 amenities]
            )

            # Detalhes do itinerário (companhia e avião)
            itinerary_details = ""
            for itinerary in flight["itineraries"]:
                for segment in itinerary["segments"]:
                    departure = segment["departure"]["iataCode"]
                    arrival = segment["arrival"]["iataCode"]
                    airline = dictionaries["carriers"].get(segment["carrierCode"], "Unknown Airline")
                    aircraft = dictionaries["aircraft"].get(segment["aircraft"]["code"], "Unknown Aircraft")
                    departure_time = segment["departure"]["at"]
                    duration = segment["duration"]

                    itinerary_details += f"""
                    - From {departure} to {arrival}
                      Airline: {airline}
                      Aircraft: {aircraft}
                      Departure: {departure_time}
                      Duration: {duration}
                    """

            # Informações detalhadas
            flight_info = f"""
    Flight {i + 1}:
    Total Price: {price['grandTotal']} {price['currency']}
    Duration: {flight['itineraries'][0]['duration']}
    Stops: {len(flight['itineraries'][0]['segments']) - 1}
    Bags Included: {checked_bags}

    Amenities:
    {services}

    Itinerary Details:
    {itinerary_details}
            """

            # Ajusta exibição do texto no frame
            tk.Label(frame, text=flight_info.strip(), bg=FOREST_GREEN, fg=BRIGHT_YELLOW, font=("Arial", 10),
                     justify="left", anchor="w", wraplength=700).pack(side="left", padx=10, pady=5)

            tk.Button(
                frame,
                text="Select",
                bg=LEAF_GREEN,
                fg=DEEP_FOREST,
                font=("Arial", 10, "bold"),
                command=lambda f=flight: self.controller.select_flight(f),
            ).pack(side="right", padx=10, pady=10)

        self.results_frame.update_idletasks()
        self.results_canvas.config(scrollregion=self.results_canvas.bbox("all"))

    def show_route(self):
        """Coleta os dados de origem e destino e exibe o mapa de rota."""
        origin = self.origin_var.get().split(" - ")[0]
        destination = self.destination_var.get().split(" - ")[0]

        if origin and destination:
            self.controller.generate_route_map(origin, destination)
        else:
            tk.messagebox.showerror("Error", "Please select both origin and destination.")

    def calculate_carbon(self):
        """Coleta dados do formulário e envia para cálculo de carbono."""
        origin = self.origin_var.get().split(" - ")[0]
        destination = self.destination_var.get().split(" - ")[0]
        passengers = self.passenger_var.get()

        if origin and destination:
            self.controller.calculate_carbon_emissions(origin, destination, passengers)
        else:
            tk.messagebox.showerror("Error", "Please select both origin and destination.")

    def display_logged_in_user(self, email):
        """Displays the logged-in user's email on the flight search form."""
        label = tk.Label(
            self.frame, text=f"logged in as: {email}", bg=DEEP_FOREST, fg=BRIGHT_YELLOW, font=("Arial", 8)
        )
        label.grid(row=10, column=0, columnspan=2, sticky="w", padx=10, pady=5)


























