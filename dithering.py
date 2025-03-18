import streamlit as st
from PIL import Image
from io import BytesIO
import os

# Configuración de página en modo ancho
st.set_page_config(page_title="Aplicación de Filtros (Semitonos y Dados)", layout="wide")

# =============================================================================
# 1) Definir TRES sets de archivos de semitonos
#    El orden importa: el primero es el tile para zonas claras
#    y el último, para zonas oscuras (o al revés, si quieres invertir).
# =============================================================================

HALFTONE_SET = {
    "A": [
        # Orden sugerido: de más blanco a más negro
        "a10.jpg",  # Más claro
        "a9.jpg",
        "a8.jpg",
        "a7.jpg",
        "a6.jpg",
        "a5.jpg",
        "a4.jpg",
        "a3.jpg",
        "a2.jpg",
        "a1.jpg"  # Más oscuro
    ],
    "B": [
        "b0.jpg",
        "b1.jpg",
        "b2.jpg",
        "b3.jpg",
        "b4.jpg",
        "b5.jpg",
        "b6.jpg",
        "b7.jpg",
        "b8.jpg",
        "b9.jpg"
    ],
    "C": [
        # c0, c1, c2, c3, c4...
        # Ajustar según tus archivos reales
        "c0.jpg",
        "c1.jpg",
        "c2.jpg",
        "c3.jpg",
        "c4.jpg"
    ],
}


# =============================================================================
# 2) Función para cargar los tiles de un set dado
# =============================================================================
def cargar_tiles_de_set(set_name):
    """
    Carga las imágenes de semitonos (tiles) desde la carpeta 'semitonos/'
    según el set seleccionado (A, B, o C).
    Devuelve una lista de PIL.Images en orden.
    """
    file_list = HALFTONE_SET[set_name]
    halftone_tiles = []
    for fname in file_list:
        # Ajusta la carpeta si es diferente
        path = os.path.join("semitonos", fname)
        tile_img = Image.open(path).convert("RGB")
        halftone_tiles.append(tile_img)
    return halftone_tiles


# =============================================================================
# 3) Función principal para aplicar semitonos
# =============================================================================
def aplicar_filtro_semitonos(imagen, set_name, tile_size=20):
    """
    Aplica el filtro de semitonos con mosaicos basados en el set (A, B o C).

    - imagen: PIL.Image en RGB.
    - set_name: 'A', 'B' o 'C'.
    - tile_size: tamaño en píxeles para cada bloque.
    """
    # Cargamos los tiles de semitonos del set elegido
    halftone_tiles = cargar_tiles_de_set(set_name)
    num_tiles = len(halftone_tiles)

    # Convertimos la imagen a escala de grises para calcular promedio
    gray = imagen.convert("L")
    width, height = gray.size

    # Creamos la imagen de resultado
    result = Image.new("RGB", (width, height))

    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            # Recortamos el bloque [x, x+tile_size) x [y, y+tile_size)
            box = (x, y, x + tile_size, y + tile_size)
            region = gray.crop(box)

            # Calculamos el gris promedio a partir del histograma
            hist = region.histogram()
            total_pixels = region.size[0] * region.size[1]
            suma = 0
            for i, h in enumerate(hist):
                suma += i * h
            valor_prom = suma / total_pixels  # valor en [0..255]

            # Mapeamos a un índice de la lista halftone_tiles
            # Si halftone_tiles[0] es la más clara => valor_prom=255 => index=0
            #    => tal vez quieras invertir la fórmula.
            #
            # Aquí asumimos la PRIMERA es la más clara => la escogemos
            # cuando valor_prom sea ALTO. (es decir, invertimos la escala).
            # Si no es tu caso, ajusta la línea de index.

            # Ejemplo: invertimos el valor_prom para que 0 -> tile oscuro, 255 -> tile claro
            invertido = 255 - valor_prom
            index = int((invertido / 255) * (num_tiles - 1))
            index = max(0, min(num_tiles - 1, index))

            # Tomamos la tile correspondiente
            tile = halftone_tiles[index]
            # Redimensionamos la tile si es distinto su tamaño
            tile_resized = tile.resize((tile_size, tile_size), Image.Resampling.LANCZOS)

            # Pegamos la tile en (x,y) del resultado
            result.paste(tile_resized, (x, y))

    return result


# =============================================================================
# 4) Filtro "Dados" (placeholder)
# =============================================================================
def aplicar_filtro_dados(imagen):
    """
    Aquí iría la implementación real de tu filtro 'Dados'.
    Por ahora, solo devolvemos la imagen tal cual.
    """
    return imagen


# =============================================================================
# 5) Función para decidir qué filtro aplicar dentro de Streamlit
# =============================================================================
def aplicar_filtro_seleccionado(imagen, filtro):
    if filtro == "Filtro de Semitonos":
        # En este caso, mostramos un submenú en la barra lateral
        set_name = st.sidebar.selectbox(
            "Selecciona el tipo de semitonos:",
            ("A", "B", "C")
        )
        tile_size = st.sidebar.slider("Tamaño de cada bloque (px)", 5, 50, 20)

        return aplicar_filtro_semitonos(imagen, set_name, tile_size)

    elif filtro == "Filtro de Dados":
        return aplicar_filtro_dados(imagen)

    # Si no coincide, o no se ha seleccionado nada, devolvemos la imagen original
    return imagen


# =============================================================================
# 6) Lógica principal de la App
# =============================================================================
def main():
    st.sidebar.title("Configuraciones")

    # Menú para seleccionar el filtro
    filtro_seleccionado = st.sidebar.selectbox(
        "Selecciona un filtro:",
        ("Filtro de Semitonos", "Filtro de Dados")
    )

    # Uploader de imagen
    uploaded_file = st.sidebar.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

    st.title("Aplicación de Filtros (Semitonos y Dados)")

    if uploaded_file is not None:
        # Cargamos la imagen en RGB
        imagen_original = Image.open(uploaded_file).convert("RGB")

        # Creamos dos columnas: original y resultado
        col1, col2 = st.columns(2)

        with col1:
            st.image(imagen_original, caption="Imagen Original", use_container_width=True)

        with col2:
            # Aplicar el filtro
            imagen_resultante = aplicar_filtro_seleccionado(imagen_original, filtro_seleccionado)

            st.image(imagen_resultante, caption=f"Imagen con {filtro_seleccionado}", use_container_width=True)

            # Botón para descargar la imagen resultante
            buf = BytesIO()
            imagen_resultante.save(buf, format="PNG")
            st.download_button(
                label="⬇️ Descargar imagen",
                data=buf.getvalue(),
                file_name="imagen_resultante.png",
                mime="image/png"
            )
    else:
        st.info("Por favor, sube una imagen para probar los filtros de Semitonos o Dados.")


if __name__ == "__main__":
    main()
