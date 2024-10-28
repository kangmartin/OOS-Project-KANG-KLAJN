import sqlite3
import os

class Database:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'hotel.db')

    def connect(self):
        return sqlite3.connect(self.db_path)

    def ajouter_chambre(self, numero):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO chambres (numero) VALUES (?)", (numero,))
            conn.commit()
            succes = True
            message = "Chambre ajoutée avec succès"
        except sqlite3.IntegrityError:
            succes = False
            message = "Une chambre avec ce numéro existe déjà"
        conn.close()
        return succes, message

    def supprimer_chambre(self, numero):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chambres WHERE numero = ?", (numero,))
        conn.commit()
        rows_deleted = cursor.rowcount
        conn.close()
        if rows_deleted > 0:
            return True, "Chambre supprimée avec succès"
        else:
            return False, "Chambre non trouvée"

    def get_chambre_id(self, numero):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM chambres WHERE numero = ?", (numero,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def reserver_chambre(self, chambre_id, date_debut, date_fin):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM chambres WHERE id = ?", (chambre_id,))
        if not cursor.fetchone():
            conn.close()
            return False, "La chambre n'existe pas"

        cursor.execute("""
            SELECT COUNT(*) FROM reservations
            WHERE chambre_id = ? AND (
                (? BETWEEN date_debut AND date_fin) OR
                (? BETWEEN date_debut AND date_fin) OR
                (date_debut BETWEEN ? AND ?) OR
                (date_fin BETWEEN ? AND ?)
            )
        """, (
            chambre_id,
            date_debut, date_fin,
            date_debut, date_fin,
            date_debut, date_fin
        ))
        (count,) = cursor.fetchone()

        if count == 0:
            cursor.execute("""
                INSERT INTO reservations (chambre_id, date_debut, date_fin)
                VALUES (?, ?, ?)
            """, (chambre_id, date_debut, date_fin))
            conn.commit()
            succes = True
            message = "Réservation réussie"
        else:
            succes = False
            message = "Chambre non disponible pour les dates sélectionnées"

        conn.close()
        return succes, message

    def verifier_disponibilite(self, chambre_id, date_debut, date_fin):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM chambres WHERE id = ?", (chambre_id,))
        if not cursor.fetchone():
            conn.close()
            return False, "La chambre n'existe pas"

        cursor.execute("""
            SELECT COUNT(*) FROM reservations
            WHERE chambre_id = ? AND (
                (? BETWEEN date_debut AND date_fin) OR
                (? BETWEEN date_debut AND date_fin) OR
                (date_debut BETWEEN ? AND ?) OR
                (date_fin BETWEEN ? AND ?)
            )
        """, (
            chambre_id,
            date_debut, date_fin,
            date_debut, date_fin,
            date_debut, date_fin
        ))
        (count,) = cursor.fetchone()
        conn.close()

        disponible = count == 0
        message = "Chambre disponible" if disponible else "Chambre non disponible"
        return disponible, message

    def annuler_reservation(self, reservation_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM reservations WHERE id = ?", (reservation_id,))
        conn.commit()
        rows_deleted = cursor.rowcount
        conn.close()

        succes = rows_deleted > 0
        message = "Réservation annulée avec succès" if succes else "Réservation non trouvée"
        return succes, message

    def consulter_reservations(self, reservation_id=None):
        conn = self.connect()
        cursor = conn.cursor()

        if reservation_id:
            cursor.execute("""
                SELECT reservations.id, chambres.numero, reservations.date_debut, reservations.date_fin
                FROM reservations
                JOIN chambres ON reservations.chambre_id = chambres.id
                WHERE reservations.id = ?
            """, (reservation_id,))
        else:
            cursor.execute("""
                SELECT reservations.id, chambres.numero, reservations.date_debut, reservations.date_fin
                FROM reservations
                JOIN chambres ON reservations.chambre_id = chambres.id
            """)

        reservations = cursor.fetchall()
        conn.close()

        return reservations

    def get_all_chambres(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT numero FROM chambres")
        chambres = [row[0] for row in cursor.fetchall()]
        conn.close()
        return chambres

