import sqlite3
from dotenv import load_dotenv, dotenv_values
from pathlib import Path

env_variables = dotenv_values(Path(__file__).parent / "database_info.env")


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
        f"""
        CREATE TABLE IF NOT EXISTS {env_variables['DRIVERS_TABLE_NAME']} (
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

    cursor.execute(f"DROP TABLE {env_variables['DRIVERS_TABLE_NAME']}")

    connection.commit()
    cursor.close()


def drop_table_vehicles(connection: sqlite3.Connection):
    cursor = connection.cursor()

    cursor.execute(f"DROP TABLE {env_variables['VEHICLES_TABLE_NAME']}")

    connection.commit()
    cursor.close()


def create_table_vehicles(connection: sqlite3.Connection):
    cursor = connection.cursor()
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {env_variables['VEHICLES_TABLE_NAME']} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_owner INTEGER,
            crv TEXT NOT NULL,
            chassi_number TEXT UNIQUE NOT NULL,
            year of manufacture INTEGER NOT NULL,
            model TEXT NOT NULL,
            color TEXT NOT NULL,
            vehicle_category TEXT NOT NULL,
            plate TEXT NOT NULL,
            FOREIGN KEY (id_owner) REFERENCES drivers(id)
        );
        """
    )
    connection.commit()
    cursor.close()


def register_new_driver(
    connection: sqlite3.Connection, driver: Driver
) -> list[bool | str] | None:

    cursor = connection.cursor()
    # cheque se o email do motorista já está em uso
    users_with_same_email = cursor.execute(
        f"SELECT COUNT(*) FROM {env_variables['DRIVERS_TABLE_NAME']} WHERE email=?",
        [driver.email],
    ).fetchone()

    # cheque se o cpf do motorista já está em uso:
    users_with_same_cpf = cursor.execute(
        f"SELECT COUNT(*) FROM {env_variables['DRIVERS_TABLE_NAME']} WHERE cpf=?",
        [driver.cpf],
    ).fetchone()

    # cheque se a cnh do motorista já está em uso:
    users_with_same_cnh = cursor.execute(
        f"SELECT COUNT(*) FROM {env_variables['DRIVERS_TABLE_NAME']} WHERE cnh_number=?",
        [driver.cnh],
    ).fetchone()

    conditions = [
        users_with_same_email[0] == 0,
        users_with_same_cpf[0] == 0,
        users_with_same_cnh[0] == 0,
    ]

    if all(conditions):
        cursor.execute(
            f"""
                INSERT INTO {env_variables['DRIVERS_TABLE_NAME']} (
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

        register_confirmation = cursor.execute(
            f"""
            SELECT COUNT(*) FROM {env_variables['DRIVERS_TABLE_NAME']} 
            WHERE cpf = ? and cnh_number = ?""",
            [driver.cpf, driver.cnh],
        ).fetchone()

        cursor.close()

        return (
            [True, "Motorista cadastrado com sucesso."]
            if register_confirmation[0] == 1
            else [False, "Algo deu errado"]
        )

    else:
        cursor.close()

        for condition, evaluation in enumerate(conditions):
            if evaluation is False:
                match condition:
                    case 0:
                        return [False, "Esse endereço de email já está em uso"]
                    case 1:
                        return [False, "CPF já cadastrado"]
                    case 2:
                        return [False, "CNH já cadastrada"]


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
