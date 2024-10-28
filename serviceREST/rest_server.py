from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from datetime import datetime
import grpc
from client import ReservationClient

app = FastAPI()
client = ReservationClient()

class Reservation(BaseModel):
    chambre_id: int
    date_debut: str
    date_fin: str

    @validator('date_debut', 'date_fin')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('La date doit être au format YYYY-MM-DD')
        return v

class Disponibilite(BaseModel):
    chambre_id: int
    date_debut: str
    date_fin: str

    @validator('date_debut', 'date_fin')
    def validate_date(cls, v):
        return Reservation.validate_date(v)

class Annulation(BaseModel):
    reservation_id: int

class Chambre(BaseModel):
    numero: int

@app.get("/chambres")
async def liste_chambres():
    chambres = client.get_all_chambres()
    return {"chambres": chambres}
@app.post("/ajouter_chambre")
async def ajouter_chambre(chambre: Chambre):
    try:
        response = client.ajouter_chambre(chambre.numero)
        return {
            "succes": response.succes,
            "message": response.message
        }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail="Erreur de communication avec le service gRPC: " + e.details())

@app.post("/supprimer_chambre")
async def supprimer_chambre(chambre: Chambre):
    try:
        response = client.supprimer_chambre(chambre.numero)
        return {
            "succes": response.succes,
            "message": response.message
        }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail="Erreur de communication avec le service gRPC: " + e.details())

@app.post("/reserver")
async def reserver(reservation: Reservation):
    try:
        response = client.reserver_chambre(
            reservation.chambre_id,
            reservation.date_debut,
            reservation.date_fin
        )
        return {
            "succes": response.succes,
            "message": response.message,
            "reservation_id": response.reservation_id
        }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail="Erreur de communication avec le service gRPC: " + e.details())

@app.get("/reservations")
async def consulter_reservations(reservation_id: int = None):
    try:
        response = client.consulter_reservations(reservation_id)
        reservations = []
        for res in response.reservations:
            reservations.append({
                "reservation_id": res.reservation_id,
                "chambre_id": res.chambre_id,
                "date_debut": res.date_debut,
                "date_fin": res.date_fin
            })
        return reservations
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail="Erreur de communication avec le service gRPC: " + e.details())

@app.post("/verifier_disponibilite")
async def verifier_disponibilite(disponibilite: Disponibilite):
    try:
        response = client.verifier_disponibilite(
            disponibilite.chambre_id,
            disponibilite.date_debut,
            disponibilite.date_fin
        )
        return {
            "disponible": response.disponible,
            "message": response.message
        }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail="Erreur de communication avec le service gRPC: " + e.details())

@app.post("/annuler_reservation")
async def annuler_reservation(annulation: Annulation):
    try:
        response = client.annuler_reservation(annulation.reservation_id)
        return {
            "succes": response.succes,
            "message": response.message
        }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail="Erreur de communication avec le service gRPC: " + e.details())


