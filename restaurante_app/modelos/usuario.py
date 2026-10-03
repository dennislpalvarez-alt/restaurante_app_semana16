class Usuario:
    """
    Clase que representa un usuario del restaurante.
    Incorpora el atributo 'rol' para diferenciar entre Administrador, Empleado y Cliente.
    """

    ROLES_PERMITIDOS = ("Administrador", "Empleado", "Cliente")

    def __init__(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        usuario: str,
        contrasena: str,
        rol: str = "Empleado",
    ) -> None:
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

    @staticmethod
    def validar_texto(valor: str, campo: str) -> str:
        if not valor or not valor.strip():
            raise ValueError(f"El campo {campo} no puede estar vacío.")
        return valor.strip()

    @property
    def identificacion(self) -> str:
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        self._identificacion = self.validar_texto(valor, "identificación")

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self._nombre = self.validar_texto(valor, "nombre")

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        # El correo es opcional, no se valida si está vacío
        self._correo = valor.strip() if valor else ""

    @property
    def usuario(self) -> str:
        return self._usuario

    @usuario.setter
    def usuario(self, valor: str) -> None:
        self._usuario = self.validar_texto(valor, "usuario")

    @property
    def contrasena(self) -> str:
        return self._contrasena

    @contrasena.setter
    def contrasena(self, valor: str) -> None:
        self._contrasena = self.validar_texto(valor, "contraseña")

    @property
    def rol(self) -> str:
        return self._rol

    @rol.setter
    def rol(self, valor: str) -> None:
        rol_validado = self.validar_texto(valor, "rol")
        if rol_validado not in self.ROLES_PERMITIDOS:
            raise ValueError(
                f"El rol '{rol_validado}' no es válido. "
                f"Los roles permitidos son: {', '.join(self.ROLES_PERMITIDOS)}"
            )
        self._rol = rol_validado

    def a_diccionario(self) -> dict:
        """Convierte el objeto Usuario a un diccionario para persistencia JSON."""
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "rol": self.rol,
        }

    @classmethod
    def desde_diccionario(cls, datos: dict) -> "Usuario":
        """Crea un objeto Usuario desde un diccionario (lectura de JSON)."""
        return cls(
            identificacion=datos.get("identificacion", ""),
            nombre=datos.get("nombre", ""),
            correo=datos.get("correo", ""),
            usuario=datos.get("usuario", ""),
            contrasena=datos.get("contrasena", ""),
            rol=datos.get("rol", "Empleado"),
        )