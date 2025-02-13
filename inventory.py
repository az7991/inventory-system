from db import connect_db
import csv
import json

def add_inventory(item, quantity):
    """Lägg till en råvara i lagret. Om den redan finns, uppdatera kvantiteten."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO inventory (item, quantity) VALUES (?, ?) ON CONFLICT(item) DO UPDATE SET quantity = quantity + ?", 
                       (item, quantity, quantity))
        conn.commit()
        print(f"Råvara {item} med mängd {quantity} kg har lagts till.")
    except Exception as e:
        print(f"Ett fel uppstod: {e}")
    finally:
        conn.close()

def remove_inventory(item, quantity):
    """Ta bort en råvara från lagret. Om kvantiteten blir negativ, sätt den till 0."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT quantity FROM inventory WHERE item = ?", (item,))
        current_quantity = cursor.fetchone()

        if current_quantity:
            new_quantity = current_quantity[0] - quantity
            if new_quantity < 0:
                new_quantity = 0
            cursor.execute("UPDATE inventory SET quantity = ? WHERE item = ?", (new_quantity, item))
            conn.commit()
            print(f"Råvara {item} har tagits bort. Ny mängd: {new_quantity} kg.")
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
        
def export_inventory_csv(filename="inventory.csv"):
    """Exportera lagret till en CSV-fil."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT item, quantity FROM inventory")
    items = cursor.fetchall()
    conn.close()

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Item", "Quantity"])
        writer.writerows(items)
    print(f"Lagerdata exporterad till {filename}")

def import_inventory_csv(filename="inventory.csv"):
    """Importera lagerdata från en CSV-fil."""
    conn = connect_db()
    cursor = conn.cursor()
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cursor.execute("INSERT INTO inventory (item, quantity) VALUES (?, ?) ON CONFLICT(item) DO UPDATE SET quantity = quantity + ?", (row[0], int(row[1]), int(row[1])))
    conn.commit()
    conn.close()
    print(f"Lagerdata importerad från {filename}")

def export_inventory_json(filename="inventory.json"):
    """Exportera lagret till en JSON-fil."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT item, quantity FROM inventory")
    items = cursor.fetchall()
    conn.close()
    data = {item: quantity for item, quantity in items}
    with open(filename, "w") as file:
        json.dump(data, file)
    print(f"Lagerdata exporterad till {filename}")

def import_inventory_json(filename="inventory.json"):
    """Importera lagerdata från en JSON-fil."""
    conn = connect_db()
    cursor = conn.cursor()
    with open(filename, "r") as file:
        data = json.load(file)
        for item, quantity in data.items():
            cursor.execute("INSERT INTO inventory (item, quantity) VALUES (?, ?) ON CONFLICT(item) DO UPDATE SET quantity = quantity + ?", (item, quantity, quantity))
    conn.commit()
    conn.close()
    print(f"Lagerdata importerad från {filename}")





