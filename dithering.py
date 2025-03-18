import streamlit as st
from PIL import Image
from io import BytesIO

# Configuración de la página en modo ancho
st.set_page_config(page_title="Aplicación de Filtros (Semitonos y Dados)", layout="wide")

def aplicar_filtro_seleccionado(image, filtro):
    """
    Función que aplicará el filtro seleccionado.
    Aquí irán las implementaciones de los filtros de semitonos y dados.
    Por ahora, se deja como estructura sin lógica interna.
    """
    if filtro == "Filtro de Semitonos":
        # Lógica para semitonos se implementará aquí
        pass

    elif filtro == "Filtro de Dados":
        # Lógica para dados se implementará aquí
        pass

    # Si aún no se aplica nada, devolver la imagen tal cual.
    return image

def main():
    st.sidebar.title("Configuraciones")

    # Menú desplegable para seleccionar el filtro (ej. Semitonos, Dados)
    filtro_seleccionado = st.sidebar.selectbox(
        "Selecciona un filtro:",
        ("Filtro de Semitonos", "Filtro de Dados")
    )

    # Uploader de imagen
    uploaded_file = st.sidebar.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

    st.title("Aplicación de Filtros (Semitonos y Dados)")

    if uploaded_file is not None:
        # Cargar la imagen y convertirla a RGB (en caso de que tenga canal alfa)
        imagen_original = Image.open(uploaded_file).convert("RGB")

        # Dividir la vista en dos columnas para mostrar la imagen original y la procesada
        col1, col2 = st.columns(2)

        with col1:
            st.image(imagen_original, caption="Imagen Original", use_container_width=True)

        with col2:
            # Aplicar el filtro seleccionado (sin lógica interna por ahora)
            imagen_resultante = aplicar_filtro_seleccionado(imagen_original, filtro_seleccionado)

            st.image(imagen_resultante, caption=f"Imagen con Filtro: {filtro_seleccionado}", use_container_width=True)

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
        st.info("Por favor, sube una imagen para probar los filtros de Semitonos y Dados.")

if __name__ == "__main__":
    main()
