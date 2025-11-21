# 🕒 Generador de Turnos - Cafetería

Sistema de generación automática de turnos para cafeterías, desarrollado con Python y Tkinter. Permite la gestión eficiente de horarios para trabajadores Full-Time y Part-Time, considerando la demanda semanal y las restricciones de descanso.

## ✨ Características

- 📊 **Interfaz gráfica moderna** con tema oscuro y diseño intuitivo
- 📁 **Importación desde Excel** de parámetros y demanda semanal
- 🎯 **Asignación automática** de turnos optimizada según demanda
- 👥 **Gestión de trabajadores** Full-Time y Part-Time con reglas específicas
- 📅 **Horarios semanales** individualizados para cada trabajador
- 📥 **Exportación a Excel** con informes formateados y coloreados
- 🔄 **Scrollbars** para navegación fluida en tablas extensas

## 🚀 Instalación

### Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Configuración del entorno

1. **Clonar el repositorio**
```bash
git clone https://github.com/Duridev/app-turnos-funciones-y-matrices.git
cd app-turnos-funciones-y-matrices
```

2. **Crear y activar entorno virtual**
```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat

# Linux/Mac
source .venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install openpyxl numpy
```

## 📖 Uso

### Iniciar la aplicación

```bash
python app.py
```

### Flujo de trabajo

1. **Cargar Excel**: Haz clic en "Cargar Excel" y selecciona el archivo con los parámetros y demanda
2. **Generar Turnos**: Presiona "Generar Turnos" para crear la asignación automática
3. **Exportar**: Usa "Exportar a Excel" para descargar el informe completo

### Formato del archivo Excel de entrada

El archivo Excel debe contener:

| Celda | Contenido |
|-------|-----------|
| C3 | Cantidad de trabajadores Full-Time |
| C4 | Cantidad de trabajadores Part-Time |
| C5 | Tipo de turno (A o B) |

**Demanda semanal** (filas 8-14):

| Fila | Día | C (Mañana) | D (Intermedio) | E (Tarde) |
|------|-----|------------|----------------|-----------|
| 8 | Lunes | # trabajadores | # trabajadores | # trabajadores |
| 9 | Martes | # trabajadores | # trabajadores | # trabajadores |
| ... | ... | ... | ... | ... |

## 🏗️ Estructura del proyecto

```
app-turnos-funciones-y-matrices/
├── app.py                    # Aplicación principal con interfaz gráfica
├── config.py                 # Configuración de estilos y constantes
├── ui_components.py          # Componentes reutilizables de UI
├── main.py                   # Lógica de generación de turnos
├── leer_excel.py            # Lectura de archivos Excel
├── exportar_excel.py        # Exportación de informes a Excel
└── README.md                # Documentación
```

### Descripción de módulos

- **app.py**: Interfaz gráfica principal con Tkinter, gestiona la interacción del usuario
- **config.py**: Centraliza colores, fuentes y constantes de la aplicación
- **ui_components.py**: Define componentes Treeview reutilizables (demanda, turnos, horarios)
- **main.py**: Algoritmo de asignación de turnos y distribución de trabajadores
- **leer_excel.py**: Parseo y validación de datos desde archivos Excel
- **exportar_excel.py**: Generación de informes Excel formateados con múltiples hojas

## 🎨 Capturas de pantalla

La aplicación cuenta con:
- Panel izquierdo: Parámetros y demanda semanal
- Panel derecho: Turnos generados por día
- Panel inferior: Horarios individuales de cada trabajador
- Tema oscuro con alta legibilidad

## 📋 Reglas de asignación

### Trabajadores Full-Time
- Trabajan 6 días a la semana
- Descansan **1 día** del fin de semana (sábado o domingo)
- Primera mitad descansa el sábado
- Segunda mitad descansa el domingo
- Se asignan equitativamente entre todos los turnos

### Trabajadores Part-Time
- Trabajan **solo fines de semana** (sábado y domingo)
- Muestran "-" de lunes a viernes
- Se distribuyen según demanda del fin de semana

## 📤 Formato del informe exportado

El archivo Excel generado contiene 3 hojas:

1. **Resumen General**: Parámetros y demanda semanal
2. **Horario Semanal**: Tabla detallada con asignación por trabajador
   - Colores por turno: Amarillo (Mañana), Verde (Intermedio), Azul (Tarde)
   - Ordenados: Full-Time primero, luego Part-Time
3. **Leyenda**: Explicación de colores y estados

## 🛠️ Tecnologías utilizadas

- **Python 3.x**: Lenguaje de programación principal
- **Tkinter**: Framework de interfaz gráfica
- **NumPy**: Operaciones con matrices para cálculos de asignación
- **OpenPyXL**: Lectura y escritura de archivos Excel con formato

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👤 Autor

**Duridev**
- GitHub: [@Duridev](https://github.com/Duridev)
- Repositorio: [app-turnos-funciones-y-matrices](https://github.com/Duridev/app-turnos-funciones-y-matrices)

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias:
- Abre un [Issue](https://github.com/Duridev/app-turnos-funciones-y-matrices/issues)
- Contacta al autor a través de GitHub

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub
