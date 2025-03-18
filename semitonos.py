import streamlit as st
from PIL import Image
from io import BytesIO
import os

# Configuración de la página
st.set_page_config(page_title="Aplicación de Filtros (Semitonos y Dados)", layout="wide")

# =============================================================================
# 1) Conjuntos de semitonos (A, B, C)
# =============================================================================
HALFTONE_SET = {
    "A": [
        "a10.jpg", "a9.jpg", "a8.jpg", "a7.jpg", "a6.jpg",
        "a5.jpg", "a4.jpg", "a3.jpg", "a2.jpg", "a1.jpg"
    ],
    "B": [
        "b0.jpg", "b1.jpg", "b2.jpg", "b3.jpg", "b4.jpg",
        "b5.jpg", "b6.jpg", "b7.jpg", "b8.jpg", "b9.jpg"
    ],
    "C": [
        "c0.jpg", "c1.jpg", "c2.jpg", "c3.jpg", "c4.jpg"
    ],
}

# =============================================================================
# 2) Conjuntos para el Filtro de Dados (m, g, c)
#    Orden de "más claro" a "más oscuro" (o al revés)
# =============================================================================
DICE_SET = {
    "m": [
        # Donde m0d.jpg es el más claro y m6d.jpg el más oscuro
        "m0d.jpg", "m1d.jpg", "m2d.jpg", "m3d.jpg", "m4d.jpg", "m5d.jpg", "m6d.jpg"
    ],
    "g": [
        # Donde g6d = más claro, g0d = más oscuro:
        "g6d.jpg", "g5d.jpg", "g4d.jpg", "g3d.jpg", "g2d.jpg", "g1d.jpg", "g0d.jpg"
    ],
    "c": [
        # c0.jpg (blanco) -> c4.jpg (más relleno en negro)
        "c0.jpg", "c1.jpg", "c2.jpg", "c3.jpg", "c4.jpg"
    ]
}


# =============================================================================
# Funciones de ayuda para cargar "imagenes de semitono" de los distintos sets
# =============================================================================

def cargar_tiles_semitonos(set_name):
    """
    Carga las imágenes de semitonos para el filtro de semitonos.
    """
    file_list = HALFTONE_SET[set_name]
    tiles = []
    for fname in file_list:
        path = os.path.join("semitonos", fname)
        tile_img = Image.open(path).convert("RGB")
        tiles.append(tile_img)
    return tiles


def cargar_tiles_dados(set_name):
    """
    Carga las imágenes de dados para el filtro de dados.
    """
    file_list = DICE_SET[set_name]
    tiles = []
    for fname in file_list:
        path = os.path.join("dados", fname)
        tile_img = Image.open(path).convert("RGB")
        tiles.append(tile_img)
    return tiles


# =============================================================================
# Función genérica para aplicar "mosaicos" (semitonos o dados)
# =============================================================================
def aplicar_mosaico(imagen, tile_images, tile_size=20, invert=False):
    """
    Dado un conjunto de tiles (tile_images) ordenados de más claro a más oscuro
    (o al revés), recorre la imagen en bloques de tile_size y decide qué tile pegar.

    - invert=True/False te permite invertir la fórmula de mapeo si ves que
      las zonas claras aparecen con tile oscuro.
    """
    gray = imagen.convert("L")
    width, height = gray.size

    result = Image.new("RGB", (width, height))
    num_tiles = len(tile_images)

    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            box = (x, y, x + tile_size, y + tile_size)
            region = gray.crop(box)

            # Calcular gris promedio
            hist = region.histogram()
            total_pixels = region.size[0] * region.size[1]
            suma = 0
            for i, h in enumerate(hist):
                suma += i * h
            prom = suma / total_pixels  # 0..255

            # Mapeo a índice
            # Caso "invert=False" => tile_images[0] = 0 (negro?), tile_images[-1] = 255 (blanco?)
            if invert:
                # 0..255 => invertimos => 255 - prom
                val = 255 - prom
                index = int((val / 255) * (num_tiles - 1))
            else:
                index = int((prom / 255) * (num_tiles - 1))

            index = max(0, min(num_tiles - 1, index))

            # Escogemos la imagen
            tile = tile_images[index].resize((tile_size, tile_size), Image.Resampling.LANCZOS)
            result.paste(tile, (x, y))

    return result


# =============================================================================
# Filtros específicos
# =============================================================================

def aplicar_filtro_semitonos(imagen):
    """
    Aplica un filtro de semitonos con 3 "sets" (A, B, C) a escoger en la barra lateral.
    """
    # Submenú en la barra lateral
    set_name = st.sidebar.selectbox("Selecciona el tipo de Semitonos:", ("A", "B", "C"))
    tile_size = st.sidebar.slider("Tamaño de Bloque (px)", 5, 50, 20)
    invert = st.sidebar.checkbox("¿Invertir el mapeo de gris?", value=False)

    # Cargamos las imagenes
    tiles = cargar_tiles_semitonos(set_name)
    # Llamamos a la función genérica
    return aplicar_mosaico(imagen, tiles, tile_size=tile_size, invert=invert)


def aplicar_filtro_dados(imagen):
    """
    Aplica el "filtro de dados" con 3 sets (m, g, c) a escoger en la barra lateral.
    """
    set_name = st.sidebar.selectbox("Selecciona el set de Dados:", ("m", "g", "c"))
    tile_size = st.sidebar.slider("Tamaño de Bloque (px)", 5, 50, 20)
    invert = st.sidebar.checkbox("¿Invertir el mapeo de gris?", value=False)

    # Cargamos los tiles
    tiles = cargar_tiles_dados(set_name)
    # Usamos la misma lógica de mosaico
    return aplicar_mosaico(imagen, tiles, tile_size=tile_size, invert=invert)


# =============================================================================
# Función para decidir el filtro
# =============================================================================
def aplicar_filtro_seleccionado(imagen, filtro):
    if filtro == "Filtro de Semitonos":
        return aplicar_filtro_semitonos(imagen)
    elif filtro == "Filtro de Dados":
        return aplicar_filtro_dados(imagen)
    return imagen


# =============================================================================
# Main de la aplicación
# =============================================================================
def main():
    st.sidebar.title("Configuraciones")

    filtro_seleccionado = st.sidebar.selectbox(
        "Selecciona un filtro:",
        ("Filtro de Semitonos", "Filtro de Dados")
    )

    uploaded_file = st.sidebar.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

    # Variable para almacenar la imagen resultante
    imagen_resultante = None

    if uploaded_file is not None:
        imagen_original = Image.open(uploaded_file).convert("RGB")

        # Aplicar el filtro seleccionado
        imagen_resultante = aplicar_filtro_seleccionado(imagen_original, filtro_seleccionado)

        # Preparar buffer para descarga (antes de mostrar la UI)
        buf = BytesIO()
        imagen_resultante.save(buf, format="PNG")
        buf_value = buf.getvalue()

    # Crear la fila del título con el botón de descarga
    title_col, button_col = st.columns([4, 1])

    with title_col:
        st.title("Aplicación de Filtros (Semitonos y Dados)")

    with button_col:
        if imagen_resultante is not None:
            st.download_button(
                label="⬇️ Descargar imagen",
                data=buf_value,
                file_name="imagen_resultante.png",
                mime="image/png",
                key="download_button_top"
            )

    # Mostrar las imágenes si se subió un archivo
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.image(imagen_original, caption="Imagen Original", use_container_width=True)

        with col2:
            st.image(imagen_resultante, caption=f"Imagen con {filtro_seleccionado}", use_container_width=True)

    else:
        st.info("Sube una imagen para aplicar los filtros de Semitonos o Dados.")


if __name__ == "__main__":
    main()