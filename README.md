# Restaurante App — Semana 16

## Propósito
Cuarta iteración del proyecto **restaurante_app**, evolucionando la interfaz gráfica construida con **Tkinter**.
Esta semana se enfoca en el **manejo explícito de eventos mediante `bind()`**, aplicado a la **gestión de usuarios** del restaurante. El objetivo es demostrar cómo una interfaz reactiva detecta diferentes interacciones (selección de una fila, teclas, cambio de opción) sin trasladar la lógica de negocio a la vista.

## Novedades — Semana 16

### Gestión de usuarios con roles
- **Modelo `Usuario`**: incorpora el atributo `rol`, con los valores permitidos **Administrador**, **Empleado** y **Cliente**, persistido en `datos/usuarios.json`.
- **CRUD completo** desde la interfaz: registrar, consultar, actualizar y eliminar usuarios.
- **Formulario**: identificador, nombre, usuario, contraseña (oculta con `show="*"`) y un `ttk.Combobox` para el rol.
- **Treeview**: muestra únicamente identificador, nombre, usuario y rol. La contraseña nunca aparece en la tabla.
- **Control de acceso**: solo el Administrador ve y puede usar la sección **Usuarios**. Para un Empleado o un Cliente el botón no aparece en el menú lateral.

### Roles utilizados
| Rol | Secciones del menú | Gestión de usuarios |
|---|---|---|
| Administrador | Inicio, Usuarios, Productos, Ventas | Sí: gestiona usuarios Empleado y Cliente |
| Empleado | Inicio, Productos, Ventas | No |
| Cliente | Inicio, Productos, Ventas | No |

### Manejo de eventos: `command=` y `bind()`
- **`command=`** asocia la *acción principal* de un botón con un método. El callback no recibe el objeto `event`. Se mantiene en **Registrar, Actualizar, Eliminar y Limpiar**.
- **`bind()`** asocia un *evento específico* de un widget con un callback, que recibe el objeto `event`. Todos los bindings son **locales** a su widget; no se usa `bind_all()`.

| Evento | Widget | Callback | Respuesta |
|---|---|---|---|
| `<<TreeviewSelect>>` | Treeview de usuarios | `al_seleccionar_usuario(event)` | Obtiene el identificador, consulta el usuario en `RestauranteServicio` y lo carga en el formulario (la fila queda resaltada) |
| `<Return>` | Campos del formulario y Combobox de rol | `al_presionar_enter(event)` | Reutiliza `registrar_usuario()`, el mismo método del botón Registrar |
| `<Escape>` | Campos del formulario, Combobox y Treeview | `al_presionar_escape(event)` | Limpia el formulario, cancela la selección y devuelve el foco al primer campo |
| `<<ComboboxSelected>>` | Combobox de rol | `al_seleccionar_rol(event)` | Actualiza la etiqueta "Rol seleccionado: ..." |

Los callbacks **no duplican lógica**: el atajo `<Return>` y el botón Registrar ejecutan el mismo método. El callback coordina (lee la interfaz, llama al servicio, refresca la tabla, muestra el resultado) y no contiene reglas de negocio.

### Reglas de negocio (en `RestauranteServicio`)
- Solo el Administrador puede registrar, actualizar y eliminar usuarios.
- No se permite crear nuevos Administradores desde la interfaz.
- No se repiten la identificación ni el nombre de usuario (login).
- El Administrador puede editar su propia cuenta, pero no puede cambiar su rol.
- El Administrador autenticado no puede eliminar su propia cuenta.
- No se elimina un usuario que ya tiene ventas registradas, para no dejar ventas huérfanas.
- Al actualizar un usuario se conserva el correo que ya tenía.
- La interfaz nunca lee ni escribe los archivos JSON directamente.

### Recursos visuales (`assets/`)
- `assets/logo/logo.png`: logotipo del sistema, cargado como ícono de la ventana.
- `assets/icons/`: íconos de la interfaz (`icon_inicio`, `icon_usuarios`, `icon_productos`, `icon_ventas`, `icon_agregar`, `icon_salir`), usados en el menú lateral y en los botones de acción.

## Estructura del proyecto

```text
restaurante_app_semana16/
├── restaurante_app/
│   ├── assets/
│   │   ├── icons/
│   │   │   ├── icon_inicio.png
│   │   │   ├── icon_usuarios.png
│   │   │   ├── icon_productos.png
│   │   │   ├── icon_ventas.png
│   │   │   ├── icon_agregar.png
│   │   │   └── icon_salir.png
│   │   └── logo/
│   │       └── logo.png
│   ├── datos/
│   │   ├── productos.json
│   │   ├── usuarios.json
│   │   └── ventas.json
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── producto.py
│   │   ├── usuario.py
│   │   └── venta.py
│   ├── servicios/
│   │   ├── __init__.py
│   │   ├── archivo_servicio.py
│   │   └── restaurante_servicio.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── login_view.py
│   │   └── main_view.py
│   └── main.py
└── README.md
```

## Responsabilidades por capa

- **`modelos/usuario.py`**: entidad `Usuario` con el atributo `rol`, validado contra los roles permitidos.
- **`servicios/archivo_servicio.py`**: lee y guarda los archivos JSON de productos, usuarios y ventas, sin lógica de negocio.
- **`servicios/restaurante_servicio.py`**: concentra las reglas de negocio de usuarios, productos y ventas, y gestiona la persistencia.
- **`ui/main_view.py`**: construye las vistas con Tkinter, asocia eventos con `bind()` y botones con `command=`, y coordina la interacción sin tocar el JSON.
- **`main.py`**: crea la ventana `Tk()`, configura el ícono desde `assets/logo/logo.png` y alterna entre `LoginView` y `MainView`.

## Flujo de la aplicación y manejo de eventos

```text
Inicio de la aplicación
        |
main.py prepara Tkinter, carga el icono y los servicios
        |
LoginView (validación de acceso con RestauranteServicio)
        |
MainView (menú lateral según el rol)
        |
Inicio | Usuarios (solo Administrador) | Productos | Ventas
        |
--- EVENTOS EN LA SECCIÓN USUARIOS ---
Treeview  -> <<TreeviewSelect>> -> bind() -> callback(event)
          -> obtiene el identificador -> RestauranteServicio busca el usuario
          -> la interfaz carga el formulario

Teclado   -> <Return>           -> bind() -> callback(event) -> registrar_usuario()
Teclado   -> <Escape>           -> bind() -> callback(event) -> limpiar formulario y selección
Combobox  -> <<ComboboxSelected>> -> bind() -> callback(event) -> responde al cambio de rol
Botones   -> command= -> callback -> Registrar / Actualizar / Eliminar / Limpiar
        |
RestauranteServicio valida y guarda en usuarios.json
        |
Actualización del Treeview y respuesta visual (messagebox)
        |
Cerrar sesión -> LoginView
```

## Cómo ejecutar

1. Ubicarse dentro de la carpeta `restaurante_app`:

```bash
cd restaurante_app
```

2. Ejecutar el punto de entrada:

```bash
python main.py
```

3. Iniciar sesión con alguno de los usuarios cargados en `datos/usuarios.json`:

| Rol | Usuario | Contraseña |
|---|---|---|
| Administrador | `jperez` | `1234` |
| Empleado | `cmesero` | `emp123` |
| Cliente | `lcliente` | `cli123` |

4. Con el Administrador, abrir **Usuarios** en el menú lateral y probar: seleccionar una fila, registrar con el botón o con **Enter**, limpiar con **Escape**, cambiar el rol, actualizar y eliminar.
5. Entrar con el Empleado o el Cliente y comprobar que el menú **no muestra** la sección Usuarios.
6. Cerrar y volver a abrir la aplicación para verificar que los usuarios se recuperan desde `usuarios.json`.

## Requisitos técnicos
- Python 3.10 o superior (el código usa anotaciones como `Usuario | None`)
- Tkinter (incluido con la instalación estándar de Python)

## Referencias
Estructura y flujo adaptados y evolucionados de los proyectos docentes Biblioteca App:
- Semana 13: https://github.com/kevin10lascano-sketch/Clase-Semana-13-POO.git
- Semana 14: https://github.com/kevin10lascano-sketch/Clase-Semana-14-POO.git
- Semana 15: https://github.com/kevin10lascano-sketch/Clase-Semana-15-POO.git
- Semana 16: https://github.com/kevin10lascano-sketch/Clase-Semana-16-POO.git
- Semana 16.1 (Explorador de eventos): https://github.com/kevin10lascano-sketch/Clase-Semana-16.1-POO.git

## Autor
Dennis Leonardo Pacheco Álvarez — Proyecto académico de Programación Orientada a Objetos.