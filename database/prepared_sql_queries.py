import sqlite3
from dotenv import load_dotenv


class Driver:
    """this class instanciates new drivers that will be added to the database"""

    def __init__(
        self, full_name, cpf, birth_date, address, phone, email, password, cnh
    ):
        self.full_name = full_name
        self.cpf = cpf
        self.birth_date = birth_date
        self.address = address
        self.phone = phone
        self.email = email
        self.password = password
        self.cnh = cnh

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

        """
        return repr


def create_table_drivers(connection: sqlite3.Connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS motoristas (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            full_name TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            birth_date TEXT NOT NULL,
            address TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            cnh_number TEXT UNIQUE NOT NULL
        );
        """
    )
    connection.commit()
    cursor.close()


def drop_table_drivers(connection: sqlite3.Connection):
    cursor = connection.cursor()

    cursor.execute("DROP TABLE drivers")

    connection.commit()
    cursor.close()


def create_table_vehicles(connection: sqlite3.Connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_proprietario INTEGER,
            crv TEXT NOT NULL,
            numero_do_chassi TEXT UNIQUE NOT NULL,
            ano_de_fabricacao INTEGER NOT NULL,
            modelo TEXT NOT NULL,
            cor TEXT NOT NULL,
            categoria_do_veiculo TEXT NOT NULL,
            FOREIGN KEY (id_proprietario) REFERENCES drivers(id)
        );
        """
    )
    connection.commit()
    cursor.close()


def register_new_driver(connection: sqlite3.Connection, driver: Driver):
    cursor = connection.cursor()

    # first check if the email is already being used
    users_with_same_email = cursor.execute(
        "SELECT COUNT(*) FROM motoristas WHERE email=?", [driver.email]
    ).fetchone()

    if users_with_same_email[0] == 0:
        print("Validas informações")
        cursor.execute(
            """
                INSERT INTO motoristas (
                    full_name, 
                    cpf,
                    birth_date,
                    address ,
                    phone_number,
                    email ,
                    password ,
                    cnh_number
                ) VALUES (?,?,?,?,?,?,?,?)
            """,
            [
                driver.full_name,
                driver.cpf,
                driver.birth_date,
                driver.address,
                driver.phone,
                driver.email,
                driver.password,
                driver.cnh,
            ],
        )

        connection.commit()
    else:
        print("Email já cadastrado")

    cursor.close()


def clear_table(connection: sqlite3.Connection, table_name: str):
    cursor = connection.cursor()

    # limpa a tabela inteira
    cursor.execute(
        f"""
        DELETE FROM {table_name}
        """
    )

    # Reindexa as linhas de forma crescente
    cursor.execute(
        f"""
        DELETE FROM sqlite_sequence WHERE name="{table_name}"
        """
    )

    connection.commit()

    cursor.close()
