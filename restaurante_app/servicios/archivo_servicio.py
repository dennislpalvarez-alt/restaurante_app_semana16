import json
import os


class ArchivoServicio:
    """
    Lee y escribe los archivos locales de productos, usuarios y ventas.
    No conoce reglas de negocio del restaurante.
    """

    def __init__(
        self,
        ruta_productos: str = "datos/productos.json",
        ruta_usuarios: str = "datos/usuarios.json",
        ruta_ventas: str = "datos/ventas.json",
    ) -> None:
        self.ruta_productos: str = ruta_productos
        self.ruta_usuarios: str = ruta_usuarios
        self.ruta_ventas: str = ruta_ventas

    def _leer_json(self, ruta_archivo: str) -> list[dict]:
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            print(f"Aviso: no se encontro el archivo '{ruta_archivo}'.")
            return []
        except json.JSONDecodeError:
            print(f"Aviso: '{ruta_archivo}' no tiene un JSON valido.")
            return []

    def _guardar_json(self, ruta_archivo: str, datos: list[dict]) -> bool:
        carpeta = os.path.dirname(ruta_archivo)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)
        try:
            with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"Error: no hay permisos para escribir '{ruta_archivo}'.")
            return False

    # ---------------- PRODUCTOS ----------------

    def leer_productos(self) -> list[dict]:
        return self._leer_json(self.ruta_productos)

    def guardar_productos(self, productos: list[dict]) -> bool:
        return self._guardar_json(self.ruta_productos, productos)

    # ---------------- USUARIOS ----------------

    def leer_usuarios(self) -> list[dict]:
        return self._leer_json(self.ruta_usuarios)

    def guardar_usuarios(self, usuarios: list[dict]) -> bool:
        """Guarda la lista de usuarios en usuarios.json (Semana 16)."""
        return self._guardar_json(self.ruta_usuarios, usuarios)

    # ---------------- VENTAS (Semana 15) ----------------

    def leer_ventas(self) -> list[dict]:
        """Lee el archivo de ventas y devuelve la lista de diccionarios."""
        return self._leer_json(self.ruta_ventas)

    def guardar_ventas(self, ventas: list[dict]) -> bool:
        """Guarda la lista de ventas en el archivo JSON."""
        return self._guardar_json(self.ruta_ventas, ventas)