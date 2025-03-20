import sqlite3
from datetime import datetime

# Conectar a la base de datos (la crea si no existe)
conn = sqlite3.connect('gamehive.db')
cursor = conn.cursor()

# Crear la tabla de juegos
cursor.execute('''
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NOT NULL,
    image TEXT NOT NULL,
    category TEXT NOT NULL,
    contactEmail TEXT,
    contactPhone TEXT,
    isNew BOOLEAN DEFAULT 0,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Datos de ejemplo para insertar
games = [
    {
        'title': 'The Last of Us Part I',
        'description': 'Un emocionante juego de supervivencia post-apocalíptico',
        'price': 59.99,
        'image': 'https://cdn1.epicgames.com/offer/0c40923dd1174a768f732a3b013dcff2/EGS_TheLastofUsPartI_NaughtyDogLLC_S1_2560x1440-3659b5fe340f8fc073257975b20b7f84',
        'category': 'Acción',
        'isNew': True
    },
    {
        'title': 'God of War Ragnarök',
        'description': 'La nueva aventura de Kratos y Atreus en los nueve reinos',
        'price': 69.99,
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTkq50ZrWy8rAfROsZ8eUzytc5nsi8X0wlty6nKiVeKk3v76cWl12oSLFMqpLIg0Me-VOY&usqp=CAU',
        'category': 'Acción',
        'isNew': False
    },
    {
        'title': 'Elden Ring',
        'description': 'Un vasto mundo abierto lleno de peligros y descubrimientos',
        'price': 59.99,
        'image': 'http://i.blogs.es/fc72f2/maxresdefault/1366_2000.webp',
        'category': 'RPG',
        'isNew': False
    },
    {
        'title': 'Baldur\'s Gate 3',
        'description': 'Un RPG épico basado en Dungeons & Dragons',
        'price': 59.99,
        'image': 'https://gaming-cdn.com/images/news/articles/2534/cover/baldur-s-gate-3-ya-es-el-segundo-mejor-lanzamiento-del-ano-en-steam-cover64db968342a07.jpg',
        'category': 'RPG',
        'isNew': True
    },
    {
        'title': 'FIFA 23',
        'description': 'El simulador de fútbol más popular del mundo',
        'price': 49.99,
        'image': 'https://imagenes.20minutos.es/files/image_990_556/uploads/imagenes/2023/02/24/fifa-23.jpeg',
        'category': 'Deportes',
        'isNew': False
    },
    {
        'title': 'Red Dead Redemption 2',
        'description': 'Explora el salvaje oeste con una historia increíble y gráficos impresionantes',
        'price': 49.99,
        'image': 'https://image.api.playstation.com/vulcan/img/rnd/202009/2818/GGyEnCkLxPppyqOHf24HQy6P.png',
        'category': 'Acción',
        'isNew': False
    },
    {
        'title': 'Cyberpunk 2077',
        'description': 'Un RPG de mundo abierto ambientado en un futuro distópico',
        'price': 39.99,
        'image': 'https://image.api.playstation.com/vulcan/ap/rnd/202111/3013/cKH4SnN0zt9Tb0V0rjzj9ims.png',
        'category': 'RPG',
        'isNew': False
    },
    {
        'title': 'Hogwarts Legacy',
        'description': 'Explora el mundo mágico de Harry Potter en esta aventura RPG',
        'price': 59.99,
        'image': 'https://cdn1.epicgames.com/offer/e97659b501af4e3981d5430dad170911/EGS_HogwartsLegacy_AvalancheSoftware_S1_2560x1440-2baf3188eb3c1aa248bcc1af6a927b7e',
        'category': 'RPG',
        'isNew': True
    }
]

# Insertar los juegos en la base de datos
for game in games:
    cursor.execute('''
    INSERT INTO games (title, description, price, image, category, isNew, date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        game['title'],
        game['description'],
        game['price'],
        game['image'],
        game['category'],
        1 if game['isNew'] else 0,
        datetime.now().isoformat()
    ))

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("Base de datos 'gamehive.db' creada e inicializada con éxito.")
