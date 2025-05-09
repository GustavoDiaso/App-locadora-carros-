import sqlite3
from dotenv import dotenv_values
from pathlib import Path

env_variables = dotenv_values(Path(__file__).parent.parent / "database_info.env")

_connection: sqlite3.Connection | None = None


def set_connection(connection):
    global _connection
    _connection = connection


def _check_connection():
    if _connection is None:
        raise RuntimeError(
            """
            Nenhuma conexão com o banco de dados foi inicializada. 
            Conecte-se ao banco de dados antes de tentar executar qualquer query. 

            use db_service.set_connection()
            """
        )


def recreate_sqlite_database(path: str, database_name: str):
    full_path = Path(path) / f"{database_name}.sqlite3"
    try:
        with open(full_path, "w") as database:
            pass
    except Exception:
        raise Exception("Não foi possível criar o banco de dados.")


def create_table_drivers():
    _check_connection()

    global _connection
    cursor = _connection.cursor()
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
            cnh_number TEXT UNIQUE NOT NULL,
            permission_level TEXT NOT NULL
        );
        """
    )
    _connection.commit()
    cursor.close()


def drop_table_drivers():
    _check_connection()

    global _connection
    cursor = _connection.cursor()
    cursor.execute(f"DROP TABLE {env_variables['DRIVERS_TABLE_NAME']}")

    _connection.commit()
    cursor.close()


def drop_table_vehicles():
    _check_connection()

    global _connection
    cursor = _connection.cursor()
    cursor.execute(f"DROP TABLE {env_variables['VEHICLES_TABLE_NAME']}")

    _connection.commit()
    cursor.close()


def create_table_vehicles():
    _check_connection()

    global _connection
    cursor = _connection.cursor()
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {env_variables['VEHICLES_TABLE_NAME']} (
            vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_owner INTEGER,
            chassi_number TEXT UNIQUE NOT NULL,
            year_of_manufacture INTEGER NOT NULL,
            model TEXT NOT NULL,
            color TEXT NOT NULL,
            plate TEXT NOT NULL,
            car_return_location TEXT NOT NULL,
            rented BOOLEAN NOT NULL,
            FOREIGN KEY (id_owner) REFERENCES drivers(id)
        );
        """
    )
    _connection.commit()
    cursor.close()


def register_new_driver(driver) -> list[bool | str] | None:
    _check_connection()

    global _connection
    cursor = _connection.cursor()

    cursor = _connection.cursor()
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
                    email,
                    password,
                    cnh_number,
                    permission_level
                ) VALUES (?,?,?,?,?,?,?,?,?)
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
                driver.permission_level,
            ],
        )

        _connection.commit()

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


def clear_table(table_name: str):
    _check_connection()

    global _connection
    cursor = _connection.cursor()

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

    _connection.commit()

    cursor.close()


def driver_login(cpf, password):
    _check_connection()

    global _connection
    cursor = _connection.cursor()

    response = cursor.execute(
        f"""
        SELECT * FROM {env_variables['DRIVERS_TABLE_NAME']} WHERE cpf=? and password=? 
        """,
        [cpf, password],
    ).fetchone()

    _connection.commit()
    cursor.close()

    return response


def register_new_vehicle(vehicle):
    _check_connection()

    global _connection
    cursor = _connection.cursor()

    cursor.execute(
        f"""
        INSERT INTO {env_variables["VEHICLES_TABLE_NAME"]} (
            id_owner,
            chassi_number,
            year_of_manufacture,
            model,
            color,
            plate,
            car_return_location,
            rented 
        ) VALUES (?,?,?,?,?,?,?,?)
        """,
        [
            vehicle.id_owner,
            vehicle.chassi_number,
            vehicle.year_of_manufacture,
            vehicle.model,
            vehicle.color,
            vehicle.plate,
            vehicle.car_return_location,
            vehicle.rented,
        ],
    )

    _connection.commit()
    cursor.close()


def get_all_vehicles():
    _check_connection()

    global _connection
    cursor = _connection.cursor()

    vehicles = cursor.execute(
        f"""
        SELECT * FROM {env_variables["VEHICLES_TABLE_NAME"]} ORDER BY rented DESC
        """
    ).fetchall()

    _connection.commit()
    cursor.close()

    return vehicles


def get_available_vehicles():
    _check_connection()

    global _connection
    cursor = _connection.cursor()

    vehicles = cursor.execute(
        f"""
        SELECT * FROM {env_variables["VEHICLES_TABLE_NAME"]} WHERE rented = 0
        """
    ).fetchall()

    _connection.commit()
    cursor.close()

    return vehicles


def get_unavailable_vehicles():
    _check_connection()

    global _connection
    cursor = _connection.cursor()

    vehicles = cursor.execute(
        f"""
        SELECT * FROM {env_variables["VEHICLES_TABLE_NAME"]} WHERE rented = 1
        """
    ).fetchall()

    _connection.commit()
    cursor.close()

    return vehicles
