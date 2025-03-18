import streamlit as st
from PIL import Image
from io import BytesIO
import random

# Configuración de la página en modo ancho
st.set_page_config(page_title="Aplicación que aplica distintos filtros de Dithering", layout="wide")

def random_dithering(image):
    """
    Aplica el filtro de dithering por azar (random dithering).
    """
    # 1. Convertir la imagen a escala de grises
    gray_img = image.convert("L")

    # Crear una nueva imagen en 'L' para la salida
    width, height = gray_img.size
    dithered_img = Image.new("L", (width, height))

    # Cargar los pixeles
    src_pixels = gray_img.load()
    dst_pixels = dithered_img.load()

    # 2. Recorrer cada píxel y asignar blanco/negro según número aleatorio
    for y in range(height):
        for x in range(width):
            gray_val = src_pixels[x, y]
            rand_val = random.randint(0, 255)
            if gray_val > rand_val:
                dst_pixels[x, y] = 255  # Blanco
            else:
                dst_pixels[x, y] = 0  # Negro

    # 3. Convertir a RGB para guardar en la misma línea de color que la original
    return dithered_img.convert("RGB")


def ordered_clustered_dithering(image):
    """
    Aplica el dithering ordenado y disperso (Clustered) usando una matriz de Bayer 4x4.
    """
    # 1) Convertir la imagen a escala de grises
    gray_img = image.convert("L")

    # 2) Definir la matriz de Bayer 4x4
    bayer_4x4 = [
        [ 0,  8,  2, 10],
        [12,  4, 14,  6],
        [ 3, 11,  1,  9],
        [15,  7, 13,  5]
    ]
    # Nota: Esta matriz contiene valores de 0 a 15.

    # 3) Crear una nueva imagen en 'L' para la salida
    width, height = gray_img.size
    dithered_img = Image.new("L", (width, height))

    # Cargar los píxeles de ambas imágenes
    src_pixels = gray_img.load()
    dst_pixels = dithered_img.load()

    # 4) Recorrer cada píxel y aplicar la comparación con la matriz Bayer
    for y in range(height):
        for x in range(width):
            gray_val = src_pixels[x, y]  # Valor de 0..255
            # Obtener el valor de la matriz Bayer en función de la posición (x, y)
            bayer_value = bayer_4x4[y % 4][x % 4]  # Valor de 0..15
            # Escalar el valor Bayer a 0..255
            threshold = (bayer_value / 16) * 255

            # Comparar con el valor de gris
            if gray_val > threshold:
                dst_pixels[x, y] = 255  # Blanco
            else:
                dst_pixels[x, y] = 0    # Negro

    # 5) Convertir a RGB para mantener la misma consistencia de color
    return dithered_img.convert("RGB")


def dispersed_dithering_2x2(image):
    """
    Dithering disperso usando una matriz de Bayer 2×2.
    """
    # Convertir a escala de grises
    gray_img = image.convert("L")
    width, height = gray_img.size

    # Matriz de Bayer 2×2 (dispersa)
    # Niveles de 0..3 (4 niveles)
    bayer_2x2 = [
        [0, 2],
        [3, 1]
    ]

    # Crear imagen de salida en modo 'L'
    dithered_img = Image.new("L", (width, height))
    src_pixels = gray_img.load()
    dst_pixels = dithered_img.load()

    for y in range(height):
        for x in range(width):
            gray_val = src_pixels[x, y]  # 0..255
            # Obtener el valor de la matriz (0..3)
            bayer_val = bayer_2x2[y % 2][x % 2]
            # Escalar a rango [0..255]
            # En 2×2, los valores van de 0..3, así que dividimos entre 4
            threshold = (bayer_val / 4) * 255

            if gray_val > threshold:
                dst_pixels[x, y] = 255  # Blanco
            else:
                dst_pixels[x, y] = 0    # Negro

    return dithered_img.convert("RGB")


def dispersed_dithering_4x4(image):
    """
    Dithering disperso usando una matriz de Bayer 4×4.
    """
    # Convertir a escala de grises
    gray_img = image.convert("L")
    width, height = gray_img.size

    # Matriz de Bayer 4×4 “dispersa” (versión clásica)
    # Niveles de 0..15 (16 niveles)
    bayer_4x4 = [
        [ 0,  8,  2, 10],
        [12,  4, 14,  6],
        [ 3, 11,  1,  9],
        [15,  7, 13,  5]
    ]

    # Crear imagen de salida en modo 'L'
    dithered_img = Image.new("L", (width, height))
    src_pixels = gray_img.load()
    dst_pixels = dithered_img.load()

    for y in range(height):
        for x in range(width):
            gray_val = src_pixels[x, y]  # 0..255
            # Obtener el valor de la matriz (0..15)
            bayer_val = bayer_4x4[y % 4][x % 4]
            # Escalar a rango [0..255]
            # En 4×4, los valores van de 0..15, así que dividimos entre 16
            threshold = (bayer_val / 16) * 255

            if gray_val > threshold:
                dst_pixels[x, y] = 255  # Blanco
            else:
                dst_pixels[x, y] = 0    # Negro

    return dithered_img.convert("RGB")


def floyd_steinberg_dithering(image):
    """
    Aplica dithering Floyd Steinberg a la imagen.
    Recorre cada píxel, decide blanco/negro y reparte el error a sus vecinos.
    """
    # 1) Convertir la imagen a escala de grises
    gray_img = image.convert("L")
    width, height = gray_img.size

    # Cargar pixeles en memoria
    pixels = gray_img.load()

    # Función para asegurar que el valor queda en [0..255]
    def clamp(val):
        return max(0, min(255, int(val)))

    # 2) Recorrer de arriba a abajo, izquierda a derecha
    for y in range(height):
        for x in range(width):
            old_val = pixels[x, y]

            # 3) Determinar nuevo valor (blanco o negro).
            #    Por simplicidad, usamos 128 como umbral.
            new_val = 255 if old_val >= 128 else 0
            pixels[x, y] = new_val

            # 4) Calcular error
            error = old_val - new_val  # diferencia entre pixel original y 'forzado'

            # 5) Distribuir el error a los píxeles vecinos (si existen) siguiendo
            #    la clásica matriz de Floyd Steinberg:
            #
            #        (x+1, y)   += error * 7/16
            #        (x-1, y+1) += error * 3/16
            #        (x,   y+1) += error * 5/16
            #        (x+1, y+1) += error * 1/16
            #
            #    Verificamos que estén dentro de los límites de la imagen.

            # píxel derecho
            if x + 1 < width:
                pixels[x + 1, y] = clamp(pixels[x + 1, y] + error * (7 / 16))

            # píxel abajo izquierda
            if x - 1 >= 0 and y + 1 < height:
                pixels[x - 1, y + 1] = clamp(pixels[x - 1, y + 1] + error * (3 / 16))

            # píxel abajo
            if y + 1 < height:
                pixels[x, y + 1] = clamp(pixels[x, y + 1] + error * (5 / 16))

            # píxel abajo derecha
            if x + 1 < width and y + 1 < height:
                pixels[x + 1, y + 1] = clamp(pixels[x + 1, y + 1] + error * (1 / 16))

    # Convertir a RGB para mantener el mismo modo de color que otras funciones
    return gray_img.convert("RGB")


def fake_floyd_steinberg_dithering(image):
    """
    Aplica dithering Fake Floyd Steinberg, una versión simplificada de Floyd Steinberg,
    donde el error solo se reparte a menos vecinos (por ejemplo, derecha y abajo).
    """
    # 1) Convertir la imagen a escala de grises
    gray_img = image.convert("L")
    width, height = gray_img.size

    # Cargar pixeles en memoria
    pixels = gray_img.load()

    # Función para asegurar que el valor queda en [0..255]
    def clamp(val):
        return max(0, min(255, int(val)))

    # 2) Recorrer la imagen de arriba a abajo, izquierda a derecha
    for y in range(height):
        for x in range(width):
            old_val = pixels[x, y]

            # 3) Determinar nuevo valor (blanco o negro)
            new_val = 255 if old_val >= 128 else 0
            pixels[x, y] = new_val

            # 4) Calcular error
            error = old_val - new_val

            # 5) Distribuir el error a MENOS vecinos que Floyd Steinberg estándar.
            #    Ejemplo sencillo: la mitad del error al píxel de la derecha,
            #    y la otra mitad al píxel de abajo, si existen.

            # píxel a la derecha
            if x + 1 < width:
                pixels[x + 1, y] = clamp(pixels[x + 1, y] + error * 0.5)

            # píxel abajo
            if y + 1 < height:
                pixels[x, y + 1] = clamp(pixels[x, y + 1] + error * 0.5)

    # Convertir a RGB para mantener consistencia con el resto de la app
    return gray_img.convert("RGB")


def jarvis_judice_ninke_dithering(image):
    """
    Aplica dithering Jarvis, Judice, y Ninke (JJN).
    Reparte el error a un conjunto mayor de vecinos que Floyd Steinberg,
    obteniendo un tramado más fino.
    """
    # 1) Convertir la imagen a escala de grises
    gray_img = image.convert("L")
    width, height = gray_img.size

    # Cargar pixeles en memoria
    pixels = gray_img.load()

    # Función para asegurar que el valor queda en [0..255]
    def clamp(val):
        return max(0, min(255, int(val)))

    # 2) Definir la distribución de error para JJN
    #    Cada tupla: (desplazamiento_x, desplazamiento_y, factor)
    #    Referencia típica del patrón:
    #    (x+1,  y)   = 7/48,  (x+2,  y)   = 5/48
    #    (x-2,  y+1) = 3/48,  (x-1,  y+1) = 5/48, (x, y+1) = 7/48, (x+1, y+1) = 5/48, (x+2, y+1) = 3/48
    #    (x-2,  y+2) = 1/48,  (x-1,  y+2) = 3/48, (x, y+2) = 5/48, (x+1, y+2) = 3/48, (x+2, y+2) = 1/48

    diffusion_map = [
        (1, 0, 7 / 48), (2, 0, 5 / 48),
        (-2, 1, 3 / 48), (-1, 1, 5 / 48), (0, 1, 7 / 48), (1, 1, 5 / 48), (2, 1, 3 / 48),
        (-2, 2, 1 / 48), (-1, 2, 3 / 48), (0, 2, 5 / 48), (1, 2, 3 / 48), (2, 2, 1 / 48)
    ]

    # 3) Recorrer la imagen de arriba a abajo, izquierda a derecha
    for y in range(height):
        for x in range(width):
            old_val = pixels[x, y]

            # 4) Redondear (decidir blanco o negro).
            #    Usamos 128 como umbral, pero puedes ajustar.
            new_val = 255 if old_val >= 128 else 0
            pixels[x, y] = new_val

            # 5) Calcular error
            error = old_val - new_val

            # 6) Repartir el error entre los vecinos que aún no han sido procesados
            for dx, dy, factor in diffusion_map:
                nx = x + dx
                ny = y + dy
                # Verifica que (nx, ny) esté dentro de la imagen
                if 0 <= nx < width and 0 <= ny < height:
                    current_val = pixels[nx, ny]
                    # Sumar el error con su factor
                    pixels[nx, ny] = clamp(current_val + error * factor)

    # 7) Convertir de nuevo a RGB para mantener consistencia en la salida
    return gray_img.convert("RGB")


def apply_dithering_filter(image, filter_type):
    """
    Aplica el filtro de dithering seleccionado.
    """
    if filter_type == "1. Filtro de Azar":
        return random_dithering(image)

    elif filter_type == "2. Ordenado y disperso (Clustered)":
        return ordered_clustered_dithering(image)


    elif filter_type == "3. Disperso 2x2, 4x4":
        # Aquí podemos preguntar al usuario (o decidir por defecto)
        # si aplicamos el 2x2 o el 4x4.
        # Por ejemplo, un sub-menú en Streamlit:
        sub_option = st.sidebar.selectbox(
            "Selecciona el tamaño de la matriz dispersa:",
            ("2x2", "4x4")
        )
        if sub_option == "2x2":
            return dispersed_dithering_2x2(image)
        else:
            return dispersed_dithering_4x4(image)

    elif filter_type == "4. Floyd Steinberg":
        return floyd_steinberg_dithering(image)

    elif filter_type == "5. Fake Floyd Steinberg":
        return fake_floyd_steinberg_dithering(image)

    elif filter_type == "6. Jarvis, Judice, Ninken":
        return jarvis_judice_ninke_dithering(image)


    else:
        return image


def main():
    st.sidebar.title("Configuraciones")

    # Menú desplegable para seleccionar el filtro de dithering
    dithering_filter = st.sidebar.selectbox(
        "Selecciona un filtro de dithering:",
        (
            "1. Filtro de Azar",
            "2. Ordenado y disperso (Clustered)",
            "3. Disperso 2x2, 4x4",
            "4. Floyd Steinberg",
            "5. Fake Floyd Steinberg",
            "6. Jarvis, Judice, Ninken"
        )
    )

    # Uploader de imagen
    uploaded_file = st.sidebar.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

    st.title("Aplicación que aplica distintos filtros de Dithering")

    if uploaded_file is not None:
        # Cargar la imagen y convertirla a RGB (en caso de que tenga canal alfa)
        original_image = Image.open(uploaded_file).convert("RGB")

        # Dividir la vista en dos columnas para mostrar la imagen original y la procesada
        col1, col2 = st.columns(2)

        with col1:
            st.image(original_image, caption="Imagen Original", use_container_width=True)

        with col2:
            # Aplicar el filtro de dithering seleccionado
            result_image = apply_dithering_filter(original_image, dithering_filter)

            st.image(result_image, caption=f"Imagen con Filtro: {dithering_filter}", use_container_width=True)

            # Botón para descargar la imagen resultante
            buf = BytesIO()
            result_image.save(buf, format="PNG")
            st.download_button(
                label="⬇️ Descargar imagen",
                data=buf.getvalue(),
                file_name="imagen_resultante.png",
                mime="image/png"
            )
    else:
        st.info("Por favor, sube una imagen para quitar la marca de agua y/o aplicar un filtro de dithering.")


if __name__ == "__main__":
    main()