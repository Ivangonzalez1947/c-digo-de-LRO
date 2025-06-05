class LRUPageReplacer:
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.frames = []          # Marcos de memoria
        self.recent_use = []      # Orden de uso reciente (más antiguo -> más reciente)
        self.page_faults = 0      # Contador de fallos de página
        self.history = []         # Historial de estados para visualización

    def access_page(self, page):
        """Accede a una página, actualizando el estado según LRU"""
        status = ""
        if page in self.frames:
            # Hit: la página ya está en memoria
            self.recent_use.remove(page)
            self.recent_use.append(page)
            status = f"Referencia {page}: ✅ Hit (Pagina en memoria)"
        else:
            # Page fault: la página no está en memoria
            self.page_faults += 1
            if len(self.frames) < self.num_frames:
                # Hay espacio libre en los marcos
                self.frames.append(page)
                self.recent_use.append(page)
                status = f"Referencia {page}: ❌ Miss (Agregado a marco libre)"
            else:
                # Reemplazo LRU: eliminar página menos usada recientemente
                lru_page = self.recent_use.pop(0)
                idx = self.frames.index(lru_page)
                self.frames[idx] = page
                self.recent_use.append(page)
                status = f"Referencia {page}: ❌ Miss (Reemplazando a la pagina {lru_page})"
        
        # Guardar estado actual para historial
        self.history.append({
            "page": page,
            "frames": list(self.frames),
            "recent_use": list(self.recent_use),
            "status": status
        })
    
    def simulate(self, references):
        """Ejecuta una simulación completa con una secuencia de referencias"""
        for page in references:
            self.access_page(page)
    
    def print_history(self):
        """Imprime el historial de la simulación"""
        print(f"{'Referencia':<10} | {'Marcos':<20} | {'Orden LRU':<20} | {'Estado'}")
        print("-" * 70)
        for entry in self.history:
            # Completar con espacios si hay marcos vacíos
            frames_display = str(entry['frames'])
            if len(entry['frames']) < self.num_frames:
                frames_display = str(entry['frames'] + ['-'] * (self.num_frames - len(entry['frames'])))
            
            print(f"{entry['page']:<10} | {frames_display:<20} | {str(entry['recent_use']):<20} | {entry['status']}")
        
        print("\n" + "=" * 70)
        print(f"Total de fallos de página: {self.page_faults}")

def main():
    """Función principal con interfaz de usuario"""
    print("SIMULADOR DE ALGORITMO LRU PARA REEMPLAZO DE PÁGINAS")
    print("=" * 70)
    
    # Obtener número de marcos
    while True:
        try:
            num_frames = int(input("\nIngrese el número de marcos disponibles (1-10): "))
            if 1 <= num_frames <= 10:
                break
            else:
                print("Por favor ingrese un número entre 1 y 10")
        except ValueError:
            print("Entrada inválida. Intente nuevamente.")
    
    # Obtener secuencia de referencias
    print("\nIngrese la secuencia de referencias (números separados por espacios)")
    print("Ejemplo: 7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1")
    while True:
        try:
            references = list(map(int, input("Secuencia: ").split()))
            if references:
                break
            else:
                print("Secuencia no puede estar vacía")
        except ValueError:
            print("Solo se permiten números enteros. Intente nuevamente.")
    
    # Crear y ejecutar simulador LRU
    lru_simulator = LRUPageReplacer(num_frames)
    lru_simulator.simulate(references)
    
    # Mostrar resultados
    print("\n" + "=" * 70)
    print("RESULTADOS DE LA SIMULACIÓN")
    print(f"Secuencia de referencias: {references}")
    print(f"Número de marcos: {num_frames}")
    print("=" * 70 + "\n")
    lru_simulator.print_history()
    
    # Estadísticas adicionales
    total_references = len(references)
    hit_count = total_references - lru_simulator.page_faults
    fault_percentage = (lru_simulator.page_faults / total_references) * 100
    hit_percentage = (hit_count / total_references) * 100
    
    print("\nESTADÍSTICAS:")
    print(f"Total de referencias: {total_references}")
    print(f"Total de hits: {hit_count} ({hit_percentage:.2f}%)")
    print(f"Total de fallos: {lru_simulator.page_faults} ({fault_percentage:.2f}%)")
    print("=" * 70)

if __name__ == "__main__":
    main()