# TextAnalyzer

# 📝 Analizador de Texto CLI

Una herramienta de línea de comandos (CLI) interactiva desarrollada en Python para el análisis léxico y estadístico de textos. El programa procesa cadenas de texto, las limpia, extrae métricas detalladas e incluye una interfaz de consultas en tiempo real.

## ✨ Características Principales

* **Dos modos de entrada:** Permite analizar archivos `.txt` locales o pegar texto directamente en la consola.
* **Normalización de texto:** Convierte todo a minúsculas, elimina signos de puntuación comunes y suprime espacios extra sin depender de librerías externas.
* **Reporte estadístico detallado:**
  * Conteo de tokens totales y únicos.
  * Cálculo de longitud promedio de palabras.
  * Identificación de las palabras más largas y más cortas (manejando empates).
  * Top 10 de palabras más frecuentes.
* **Modo de Consulta Interactiva:** Permite buscar palabras específicas dentro del texto analizado para conocer su frecuencia absoluta, porcentaje de aparición y clasificación (*Rara*, *Normal* o *Común*).
* **Interfaz de Usuario Nativa:** Utiliza Códigos de Escape ANSI y Arte ASCII para ofrecer una experiencia visual rica (colores y maquetación) sin requerir la instalación de dependencias de terceros.
* **Pruebas integradas:** Incluye un test unitario básico automatizado que se ejecuta al inicio para asegurar que la lógica de normalización y conteo funciona correctamente.

## 🚀 Requisitos

* **Python 3.x** instalado en tu sistema.
* No se requieren librerías externas. El programa utiliza puramente la biblioteca estándar de Python (módulo `os`).

## 🛠️ Cómo utilizarlo

1. Clona este repositorio o descarga el archivo `.py` (ej. `text_analyzer.py`).
2. Abre tu terminal o línea de comandos.
3. Navega hasta el directorio donde guardaste el archivo.
4. Ejecuta el script con el siguiente comando:

   ```bash
   python text_analyzer.py
