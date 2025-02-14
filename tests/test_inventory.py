import pytest
import os
from inventory import add_inventory, remove_inventory, get_inventory, export_inventory_pandas, inventory_statistics, check_inventory_threshold

from db import connect_db

@pytest.fixture
def setup_db():
    """ Skapar en testdatabas för inventory """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory")  # Rensar lagret innan test
    conn.commit()
    conn.close()


def test_add_inventory(setup_db: None):
    add_inventory("Äpplen", 10)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM inventory WHERE item = ?", ("Äpplen",))
    result = cursor.fetchone()
    conn.close()
    assert result is not None
    assert result[0] == 10


def test_remove_inventory(setup_db: None):
    add_inventory("Bananer", 20)
    remove_inventory("Bananer", 5)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM inventory WHERE item = ?", ("Bananer",))
    result = cursor.fetchone()
    conn.close()
    assert result is not None
    assert result[0] == 15


def test_export_inventory_pandas(setup_db: None):
    """Testa om export till Excel fungerar."""
    # Lägg till några testdata
    add_inventory("Råvara1", 100)
    add_inventory("Råvara2", 200)
    
    # Definiera filnamn
    filename = "test_inventory.xlsx"
    
    # Kör funktionen
    export_inventory_pandas(filename)
    
    # Kontrollera om filen har skapats
    assert os.path.exists(filename)
    
    # Rensa upp filen
    os.remove(filename)


def test_inventory_statistics(setup_db: None, capsys: pytest.CaptureFixture[str]):
    """Testa om lagerstatistik beräknas korrekt."""
    
    # Lägg till några testdata
    add_inventory("Råvara1", 100)
    add_inventory("Råvara2", 200)
    add_inventory("Råvara3", 300)
    
    # Kör lagerstatistik funktionen
    inventory_statistics()

    # Fånga utdata
    captured = capsys.readouterr()

    # Kontrollera om genomsnittlig mängd och total mängd finns i utskriften
    assert "Genomsnittlig mängd" in captured.out
    assert "Total mängd" in captured.out
    assert "Högsta lagermängd" in captured.out
    assert "Lägsta lagermängd" in captured.out


def test_inventory_statistics_empty(capsys: pytest.CaptureFixture[str]):
    """Testa statistik för tomt lager."""
    # Rensa alla varor från lagret
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory")
    conn.commit()
    conn.close()

    # Kör lagerstatistik funktionen
    inventory_statistics()

    # Fånga utdata
    captured = capsys.readouterr()

    # Kontrollera om det finns ett meddelande om att lagret är tomt
    assert "Lagerstatistik kan inte beräknas eftersom lagret är tomt." in captured.out

    def test_check_inventory_threshold(setup_db: None, capsys: pytest.CaptureFixture[str]):
        """Testa att påminnelser om låga lager fungerar som förväntat."""
    add_inventory("Råvara1", 10)
    add_inventory("Råvara2", 4)  # Denna råvara kommer att vara under tröskelnivån
    
    # Kör kontrollen av lagerstatus
    check_inventory_threshold(threshold=5)

    # Fånga utdata
    captured = capsys.readouterr()

    # Kontrollera om den låga lagernivån har påmints
    assert "Råvara2" in captured.out
    assert "Följande råvaror är på väg att ta slut!" in captured.out


