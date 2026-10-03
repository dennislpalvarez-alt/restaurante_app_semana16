from datetime import date
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    def __init__(self, archivo_servicio) -> None:
        self.archivo_servicio = archivo_servicio
        self.productos: list[Producto] = []
        self.usuarios: list[Usuario] = []
        self.ventas: list[Venta] = []
        self.cargar_datos()

    def cargar_datos(self) -> None:
        productos_json = self.archivo_servicio.leer_productos()
        usuarios_json = self.archivo_servicio.leer_usuarios()
        ventas_json = self.archivo_servicio.leer_ventas()

        self.productos = [Producto.desde_diccionario(d) for d in productos_json]
        self.usuarios = [Usuario.desde_diccionario(d) for d in usuarios_json]
        self.ventas = [
            Venta(
                d.get("identificador", ""),
                d.get("usuario_id", ""),
                d.get("producto_codigo", ""),
                d.get("fecha", ""),
            )
            for d in ventas_json
        ]

    def validar_acceso(self, usuario: str, contrasena: str) -> Usuario | None:
        for u in self.usuarios:
            if u.usuario == usuario and u.contrasena == contrasena:
                return u
        return None

    def listar_productos(self) -> list[Producto]:
        return self.productos

    def listar_usuarios(self) -> list[Usuario]:
        return self.usuarios

    def listar_ventas(self) -> list[Venta]:
        return self.ventas

    def cantidad_productos(self) -> int:
        return len(self.productos)

    def cantidad_usuarios(self) -> int:
        return len(self.usuarios)

    def cantidad_ventas(self) -> int:
        return len(self.ventas)

    def buscar_producto(self, codigo: str) -> Producto | None:
        for producto in self.productos:
            if producto.codigo == codigo.strip():
                return producto
        return None

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        for usuario in self.usuarios:
            if usuario.identificacion == identificacion.strip():
                return usuario
        return None

    def registrar_producto(
        self, codigo: str, nombre: str, categoria: str, precio: str, stock: str
    ) -> Producto:
        if self.buscar_producto(codigo) is not None:
            raise ValueError("Ya existe un producto con ese codigo.")
        nuevo = Producto(
            codigo.strip(),
            nombre.strip(),
            categoria.strip(),
            self._a_float(precio),
            self._a_int(stock),
        )
        self.productos.append(nuevo)
        self.guardar_productos()
        return nuevo

    def actualizar_producto(
        self, codigo: str, nombre: str, categoria: str, precio: str, stock: str
    ) -> Producto:
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise ValueError("No existe un producto con ese codigo.")
        producto.nombre = nombre.strip()
        producto.categoria = categoria.strip()
        producto.precio = self._a_float(precio)
        producto.stock = self._a_int(stock)
        self.guardar_productos()
        return producto

    def eliminar_producto(self, codigo: str) -> Producto:
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise ValueError("No existe un producto con ese codigo.")
        self.productos.remove(producto)
        self.guardar_productos()
        return producto

    def guardar_productos(self) -> None:
        self.archivo_servicio.guardar_productos(
            [p.a_diccionario() for p in self.productos]
        )

    def generar_identificador_venta(self) -> str:
        return f"V{len(self.ventas) + 1:03d}"

    def registrar_venta(self, usuario_id: str, producto_codigo: str) -> Venta:
        usuario_id = usuario_id.strip()
        producto_codigo = producto_codigo.strip()
        if not usuario_id:
            raise ValueError("Debe seleccionar un usuario.")
        if not producto_codigo:
            raise ValueError("Debe seleccionar un producto.")
        if self.buscar_usuario(usuario_id) is None:
            raise ValueError("El usuario seleccionado no existe.")
        if self.buscar_producto(producto_codigo) is None:
            raise ValueError("El producto seleccionado no existe.")

        nueva_venta = Venta(
            self.generar_identificador_venta(),
            usuario_id,
            producto_codigo,
            date.today().isoformat(),
        )
        self.ventas.append(nueva_venta)
        self.guardar_ventas()
        return nueva_venta

    def guardar_ventas(self) -> None:
        datos = [
            {
                "identificador": v.identificador,
                "usuario_id": v.usuario_id,
                "producto_codigo": v.producto_codigo,
                "fecha": v.fecha,
            }
            for v in self.ventas
        ]
        self.archivo_servicio.guardar_ventas(datos)

    # ====================================================================
    # GESTIÓN DE USUARIOS (Semana 16)
    # ====================================================================

    def buscar_usuario_por_login(self, login: str) -> Usuario | None:
        """Busca un usuario por su nombre de usuario (el que se usa para entrar)."""
        for usuario in self.usuarios:
            if usuario.usuario == login.strip():
                return usuario
        return None

    def validar_administrador(self, usuario_actual: Usuario | None, accion: str) -> None:
        """Regla de acceso: solo el Administrador gestiona usuarios."""
        if usuario_actual is None or usuario_actual.rol != "Administrador":
            raise ValueError(f"Solo el Administrador puede {accion} usuarios.")

    def usuario_tiene_ventas(self, identificacion: str) -> bool:
        return any(v.usuario_id == identificacion for v in self.ventas)

    def registrar_usuario(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        usuario: str,
        contrasena: str,
        rol: str,
        usuario_actual: Usuario | None = None,
    ) -> Usuario:
        """
        Registra un nuevo usuario.
        Reglas de negocio:
        - Solo el Administrador puede registrar usuarios.
        - No se permite crear nuevos Administradores desde la interfaz.
        - No se repite la identificación ni el nombre de usuario (login).
        """
        self.validar_administrador(usuario_actual, "registrar")

        if rol.strip() == "Administrador":
            raise ValueError(
                "No se permite crear nuevos Administradores desde la interfaz."
            )

        nuevo = Usuario(
            identificacion.strip(),
            nombre.strip(),
            correo.strip(),
            usuario.strip(),
            contrasena.strip(),
            rol.strip(),
        )

        if self.buscar_usuario(nuevo.identificacion) is not None:
            raise ValueError("Ya existe un usuario con esa identificacion.")
        if self.buscar_usuario_por_login(nuevo.usuario) is not None:
            raise ValueError("Ya existe un usuario con ese nombre de usuario.")

        self.usuarios.append(nuevo)
        self.guardar_usuarios()
        return nuevo

    def actualizar_usuario(
        self,
        identificacion: str,
        nombre: str,
        correo: str | None,
        usuario: str,
        contrasena: str,
        rol: str,
        usuario_actual: Usuario | None = None,
    ) -> Usuario:
        """
        Actualiza un usuario existente.
        Reglas de negocio:
        - Solo el Administrador puede actualizar usuarios.
        - Nadie puede recibir el rol Administrador desde la interfaz; la cuenta
          administradora existente sí puede editar sus datos conservando su rol.
        - No se repite el nombre de usuario (login) de otra cuenta.
        - Si correo es None se conserva el correo que ya tenía el usuario.
        """
        self.validar_administrador(usuario_actual, "actualizar")

        usuario_obj = self.buscar_usuario(identificacion)
        if usuario_obj is None:
            raise ValueError("No existe un usuario con esa identificacion.")

        rol = rol.strip()
        if usuario_obj.rol == "Administrador":
            # La cuenta administradora no puede perder su rol.
            if rol != "Administrador":
                raise ValueError("No puede cambiar el rol de la cuenta Administrador.")
        elif rol == "Administrador":
            raise ValueError(
                "No se permite asignar el rol de Administrador desde la interfaz."
            )

        # Se valida todo con un objeto temporal antes de modificar el real.
        datos_validados = Usuario(
            usuario_obj.identificacion,
            nombre,
            usuario_obj.correo if correo is None else correo,
            usuario,
            contrasena,
            rol,
        )
        otro = self.buscar_usuario_por_login(datos_validados.usuario)
        if otro is not None and otro.identificacion != usuario_obj.identificacion:
            raise ValueError("Ya existe otro usuario con ese nombre de usuario.")

        usuario_obj.nombre = datos_validados.nombre
        usuario_obj.correo = datos_validados.correo
        usuario_obj.usuario = datos_validados.usuario
        usuario_obj.contrasena = datos_validados.contrasena
        usuario_obj.rol = datos_validados.rol
        self.guardar_usuarios()
        return usuario_obj

    def eliminar_usuario(
        self, identificacion: str, usuario_actual: Usuario | None = None
    ) -> Usuario:
        """
        Elimina un usuario.
        Reglas de negocio:
        - Solo el Administrador puede eliminar usuarios.
        - No se permite eliminar la propia cuenta del Administrador autenticado.
        - No se elimina un usuario que ya tiene ventas registradas.
        """
        self.validar_administrador(usuario_actual, "eliminar")

        usuario_obj = self.buscar_usuario(identificacion)
        if usuario_obj is None:
            raise ValueError("No existe un usuario con esa identificacion.")

        if usuario_actual.identificacion == usuario_obj.identificacion:
            raise ValueError("No puede eliminar su propia cuenta de Administrador.")
        if usuario_obj.rol == "Administrador":
            raise ValueError("No se puede eliminar una cuenta de Administrador.")
        if self.usuario_tiene_ventas(usuario_obj.identificacion):
            raise ValueError(
                "No se puede eliminar: el usuario tiene ventas registradas."
            )

        self.usuarios.remove(usuario_obj)
        self.guardar_usuarios()
        return usuario_obj

    def guardar_usuarios(self) -> None:
        self.archivo_servicio.guardar_usuarios(
            [u.a_diccionario() for u in self.usuarios]
        )

    @staticmethod
    def _a_float(valor: str) -> float:
        try:
            return float(valor)
        except ValueError:
            raise ValueError("El precio debe ser un numero valido.")

    @staticmethod
    def _a_int(valor: str) -> int:
        try:
            return int(valor)
        except ValueError:
            raise ValueError("El stock debe ser un numero entero valido.")