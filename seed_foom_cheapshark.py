import requests
import random
import uuid
from datetime import datetime
from app import app, db, Game, User


CATEGORIES = ["accion", "aventura", "rpg", "estrategia", "deportes", "simulacion", "indie", "shooter", "survival", "horror", "roguelike"]


CONTACT_EMAILS = [
    "vendedor.juegos@gamestore.net",
    "maria.games@digitalgamer.com",
    "carlos.estratega@juegospc.es",
    "alex.gaming@shootergames.com",
    "laura.adventures@gameworld.net",
    "pablo.simulator@simuverse.org",
    "monica.indie@indiegamestore.com",
    "javier.sports@deportesvirtuales.es"
]

CONTACT_PHONES = [
    "+34 612 345 789",
    "+34 678 123 456",
    "+34 654 987 321",
    "+34 691 234 567",
    "+34 623 456 789",
    "+34 687 345 912",
    "+34 632 198 765",
    "+34 645 789 321"
]

def fetch_games_from_cheapshark(limit=20):
    """Obtiene juegos desde la API de CheapShark"""
    url = f"https://www.cheapshark.com/api/1.0/deals?storeID=1&upperPrice=50&pageSize={limit}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener datos: {response.status_code}")
        return []

def seed_database_from_cheapshark():
    with app.app_context():

        if Game.query.count() > 0:
            print("La base de datos ya tiene juegos. ¿Deseas borrarlos y añadir nuevos? (s/n)")
            response = input().lower()
            if response != 's':
                print("Operación cancelada.")
                return
            else:
                Game.query.delete()
                db.session.commit()
                print("Juegos existentes eliminados.")
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Usuario admin no encontrado. Creando usuario admin...")
            admin = User('admin', 'admin@gamehive.com', 'admin123')
            db.session.add(admin)
            db.session.commit()
        
    
        cheapshark_games = fetch_games_from_cheapshark(30)  # Obtener 30 juegos
        
        if not cheapshark_games:
            print("No se pudieron obtener juegos de CheapShark.")
            return
        
        print(f"Se obtuvieron {len(cheapshark_games)} juegos de CheapShark.")
        
  
        for game_data in cheapshark_games:
           
            title = game_data['title']
            description = f"Disfruta de {title}, un juego increíble con gráficos impresionantes y una jugabilidad adictiva. Este título te ofrece horas de diversión y desafíos que pondrán a prueba tus habilidades. Ideal para jugadores de todos los niveles."
            
          
            category = random.choice(CATEGORIES)
            
      
            is_new = random.random() < 0.3
            
        
            game = Game(
                title=title,
                description=description,
                price=float(game_data['salePrice']),
                category=category,
                image=game_data['thumb'],
                contact_email=random.choice(CONTACT_EMAILS),
                contact_phone=random.choice(CONTACT_PHONES),
                is_new=is_new,
                user_id=admin.id
            )
            
            db.session.add(game)
        
      
        db.session.commit()
        print(f"Base de datos poblada con {len(cheapshark_games)} juegos.")

if __name__ == "__main__":
    seed_database_from_cheapshark()
