import grpc
from concurrent import futures
import hotel_pb2
import hotel_pb2_grpc
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Data')))
from database import Database

class ReservationServiceServicer(hotel_pb2_grpc.ReservationServiceServicer):
    def __init__(self):
        self.db = Database()

    def ReserverChambre(self, request, context):
        try:
            succes, message = self.db.reserver_chambre(
                request.chambre_id,
                request.date_debut,
                request.date_fin
            )
            reservation_id = 0
            if succes:
                conn = self.db.connect()
                cursor = conn.cursor()
                cursor.execute("SELECT last_insert_rowid()")
                (reservation_id,) = cursor.fetchone()
                conn.close()
            return hotel_pb2.ReservationResponse(succes=succes, message=message, reservation_id=reservation_id)
        except Exception as e:
            print(f"Erreur lors de la réservation : {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return hotel_pb2.ReservationResponse(succes=False, message="Erreur interne du serveur", reservation_id=0)

    def VerifierDisponibilite(self, request, context):
        try:
            disponible, message = self.db.verifier_disponibilite(
                request.chambre_id,
                request.date_debut,
                request.date_fin
            )
            return hotel_pb2.DisponibiliteResponse(disponible=disponible, message=message)
        except Exception as e:
            print(f"Erreur lors de la vérification de disponibilité : {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return hotel_pb2.DisponibiliteResponse(disponible=False, message="Erreur interne du serveur")

    def AnnulerReservation(self, request, context):
        try:
            succes, message = self.db.annuler_reservation(request.reservation_id)
            return hotel_pb2.AnnulationResponse(succes=succes, message=message)
        except Exception as e:
            print(f"Erreur lors de l'annulation de la réservation : {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return hotel_pb2.AnnulationResponse(succes=False, message="Erreur interne du serveur")

    def ConsulterReservations(self, request, context):
        try:
            reservations_data = self.db.consulter_reservations(request.reservation_id or None)
            reservations = []
            for res in reservations_data:
                reservations.append(hotel_pb2.Reservation(
                    reservation_id=res[0],
                    chambre_id=res[1],
                    date_debut=res[2],
                    date_fin=res[3]
                ))
            return hotel_pb2.ConsultationResponse(reservations=reservations)
        except Exception as e:
            print(f"Erreur lors de la consultation des réservations : {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return hotel_pb2.ConsultationResponse()

    def AjouterChambre(self, request, context):
        try:
            succes, message = self.db.ajouter_chambre(request.numero)
            return hotel_pb2.ChambreResponse(succes=succes, message=message)
        except Exception as e:
            print(f"Erreur lors de l'ajout de la chambre : {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return hotel_pb2.ChambreResponse(succes=False, message="Erreur interne du serveur")

    def SupprimerChambre(self, request, context):
        try:
            succes, message = self.db.supprimer_chambre(request.numero)
            return hotel_pb2.ChambreResponse(succes=succes, message=message)
        except Exception as e:
            print(f"Erreur lors de la suppression de la chambre : {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return hotel_pb2.ChambreResponse(succes=False, message="Erreur interne du serveur")

    def GetAllChambres(self, request, context):
        chambres = self.db.liste_chambres()
        for numero in chambres:
            yield hotel_pb2.Chambre(numero=numero)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hotel_pb2_grpc.add_ReservationServiceServicer_to_server(ReservationServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Le serveur gRPC est en cours d'exécution sur le port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
