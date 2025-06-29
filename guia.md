# Guía de Estilo y Convenciones del Proyecto

## 1. Estructura Común de la Interfaz

1. **Header**  
   - Es idéntico en todas las aplicaciones.

2. **Menú Lateral de Navegación**  
   - Único para cada aplicación.

---

## 2. Iconografía

- Usar [Font Awesome](https://fontawesome.com/icons) para todos los íconos.
- Busca y copia el nombre de la clase correspondiente (por ejemplo, `fa-solid fa-user`).

---

## 3. CSS

### 3.1. Archivos Globales Base  
- **No modificar**:
  - `reset.css`  
  - `root.css`

### 3.2. Archivos Globales Extensibles  
- **Se pueden ampliar** (consultar antes de cambiar lo existente):
  - `colores.css`  
  - `fuentes.css`  
  - `variables.css`  
  - `texto.css`

### 3.3. Componentes Globales  
- Carpeta `componentes/` con estilos para:
  - Header  
  - Footer  
  - Main  
  - Barra lateral  
  - Otros elementos del layout base de cada aplicación (`base.html`)

### 3.4. Selectores y Convenciones  
- **Clases** para estilos generales.  
- **IDs** sólo en casos muy puntuales (p. ej. anclajes o scripts específicos).  
- **Nomenclatura de clases**:
  - Colores y tipografía: ver sección “Reglas de nombres para clases”.
  - Hover:
    - `.hover_color` → cambia el color al pasar el ratón.
    - `.hover_scale` → escala el elemento al pasar el ratón.

---

## 4. Tema Claro / Oscuro

- Archivo: `modo_oscuro.css`.
- Variables principales:
  - `--color-primario` (por defecto, negro): se aplica a texto o íconos que deben invertirse según el tema.
  - `--color-secundario` (por defecto, blanco): contraste de fondo.
- Clases de ejemplo:
  ```html
  <div class="fondo_secundario">
    <p class="color_primario">Texto adaptable al tema</p>
  </div>

---

## 5. Reglas de Nombres para Clases  
*(definidas en `colores.css`)*

- `color_<nombre_del_color>`  
  - Aplica `color: var(--color-<nombre_del_color>);`
- `fondo_<nombre_del_color>`  
  - Aplica `background-color: var(--color-<nombre_del_color>);`

> **Si falta un color**, añade la variable correspondiente en `variables.css` y crea su clase aquí.

---

## 6. Paleta de Colores

**Archivo**: `variables.css`  
**Selector**: `:root`

```css
:root {
  --color-primario:   #000000;
  --color-secundario: #FFFFFF;
  --color-rosa:       #FF69B4;
  /* … demás colores necesarios … */
}
```

Define aquí todos los colores que usarás y luego refiérete a ellos en colores.css.

---

## 7. Javascript

### Convenciones de selección
- Por ID:
```js
const elemento = document.getElementById('miElemento');
```

- Por clase (sólo para estilos dinámicos):
```js
const items = document.getElementsByClassName('miClase');
```

### Archivos globales
- NO modificar:
    - `nav.js` → controla el comportamiento de la navegación lateral
    - `profileMenu.js` → controla el menú de usuario desplegable.

- Pendiente de definir:

    - Validación y formateo de formularios del lado del cliente.

    - Otros comportamientos dinámicos del layout base.

---

## 8. Python / Django

### Convenciones de Nombres

- **Snake case** para variables y funciones:
    ```python
    nombre_de_variable = 42

    def procesar_datos():
        pass
    ```

- **Camel case** solo para clases:
    ```python
    class MiClasePersonalizada(models.Model):
        pass
    ```

### Vistas
- Preferir Class-Based Views (CBV).
- Function-Based Views (FBV) también válidas si el caso lo requiere.

| Archivo / Directorio | Propósito                                | Modificar          |
| -------------------- | ---------------------------------------- | ------------------ |
| `urls.py`            | Define rutas de la app                   | Sí                 |
| `views.py`           | Lógica de las vistas                     | Sí                 |
| `models.py`          | Definición de modelos (tablas)           | Sí                 |
| `admin.py`           | Registro de modelos en el panel de admin | Sí                 |
| `apps.py`            | Identificación de la app                 | **No modificar**   |
| `__init__.py`        | Marca el directorio como paquete Python  | **No eliminar**    |
| `migrations/`        | Contiene migraciones generadas           | Eliminar/regenerar |
