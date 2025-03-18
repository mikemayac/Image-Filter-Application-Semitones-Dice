# Aplicación de Filtros de Dithering con Streamlit

### Joel Miguel Maya Castrejón │ mike.maya@ciencias.unam.mx │ 417112602

Este proyecto consiste en una aplicación web interactiva creada con **Python** y **Streamlit** que permite aplicar diferentes **filtros de dithering** a una imagen. Entre los filtros implementados se encuentran:

1. **Filtro de Azar (Random Dithering)**  
2. **Ordenado y disperso (Clustered Dithering)**  
3. **Disperso 2×2, 4×4**  
4. **Floyd Steinberg**  
5. **Fake Floyd Steinberg**  
6. **Jarvis, Judice, Ninken**

## Requisitos

- Python 3.12 o superior.
- [Streamlit](https://docs.streamlit.io/) para la creación de la interfaz web.
- [Pillow](https://pillow.readthedocs.io/) (PIL) para la manipulación de imágenes.

En el archivo **requirements.txt** se listan las dependencias necesarias (al menos Streamlit y Pillow). Asegúrate de instalarlas antes de ejecutar la aplicación.

## Instalación

1. **Clona** o **descarga** [este repositorio](https://github.com/mikemayac/Image-Filter-Application-Dithering) en tu máquina local (o la URL donde tengas tu repo).
2. Crea un **entorno virtual** (opcional, pero recomendado) e **instálalo**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # En Linux/Mac
   # o en Windows: venv\Scripts\activate
   ```
3. Instala los paquetes necesarios:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución de la Aplicación

1. Dentro del entorno virtual y en la carpeta donde se encuentra el archivo principal (`dithering.py` o el nombre de tu script), ejecuta:
   ```bash
   streamlit run semitonos.py
   ```
2. Automáticamente se abrirá tu navegador mostrando la interfaz de la aplicación. Si no se abre, puedes copiar la URL que aparece en la terminal y pegarla en tu navegador.

## Uso de la Aplicación

1. **Sube una imagen** en la barra lateral (sidebar). Acepta formatos `JPG`, `JPEG` o `PNG`.  
2. **Selecciona** el filtro de dithering que deseas aplicar desde la lista desplegable. Encontrarás los siguientes modos:
   - **1. Filtro de Azar (Random Dithering)**  
     Aplica un umbral aleatorio a cada píxel para decidir si va a blanco o negro.  
   - **2. Ordenado y disperso (Clustered)**  
     Emplea una matriz de Bayer 4×4 para producir un tramado “clustered”.  
   - **3. Disperso 2×2, 4×4**  
     Ofrece un sub-menú para elegir entre una matriz de Bayer 2×2 o 4×4, donde los puntos están más dispersos.  
   - **4. Floyd Steinberg**  
     Método de difusión de error clásico, distribuye el error a los vecinos según la matriz Floyd Steinberg.  
   - **5. Fake Floyd Steinberg**  
     Versión simplificada de Floyd Steinberg, usando menos vecinos para la difusión de error.  
   - **6. Jarvis, Judice, Ninken**  
     Otro método de difusión de error más amplio, difunde el error a 12 vecinos en varias filas.  
3. **Observa** cómo se muestra la **imagen original** en la columna izquierda y la **imagen resultante** (con el filtro aplicado) en la columna derecha.
4. **Descarga** la imagen procesada haciendo clic en el botón de descarga que aparece bajo la imagen resultante.

## Estructura del Proyecto

```
├── dithering.py          # Código principal de la aplicación (o nombre que uses)
├── .streamlit/            # Carpeta de configuración (opcional)
│    └── config.toml       # Configuraciones extra de Streamlit
├── README.md              # Archivo de documentación
├── requirements.txt       # Dependencias del proyecto (Streamlit, Pillow, etc.)
└── venv/                  # Entorno virtual (opcional)
```

## Contribuir

Si deseas contribuir:

1. Haz un **fork** de este repositorio.
2. Crea una **rama** con la nueva funcionalidad o corrección de errores:  
   ```bash
   git checkout -b nueva-funcionalidad
   ```
3. Realiza tus cambios y haz **commit**:  
   ```bash
   git commit -m "Agrega nueva funcionalidad"
   ```
4. Haz un **push** a tu repositorio:  
   ```bash
   git push origin nueva-funcionalidad
   ```
5. Crea un **Pull Request** en este repositorio para revisar y fusionar tus cambios.

## Licencia

MIT.