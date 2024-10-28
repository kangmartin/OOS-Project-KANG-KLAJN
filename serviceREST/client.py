# serviceREST/reservation_client.py
import grpc
import hotel_pb2
import hotel_pb2_grpc


class ReservationClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = hotel_pb2_grpc.ReservationServiceStub(self.channel)

    def reserver_chambre(self, chambre_id, date_debut, date_fin):
        request = hotel_pb2.ReservationRequest(
            chambre_id=chambre_id,
            date_debut=date_debut,
            date_fin=date_fin
        )
        return self.stub.ReserverChambre(request)

    def verifier_disponibilite(self, chambre_id, date_debut, date_fin):
        request = hotel_pb2.DisponibiliteRequest(
            chambre_id=chambre_id,
            date_debut=date_debut,
            date_fin=date_fin
        )
        return self.stub.VerifierDisponibilite(request)

    def annuler_reservation(self, reservation_id):
        request = hotel_pb2.AnnulationRequest(reservation_id=reservation_id)
        return self.stub.AnnulerReservation(request)

    def consulter_reservations(self, reservation_id=None):
        request = hotel_pb2.ConsultationRequest(reservation_id=reservation_id or 0)
        return self.stub.ConsulterReservations(request)

    def ajouter_chambre(self, numero):
        request = hotel_pb2.ChambreRequest(numero=numero)
        return self.stub.AjouterChambre(request)

    def supprimer_chambre(self, numero):
        request = hotel_pb2.ChambreRequest(numero=numero)
        return self.stub.SupprimerChambre(request)

    def get_all_chambres(self):
        request = hotel_pb2.Empty()  # En supposant qu'un type de message Empty existe dans le fichier proto
        response = self.stub.GetAllChambres(request)
        return [chambre.numero for chambre in response]

