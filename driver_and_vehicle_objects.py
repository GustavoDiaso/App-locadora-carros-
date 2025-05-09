import random
import string
import uuid


class Driver:
    """This class represents the driver that will be registered in the database or logged in the app"""

    def __init__(
        self,
        full_name,
        cpf,
        birth_date,
        address,
        phone,
        email,
        password,
        cnh,
        permission_level="user",
    ):
        self.full_name = full_name
        self.cpf = cpf
        self.birth_date = birth_date
        self.address = address
        self.phone = phone
        self.email = email
        self.password = password
        self.cnh = cnh
        self.permission_level = permission_level

    def __repr__(self):
        repr = f"""
        Nome: {self.full_name}
        CPF: {self.cpf}
        BIRTH DATE: {self.birth_date}
        ADDRESS: {self.address}
        PHONE: {self.phone}
        EMAIL: {self.email}
        PASSWORD: {self.password}
        CNH: {self.cnh}
        PERMISSION LEVEL {self.permission_level}
        """
        return repr


class Vehicle:
    def __init__(
        self,
        id_owner,
        chassi_number,
        year_of_manufacture,
        model,
        color,
        plate,
        car_return_location,
        rented,
    ):
        self.id_owner = id_owner
        self.chassi_number = chassi_number
        self.year_of_manufacture = year_of_manufacture
        self.model = model
        self.color = color
        self.plate = plate
        self.car_return_location = car_return_location
        self.rented = rented


# Função para gerar um número de chassi aleatório (simplificado)
def gerar_chassi_aleatorio(length=17):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


# Função para gerar uma placa aleatória no formato Mercosul (LLLNLNN) ou antigo (LLLNNNN)
def gerar_placa_aleatoria():
    if random.choice([True, False]):  # Formato Mercosul (aproximado)
        letras1 = "".join(random.choices(string.ascii_uppercase, k=3))
        numero1 = random.randint(0, 9)
        letra2 = random.choice(string.ascii_uppercase)
        numeros2 = "".join(random.choices(string.digits, k=2))
        return f"{letras1}{numero1}{letra2}{numeros2}"
    else:  # Formato antigo
        letras = "".join(random.choices(string.ascii_uppercase, k=3))
        numeros = "".join(random.choices(string.digits, k=4))
        return f"{letras}{numeros}"


my_vehicle_collection = []

random_models = [
    "Onix",
    "HB20",
    "Kwid",
    "Mobi",
    "Gol",
    "Argo",
    "Strada",
    "Toro",
    "Compass",
    "Renegade",
    "Creta",
    "Tracker",
    "Corolla",
    "Civic",
    "Hilux",
]

colors_exemple = [
    "Preto",
    "Branco",
    "Prata",
    "Cinza",
    "Vermelho",
    "Azul",
    "Verde",
    "Amarelo",
]

devolution_locations = [
    "Aeroporto GIG",
    "Aeroporto SDU",
    "Centro RJ",
    "Barra da Tijuca",
    "Copacabana",
    "Aeroporto GRU",
    "Centro SP",
    "Paulista",
    "Aeroporto CNF",
    "Centro BH",
]

number_of_vehicles = 35  # Criando X carros diferentes

current_year = 2025  # Considerando o ano atual para o limite superior de fabricação

for i in range(number_of_vehicles):
    id_owner = random.randint(1000, 9999)  # ID do proprietário aleatório
    chassi_number = gerar_chassi_aleatorio()
    year_of_manufacture = random.randint(
        1990, current_year
    )  # Ano entre 1990 e o ano atual
    model = random.choice(random_models)
    color = random.choice(colors_exemple)
    plate = gerar_placa_aleatoria()
    car_return_location = random.choice(devolution_locations)
    rented = random.choice([0, 1])

    novo_veiculo = Vehicle(
        id_owner=id_owner,
        chassi_number=chassi_number,
        year_of_manufacture=year_of_manufacture,
        model=model,
        color=color,
        plate=plate,
        car_return_location=car_return_location,
        rented=rented,
    )
    my_vehicle_collection.append(novo_veiculo)
