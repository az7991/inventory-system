import sqlite3
from db import connect_db
import csv
import json
import pandas as pd
import numpy as np

def check_inventory_threshold(threshold=5):
    """Kontrollera lagerstatus och påminn om nivån är under tröskelvärdet."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT item, quantity FROM inventory")
    items = cursor.fetchall()
    conn.close()

    low_stock_items = [item for item, quantity in items if quantity <= threshold]
    
    if low_stock_items:
        print("\n⚠️ **Varning: Följande råvaror är på väg att ta slut!**")
        for item in low_stock_items:
            print(f"- {item}")
    else:
        print("Alla råvaror har tillräcklig mängd.")

import pandas as pd
from db import connect_db

def export_inventory_pandas(filename):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT item, quantity FROM inventory")
        items = cursor.fetchall()
        conn.close()

        if items:
            # Se till att antalet kolumner stämmer: 2 kolumner -> 2 rubriker
            df = pd.DataFrame(items, columns=["Item", "Quantity"])
            df.to_excel(filename, index=False)
            print(f"🔄 Exporterar lager till {filename}...")
        else:
            print("Inga råvaror att exportera.")
    except Exception as e:
        print(f"❌ Ett fel uppstod vid exporten: {e}")


def inventory_statistics():
    """Beräkna statistik för lagret med NumPy."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT quantity FROM inventory")
        quantities = [row[0] for row in cursor.fetchall()]
        conn.close()

        if quantities:
            avg_quantity = np.mean(quantities)
            total_quantity = np.sum(quantities)
            max_quantity = np.max(quantities)
            min_quantity = np.min(quantities)

            print("\n📊 **Lagerstatistik:**")
            print(f"- Genomsnittlig mängd: {avg_quantity:.2f} kg")
            print(f"- Total mängd: {total_quantity} kg")
            print(f"- Högsta lagermängd: {max_quantity} kg")
            print(f"- Lägsta lagermängd: {min_quantity} kg")
        else:
            print("Lagerstatistik kan inte beräknas eftersom lagret är tomt.")
    except Exception as e:
        print(f"Ett fel uppstod vid beräkning av statistik: {e}")


def add_inventory(item, quantity):
    """Lägg till en råvara i lagret. Om den redan finns, uppdatera kvantiteten."""
    print(f"🛠️ Lägger till {quantity} kg av {item} i lagret...")
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO inventory (item, quantity) VALUES (?, ?) ON CONFLICT(item) DO UPDATE SET quantity = quantity + ?", 
                    (item, quantity, quantity))
        conn.commit()
        print(f"✅ Råvara {item} med mängd {quantity} kg har lagts till.")
    except Exception as e:
        print(f"❌ Ett fel uppstod: {e}")
    finally:
        conn.close()

def remove_inventory(item, quantity):
    """Ta bort en råvara från lagret. Om kvantiteten blir 0, ta bort den helt."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT quantity FROM inventory WHERE item = ?", (item,))
        current_quantity = cursor.fetchone()

        if current_quantity:
            new_quantity = current_quantity[0] - quantity
            if new_quantity <= 0:
                cursor.execute("DELETE FROM inventory WHERE item = ?", (item,))
                print(f"Råvara {item} har tagits bort från lagret helt.")
            else:
                cursor.execute("UPDATE inventory SET quantity = ? WHERE item = ?", (new_quantity, item))
                print(f"Råvara {item} har uppdaterats. Ny mängd: {new_quantity} kg.")

            conn.commit()
        else:
            print(f"Ingen råvara med namn {item} hittades.")
    except Exception as e:
        print(f"Ett fel uppstod: {e}")
    finally:
        conn.close()


def get_inventory():
    """Hämta lagerstatus för alla råvaror."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT item, quantity FROM inventory")
    items = cursor.fetchall()
    conn.close()

    if items:
        print("\n📦 **Lagerstatus:**")
        for item, quantity in items:
            print(f"- {item}: {quantity} kg")
    else:
        print("Inget lager finns.")










