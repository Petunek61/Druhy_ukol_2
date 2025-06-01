import pytest
import mysql.connector
from mysql.connector import Error

# Konstanty
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "19611966"
TEST_DB_NAME = "test_ukoly_db"

# Funkce z aplikace pro testování

def pridat_ukol_db(connection, nazev, popis):
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO ukoly (nazev, popis, stav)
    VALUES (%s, %s, %s)
    """, (nazev, popis, "nezahájeno"))
    connection.commit()
    print("Úkol byl úspěšně přidán.")

def aktualizovat_ukol_db(connection, novy_stav, id_ukolu):
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE ukoly
        SET stav = %s
        WHERE id = %s
    """, (novy_stav, id_ukolu))
    connection.commit()

def odstranit_ukol_db(connection, id_ukolu):
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM ukoly
        WHERE id = %s
    """, (id_ukolu,))
    connection.commit()
    return cursor.rowcount

# Fixture: vytvoření a odstranění testovací databáze
@pytest.fixture(scope="module")
def test_db():
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = connection.cursor()

    # Vytvoření testovací DB a tabulky
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {TEST_DB_NAME}")
    cursor.execute(f"USE {TEST_DB_NAME}")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ukoly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nazev VARCHAR(255) NOT NULL COLLATE utf8mb4_bin CHECK (nazev <> ''),
            popis TEXT NOT NULL CHECK (popis <> ''),
            stav ENUM('nezahájeno', 'hotovo', 'probíhá') DEFAULT 'nezahájeno',
            datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    connection.database = TEST_DB_NAME
    yield connection

    # Teardown
    cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}")
    connection.close()

# ✅ Pozitivní test – přidání úkolu
def test_pridat_ukol_valid(test_db):
    pridat_ukol_db(test_db, "Testovací úkol", "Popis úkolu")
    cursor = test_db.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM ukoly WHERE nazev = %s AND popis = %s
    """, ("Testovací úkol", "Popis úkolu"))
    count = cursor.fetchone()[0]
    assert count == 1

# ❌ Negativní test – prázdný název
def test_pridat_ukol_empty_nazev(test_db):
    cursor = test_db.cursor()
    try:
        pridat_ukol_db(test_db, "", "Popis bez názvu")
    except mysql.connector.Error:
        test_db.rollback()
    else:
        pytest.fail("Očekávaná výjimka nebyla vyhozena při prázdném názvu.")

    cursor.execute("SELECT COUNT(*) FROM ukoly WHERE popis = %s", ("Popis bez názvu",))
    count = cursor.fetchone()[0]
    assert count == 0

# ✅ Pozitivní test – aktualizace stavu na 'hotovo'
def test_aktualizovat_ukol_valid(test_db):
    pridat_ukol_db(test_db, "Úkol k aktualizaci", "Popis")
    cursor = test_db.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Úkol k aktualizaci",))
    id_ukolu = cursor.fetchone()[0]

    aktualizovat_ukol_db(test_db, "hotovo", id_ukolu)

    cursor.execute("SELECT stav FROM ukoly WHERE id = %s", (id_ukolu,))
    stav = cursor.fetchone()[0]
    assert stav == "hotovo"

# ❌ Negativní test – aktualizace na neplatný stav
def test_aktualizovat_ukol_invalid_stav(test_db):
    pridat_ukol_db(test_db, "Úkol s chybným stavem", "Popis")
    cursor = test_db.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Úkol s chybným stavem",))
    id_ukolu = cursor.fetchone()[0]

    with pytest.raises(mysql.connector.Error):
        aktualizovat_ukol_db(test_db, "neplatny_stav", id_ukolu)

# ✅ Pozitivní test – odstranění existujícího úkolu
def test_odstranit_ukol_valid(test_db):
    pridat_ukol_db(test_db, "Úkol k odstranění", "Popis")
    cursor = test_db.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev = %s", ("Úkol k odstranění",))
    id_ukolu = cursor.fetchone()[0]

    rows_deleted = odstranit_ukol_db(test_db, id_ukolu)
    assert rows_deleted == 1

    cursor.execute("SELECT COUNT(*) FROM ukoly WHERE id = %s", (id_ukolu,))
    count = cursor.fetchone()[0]
    assert count == 0

# ❌ Negativní test – odstranění neexistujícího úkolu
def test_odstranit_ukol_invalid_id(test_db):
    id_neexistujici = 999999
    rows_deleted = odstranit_ukol_db(test_db, id_neexistujici)
    assert rows_deleted == 0
