from db import create_tables, connect_db
from auth import login, create_user, delete_user, get_all_users, decode_jwt
from inventory import add_inventory, remove_inventory, get_inventory, export_inventory_pandas, inventory_statistics
import getpass

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

def admin_menu():
    while True:
        print("\n📌 **Admin meny:**")
        print("1. Lista alla användare")
        print("2. Skapa användare")
        print("3. Ta bort användare")
        print("4. Lägg till råvara i lager")
        print("5. Ta bort råvara från lager")
        print("6. Exportera lager")
        print("7. Se lagerstatistik")
        print("8. Se lagerstatus")
        print("9. Logga ut")
        
        val = input("Val: ")
        
        if val == "1":
            # Lista alla användare
            users = get_all_users()
            if users:
                print("\n**Användare:**")
                for user in users:
                    print(f"- {user[0]}")
            else:
                print("Inga användare finns.")
        
        elif val == "2":
            # Skapa användare
            username = input("Ange användarnamn: ")
            password = getpass.getpass("Ange lösenord: ")
            role = input("Ange roll (admin/staff): ").lower()
            create_user(username, password, role)
        
        elif val == "3":
            # Ta bort användare
            username_to_delete = input("Ange användarnamn att ta bort: ")
            delete_user(username_to_delete)
        
        elif val == "4":
            # Lägg till råvara i lager
            item = input("Namn på råvara: ")
            quantity = int(input("Mängd i kg att lägga till: "))
            add_inventory(item, quantity)
        
        elif val == "5":
            # Ta bort råvara från lager
            item_to_remove = input("Ange råvarans namn att ta bort: ")
            quantity_to_remove = int(input("Ange mängd att ta bort: "))
            remove_inventory(item_to_remove, quantity_to_remove)
        
        elif val == "6":
            # Exportera lager
            filename = input("Ange filnamn för export (t.ex. inventory.xlsx): ")
            export_inventory_pandas(filename)
        
        elif val == "7":
            # Se lagerstatistik
            inventory_statistics()
        
        elif val == "8":
            # Se lagerstatus
            get_inventory()
        
        elif val == "9":
            print("Loggar ut...")
            break
        else:
            print("Ogiltigt val. Försök igen.")

def staff_menu():
    while True:
        print("\n📌 **Staff meny:**")
        print("1. Ta ut råvara från lager")
        print("2. Se lagerstatus")
        print("3. Logga ut")
        
        choice = input("Val: ")
        
        if choice == "1":
            item = input("Namn på råvara: ")
            quantity = int(input("Mängd i kg att ta ut: "))
            remove_inventory(item, quantity)  # Du måste ha denna funktion definierad någonstans
            check_inventory_threshold()  # Och denna också
        elif choice == "2":
            get_inventory()  # Och denna, för att visa lagerstatus
        elif choice == "3":
            print("🔓 Loggar ut...")
            break
        else:
            print("❌ Ogiltigt val, försök igen!")


def main():
    create_tables()
    print("Välkommen till inventariesystemet!")
    
    username = input("Användarnamn: ")
    password = getpass.getpass("Lösenord: ")
    token = login(username, password)
    
    if token:
        decoded_data = decode_jwt(token)
        if decoded_data:
            role = decoded_data['role']
            check_inventory_threshold()
            if role == "admin":
                admin_menu()
            elif role == "staff":
                staff_menu()
        else:
            print("Ogiltig token eller token har gått ut.")
    else:
        print("Felaktigt användarnamn eller lösenord.")

if __name__ == "__main__":
    main()










