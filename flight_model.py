# flight_model.py

import requests
import json
import hashlib

class FlightModel:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://test.api.amadeus.com"
        self.token = None

    def authenticate(self):
        url = f"{self.base_url}/v1/security/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret
        }
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            self.token = response.json().get("access_token")
        else:
            raise Exception(f"Failed to authenticate with Amadeus API: {response.text}")

    def search_flights(self, origin, destination, departure, return_date, passengers, filters):
        """Busca voos no Amadeus API com filtros adicionais."""
        if not self.token:
            self.authenticate()

        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure,
            "returnDate": return_date,
            "adults": passengers,
            "max": 10,
        }

        # Aplicar os filtros recebidos
        if filters.get("price_max"):
            params["maxPrice"] = int(filters["price_max"])

        if filters.get("non_stop"):
            params["nonStop"] = filters["non_stop"]

        if filters.get("carrier"):
            params["includedAirlineCodes"] = filters["carrier"]

        if filters.get("max_duration"):
            # Converter duração máxima para minutos e aplicar no filtro
            max_duration = int(filters["max_duration"]) * 60
            params["maxFlightDuration"] = max_duration

        # Paradas (quantidade de escalas)
        if filters.get("stops"):
            stops = filters["stops"]
            if stops == "Non-stop":
                params["max"] = 0
            elif stops == "1 Stop":
                params["max"] = 1
            elif stops == "2+ Stops":
                params["max"] = 2

        # Escalas (aeroportos específicos)
        if filters.get("layover_airport"):
            params["viaAirlineCode"] = filters["layover_airport"]

        response = requests.get(f"{self.base_url}/v2/shopping/flight-offers", headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            return data.get("data", []), data.get("dictionaries", {})
        else:
            print(f"API Amadeus falhou: {e}")
            # Carregar voos de backup local
            with open("backup_flights.json", "r") as file:
                return json.load(file)

    def get_destinations(self):
        """Busca todas as cidades e aeroportos disponíveis no Amadeus API."""
        if not self.token:
            self.authenticate()

        url = f"{self.base_url}/v1/reference-data/locations"
        params = {
            "subType": "AIRPORT,CITY",
            "keyword": "A",
            "page[limit]": 100
        }
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            locations = response.json().get("data", [])

            unique_destinations = set()
            for loc in locations:
                if "iataCode" in loc and "name" in loc:
                    unique_destinations.add(f"{loc['iataCode']} - {loc['name']}")

            additional_destinations = ["LIS - Lisbon", "OPO - Porto", "FNC - Funchal"]
            unique_destinations.update(additional_destinations)

            return sorted(unique_destinations)

        except requests.exceptions.RequestException as e:
            print(f"API Amadeus falhou: {e}")
            # Carregar destinos de backup local
            with open("backup_destinations.json", "r") as file:
                return json.load(file)

        except KeyError as e:
            print(f"API Amadeus falhou: {e}")
            # Carregar destinos de backup local
            with open("backup_destinations.json", "r") as file:
                return json.load(file)

    def get_airlines(self):
        """Busca todas as companhias aéreas disponíveis."""
        if not self.token:
            self.authenticate()

        url = f"{self.base_url}/v1/reference-data/airlines"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return {
                airline['iataCode']: airline.get('commonName', airline.get('businessName', 'Unknown Airline'))
                for airline in data.get('data', [])
            }
        else:
            raise Exception(f"Failed to retrieve airlines: {response.text}")

    def hash_password(self, password):
        """Converte uma senha em hash SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_login(self, email, password):
        """Valida as credenciais de login do usuário."""
        try:
            with open("users.json", "r") as file:
                users = json.load(file)

            hashed_password = self.hash_password(password)
            return users.get(email) == hashed_password
        except FileNotFoundError:
            return False

    def register_user(self, email, password):
        """Registra um novo usuário no arquivo JSON."""
        try:
            # Tenta carregar os usuários existentes
            try:
                with open("users.json", "r") as file:
                    users = json.load(file)
            except FileNotFoundError:
                users = {}

            if email in users:
                return False  # Email já registrado

            # Salva o novo usuário
            hashed_password = self.hash_password(password)
            users[email] = hashed_password

            with open("users.json", "w") as file:
                json.dump(users, file, indent=4)

            return True
        except Exception as e:
            raise Exception(f"Failed to register user: {e}")










