import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk


class MainView(tk.Frame):
    """
    Panel principal del restaurante. Organiza la interfaz mediante un
    menu lateral y un area de contenido que cambia segun la seccion
    seleccionada. Toda operacion se delega a RestauranteServicio.
    """

    def __init__(self, master, restaurante_servicio, usuario_actual, al_cerrar_sesion):
        super().__init__(master, bg="#f7fafc")
        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion

        self.contenido = None
        self.etiqueta_estado = None
        self.botones_menu = {}

        self.producto_codigo_entry = None
        self.producto_nombre_entry = None
        self.producto_categoria_entry = None
        self.producto_precio_entry = None
        self.producto_stock_entry = None
        self.tabla_productos = None
        self.tabla_usuarios = None

        # Semana 15: Variables para la sección de Ventas
        self.usuario_venta_combo = None
        self.producto_venta_combo = None
        self.tabla_ventas = None
        self.opciones_usuarios_venta = {}
        self.opciones_productos_venta = {}

        # Semana 15: íconos del menú y de acciones (assets/icons)
        self.iconos = {}
        self.cargar_iconos()

        # Atributos para la gestión de usuarios (Semana 16)
        self.usuario_identificador_entry = None
        self.usuario_nombre_entry = None
        self.usuario_login_entry = None
        self.usuario_contrasena_entry = None
        self.usuario_rol_combo = None
        self.usuario_rol_estado = None
        self.usuario_identificador_seleccionado = None

        self.definir_estilos()
        self.construir_interfaz()

    # ---------------- ICONOS (assets/icons) ----------------
    def cargar_iconos(self):
        """Carga los íconos PNG desde assets/icons/ y conserva su referencia."""
        carpeta_icons = Path(__file__).resolve().parent.parent / "assets" / "icons"
        nombres = {
            "inicio": "icon_inicio.png",
            "usuarios": "icon_usuarios.png",
            "productos": "icon_productos.png",
            "ventas": "icon_ventas.png",
            "agregar": "icon_agregar.png",
            "salir": "icon_salir.png",
        }
        for clave, archivo in nombres.items():
            ruta = carpeta_icons / archivo
            if ruta.exists():
                try:
                    self.iconos[clave] = tk.PhotoImage(file=str(ruta))
                except tk.TclError:
                    self.iconos[clave] = None
            else:
                self.iconos[clave] = None

    # ---------------- ESTILOS ----------------
    def definir_estilos(self):
        self.color_fondo = "#f7fafc"
        self.color_panel = "#ffffff"
        self.color_encabezado = "#1f2a44"
        self.color_texto = "#243447"
        self.color_secundario = "#dbeafe"
        self.color_resaltado = "#2563eb"

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "MenuApp.TButton", background="#334155", foreground="#ffffff",
            font=("Arial", 10, "bold"), padding=(12, 10), borderwidth=0, anchor="w",
        )
        estilo.map("MenuApp.TButton", background=[("active", "#475569")])
        estilo.configure(
            "MenuActivo.TButton", background=self.color_resaltado, foreground="#ffffff",
            font=("Arial", 10, "bold"), padding=(12, 10), borderwidth=0, anchor="w",
        )
        estilo.map("MenuActivo.TButton", background=[("active", "#1d4ed8")])
        estilo.configure(
            "Secundario.TButton", background="#1f2a44", foreground="#ffffff",
            font=("Arial", 10, "bold"), padding=(10, 7), borderwidth=0,
        )
        estilo.map("Secundario.TButton", background=[("active", "#334155")])
        estilo.configure(
            "Accion.TButton", background=self.color_resaltado, foreground="#ffffff",
            font=("Arial", 10, "bold"), padding=(10, 7), borderwidth=0,
        )
        estilo.map("Accion.TButton", background=[("active", "#1d4ed8")])
        estilo.configure(
            "Eliminar.TButton", background="#e11d48", foreground="#ffffff",
            font=("Arial", 10, "bold"), padding=(10, 7), borderwidth=0,
        )
        estilo.map("Eliminar.TButton", background=[("active", "#be123c")])
        estilo.configure(
            "Treeview.Heading", background=self.color_secundario,
            foreground=self.color_encabezado, font=("Arial", 10, "bold"),
        )

    def crear_boton(self, contenedor, texto, comando, estilo, icono=None):
        if icono and self.iconos.get(icono):
            return ttk.Button(
                contenedor, text=texto, command=comando, style=estilo,
                image=self.iconos[icono], compound="left",
            )
        return ttk.Button(contenedor, text=texto, command=comando, style=estilo)

    # ---------------- ESTRUCTURA: MENU LATERAL + CONTENIDO ----------------
    def construir_interfaz(self):
        frame_sidebar = tk.Frame(self, bg=self.color_encabezado, width=215, padx=16, pady=18)
        frame_sidebar.pack(side="left", fill="y")
        frame_sidebar.pack_propagate(False)

        tk.Label(
            frame_sidebar, text="RESTAURANTE", bg=self.color_encabezado,
            fg="#ffffff", font=("Arial", 17, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            frame_sidebar, text=self.usuario_actual.nombre, bg=self.color_encabezado,
            fg="#dbeafe", font=("Arial", 10), wraplength=150, justify="left",
        ).pack(anchor="w", pady=(0, 24))

        self.crear_boton_menu(frame_sidebar, "Inicio", self.mostrar_inicio, "inicio")
        self.crear_boton_menu(frame_sidebar, "Usuarios", self.mostrar_usuarios, "usuarios")
        self.crear_boton_menu(frame_sidebar, "Productos", self.mostrar_productos, "productos")
        self.crear_boton_menu(frame_sidebar, "Ventas", self.mostrar_ventas, "ventas")

        tk.Frame(frame_sidebar, bg=self.color_encabezado).pack(fill="both", expand=True)

        self.crear_boton(
            frame_sidebar, "Cerrar sesion", self.cerrar_sesion, "Eliminar.TButton", "salir"
        ).pack(fill="x", pady=(16, 0))

        frame_principal = tk.Frame(self, bg=self.color_fondo)
        frame_principal.pack(side="left", fill="both", expand=True)

        self.contenido = tk.Frame(frame_principal, bg=self.color_fondo, padx=28, pady=24)
        self.contenido.pack(fill="both", expand=True)

        barra_estado = tk.Frame(frame_principal, bg=self.color_secundario, padx=18, pady=8)
        barra_estado.pack(fill="x", side="bottom")

        self.etiqueta_estado = tk.Label(
            barra_estado, bg=self.color_secundario, fg=self.color_texto, font=("Arial", 10),
        )
        self.etiqueta_estado.pack(side="left")

        self.mostrar_inicio()

    def crear_boton_menu(self, contenedor, texto, comando, icono=None):
        boton = self.crear_boton(contenedor, texto, comando, "MenuApp.TButton", icono)
        boton.pack(fill="x", pady=(0, 8))
        self.botones_menu[texto] = boton

    def marcar_seccion(self, seccion):
        for texto, boton in self.botones_menu.items():
            boton.configure(style="MenuActivo.TButton" if texto == seccion else "MenuApp.TButton")

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def actualizar_barra_estado(self):
        self.etiqueta_estado.config(
            text=(
                f"Productos: {self.restaurante_servicio.cantidad_productos()} | "
                f"Usuarios: {self.restaurante_servicio.cantidad_usuarios()} | "
                f"Ventas: {self.restaurante_servicio.cantidad_ventas()} | "
                "Datos JSON locales"
            )
        )

    # ---------------- INICIO ----------------
    def mostrar_inicio(self):
        self.marcar_seccion("Inicio")
        self.limpiar_contenido()
        self.actualizar_barra_estado()

        tk.Label(
            self.contenido, text="Panel principal", bg=self.color_fondo,
            fg=self.color_encabezado, font=("Arial", 20, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            self.contenido, text="Consulte usuarios y gestione productos desde el menu lateral.",
            bg=self.color_fondo, fg=self.color_texto, font=("Arial", 12),
        ).pack(anchor="w", pady=(0, 22))

        resumen = tk.Frame(self.contenido, bg=self.color_fondo)
        resumen.pack(fill="x")
        self.crear_tarjeta_resumen(resumen, "Usuarios registrados", self.restaurante_servicio.cantidad_usuarios())
        self.crear_tarjeta_resumen(resumen, "Productos registrados", self.restaurante_servicio.cantidad_productos())

    def crear_tarjeta_resumen(self, contenedor, titulo, valor):
        tarjeta = tk.Frame(contenedor, bg=self.color_panel, padx=18, pady=16)
        tarjeta.pack(side="left", fill="x", expand=True, padx=(0, 14))
        tk.Label(
            tarjeta, text=titulo, bg=self.color_panel, fg=self.color_texto, font=("Arial", 10, "bold"),
        ).pack(anchor="w")
        tk.Label(
            tarjeta, text=str(valor), bg=self.color_panel, fg=self.color_resaltado, font=("Arial", 24, "bold"),
        ).pack(anchor="w", pady=(8, 0))

    # ---------------- USUARIOS (Semana 16) ----------------
    def mostrar_usuarios(self):
        """
        Muestra la sección de Usuarios con formulario y Treeview.
        Solo accesible para el Administrador.
        """
         # Validación de rol (Semana 16)
        if self.usuario_actual.rol != "Administrador":
            messagebox.showerror(
                "Usuarios",
                "Solo el Administrador puede acceder a esta sección.",
            )
            self.mostrar_inicio()
            return

        self.marcar_seccion("Usuarios")
        self.limpiar_contenido()

        self.crear_titulo_seccion("Gestión de usuarios")

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        # Formulario de usuario
        formulario = tk.LabelFrame(
            cuerpo,
            text="Datos del usuario",
            bg=self.color_panel,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=14,
            pady=14,
        )
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 18))

        self.usuario_identificador_entry = self.crear_campo(formulario, "Identificador", 0)
        self.usuario_nombre_entry = self.crear_campo(formulario, "Nombre", 1)
        self.usuario_login_entry = self.crear_campo(formulario, "Usuario", 2)
        self.usuario_contrasena_entry = self.crear_campo(
            formulario, "Contraseña", 3, show="*"
        )

        # Combobox para el rol
        tk.Label(
            formulario,
            text="Rol",
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=4, column=0, sticky="w", pady=(0, 8), padx=(0, 10))

        self.usuario_rol_combo = ttk.Combobox(
            formulario,
            values=("Empleado", "Cliente"),
            state="readonly",
            width=25,
        )
        self.usuario_rol_combo.grid(row=4, column=1, sticky="ew", pady=(0, 8))
        self.usuario_rol_combo.set("Cliente")

        # Etiqueta de estado del rol
        self.usuario_rol_estado = tk.Label(
            formulario,
            text="Rol seleccionado: Cliente",
            bg=self.color_panel,
            fg=self.color_texto,
            font=("Arial", 9),
        )
        self.usuario_rol_estado.grid(row=5, column=0, columnspan=2, sticky="w", pady=(0, 8))

        # Botones de acción (command=)
        acciones = tk.Frame(formulario, bg=self.color_panel)
        acciones.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        botones = (
            ("Registrar", self.registrar_usuario, "Accion.TButton"),
            ("Actualizar", self.actualizar_usuario, "Accion.TButton"),
            ("Eliminar", self.eliminar_usuario, "Eliminar.TButton"),
            ("Limpiar", self.limpiar_formulario_usuario, "Secundario.TButton"),
        )
        for texto, comando, estilo in botones:
            self.crear_boton(acciones, texto, comando, estilo).pack(fill="x", pady=(0, 7))

        # Treeview de usuarios (sin mostrar contraseña)
        listado = self.crear_listado(cuerpo, "Usuarios registrados", usar_grid=True)
        self.tabla_usuarios = self.crear_tabla(
            listado,
            ("identificador", "nombre", "usuario", "rol"),
            ("Identificador", "Nombre", "Usuario", "Rol"),
        )

        # Eventos bind() (Semana 16)
        self.tabla_usuarios.bind("<<TreeviewSelect>>", self.al_seleccionar_usuario)
        self.usuario_rol_combo.bind("<Return>", self.al_presionar_enter)
        self.usuario_rol_combo.bind("<<ComboboxSelected>>", self.al_seleccionar_rol)

        for widget in (
            self.usuario_identificador_entry,
            self.usuario_nombre_entry,
            self.usuario_login_entry,
            self.usuario_contrasena_entry,
            self.usuario_rol_combo,
            self.tabla_usuarios,
        ):
            widget.bind("<Escape>", self.al_presionar_escape)

        self.refrescar_usuarios()

    def refrescar_usuarios(self):
        """Actualiza la tabla de usuarios desde el servicio."""
        if self.tabla_usuarios is None:
            return
        self.limpiar_tabla(self.tabla_usuarios)
        for usuario in self.restaurante_servicio.listar_usuarios():
            self.tabla_usuarios.insert(
                "",
                tk.END,
                values=(
                    usuario.identificacion,
                    usuario.nombre,
                    usuario.usuario,
                    usuario.rol,
                ),
            )
        self.actualizar_barra_estado()

    # ---------------- PRODUCTOS (CRUD completo) ----------------
    def mostrar_productos(self):
        self.marcar_seccion("Productos")
        self.limpiar_contenido()

        self.crear_titulo_seccion("Gestion de productos")

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        formulario = tk.LabelFrame(
            cuerpo, text="Datos del producto", bg=self.color_panel, fg=self.color_encabezado,
            font=("Arial", 10, "bold"), padx=14, pady=14,
        )
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 18))

        self.producto_codigo_entry = self.crear_campo(formulario, "Codigo", 0)
        self.producto_nombre_entry = self.crear_campo(formulario, "Nombre", 1)
        self.producto_categoria_entry = self.crear_campo(formulario, "Categoria", 2)
        self.producto_precio_entry = self.crear_campo(formulario, "Precio", 3)
        self.producto_stock_entry = self.crear_campo(formulario, "Stock", 4)

        acciones = tk.Frame(formulario, bg=self.color_panel)
        acciones.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        botones = (
            ("Registrar", self.registrar_producto, "Accion.TButton"),
            ("Cargar por codigo", self.cargar_producto_en_formulario, "Secundario.TButton"),
            ("Actualizar", self.actualizar_producto, "Accion.TButton"),
            ("Eliminar", self.eliminar_producto, "Eliminar.TButton"),
            ("Limpiar", self.limpiar_formulario_producto, "Secundario.TButton"),
        )
        for texto, comando, estilo in botones:
            self.crear_boton(acciones, texto, comando, estilo).pack(fill="x", pady=(0, 7))

        listado = self.crear_listado(cuerpo, "Productos registrados", usar_grid=True)
        self.tabla_productos = self.crear_tabla(
            listado,
            ("codigo", "nombre", "categoria", "precio", "stock"),
            ("Codigo", "Nombre", "Categoria", "Precio", "Stock"),
        )
        self.refrescar_productos()

    def obtener_datos_producto(self):
        return (
            self.producto_codigo_entry.get(),
            self.producto_nombre_entry.get(),
            self.producto_categoria_entry.get(),
            self.producto_precio_entry.get(),
            self.producto_stock_entry.get(),
        )

    def registrar_producto(self):
        try:
            self.restaurante_servicio.registrar_producto(*self.obtener_datos_producto())
            self.limpiar_formulario_producto()
            self.refrescar_productos()
            messagebox.showinfo("Productos", "Producto registrado correctamente.")
        except ValueError as error:
            messagebox.showerror("Productos", str(error))

    def cargar_producto_en_formulario(self):
        producto = self.restaurante_servicio.buscar_producto(self.producto_codigo_entry.get())
        if producto is None:
            messagebox.showerror("Productos", "No existe un producto con ese codigo.")
            return

        self.limpiar_formulario_producto()
        self.producto_codigo_entry.insert(0, producto.codigo)
        self.producto_nombre_entry.insert(0, producto.nombre)
        self.producto_categoria_entry.insert(0, producto.categoria)
        self.producto_precio_entry.insert(0, str(producto.precio))
        self.producto_stock_entry.insert(0, str(producto.stock))

    def actualizar_producto(self):
        try:
            self.restaurante_servicio.actualizar_producto(*self.obtener_datos_producto())
            self.refrescar_productos()
            messagebox.showinfo("Productos", "Producto actualizado correctamente.")
        except ValueError as error:
            messagebox.showerror("Productos", str(error))

    def eliminar_producto(self):
        try:
            self.restaurante_servicio.eliminar_producto(self.producto_codigo_entry.get())
            self.limpiar_formulario_producto()
            self.refrescar_productos()
            messagebox.showinfo("Productos", "Producto eliminado correctamente.")
        except ValueError as error:
            messagebox.showerror("Productos", str(error))

    def limpiar_formulario_producto(self):
        for entrada in (
            self.producto_codigo_entry, self.producto_nombre_entry,
            self.producto_categoria_entry, self.producto_precio_entry, self.producto_stock_entry,
        ):
            entrada.delete(0, tk.END)

    def refrescar_productos(self):
        self.limpiar_tabla(self.tabla_productos)
        for producto in self.restaurante_servicio.listar_productos():
            self.tabla_productos.insert(
                "", tk.END,
                values=(producto.codigo, producto.nombre, producto.categoria, producto.precio, producto.stock),
            )
        self.actualizar_barra_estado()

    # ---------------- VENTAS (Semana 15) ----------------
    def mostrar_ventas(self):
        """Muestra la sección de Ventas con selectores y tabla."""
        self.marcar_seccion("Ventas")
        self.limpiar_contenido()

        self.crear_titulo_seccion("Registro de Ventas")

        cuerpo = tk.Frame(self.contenido, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.grid_columnconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(0, weight=1)

        # Formulario de registro
        formulario = tk.LabelFrame(
            cuerpo, text="Nueva Venta", bg=self.color_panel, fg=self.color_encabezado,
            font=("Arial", 10, "bold"), padx=14, pady=14,
        )
        formulario.grid(row=0, column=0, sticky="n", padx=(0, 18))

        # Selectores (Combobox)
        self.usuario_venta_combo = self.crear_selector_venta(
            formulario, "Usuario", 0, self.obtener_opciones_usuarios_venta()
        )
        self.producto_venta_combo = self.crear_selector_venta(
            formulario, "Producto", 1, self.obtener_opciones_productos_venta()
        )

        # Botón de acción - command= sin paréntesis (Semana 15)
        acciones = tk.Frame(formulario, bg=self.color_panel)
        acciones.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        self.crear_boton(
            acciones, "Registrar venta", self.registrar_venta, "Accion.TButton", "agregar"
        ).pack(fill="x")

        # Tabla de ventas
        listado = self.crear_listado(cuerpo, "Ventas registradas", usar_grid=True)
        self.tabla_ventas = self.crear_tabla(
            listado,
            ("identificador", "usuario", "producto", "fecha"),
            ("ID Venta", "Usuario", "Producto", "Fecha"),
        )
        self.refrescar_ventas()

    def crear_selector_venta(self, contenedor, etiqueta, fila, opciones):
        """Crea un Combobox de solo lectura para seleccionar usuario o producto."""
        tk.Label(
            contenedor, text=etiqueta, bg=self.color_panel, fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))

        selector = ttk.Combobox(
            contenedor, values=list(opciones.keys()), state="readonly", width=34
        )
        selector.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        return selector

    def obtener_opciones_usuarios_venta(self):
        """Genera el diccionario de opciones para el Combobox de Usuarios."""
        self.opciones_usuarios_venta = {
            f"{u.identificacion} - {u.nombre}": u.identificacion
            for u in self.restaurante_servicio.listar_usuarios()
        }
        return self.opciones_usuarios_venta

    def obtener_opciones_productos_venta(self):
        """Genera el diccionario de opciones para el Combobox de Productos."""
        self.opciones_productos_venta = {
            f"{p.codigo} - {p.nombre}": p.codigo
            for p in self.restaurante_servicio.listar_productos()
        }
        return self.opciones_productos_venta

    def registrar_venta(self):
        """
        Callback del botón: obtiene datos, llama al servicio y actualiza UI.
        Flujo: Evento → Callback → Servicio → Persistencia → Respuesta visual
        """
        usuario_seleccionado = self.usuario_venta_combo.get()
        producto_seleccionado = self.producto_venta_combo.get()

        usuario_id = self.opciones_usuarios_venta.get(usuario_seleccionado, "")
        producto_codigo = self.opciones_productos_venta.get(producto_seleccionado, "")

        try:
            self.restaurante_servicio.registrar_venta(usuario_id, producto_codigo)
            self.limpiar_formulario_venta()
            self.refrescar_ventas()
            messagebox.showinfo("Ventas", "Venta registrada correctamente.")
        except ValueError as error:
            messagebox.showerror("Ventas", str(error))

    def limpiar_formulario_venta(self):
        """Limpia los selectores después de registrar."""
        if self.usuario_venta_combo:
            self.usuario_venta_combo.set("")
        if self.producto_venta_combo:
            self.producto_venta_combo.set("")

    def refrescar_ventas(self):
        """Actualiza la tabla Treeview con las ventas actuales."""
        if not self.tabla_ventas:
            return

        self.limpiar_tabla(self.tabla_ventas)
        for venta in self.restaurante_servicio.listar_ventas():
            usuario = self.restaurante_servicio.buscar_usuario(venta.usuario_id)
            producto = self.restaurante_servicio.buscar_producto(venta.producto_codigo)

            texto_usuario = f"{usuario.identificacion} - {usuario.nombre}" if usuario else venta.usuario_id
            texto_producto = f"{producto.codigo} - {producto.nombre}" if producto else venta.producto_codigo

            self.tabla_ventas.insert(
                "", tk.END,
                values=(venta.identificador, texto_usuario, texto_producto, venta.fecha),
            )
        self.actualizar_barra_estado()

    # ---------------- UTILIDADES COMPARTIDAS ----------------
    def crear_titulo_seccion(self, texto):
        tk.Label(
            self.contenido, text=texto, bg=self.color_fondo, fg=self.color_encabezado,
            font=("Arial", 20, "bold"),
        ).pack(anchor="w", pady=(0, 16))

    def crear_campo(self, contenedor, etiqueta, fila, show=None):
        """Crea un campo de entrada con etiqueta. Acepta parámetro 'show' para ocultar texto."""
        tk.Label(
            contenedor, text=etiqueta, bg=self.color_panel, fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))
        entrada = tk.Entry(contenedor, width=28, font=("Arial", 10), show=show)
        entrada.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        return entrada

    def crear_listado(self, contenedor, titulo, usar_grid=False):
        listado = tk.LabelFrame(
            contenedor, text=titulo, bg=self.color_panel, fg=self.color_encabezado,
            font=("Arial", 10, "bold"), padx=12, pady=12,
        )
        if usar_grid:
            listado.grid(row=0, column=1, sticky="nsew")
        else:
            listado.pack(fill="both", expand=True)
        return listado

    def crear_tabla(self, contenedor, columnas, encabezados):
        frame_tabla = tk.Frame(contenedor, bg=self.color_panel)
        frame_tabla.pack(fill="both", expand=True)

        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)
        barra = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=barra.set)

        for columna, encabezado in zip(columnas, encabezados):
            tabla.heading(columna, text=encabezado)
            tabla.column(columna, width=120, anchor="w")

        tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return tabla

    def limpiar_tabla(self, tabla):
        for item in tabla.get_children():
            tabla.delete(item)

    def cerrar_sesion(self):
        self.al_cerrar_sesion()

    # =========================================================================
    # Gestión de usuarios (Semana 16)
    # =========================================================================

    def obtener_datos_usuario(self):
        """Obtiene los datos del formulario de usuario."""
        return (
            self.usuario_identificador_entry.get(),
            self.usuario_nombre_entry.get(),
            self.usuario_login_entry.get(),
            self.usuario_contrasena_entry.get(),
            self.usuario_rol_combo.get(),
        )

    def registrar_usuario(self):
        """Callback del botón Registrar y del evento <Return>."""
        try:
            identificacion, nombre, login, contrasena, rol = self.obtener_datos_usuario()
            self.restaurante_servicio.registrar_usuario(
                identificacion, nombre, "", login, contrasena, rol, self.usuario_actual
            )
            self.limpiar_formulario_usuario()
            self.refrescar_usuarios()
            messagebox.showinfo("Usuarios", "Usuario registrado correctamente.")
        except ValueError as error:
            messagebox.showerror("Usuarios", str(error))

    def actualizar_usuario(self):
        """Callback del botón Actualizar."""
        try:
            identificacion, nombre, login, contrasena, rol = self.obtener_datos_usuario()
            if not identificacion:
                raise ValueError("Debe seleccionar un usuario de la tabla primero.")
            self.restaurante_servicio.actualizar_usuario(
                identificacion, nombre, "", login, contrasena, rol, self.usuario_actual
            )
            self.limpiar_formulario_usuario()
            self.refrescar_usuarios()
            messagebox.showinfo("Usuarios", "Usuario actualizado correctamente.")
        except ValueError as error:
            messagebox.showerror("Usuarios", str(error))

    def eliminar_usuario(self):
        """Callback del botón Eliminar con confirmación."""
        try:
            identificacion = self.usuario_identificador_entry.get().strip()
            if not identificacion:
                raise ValueError("Debe seleccionar un usuario de la tabla primero.")

            confirmar = messagebox.askyesno(
                "Eliminar usuario",
                f"¿Está seguro de eliminar al usuario '{identificacion}'?",
            )
            if not confirmar:
                return

            self.restaurante_servicio.eliminar_usuario(
                identificacion, self.usuario_actual
            )
            self.limpiar_formulario_usuario()
            self.refrescar_usuarios()
            messagebox.showinfo("Usuarios", "Usuario eliminado correctamente.")
        except ValueError as error:
            messagebox.showerror("Usuarios", str(error))

    def limpiar_formulario_usuario(self):
        """Limpia el formulario y cancela la selección del Treeview."""
        if self.usuario_identificador_entry is not None:
            self.usuario_identificador_entry.delete(0, tk.END)
        if self.usuario_nombre_entry is not None:
            self.usuario_nombre_entry.delete(0, tk.END)
        if self.usuario_login_entry is not None:
            self.usuario_login_entry.delete(0, tk.END)
        if self.usuario_contrasena_entry is not None:
            self.usuario_contrasena_entry.delete(0, tk.END)
        if self.usuario_rol_combo is not None:
            self.usuario_rol_combo.set("Cliente")
            self.usuario_rol_combo.configure(values=("Empleado", "Cliente"), state="readonly")
        if self.usuario_rol_estado is not None:
            self.usuario_rol_estado.config(text="Rol seleccionado: Cliente")
        if self.tabla_usuarios is not None:
            self.tabla_usuarios.selection_remove(self.tabla_usuarios.selection())
        self.usuario_identificador_seleccionado = None

    def cargar_usuario_en_formulario(self, usuario):
        """Carga los datos de un usuario en el formulario."""
        self.limpiar_formulario_usuario()
        self.usuario_identificador_seleccionado = usuario.identificacion
        self.usuario_identificador_entry.insert(0, usuario.identificacion)
        self.usuario_nombre_entry.insert(0, usuario.nombre)
        self.usuario_login_entry.insert(0, usuario.usuario)
        self.usuario_contrasena_entry.insert(0, usuario.contrasena)

        # Si es el administrador autenticado, no permitir cambiar su rol
        if (
            usuario.identificacion == self.usuario_actual.identificacion
            and usuario.rol == "Administrador"
        ):
            self.usuario_rol_combo.configure(
                values=("Administrador",), state="disabled"
            )
        else:
            self.usuario_rol_combo.configure(
                values=("Empleado", "Cliente"), state="readonly"
            )
        self.usuario_rol_combo.set(usuario.rol)
        self.actualizar_texto_rol(usuario.rol)

    def al_seleccionar_usuario(self, event):
        """Callback del evento <<TreeviewSelect>>."""
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            return
        valores = self.tabla_usuarios.item(seleccion[0], "values")
        identificador = valores[0]
        usuario = self.restaurante_servicio.buscar_usuario(identificador)
        if usuario is not None:
            self.cargar_usuario_en_formulario(usuario)

    def al_presionar_enter(self, event):
        """Callback del evento <Return>."""
        self.registrar_usuario()

    def al_presionar_escape(self, event):
        """Callback del evento <Escape>."""
        self.limpiar_formulario_usuario()

    def al_seleccionar_rol(self, event):
        """Callback del evento <<ComboboxSelected>>."""
        rol_seleccionado = self.usuario_rol_combo.get()
        self.actualizar_texto_rol(rol_seleccionado)

    def actualizar_texto_rol(self, rol):
        """Actualiza la etiqueta de estado del rol."""
        if self.usuario_rol_estado is not None:
            self.usuario_rol_estado.config(text=f"Rol seleccionado: {rol}")