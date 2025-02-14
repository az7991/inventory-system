# Inloggning till admin
- **Användarnamn**: `admin`
- **Lösenord**: `admin123`

# Inventariesystem - Projektbeskrivning

Detta projekt är ett **inventariesystem** som hanterar lager och användare inom en organisation.  
Systemet skiljer mellan två roller:  
- **Admin** (administratör) – full åtkomst till alla funktioner  
- **Staff** (anställd) – begränsad åtkomst till lagerhantering  

## 📌 Syfte

Syftet med detta projekt är att implementera ett system för att hantera användare och lager där funktioner som användarhantering, lagerhantering och säkerhet via autentisering och kryptering är centrala.  

Projektet är designat för att kunna växa och anpassas efter framtida behov och krav.

## 🔹 Huvudfunktioner:

### ✅ **Användarhantering**
- Skapa nya användare  
- Ta bort användare  
- Visa alla användare  

### 📦 **Lagerhantering**
- Lägg till råvaror i lagret  
- Ta bort råvaror från lagret  
- Visa lagerstatus (enbart i kg)
- Se lagerstatistik

### 🔒 **Autentisering och säkerhet**
- Lösenordshantering med **bcrypt** för att säkerställa att lösenord lagras på ett säkert sätt  
- Kryptering och dekryptering av lösenord med **Fernet** för att skydda användarlösenord  
- Användning av **JWT (JSON Web Tokens)** för autentisering och säkerhet  

---

## ⚙️ Installation

Följ dessa steg för att köra systemet lokalt:

- Installera Sqlite3 i Python
- pip install -r requirements.txt

# Starta applikationen
- python3 main.py

# Kör tester
- pytest

## 📌 Förutsättningar

För att kunna köra projektet behöver du:

- Python 3.x installerat
- Alla nödvändiga Python-bibliotek (anges i requirements.txt)

📌 Repo: inventory-system
💬 Kontakt: Öppna en issue eller kontakta mig via GitHub.


1. **Kloning av repository**  
   ```bash
   git clone https://github.com/az7991/inventory-system
   cd inventory-system

