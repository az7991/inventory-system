# Inloggning till admin
- användarnamnet: admin
- lösenord: admin123


# Inventariesystem - Projektbeskrivning

Detta projekt är ett **inventariesystem** som hanterar lager och användare inom en organisation. Systemet skiljer mellan två roller: **admin** (administratör) och **staff** (anställd), där administratörer har full åtkomst till alla funktioner och anställda har begränsad åtkomst till lagerhantering.

## Syfte

Syftet med detta projekt är att implementera ett system för att hantera användare och lager där funktioner som användarhantering, lagerhantering, och säkerhet via autentisering och kryptering är centrala. 

Projektet är designat för att kunna växa och anpassas efter framtida behov och krav.

### Huvudfunktioner:

- **Användarhantering**:
  - Skapa nya användare
  - Ta bort användare
  - Visa alla användare
- **Lagerhantering**:
  - Lägg till råvaror i lagret
  - Ta bort råvaror från lagret
  - Visa lagerstatus (enbart i kg)
- **Autentisering och säkerhet**:
  - Lösenordshantering med **bcrypt** för att säkerställa att lösenord lagras på ett säkert sätt
  - Kryptering och dekryptering av lösenord med **Fernet** för att skydda användarlösenord
  - Användning av **JWT (JSON Web Tokens)** för autentisering och säkerhet

## Installation

För att köra systemet lokalt, följ dessa steg:
- pip install -r requirements.txt
- python main.py
- pytest


### Förutsättningar
För att kunna köra projektet behöver du ha Python 3.x installerat. Se till att även installera de nödvändiga Python-biblioteken.

### 1. Klona repositoryt
Klona detta repository till din lokala dator:
```bash
git clone <repository-url>
cd <repository-folder>

