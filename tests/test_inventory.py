import pytest
from inventory import add_inventory, remove_inventory, get_inventory
from db import connect_db

@pytest.fixture
def setup_db():
    """ Skapar en testdatabas för inventory """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory")  # Rensar lagret innan test
    conn.commit()
    conn.close()

def test_add_inventory(setup_db):
    add_inventory("Äpplen", 10)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM inventory WHERE item = ?", ("Äpplen",))
    result = cursor.fetchone()
    conn.close()
    assert result is not None
    assert result[0] == 10

def test_remove_inventory(setup_db):
    add_inventory("Bananer", 20)
    remove_inventory("Bananer", 5)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM inventory WHERE item = ?", ("Bananer",))
    result = cursor.fetchone()
    conn.close()
    assert result is not None
    assert result[0] == 15
