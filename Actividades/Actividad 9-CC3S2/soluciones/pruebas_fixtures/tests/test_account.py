import json
import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models import db
from models.account import Account

ACCOUNT_DATA = {}


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Configura la base de datos antes y después de todas las pruebas"""
    # Se ejecuta antes de todas las pruebas
    db.create_all()
    yield
    # Se ejecuta después de todas las pruebas
    db.session.close()


class TestAccountModel:
    """Modelo de Pruebas de Cuenta"""

    @classmethod
    def setup_class(cls):
        """Conectar y cargar los datos necesarios para las pruebas"""
        global ACCOUNT_DATA
        with open("tests/fixtures/account_data.json") as json_data:
            ACCOUNT_DATA = json.load(json_data)
        print(f"ACCOUNT_DATA cargado: {ACCOUNT_DATA}")

    @classmethod
    def teardown_class(cls):
        """Desconectar de la base de datos"""
        pass  # Agrega cualquier acción de limpieza si es necesario

    def setup_method(self):
        """Truncar las tablas antes de cada prueba"""
        db.session.query(Account).delete()
        db.session.commit()

    def teardown_method(self):
        """Eliminar la sesión después de cada prueba"""
        db.session.remove()

    #  Casos de prueba
    def test_account_representation(self):
        """Probar la representación del nombre de una cuenta"""
        data = ACCOUNT_DATA[0]
        account = Account(**data)
        account.create()
        assert str(account) == f"<Account '{data['name']}'>"

    def test_serialization_to_dict(self):
        data = ACCOUNT_DATA[0]
        account = Account(**data)
        account.create()
        account_dict = account.to_dict()
        assert all(
            [
                key in account_dict and data[key] == account_dict[key]
                for key in data.keys()
            ]
        )

    def test_assignment_from_dict(self):
        data = ACCOUNT_DATA[0]
        account = Account(**data)
        account.create()
        new_data = {
            "name": "Amber Torres",
            "email": "reedjoann@example.org",
            "phone_number": "121.566.9078",
            "disabled": True,
        }
        account.from_dict(new_data)
        account_dict = account.to_dict()
        assert all(
            [
                key in account_dict and new_data[key] == account_dict[key]
                for key in new_data.keys()
            ]
        )

    def test_create_an_account(self):
        """Probar la creación de una sola cuenta"""
        data = ACCOUNT_DATA[0]  # obtener la primera cuenta
        account = Account(**data)
        account.create()
        assert len(Account.all()) == 1

    def test_create_all_accounts(self):
        """Probar la creación de múltiples cuentas"""
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        assert len(Account.all()) == len(ACCOUNT_DATA)

    def test_update_an_account(self):
        data = ACCOUNT_DATA[0]
        account = Account(**data)
        account.create()
        account.id = 2
        account.update()
        assert account.to_dict()["id"] == 2

    def test_update_an_account_without_id(self):
        data = ACCOUNT_DATA[0]
        account = Account(**data)
        account.create()
        account.id = None
        with pytest.raises(Exception, match="Se llamó a update sin un ID"):
            account.update()

    def test_find_account(self):
        accounts = []
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
            accounts.append(account)

        account_found = Account.find(1)
        assert accounts[0].id == account_found.id

    def test_delete_account(self):
        data = ACCOUNT_DATA[0]  # obtener la primera cuenta
        account = Account(**data)
        account.create()
        account.delete()
        assert len(Account.all()) == 0
