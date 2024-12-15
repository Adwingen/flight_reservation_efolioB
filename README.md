# flight_reservation_efolioB
Python

Flight Booking System
Descrição do Projeto
Este sistema de reservas de voos é uma aplicação interativa desenvolvida em Python com a biblioteca Tkinter para interface gráfica. Ele permite que os utilizadores pesquisem voos, selecionem assentos, calculem a pegada de carbono e visualizem o histórico de consultas.

Além disso, a aplicação conta com funcionalidades de login e registo de utilizadores, garantindo personalização e histórico individual.

Funcionalidades Principais

Login e Registo:
Permite que utilizadores novos se registem.
Validação de e-mail e armazenamento seguro de senhas (hash).

Pesquisa de Voos:
Procura voos com base em origem, destino, datas e número de passageiros.
Inclui filtros avançados (preço, duração, etc.).

Exibição de Rotas:
Integração com mapas (Google Maps ou OpenStreetMap) para mostrar trajetos.

Cálculo de Pegada de Carbono:
Estima as emissões de CO₂ baseadas nos detalhes da viagem.

Seleção de Assentos:
Interface interativa para escolha dos assentos no avião.

Histórico de Utilizadores:
Armazena e exibe pesquisas e reservas feitas pelo utilizador.

Tecnologias Utilizadas
Python 3.12
Tkinter (Interface Gráfica)
JSON (Armazenamento local de dados de utilizadores e histórico)
Requests (Integração com APIs externas como Amadeus e mapas)
Hashlib (Armazenamento seguro de senhas)
Estrutura do Projeto
plaintext
Copiar código
Flight Booking System/
│
├── controller/
│   └── app_controller.py       # Controlador principal da aplicação
│
├── model/
│   └── flight_model.py         # Lógica de pesquisa de voos e integração com APIs
│
├── view/
│   ├── flight_view.py          # Interface principal para pesquisa de voos
│   ├── passenger_info_view.py  # Interface para informações dos passageiros
│   ├── seat_selection.py       # Interface para seleção de assentos
│   ├── login_register_view.py  # Interface de login e registo
│   └── historic_view.py        # Interface do histórico de utilizadores
│
├── data/
│   ├── users.json              # Armazena dados de utilizadores
│   ├── history.json            # Armazena histórico de pesquisas/reservas
│   └── flights_backup.json     # Dados de backup de voos
│
├── main.py                     # Arquivo principal para execução
├── settings.py                 # Configurações globais (cores, API keys, etc.)
└── README.md                   # Documentação do projeto
Instalação
Clone o repositório:

bash
Copiar código
git clone https://github.com/seu-usuario/flight-booking-system.git
Instale as dependências:

bash
Copiar código
pip install -r requirements.txt
Configure as credenciais da API:

Edite o arquivo settings.py e insira suas credenciais de API (Amadeus e mapas).
Execute o projeto:

bash
Copiar código
python main.py
Configurações do Projeto
O arquivo settings.py centraliza todas as configurações globais, incluindo:

Cores da interface
Chaves de API
Parâmetros padrão para pesquisas
Exemplo:

python
Copiar código
# settings.py
BACKGROUND_COLOR = "#1F2833"
WIDGET_COLOR = "#C5C6C7"
BUTTON_COLOR = "#66FCF1"

API_KEY = "sua_api_key_aqui"
API_SECRET = "seu_api_secret_aqui"
Contribuição
Contribuições são bem-vindas! Siga estes passos:

Faça um fork do repositório.
Crie uma branch com sua funcionalidade: git checkout -b minha-funcionalidade.
Faça o commit das suas alterações: git commit -m "Descrição da funcionalidade".
Faça o push para a branch: git push origin minha-funcionalidade.
Abra um Pull Request.

Contato
Nome: Carlos Miguel Romão
E-mail: carlosmiguelromao@gmail.com
LinkedIn: https://github.com/Adwingen?tab=repositories


