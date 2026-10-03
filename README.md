# Restaurante App — Semana 16

## Propósito
Cuarta y última iteración del proyecto restaurante_app, evolucionando la interfaz gráfica construida con Tkinter. Esta semana se enfoca en el manejo explícito de eventos mediante bind(), aplicándolo al contexto de la gestión de usuarios. El objetivo es demostrar cómo una interfaz reactiva puede detectar diferentes formas de interacción (selección de fila, teclas, cambios de opción) sin trasladar la lógica de negocio hacia la vista.

## Novedades — Semana 16

### Evolución de la gestión de usuarios
- Modelo Usuario actualizado: se incorpora el atributo rol con valores permitidos: Administrador, Empleado y Cliente.
- Formulario mejorado: incluye campos de identificador, nombre, usuario, contraseña (oculta con show="*") y un Combobox para seleccionar el rol.
- Treeview de consulta: muestra únicamente identificador, nombre, usuario y rol. No expone la contraseña por seguridad visual.
- Control de acceso: solo el usuario con rol Administrador puede acceder a la gestión de usuarios.

### Manejo de eventos con bind()
Se implementan cuatro eventos específicos, diferenciándolos del uso de command= en los botones:

- <<TreeviewSelect>> en Treeview de usuarios: Carga automáticamente el usuario seleccionado en el formulario
- <Return> en Combobox de rol: Confirma el registro del usuario (atajo de teclado)
- <Escape> en formulario completo: Limpia el formulario y cancela la selección
- <<ComboboxSelected>> en Combobox de rol: Actualiza la etiqueta de estado al cambiar el rol

### Reutilización de command=
Los botones principales (Registrar, Actualizar, Eliminar, Limpiar) mantienen su asociación mediante command=, conservando el mecanismo trabajado en la Semana 15 y permitiendo comparar ambos enfoques.

### Reglas de negocio en el servicio
- Solo el Administrador puede gestionar usuarios.
- Se pueden crear usuarios tipo Empleado y Cliente.
- No se permite crear nuevos Administradores desde la interfaz.
- El administrador autenticado no puede eliminar su propia cuenta.
- Todas las validaciones y la persistencia se delegan a RestauranteServicio.

### Recursos visuales
- Se conserva la carpeta assets/ con el logotipo del sistema (logo.png) e iconos para la interfaz (icon_inicio.png, icon_usuarios.png, icon_productos.png, icon_ventas.png, icon_agregar.png, icon_salir.png).

## Estructura del proyecto

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
│   │   ── ventas.json
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

## Responsabilidades por capa

- modelos/usuario.py: representa la entidad Usuario, incorporando el atributo rol con validación contra ROLES_PERMITIDOS.
- servicios/restaurante_servicio.py: concentra las reglas de negocio, valida el rol del usuario autenticado, impide crear nuevos Administradores y bloquea la auto-eliminación. Gestiona la persistencia en usuarios.json.
- ui/main_view.py: construye las vistas con Tkinter, asocia eventos mediante bind() y botones mediante command=. Coordina la interacción sin manipular directamente los archivos JSON.
- main.py: crea la ventana principal Tk(), configura el ícono desde assets/logo/logo.png y controla el cambio entre LoginView y MainView.

## Flujo de la aplicación y manejo de eventos

Inicio de la aplicación
        |
main.py prepara Tkinter, carga el icono y los servicios
        |
   LoginView (validación de acceso)
        |
    MainView (menú lateral)
        |
Navegación: Inicio | Usuarios (solo Admin) | Productos (CRUD) | Ventas
        |
--- FLUJO DE EVENTOS EN USUARIOS (Semana 16) ---
1. Administrador accede a la sección "Usuarios"
2. Selecciona una fila en el Treeview
3. Evento <<TreeviewSelect>> activa callback al_seleccionar_usuario()
4. Callback obtiene el identificador y consulta RestauranteServicio
5. Los datos se cargan automáticamente en el formulario
6. El usuario modifica un campo y presiona "Actualizar" (command=)
        |
--- ATAJOS DE TECLADO ---
• <Return> en el Combobox de rol → ejecuta registrar_usuario()
• <Escape> en cualquier campo → limpia formulario y cancela selección
        |
--- CAMBIO DE ROL ---
• <<ComboboxSelected>> → actualiza la etiqueta "Rol seleccionado: ..."
---------------------------------
        |
   Cerrar sesión
        |
   LoginView

## Cómo ejecutar

1. Ubicarse dentro de la carpeta restaurante_app:
   cd restaurante_app

2. Ejecutar el punto de entrada:
   python main.py

3. Iniciar sesión con el usuario administrador cargado en datos/usuarios.json:
   - Usuario: jperez
   - Contraseña: 1234

4. Navegar al menú lateral "Usuarios" para probar la gestión con eventos.

5. Cerrar y volver a abrir la aplicación para verificar que los usuarios se recuperan correctamente desde usuarios.json.

## Requisitos técnicos

- Python 3.8 o superior
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