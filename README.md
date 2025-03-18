# Aplicación de Filtros de Semitonos y Dados con Streamlit

### Joel Miguel Maya Castrejón │ mike.maya@ciencias.unam.mx │ 417112602

Este proyecto es una aplicación web creada con **Python** y **Streamlit** que permite aplicar diferentes **filtros** a una imagen para generar efectos de **semitonos** y de **dados**. 
De esta forma cada bloque de la imagen se sustituye por uno de varios patrones predefinidos que varían en densidad para recrear la tonalidad original.

Entre los filtros implementados se encuentran:

1. **Filtro de Semitonos**  
   - Tres variantes (A, B, C) con distintas series para crear efectos de semitonos.  
2. **Filtro de Dados**  
   - Tres variantes (m, g, c), basadas en conjuntos que simulan distintas configuraciones de dados.

---

## Requisitos

- Python 3.12 o superior.
- [Streamlit](https://docs.streamlit.io/) para la creación de la interfaz web.
- [Pillow](https://pillow.readthedocs.io/) (PIL) para la manipulación de imágenes.

En el archivo **requirements.txt** se listan las dependencias necesarias (al menos Streamlit y Pillow). Asegúrate de instalarlas antes de ejecutar la aplicación.

---

## Instalación

1. [**Descarga** este repositorio](https://github.com/mikemayac/Image-Filter-Application-Semitones-Dice) en tu máquina local.
2. Crea y activa un **entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   # En Windows: venv\Scripts\activate
   ```
3. Instala los paquetes necesarios:
   ```bash
   pip install -r requirements.txt
   ```

---

## Ejecución de la Aplicación

1. Dentro del entorno virtual, en la carpeta donde se encuentra el archivo principal (por ejemplo, `semitonos.py` o `semitonos.py`), ejecuta:
   ```bash
   streamlit run semitonos.py
   ```
2. Automáticamente se abrirá tu navegador mostrando la interfaz de la aplicación.  
   Si no se abre, copia la URL que aparece en la terminal y pégala en tu navegador.

---

## Uso de la Aplicación

1. **Sube una imagen** en la barra lateral (sidebar), en formatos `JPG`, `JPEG` o `PNG`.  
2. **Selecciona** el tipo de filtro que deseas aplicar desde la lista desplegable:
   - **Filtro de Semitonos**  
     - Permite escoger entre tres variantes (A, B, C), cada una con un conjunto de patrones de círculos (o formas) para representar diferentes densidades de tono.  
     - Ajusta el tamaño de bloque para modificar la granularidad del efecto.
   - **Filtro de Dados**  
     - Ofrece tres variantes (m, g, c), donde cada una define distintos patrones inspirados en las caras de dados.  
     - Ajusta de nuevo el tamaño de bloque para controlar cuántos “dados” se usarán a lo largo de la imagen.
3. **Observa** cómo se muestra la **imagen original** en una columna y la **imagen resultante** en la otra columna.
4. **Descarga** la imagen procesada haciendo clic en el botón de descarga que aparece bajo la imagen resultante.

---

## Estructura del Proyecto

```bash
├── semitonos.py          # Código principal de la aplicación
├── dados/                # Carpeta con los dados para el filtro de dados
├── semitonos/            # Carpeta con los semitonos para el filtro de semitonos
├── .streamlit/           # Carpeta de configuración de Streamlit (opcional)
│    └── config.toml      # Configuraciones extra de Streamlit
├── README.md             # Archivo de documentación
├── requirements.txt      # Dependencias del proyecto (Streamlit, Pillow, etc.)
└── venv/                 # Entorno virtual 
```

---