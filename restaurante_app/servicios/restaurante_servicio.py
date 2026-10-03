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
    # NUEVOS MÉTODOS PARA GESTIÓN DE USUARIOS (Semana 16)
    # ====================================================================

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
        """
        # Validar que el usuario actual sea Administrador
        if usuario_actual is None or usuario_actual.rol != "Administrador":
            raise ValueError("Solo el Administrador puede registrar usuarios.")

        # Validar que no se pueda crear un nuevo Administrador
        if rol.strip() == "Administrador":
            raise ValueError(
                "No se permite crear nuevos Administradores desde la interfaz."
            )

        # Validar que no exista un usuario con la misma identificación
        if self.buscar_usuario(identificacion) is not None:
            raise ValueError("Ya existe un usuario con esa identificacion.")

        nuevo = Usuario(
            identificacion.strip(),
            nombre.strip(),
            correo.strip(),
            usuario.strip(),
            contrasena.strip(),
            rol.strip(),
        )
        self.usuarios.append(nuevo)
        self.guardar_usuarios()
        return nuevo

    def actualizar_usuario(
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
        Actualiza un usuario existente.
        Reglas de negocio:
        - Solo el Administrador puede actualizar usuarios.
        - No se permite cambiar el rol a Administrador.
        """
        # Validar que el usuario actual sea Administrador
        if usuario_actual is None or usuario_actual.rol != "Administrador":
            raise ValueError("Solo el Administrador puede actualizar usuarios.")

        # Validar que no se pueda cambiar el rol a Administrador
        if rol.strip() == "Administrador":
            raise ValueError(
                "No se permite asignar el rol de Administrador desde la interfaz."
            )

        usuario_obj = self.buscar_usuario(identificacion)
        if usuario_obj is None:
            raise ValueError("No existe un usuario con esa identificacion.")

        usuario_obj.nombre = nombre.strip()
        usuario_obj.correo = correo.strip()
        usuario_obj.usuario = usuario.strip()
        usuario_obj.contrasena = contrasena.strip()
        usuario_obj.rol = rol.strip()
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
        """
        # Validar que el usuario actual sea Administrador
        if usuario_actual is None or usuario_actual.rol != "Administrador":
            raise ValueError("Solo el Administrador puede eliminar usuarios.")

        usuario_obj = self.buscar_usuario(identificacion)
        if usuario_obj is None:
            raise ValueError("No existe un usuario con esa identificacion.")

        # No permitir que el administrador se elimine a sí mismo
        if usuario_actual.identificacion == usuario_obj.identificacion:
            raise ValueError(
                "No puede eliminar su propia cuenta de Administrador."
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