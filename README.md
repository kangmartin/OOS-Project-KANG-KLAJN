
# Projet de Réservation de chambres d’hôtels
## Par Martin KANG et Tom KLAJN

Ce projet est une application développée en langage Python permettant de gérer la réservation de chambres d’hôtels avec l'architecture suivante:

- **Service REST** : Fournit une API REST pour l’utilisateur, en exposant des endpoints pour interagir avec le système (réservation, annulation, etc.).
- **Service gRPC** : Sert d’intermédiaire entre le service REST et la couche de données. Il implémente  la communication avec la couche de données via des appels de fonctions.
- **Couche de Données** : Responsable de l’accès aux données, elle exécute les requêtes SQL sur la base de données SQLite.
- **Base de Données (SQLite)** : Stocke les informations relatives aux chambres et aux réservations.
<img width="737" alt="Capture d’écran 2024-10-28 à 14 20 23" src="https://github.com/user-attachments/assets/ccdfd1eb-a640-4bc8-b7b1-125449c510e0">

## Initialisation du Projet

### 1. Installer les Dépendances

Installez les dépendances du projet en exécutant la commande suivante à la racine du projet :

```bash
pip install -r requirements.txt
```

## Lancement des Services

### 1. Démarrer le Serveur gRPC

Dans un terminal, exécutez :

```bash
cd servicegRPC
python grpc_server.py
```

Le serveur gRPC est maintenant en cours d’exécution sur le port 50051.

### 2. Démarrer le Service REST

Dans un autre terminal, exécutez :

```bash
cd serviceREST
uvicorn main:app --reload
```

Le service REST est maintenant en cours d’exécution sur le port 8000.

## Documentation Swagger

Ouvrez votre navigateur et rendez-vous à l’adresse :

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Requêtes cURL

Vous pouvez tester les différentes fonctionnalités de l’application en utilisant des commandes cURL.


### Afficher la liste des chambres

Requête :

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/chambres' \
  -H 'accept: application/json'
```

Réponse attendue :

```json
{
  "chambres": [
    101,
    102,
    103
  ]
}
```

### Ajouter une Chambre

Requête :

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/ajouter_chambre' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "numero": 2000
}'
```

Réponse attendue :

```json
{
  "succes": true,
  "message": "Chambre ajoutée avec succès"
}
```

### Supprimer une Chambre

Requête :

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/supprimer_chambre' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "numero": 2000
}'
```

Réponse attendue :

```json
{
  "succes": true,
  "message": "Chambre supprimée avec succès"
}
```

### Réserver une Chambre

Requête :

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/reserver' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "chambre_id": 1,
  "date_debut": "2024-12-10",
  "date_fin": "2024-12-17"
}'
```

Réponse attendue :

```json
{
  "succes": true,
  "message": "Réservation réussie",
  "reservation_id": 1
}
```

### Annuler une Réservation

Requête :

```bash
curl -X POST "http://127.0.0.1:8000/annuler_reservation" -H "Content-Type: application/json" -d '{
  "reservation_id": 1
}'
```

Réponse attendue :

```json
{
  "succes": true,
  "message": "Réservation annulée avec succès"
}
```

### Consulter les Réservations

Requête pour toutes les réservations :

```bash
curl -X GET "http://127.0.0.1:8000/reservations"
```

Réponse attendue :

```json
[
  {
    "reservation_id": 1,
    "numero_chambre": 101,
    "date_debut": "2023-11-01",
    "date_fin": "2023-11-05"
  }
]
```

Requête pour une réservation spécifique :

```bash
curl -X GET "http://127.0.0.1:8000/reservations?reservation_id=1"
```

### Vérifier la Disponibilité d’une Chambre

Requête :

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/verifier_disponibilite' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "chambre_id": 4,
  "date_debut": "2024-10-19",
  "date_fin": "2024-10-22"
}'
```

Réponse attendue :

```json
{
  "disponible": true,
  "message": "Chambre disponible"
}
```
