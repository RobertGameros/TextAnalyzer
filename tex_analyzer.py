import os

# --- CÓDIGOS DE COLOR ANSI ---
# Esta clase almacena secuencias de escape ANSI.
# Al imprimir estos códigos antes de un texto, la terminal cambia el color o formato.
class Color:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m' # RESET es crucial para que el color no se quede "pegado" en el resto de la consola

# --- CLASE PRINCIPAL (OOP) ---
class TextAnalyzer:
    def __init__(self, raw_text: str):
        # Validación inicial: si el texto solo tiene espacios (o está vacío), lanzamos un error.
        if not raw_text.strip():
            raise ValueError("El texto proporcionado está vacío.")

        # Guardamos el estado original y procesamos el texto paso a paso.
        self.original_text = raw_text
        self.normalized_text = self.normalize_text(self.original_text)
        self.tokens = self.tokenize(self.normalized_text)

        # Validación secundaria: si tras limpiar la puntuación nos quedamos sin palabras.
        if not self.tokens:
            raise ValueError("El texto no contiene palabras válidas para analizar.")

        # Inicializamos las estructuras de datos que pide la tarea (Set y Dict)
        self.unique_tokens = set()
        self.counts = {}

    @staticmethod
    def normalize_text(text: str) -> str:
        """Convierte a minúsculas y elimina puntuación y espacios extra."""
        text = text.lower()
        punctuation = ".,;:!?()[]{}\"'"

        # Reemplazamos cada signo de puntuación por un string vacío (lo eliminamos)
        for char in punctuation:
            text = text.replace(char, '')

        # text.split() separa por espacios, ignorando si hay múltiples espacios seguidos.
        # ' '.join() los vuelve a unir, dejando exactamente un espacio entre cada palabra.
        return ' '.join(text.split())

    @staticmethod
    def tokenize(text: str) -> list[str]:
        """Convierte el string normalizado en una lista de palabras (tokens)."""
        return text.split()

    def analyze(self):
        """Genera los conteos y aísla los tokens únicos."""
        # Un 'set' elimina automáticamente los duplicados (ideal para ver palabras únicas)
        self.unique_tokens = set(self.tokens)

        # Llenamos el diccionario. Usamos el método .get(token, 0) que:
        # 1. Busca la palabra. Si existe, trae su valor actual.
        # 2. Si NO existe, devuelve un 0 por defecto. Luego le suma 1.
        for token in self.tokens:
            self.counts[token] = self.counts.get(token, 0) + 1

    def report(self):
        """Calcula métricas avanzadas e imprime el reporte visual."""
        total_tokens = len(self.tokens)
        total_unique = len(self.unique_tokens)

        # Ordenamos el diccionario por sus valores (frecuencia) de mayor a menor.
        # lambda item: item[1] le dice que ordene fijándose en el valor, no en la llave (palabra).
        sorted_tokens = sorted(self.counts.items(), key=lambda item: item[1], reverse=True)
        top_10 = sorted_tokens[:10] # Tomamos solo los primeros 10 elementos (Slicing)

        # Usamos generadores (comprensión) para iterar rápidamente y sacar longitudes
        avg_length = sum(len(t) for t in self.tokens) / total_tokens
        max_len = max(len(t) for t in self.unique_tokens)
        min_len = min(len(t) for t in self.unique_tokens)

        # Listas de comprensión para encontrar TODAS las palabras que empaten en ser las más largas o cortas
        longest = [t for t in self.unique_tokens if len(t) == max_len]
        shortest = [t for t in self.unique_tokens if len(t) == min_len]

        # --- IMPRESIÓN DEL REPORTE (Con formato y colores) ---
        print(f"\n{Color.MAGENTA}{Color.BOLD}╔════════════════════════════════════════════════╗{Color.RESET}")
        print(f"{Color.MAGENTA}{Color.BOLD}║         REPORTE DE ANÁLISIS DE TEXTO           ║{Color.RESET}")
        print(f"{Color.MAGENTA}{Color.BOLD}╚════════════════════════════════════════════════╝{Color.RESET}")
        print(f"{Color.CYAN}▶ Total de tokens:{Color.RESET} {total_tokens}")
        print(f"{Color.CYAN}▶ Tokens únicos:{Color.RESET} {total_unique}")
        print(f"{Color.CYAN}▶ Longitud promedio:{Color.RESET} {avg_length:.2f} caracteres")
        print(f"{Color.CYAN}▶ Palabra(s) más larga(s) ({max_len} letras):{Color.RESET} {', '.join(longest)}")
        print(f"{Color.CYAN}▶ Palabra(s) más corta(s) ({min_len} letras):{Color.RESET} {', '.join(shortest)}")

        print(f"\n{Color.YELLOW}{Color.BOLD}★ Top 10 tokens más frecuentes ★{Color.RESET}")
        for idx, (token, count) in enumerate(top_10, 1): # enumerate(, 1) hace que el índice empiece en 1, no en 0
            print(f"  {Color.GREEN}{idx}.{Color.RESET} '{token}': {count} veces")
        print(f"{Color.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Color.RESET}\n")

    def query(self, word: str):
        """Lógica para consultar las estadísticas de una sola palabra ingresada por el usuario."""
        # Normalizamos la palabra que el usuario buscó por si la escribió con mayúsculas o puntos
        word = self.normalize_text(word)
        total_tokens = len(self.tokens)

        if not word:
            print(f"{Color.RED}⚠ Palabra no válida.{Color.RESET}")
            return

        # Obtenemos la frecuencia del diccionario (0 si la palabra no existe en el texto original)
        freq = self.counts.get(word, 0)
        percentage = (freq / total_tokens) * 100

        # Clasificación con base en los umbrales definidos en el reporte PDF
        classification = f"{Color.RESET}Normal"
        if freq == 1:
            classification = f"{Color.CYAN}Rara{Color.RESET}"
        elif freq >= 5:
            classification = f"{Color.GREEN}Común{Color.RESET}"

        # Imprimimos los resultados
        print(f"\n{Color.BOLD}Resultados para '{word}':{Color.RESET}")
        print(f"  ├─ Frecuencia: {freq} veces")
        print(f"  ├─ Porcentaje: {percentage:.2f}%")
        print(f"  └─ Clasificación: {classification}\n")


# --- FUNCIONES DE I/O E INTERFAZ ---

def print_logo():
    """Imprime un logo ASCII en pantalla al inicio."""
    logo = f"""{Color.CYAN}{Color.BOLD}
  _____         _      _                _                     
 |_   _|____  _| |_   / \   _ __   __ _| |_   _ _______ _ __  
   | |/ _ \ \/ / __| / _ \ | '_ \ / _` | | | | |_  / _ \ '__| 
   | |  __/>  <| |_ / ___ \| | | | (_| | | |_| |/ /  __/ |    
   |_|\___/_/\_\\__/_/   \_\_| |_|\__,_|_|\__, /___\___|_|    
                                          |___/               
    {Color.RESET}"""
    print(logo)

def read_from_file() -> str:
    """Maneja la lectura de un archivo de texto con un bloque try-except."""
    print(f"\n{Color.YELLOW}📂 Modo Archivo{Color.RESET}")
    path = input(f"{Color.BOLD}Ingrese la ruta del archivo .txt:{Color.RESET} ").strip()
    try:
        # Abrimos el archivo en modo lectura ('r') y codificación utf-8 para admitir acentos/eñes
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"{Color.RED}✖ Error: El archivo no fue encontrado. Verifique la ruta.{Color.RESET}")
    except Exception as e:
        print(f"{Color.RED}✖ Error de lectura: {e}{Color.RESET}")
    return ""

def read_from_console() -> str:
    """Permite al usuario pegar múltiples líneas de texto hasta que escriba 'END'."""
    print(f"\n{Color.YELLOW}✍  Modo Consola{Color.RESET}")
    print(f"Pegue su texto abajo. Escriba {Color.RED}'END'{Color.RESET} en una línea nueva para finalizar:\n")
    lines = []
    while True:
        try:
            line = input()
            # Condición de salida para romper el bucle infinito
            if line.strip() == "END":
                break
            lines.append(line)
        except EOFError:
            # Protege contra cierres abruptos de consola (Ctrl+D / Ctrl+Z)
            break
    # Une todas las líneas ingresadas con saltos de línea (\n)
    return "\n".join(lines)

def run_tests():
    """Ejecuta pruebas automáticas usando assert para verificar la lógica básica."""
    print(f"{Color.YELLOW}⚙ Ejecutando pruebas mínimas internas...{Color.RESET}")
    text = "Hola, Mundo!! Python 3. Python es genial."

    # 1. Prueba de normalización
    norm = TextAnalyzer.normalize_text(text)
    assert norm == "hola mundo python 3 python es genial", "Error en normalización"

    # 2. Prueba de tokenización
    tokens = TextAnalyzer.tokenize(norm)
    analyzer = TextAnalyzer(text)
    analyzer.analyze()

    # 3. Prueba de diccionario/conteo
    assert analyzer.counts["python"] == 2, "Error de conteo"

    print(f"{Color.GREEN}✔ Pruebas superadas correctamente.{Color.RESET}\n")

# --- BLOQUE PRINCIPAL ---

def main():
    # Este comando 'vacío' es un truco para habilitar los colores ANSI en consolas antiguas de Windows (cmd)
    os.system("")

    # Ejecutamos las pruebas unitarias al iniciar
    run_tests()

    # Mostramos la interfaz de bienvenida
    print_logo()

    # Menú principal
    print(f"{Color.BOLD}Seleccione el origen de los datos:{Color.RESET}")
    print(f"  {Color.GREEN}1.{Color.RESET} Modo Archivo (.txt)")
    print(f"  {Color.GREEN}2.{Color.RESET} Modo Consola (pegar texto)")

    choice = input(f"\n{Color.BOLD}Opción (1/2):{Color.RESET} ").strip()

    raw_text = ""
    if choice == '1':
        raw_text = read_from_file()
    elif choice == '2':
        raw_text = read_from_console()
    else:
        print(f"{Color.RED}⚠ Opción inválida.{Color.RESET}")
        return # Termina el programa si la opción es incorrecta

    # Bloque try-except principal para atrapar los errores levantados por 'raise ValueError' en la clase
    try:
        # Instanciamos la clase y ejecutamos los métodos principales
        analyzer = TextAnalyzer(raw_text)
        analyzer.analyze()
        analyzer.report()

        # --- BUCLE INTERACTIVO (QUERY) ---
        print(f"{Color.MAGENTA}{Color.BOLD}--- MODO DE CONSULTA INTERACTIVA ---{Color.RESET}")
        print(f"Escriba una palabra para ver sus estadísticas, o {Color.RED}'exit'{Color.RESET} para salir.")

        while True:
            word = input(f"\n{Color.BOLD}🔎 Consultar palabra:{Color.RESET} ").strip()
            if word.lower() == 'exit':
                print(f"{Color.GREEN}¡Hasta luego!{Color.RESET}")
                break
            analyzer.query(word)

    except ValueError as ve:
        # Si el texto estaba vacío, capturamos el error aquí y lo mostramos en rojo
        print(f"{Color.RED}\n✖ Error de validación: {ve}{Color.RESET}")
    except Exception as e:
        # Por si ocurre algún error inesperado, el programa no se caiga bruscamente
        print(f"{Color.RED}\n✖ Ocurrió un error inesperado: {e}{Color.RESET}")

# Esta línea asegura que el código solo se ejecute si se corre este archivo directamente
if __name__ == "__main__":
    main()