class Libro:
    def __init__(self, titulo: str, autor: str, anio_publicacion: int,
                 estado: str = "disponible"):
        self.titulo = titulo
        self.autor = autor
        self.anio_publicacion = anio_publicacion
        self.estado = estado  

    # Getters y Setters 
    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("El título no puede estar vacío.")
        self._titulo = value.strip()

    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("El autor no puede estar vacío.")
        self._autor = value.strip()

    @property
    def anio_publicacion(self) -> int:
        return self._anio_publicacion

    @anio_publicacion.setter
    def anio_publicacion(self, value: int | str) -> None:
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValueError("El año de publicación debe ser un entero.")
        if value <= 0:
            raise ValueError("El año de publicación debe ser positivo.")
        self._anio_publicacion = value

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("El estado debe ser un string.")
        v = value.strip().lower()
        if v not in ("disponible", "prestado"):
            raise ValueError("Estado inválido: use 'disponible' o 'prestado'.")
        self._estado = v

    #  Comportamiento 
    def prestar(self) -> None:
        if self.estado == "prestado":
            raise ValueError("El libro ya está prestado.")
        self.estado = "prestado"

    def devolver(self) -> None:
        if self.estado == "disponible":
            raise ValueError("El libro ya está disponible.")
        self.estado = "disponible"

    def __str__(self) -> str:
        estado_txt = "Disponible" if self.estado == "disponible" else "Prestado"
        return f"Título: {self.titulo}, Autor: {self.autor}, Año: {self.anio_publicacion}, Estado: {estado_txt}"

    # Utilidades para persistencia 
    def to_dict(self) -> dict:
        return {
            "tipo": "libro",
            "titulo": self.titulo,
            "autor": self.autor,
            "anio": self.anio_publicacion,
            "estado": self.estado,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Libro":
        if data.get("tipo") == "libro_digital":
            return LibroDigital(
                data["titulo"],
                data["autor"],
                int(data["anio"]),
                data.get("formato", "PDF"),
                data.get("estado", "disponible")
            )
        return cls(
            data["titulo"],
            data["autor"],
            int(data["anio"]),
            data.get("estado", "disponible")
        )


class LibroDigital(Libro):
    def __init__(self, titulo: str, autor: str, anio_publicacion: int,
                 formato: str, estado: str = "disponible"):
        super().__init__(titulo, autor, anio_publicacion, estado)
        self.formato = formato

    @property
    def formato(self) -> str:
        return self._formato

    @formato.setter
    def formato(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("El formato no puede estar vacío (ej. 'PDF', 'ePub').")
        self._formato = value.strip()

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base}, Formato: {self.formato}"

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["tipo"] = "libro_digital"
        d["formato"] = self.formato
        return d
    

# gestor_biblioteca.py
import json
from pathlib import Path

class Biblioteca:
    def __init__(self, archivo: str = "biblioteca.txt", autoguardar: bool = True):
        self._ruta = Path(__file__).parent / archivo
        self.autoguardar = autoguardar
        self.libros: list[Libro] = []
        if self._ruta.exists():
            self.cargar()
        else:
            self.libros = [
                Libro("Kitchen", "Banana Yoshimoto", 1988),
                Libro("Amrita", "Banana Yoshimoto", 1994),

                Libro("La casa de las bellas durmientes", "Yasunari Kawabata", 1961),
                Libro("País de nieve", "Yasunari Kawabata", 1947),
                Libro("Lo bello y lo triste", "Yasunari Kawabata", 1964),

                Libro("Una pastelería en Tokio", "Dorian Sukegawa", 2013),

                Libro("Midaregami (Cabello desordenado)", "Yosano Akiko", 1901),
                Libro("Tanka de amor", "Yosano Akiko", 1910),

                Libro("Rashōmon", "Ryunosuke Akutagawa", 1915),
                Libro("En el bosque", "Ryunosuke Akutagawa", 1922),
            ]
            self.guardar() 

    # Persistencia 
    def guardar(self) -> None:
        data = [l.to_dict() for l in self.libros]
        with open(self._ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def cargar(self) -> None:
        try:
            with open(self._ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.libros = [Libro.from_dict(d) for d in data]
        except FileNotFoundError:
            self.libros = []
        except json.JSONDecodeError as e:
            raise ValueError(f"El archivo '{self._ruta.name}' está corrupto o mal formateado: {e}")

    # Operaciones principales 
    def _auto(self):
        if self.autoguardar:
            self.guardar()

    def agregar_libro(self, libro: Libro):
        for l in self.libros:
            if l.titulo.lower() == libro.titulo.lower() and l.autor.lower() == libro.autor.lower():
                raise ValueError("Ya existe un libro con el mismo título y autor.")
        self.libros.append(libro)
        self._auto()

    def eliminar_libro(self, titulo: str):
        for l in self.libros:
            if l.titulo.lower() == titulo.lower():
                self.libros.remove(l)
                self._auto()
                return True
        raise ValueError(f"No se encontró un libro con título '{titulo}'.")

    def listar_libros(self, solo_disponibles: bool = False):
        items = self.libros if not solo_disponibles else [l for l in self.libros if l.estado == "disponible"]
        if not items:
            print("No hay libros para mostrar.")
        else:
            for l in items:
                print(l)

    def buscar_libro(self, titulo: str) -> Libro | None:
        for l in self.libros:
            if l.titulo.lower() == titulo.lower():
                return l
        return None

    def prestar_libro(self, titulo: str):
        libro = self.buscar_libro(titulo)
        if libro is None:
            raise ValueError(f"No se encontró el libro '{titulo}'.")
        libro.prestar()
        self._auto()
        return True

    def devolver_libro(self, titulo: str):
        libro = self.buscar_libro(titulo)
        if libro is None:
            raise ValueError(f"No se encontró el libro '{titulo}'.")
        libro.devolver()
        self._auto()
        return True


# menú

def pedir_int(mensaje: str, minimo: int | None = None) -> int:
    while True:
        dato = input(mensaje).strip()
        try:
            num = int(dato)
            if minimo is not None and num < minimo:
                print(f"⚠️  Debe ser un número >= {minimo}.")
                continue
            return num
        except ValueError:
            print("⚠️  Ingresa un número válido.")


def pedir_str(mensaje: str) -> str:
    while True:
        dato = input(mensaje).strip()
        if dato:
            return dato
        print("⚠️  Este campo no puede estar vacío.")


def menu():
    biblio = Biblioteca(autoguardar=True) 

    while True:
        print("\n--- Gestor de Biblioteca ---")
        print("1. Agregar libro")
        print("2. Eliminar libro")
        print("3. Ver todos los libros")
        print("4. Buscar libro")
        print("5. Marcar libro como prestado")
        print("6. Devolver libro")
        print("7. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            print("\n➕ Agregar libro")
            es_digital = input("¿Es un libro digital? (s/n): ").strip().lower()
            titulo = pedir_str("Título: ")
            autor  = pedir_str("Autor: ")
            anio   = pedir_int("Año de publicación: ", minimo=1)
            estado = input("Estado (disponible/prestado): ").strip().lower() or "disponible"
            try:
                if es_digital == "s":
                    formato = pedir_str("Formato (ej. PDF, ePub): ")
                    libro = LibroDigital(titulo, autor, anio, formato, estado)
                else:
                    libro = Libro(titulo, autor, anio, estado)
                biblio.agregar_libro(libro)
                print("✅ Libro agregado correctamente.")
            except ValueError as e:
                print(f"❌ {e}")

        elif opcion == "2":
            print("\n🗑️  Eliminar libro")
            titulo = pedir_str("Título del libro a eliminar: ")
            try:
                biblio.eliminar_libro(titulo)
                print("✅ Libro eliminado.")
            except ValueError as e:
                print(f"❌ {e}")

        elif opcion == "3":
            print("\n📖 Todos los libros")
            biblio.listar_libros()

        elif opcion == "4":
            print("\n🔎 Buscar libro")
            titulo = pedir_str("Título a buscar: ")
            libro = biblio.buscar_libro(titulo)
            if libro:
                print("✅ Encontrado:")
                print(libro)
            else:
                print("❌ No se encontró ese título.")

        elif opcion == "5":
            print("\n📦 Prestar libro")
            titulo = pedir_str("Título a prestar: ")
            try:
                biblio.prestar_libro(titulo)
                print("✅ Marcado como prestado.")
            except ValueError as e:
                print(f"❌ {e}")

        elif opcion == "6":
            print("\n↩️  Devolver libro")
            titulo = pedir_str("Título a devolver: ")
            try:
                biblio.devolver_libro(titulo)
                print("✅ Marcado como disponible.")
            except ValueError as e:
                print(f"❌ {e}")

        elif opcion == "7":
            print("\n💾 Guardando y saliendo…")
            try:
                biblio.guardar()
            except Exception as e:
                print(f"⚠️  No se pudo guardar automáticamente: {e}")
            print("¡Nos vemos en otras lecturas!")
            break

        else:
            print("⚠️  Opción inválida. Intenta nuevamente.")


if __name__ == "__main__":
    menu()

