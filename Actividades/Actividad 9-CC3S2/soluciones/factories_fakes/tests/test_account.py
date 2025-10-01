"""
Casos de prueba TestAccountModel
"""

import os
import sys

import pytest

# Agrega el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from factories import AccountFactory
from models import db
from models.account import Account, DataValidationError


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Configura la base de datos antes de las pruebas"""
    db.create_all()
    yield
    db.session.close()


@pytest.fixture(autouse=True)
def clean_tables():
    """Trunca las tablas antes de cada prueba"""
    db.session.query(Account).delete()
    db.session.commit()
    yield
    db.session.remove()


class TestAccountModel:
    """Pruebas para el Modelo Account"""

    def test_account_representation(self):
        """Probar la representación del nombre de una cuenta"""
        account = AccountFactory(name="Foo")
        assert str(account) == "<Account 'Foo'>"

    def test_serialization_to_dict(self):
        account = AccountFactory()
        account_dict = account.to_dict()
        assert account.name == account_dict["name"]
        assert account.email == account_dict["email"]
        assert account.phone_number == account_dict["phone_number"]
        assert account.disabled == account_dict["disabled"]
        assert account.date_joined == account_dict["date_joined"]

    def test_assignment_from_dict(self):
        data = AccountFactory().to_dict()
        account = Account()
        account.from_dict(data)
        assert account.name == data["name"]
        assert account.email == data["email"]
        assert account.phone_number == data["phone_number"]
        assert account.disabled == data["disabled"]

    def test_create_an_account(self):
        """Prueba la creación de una Cuenta usando datos conocidos"""
        account = AccountFactory()
        account.create()
        assert len(Account.all()) == 1

    def test_create_all_accounts(self):
        """Prueba la creación de múltiples Cuentas"""
        for _ in range(10):
            account = AccountFactory()
            account.create()
        assert len(Account.all()) == 10

    def test_update_an_account(self):
        """Prueba la actualización de una Cuenta usando datos conocidos"""
        account = AccountFactory()
        account.create()
        assert account.id is not None
        account.name = "Nuevo Nombre"
        account.update()
        found = Account.find(account.id)
        assert found.name == account.name

    def test_update_an_account_without_id(self):
        """Prueba la actualización con un ID inválido"""
        account = AccountFactory()
        account.id = None
        with pytest.raises(DataValidationError, match="Actualización llamada con campo ID vacío"):
            account.update()
    
    def test_find_account(self):
        account_1 = AccountFactory()
        account_1.create()
        account_2 = AccountFactory()
        account_2.create()
        account_3 = AccountFactory()
        account_3.create()
        
        account_1_id = account_1.id
        account_2_id = account_2.id
        account_3_id = account_3.id

        assert Account.find(account_1_id).id == account_1.id
        assert Account.find(account_2_id).id == account_2.id
        assert Account.find(account_3_id).id == account_3.id

    def test_delete_account(self):
        """Prueba la eliminación de una Cuenta usando datos conocidos"""
        account = AccountFactory()
        account.create()
        assert len(Account.all()) == 1
        account.delete()
        assert len(Account.all()) == 0
