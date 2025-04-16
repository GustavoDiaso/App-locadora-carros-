class Driver:
    """ This class represents the driver that will be registered in the database or logged in the app"""
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