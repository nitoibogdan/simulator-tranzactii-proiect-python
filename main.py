import json
import os

FISIER_DATE = 'conturi.json'



def incarca_date():

    if not os.path.exists(FISIER_DATE):
        date_initiale = {
            "RO123": {"sold": 1000.0, "istoric": []},
            "RO456": {"sold": 500.0, "istoric": []}
        }
        salveaza_date(date_initiale)
        return date_initiale
    with open(FISIER_DATE, 'r') as f:
        return json.load(f)


def salveaza_date(date):
    with open(FISIER_DATE, 'w') as f:
        json.dump(date, f, indent=4)


def depunere(id_cont, suma):
    date = incarca_date()
    if id_cont in date and suma > 0:
        date[id_cont]['sold'] += suma
        date[id_cont]['istoric'].append({"tip": "depunere", "suma": suma})
        salveaza_date(date)
        return True
    return False


def retragere(id_cont, suma):
    date = incarca_date()
    if id_cont in date and suma > 0:
        if date[id_cont]['sold'] >= suma:  # Validare sold insuficient (Cerința 1)
            date[id_cont]['sold'] -= suma
            date[id_cont]['istoric'].append({"tip": "retragere", "suma": suma})
            salveaza_date(date)
            return True
    return False



def transfer(sursa, destinatie, suma):
    date = incarca_date()
    if sursa in date and destinatie in date and suma > 0:
        if date[sursa]['sold'] >= suma:  # Cerința 2: respins dacă soldul sursei e insuficient
            date[sursa]['sold'] -= suma
            date[destinatie]['sold'] += suma
            date[sursa]['istoric'].append({"tip": "retragere_transfer", "suma": suma})
            date[destinatie]['istoric'].append({"tip": "depunere_transfer", "suma": suma})
            salveaza_date(date)
            return True
    return False



def genereaza_raport(id_cont):
    date = incarca_date()
    if id_cont not in date:
        return "Cont inexistent."

    istoric = date[id_cont]['istoric']
    # Cerința 3: însumarea depunerilor și retragerilor
    total_depuneri = sum(t['suma'] for t in istoric if 'depunere' in t['tip'])
    total_retrageri = sum(t['suma'] for t in istoric if 'retragere' in t['tip'])

    raport = f"\n--- RAPORT CONT: {id_cont} ---\n"
    raport += f"Sold curent: {date[id_cont]['sold']} RON\n"
    raport += f"Total bani intrați (depuneri): +{total_depuneri} RON\n"
    raport += f"Total bani ieșiți (retrageri): -{total_retrageri} RON\n"
    raport += "-" * 30
    return raport



def meniu_interfata():
    incarca_date()  # Asigură crearea fișierului
    while True:
        print("\n=== Simulator de Tranzacții P16 ===")
        print("Conturi disponibile pt test: RO123, RO456")
        print("1. Depunere")
        print("2. Retragere")
        print("3. Transfer între conturi")
        print("4. Generare Raport (Cerința 3)")
        print("5. Ieșire")

        optiune = input("Alege o opțiune: ")

        if optiune == '1':
            cont = input("Cont: ")
            suma = float(input("Suma de depus: "))
            if depunere(cont, suma):
                print("[SUCCES] Depunere înregistrată.")
            else:
                print("[EROARE] Cont invalid.")

        elif optiune == '2':
            cont = input("Cont: ")
            suma = float(input("Suma de retras: "))
            if retragere(cont, suma):
                print("[SUCCES] Retragere efectuată.")
            else:
                print("[EROARE] Sold insuficient sau cont invalid!")

        elif optiune == '3':
            sursa = input("Cont sursă: ")
            dest = input("Cont destinație: ")
            suma = float(input("Suma de transferat: "))
            if transfer(sursa, dest, suma):
                print("[SUCCES] Transfer finalizat.")
            else:
                print("[EROARE] Fonduri insuficiente sau cont(uri) invalid(e).")

        elif optiune == '4':
            cont = input("Cont pentru raport: ")
            print(genereaza_raport(cont))

        elif optiune == '5':
            print("Se închide simulatorul...")
            break
        else:
            print("Opțiune invalidă.")


if __name__ == "__main__":
    meniu_interfata()