import face_recognition as fr
import numpy as np
from profiles.models import Profile

def is_ajax(request):
    # Esta función verifica si la solicitud es una solicitud AJAX
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

def get_encoded_faces():
    """
    Esta función carga todas las imágenes de perfil de usuario y codifica sus rostros.
    """
    # Recupera todos los perfiles de usuario de la base de datos
    qs = Profile.objects.all()

    # Crea un diccionario para almacenar el rostro codificado de cada usuario
    encoded = {}

    for p in qs:
        # Inicializa la variable de codificación como None
        encoding = None

        # Carga la imagen de perfil del usuario
        face = fr.load_image_file(p.photo.path)

        # Codifica el rostro (si se detecta)
        face_encodings = fr.face_encodings(face)
        if len(face_encodings) > 0:
            encoding = face_encodings[0]
        else:
            print("No se encontró un rostro en la imagen")

        # Agrega el rostro codificado del usuario al diccionario si la codificación no es None
        if encoding is not None:
            encoded[p.user.username] = encoding

    # Devuelve el diccionario de rostros codificados
    return encoded

def classify_face(img):
    """
    Esta función toma una imagen como entrada y devuelve el nombre del rostro que contiene.
    """
    # Carga todos los rostros conocidos y sus codificaciones
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    # Carga la imagen de entrada
    img = fr.load_image_file(img)

    try:
        # Encuentra las ubicaciones de todos los rostros en la imagen de entrada
        face_locations = fr.face_locations(img)

        # Codifica los rostros en la imagen de entrada
        unknown_face_encodings = fr.face_encodings(img, face_locations)

        # Identifica los rostros en la imagen de entrada
        face_names = []
        for face_encoding in unknown_face_encodings:
            # Compara la codificación del rostro actual con las codificaciones de todos los rostros conocidos
            matches = fr.compare_faces(faces_encoded, face_encoding)

            # Encuentra el rostro conocido con la codificación más cercana al rostro actual
            face_distances = fr.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)

            # Si el rostro conocido más cercano es una coincidencia para el rostro actual, etiqueta el rostro con el nombre conocido
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            else:
                name = "Desconocido"

            face_names.append(name)

        # Devuelve el nombre del primer rostro en la imagen de entrada
        return face_names[0]
    except:
        # Si no se encuentran rostros en la imagen de entrada o se produce un error, devuelve False
        return False
