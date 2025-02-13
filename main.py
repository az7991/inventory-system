from db import create_tables
from auth import login, create_user, delete_user, get_all_users, decode_jwt
from inventory import add_inventory, remove_inventory, get_inventory
import getpass

def show_all_users():
    """Visa alla användare i systemet."""
    print("\n📜 **Alla användare:**")
    users = get_all_users()
    if users:
        for user in users:
            print(f"- {user[0]}")
    else:
        print("Inga användare finns i systemet.")

def can_delete_user():
    """Kontrollerar om det finns fler än bara admin i systemet."""
    users = get_all_users()
    return len(users) > 1

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
            
            if role == "admin":
                while True:
                    print("\n📌 **Admin meny:**")
                    print("1. Skapa användare")
                    
                    
                    if can_delete_user():
                        print("2. Ta bort användare")
                    
                    print("3. Visa alla användare") 
                    print("4. Lägg till råvara")
                    print("5. Ta bort råvara")
                    print("6. Visa lagerstatus (endast kg)")
                    print("7. Avsluta")
                    choice = input("Val: ")
                    
                    if choice == "1":
                        new_username = input("Nytt användarnamn: ")
                        new_password = getpass.getpass("Lösenord: ")
                        create_user(new_username, new_password, "staff")
                    elif choice == "2" and can_delete_user():
                        del_username = input("Användarnamn att ta bort: ")
                        delete_user(del_username)
                    elif choice == "3":
                        show_all_users() 
                    elif choice == "4":
                        item = input("Namn på råvara: ")
                        quantity = int(input("Mängd i kg: "))
                        add_inventory(item, quantity)
                    elif choice == "5":
                        item = input("Namn på råvara: ")
                        quantity = int(input("Mängd i kg att ta bort: "))
                        remove_inventory(item, quantity)
                    elif choice == "6":
                        get_inventory()
                    elif choice == "7":
                        break
            
            elif role == "staff":
                while True:
                    print("\n📌 **Staff meny:**")
                    print("1. Ta ut råvara")
                    print("2. Visa lagerstatus (endast kg)")
                    print("3. Avsluta")
                    choice = input("Val: ")

                    if choice == "1":
                        item = input("Namn på råvara: ")
                        quantity = int(input("Mängd i kg att ta ut: "))
                        remove_inventory(item, quantity)
                    elif choice == "2":
                        get_inventory()
                    elif choice == "3":
                        break
        else:
            print("Ogiltig token eller token har gått ut.")
    else:
        print("Felaktigt användarnamn eller lösenord.")

if __name__ == "__main__":
    main()








