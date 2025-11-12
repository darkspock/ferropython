# Análisis de Enlaces y Funcionalidad - Ferrocarril Esp

## Resumen Ejecutivo

Este documento analiza la funcionalidad esperada de los enlaces según la documentación de WordPress (`wp/docs/`) y compara con la implementación actual en Python/FastAPI.

---

## 1. Enlaces en la Página Principal (index.html)

### 1.1 Sección "Líneas" 🚆

#### Según WordPress (`GUIA-COMPLETA.md`):
- **Filtros esperados:**
  - Ancho Ibérico
  - Ancho Métrico
  - Ancho Internacional
  - Otros Anchos
  - Líneas Cerradas

#### Implementación Actual:
- **Enlaces en `templates/index.html`:**
  - `/lines?type=iberico` ✅
  - `/lines?type=metrico` ✅
  - `/lines?type=internacional` ✅
  - `/lines` (Distintos tipos de líneas) ✅
  - `/lines?status=cerrada` ✅

- **Ruta en `main.py`:**
  ```python
  @app.get("/lines", response_class=HTMLResponse)
  async def list_lines(request: Request):
      lines = db.get_lines()
  ```

#### Estado: ⚠️ **PARCIALMENTE IMPLEMENTADO**
- **Problema:** La ruta `/lines` no acepta parámetros de consulta (`type`, `status`)
- **Método `get_lines()` en `database.py`:** No filtra por `type` ni `status`
- **Falta:** Implementar filtrado en la base de datos y en la ruta

---

### 1.2 Sección "Proyectos" 📋

#### Según WordPress:
- **Filtros esperados:**
  - Proyectos Cancelados
  - Proyectos Actuales
  - Proyectos en Marcha
  - Proyectos en Estudio

#### Implementación Actual:
- **Enlaces en `templates/index.html`:**
  - `/projects?status=cancelado` ✅
  - `/projects?status=actual` ✅
  - `/projects?status=en-marcha` ✅
  - `/projects?status=en-estudio` ✅

- **Ruta en `main.py`:**
  ```python
  @app.get("/projects", response_class=HTMLResponse)
  async def list_projects(request: Request):
      projects = db.get_projects()
  ```

#### Estado: ⚠️ **PARCIALMENTE IMPLEMENTADO**
- **Problema:** La ruta `/projects` no acepta parámetros de consulta (`status`)
- **Método `get_projects()` en `database.py`:** No filtra por `status`
- **Falta:** Implementar filtrado por `status` en la base de datos y en la ruta

---

### 1.3 Sección "Desarrollo ciudades" 🏙️

#### Según WordPress:
- **Filtros esperados:**
  - Filtro por ciudad (Bilbao, Sevilla, A Coruña, Valencia, Madrid, Barcelona, etc.)
  - Página de desarrollo de ciudades por ciudad

#### Implementación Actual:
- **Enlaces en `templates/index.html`:**
  - `/cities?name=Bilbao` ✅
  - `/cities?name=Sevilla` ✅
  - `/cities?name=A Coruña` ✅
  - `/cities?name=Valencia` ✅
  - `/cities?name=Madrid` ✅
  - `/cities?name=Barcelona` ✅
  - `/cities` (Ver más ciudades) ✅

- **Ruta en `main.py`:**
  ```python
  @app.get("/cities", response_class=HTMLResponse)
  async def list_cities(request: Request):
      cities = db.get_cities()
  ```

#### Estado: ⚠️ **PARCIALMENTE IMPLEMENTADO**
- **Problema:** La ruta `/cities` no acepta parámetros de consulta (`name`)
- **Método `get_cities()` en `database.py`:** No filtra por nombre de ciudad
- **Falta:** Implementar filtrado por nombre de ciudad y mostrar contenido relacionado (líneas, estaciones, proyectos) de esa ciudad

---

### 1.4 Sección "Estaciones de tren" 🚉

#### Según WordPress:
- **Filtros esperados:**
  - Mapa por provincias
  - Filtro por tipo (Principales, Regionales, Locales)
  - Filtro por ciudad

#### Implementación Actual:
- **Enlaces en `templates/index.html`:**
  - `/stations` (Mapa por provincias) ✅

- **Ruta en `main.py`:**
  ```python
  @app.get("/stations", response_class=HTMLResponse)
  async def list_stations(request: Request):
      stations = db.get_stations()
  ```

#### Estado: ⚠️ **PARCIALMENTE IMPLEMENTADO**
- **Problema:** La ruta `/stations` no acepta parámetros de consulta
- **Falta:** 
  - Implementar mapa por provincias
  - Filtrado por tipo de estación
  - Filtrado por ciudad

---

## 2. Enlaces en el Menú de Navegación (base.html)

### 2.1 Menú "Líneas" (Dropdown)

#### Enlaces actuales:
- `/lines` - Todas las Líneas ✅
- `/lines?type=iberico` - Ancho Ibérico ✅
- `/lines?type=metrico` - Ancho Métrico ✅
- `/lines?type=internacional` - Ancho Internacional ✅
- `/lines?status=cerrada` - Líneas Cerradas ✅

#### Estado: ⚠️ **ENLACES CORRECTOS PERO FUNCIONALIDAD FALTA**
- Los enlaces están bien formados, pero las rutas no procesan los parámetros

---

### 2.2 Menú "Proyectos" (Dropdown)

#### Enlaces actuales:
- `/projects` - Todos los Proyectos ✅
- `/projects?status=cancelado` - Cancelados ✅
- `/projects?status=en-marcha` - En Marcha ✅
- `/projects?status=en-estudio` - En Estudio ✅

#### Estado: ⚠️ **ENLACES CORRECTOS PERO FUNCIONALIDAD FALTA**
- Los enlaces están bien formados, pero las rutas no procesan los parámetros

---

### 2.3 Menú "Curiosidades"

#### Enlace actual:
- `/events` - Curiosidades ✅

#### Estado: ✅ **IMPLEMENTADO**
- La ruta `/events` existe y funciona

---

### 2.4 Menú "Noticias"

#### Enlace actual:
- `/` - Noticias ✅

#### Estado: ✅ **IMPLEMENTADO**
- La página principal muestra las noticias (posts)

---

### 2.5 Menú "Desarrollo ciudades"

#### Enlace actual:
- `/cities` - Desarrollo ciudades ✅

#### Estado: ⚠️ **PARCIALMENTE IMPLEMENTADO**
- La ruta existe pero no muestra contenido específico por ciudad como se espera en WordPress

---

### 2.6 Menú "Estaciones de tren"

#### Enlace actual:
- `/stations` - Estaciones de tren ✅

#### Estado: ⚠️ **PARCIALMENTE IMPLEMENTADO**
- La ruta existe pero falta el mapa por provincias

---

## 3. Estructura de Datos y Modelos

### 3.1 Modelo `Line` (models.py)

#### Campos actuales:
- `id`, `line_number`, `description`, `status`, `cities_served`, `category_id`

#### Según WordPress:
- **Falta:** Campo para tipo de ancho (ibérico, métrico, internacional)
- **Falta:** Relación con categorías para filtrar por tipo

#### Estado: ⚠️ **FALTA CAMPO DE TIPO DE ANCHO**

---

### 3.2 Modelo `Project` (models.py)

#### Campos actuales:
- `id`, `title`, `description`, `project_type`, `budget`, `timeline`, `status`, `category_id`, `city_id`

#### Estado: ✅ **COMPLETO**
- El campo `status` existe y puede usarse para filtrar

---

### 3.3 Modelo `City` (models.py)

#### Campos actuales:
- `id`, `name`, `slug`, `region`, `country`

#### Estado: ✅ **COMPLETO**
- Tiene todos los campos necesarios

---

### 3.4 Modelo `Station` (models.py)

#### Campos actuales:
- `id`, `station_code`, `name`, `address`, `services`, `accessibility`, `city_id`

#### Según WordPress:
- **Falta:** Campo para tipo de estación (Principal, Regional, Local)
- **Falta:** Campo para provincia

#### Estado: ⚠️ **FALTAN CAMPOS DE TIPO Y PROVINCIA**

---

## 4. Métodos de Base de Datos (database.py)

### 4.1 `get_lines()`

#### Estado actual:
```python
def get_lines(self, skip: int = 0, limit: int = 100) -> List[Line]:
    lines = db.query(LineModel).offset(skip).limit(limit).all()
```

#### Falta:
- Parámetro `type` para filtrar por tipo de ancho
- Parámetro `status` para filtrar por estado (cerrada, activa)
- Filtrado por ciudad

---

### 4.2 `get_projects()`

#### Estado actual:
```python
def get_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
    projects = db.query(ProjectModel).offset(skip).limit(limit).all()
```

#### Falta:
- Parámetro `status` para filtrar por estado (cancelado, en-marcha, en-estudio, actual)

---

### 4.3 `get_cities()`

#### Estado actual:
```python
def get_cities(self, skip: int = 0, limit: int = 100) -> List[City]:
    cities = db.query(CityModel).offset(skip).limit(limit).all()
```

#### Falta:
- Parámetro `name` para filtrar por nombre de ciudad
- Método para obtener contenido relacionado (líneas, estaciones, proyectos) de una ciudad

---

### 4.4 `get_stations()`

#### Estado actual:
```python
def get_stations(self, skip: int = 0, limit: int = 100) -> List[Station]:
    stations = db.query(StationModel).offset(skip).limit(limit).all()
```

#### Falta:
- Parámetro `type` para filtrar por tipo de estación
- Parámetro `city_id` para filtrar por ciudad
- Parámetro `province` para filtrar por provincia

---

## 5. Rutas en main.py

### 5.1 Ruta `/lines`

#### Estado actual:
```python
@app.get("/lines", response_class=HTMLResponse)
async def list_lines(request: Request):
    lines = db.get_lines()
```

#### Falta:
- Aceptar parámetros de consulta: `type`, `status`
- Pasar parámetros al método `get_lines()`
- Filtrar resultados según parámetros

---

### 5.2 Ruta `/projects`

#### Estado actual:
```python
@app.get("/projects", response_class=HTMLResponse)
async def list_projects(request: Request):
    projects = db.get_projects()
```

#### Falta:
- Aceptar parámetros de consulta: `status`
- Pasar parámetros al método `get_projects()`
- Filtrar resultados según parámetros

---

### 5.3 Ruta `/cities`

#### Estado actual:
```python
@app.get("/cities", response_class=HTMLResponse)
async def list_cities(request: Request):
    cities = db.get_cities()
```

#### Falta:
- Aceptar parámetros de consulta: `name`
- Si se proporciona `name`, mostrar contenido relacionado (líneas, estaciones, proyectos) de esa ciudad
- Si no se proporciona `name`, mostrar lista de ciudades

---

### 5.4 Ruta `/stations`

#### Estado actual:
```python
@app.get("/stations", response_class=HTMLResponse)
async def list_stations(request: Request):
    stations = db.get_stations()
```

#### Falta:
- Aceptar parámetros de consulta: `type`, `city_id`, `province`
- Implementar mapa por provincias
- Filtrar resultados según parámetros

---

## 6. Resumen de Problemas

### 6.1 Problemas Críticos

1. **Filtrado no implementado:** Ninguna ruta procesa parámetros de consulta
2. **Métodos de base de datos:** No aceptan parámetros de filtrado
3. **Modelo Line:** Falta campo para tipo de ancho
4. **Modelo Station:** Faltan campos para tipo y provincia

### 6.2 Problemas Menores

1. **Página de ciudades:** No muestra contenido relacionado cuando se filtra por ciudad
2. **Mapa de estaciones:** No implementado
3. **Enlaces en menú:** Funcionan pero no filtran

---

## 7. Recomendaciones de Implementación

### 7.1 Prioridad Alta

1. **Agregar campos a modelos:**
   - `Line`: Campo `gauge_type` (ibérico, métrico, internacional)
   - `Station`: Campos `station_type` (principal, regional, local) y `province`

2. **Actualizar métodos de base de datos:**
   - `get_lines(type=None, status=None)`
   - `get_projects(status=None)`
   - `get_cities(name=None)`
   - `get_stations(type=None, city_id=None, province=None)`

3. **Actualizar rutas en main.py:**
   - Aceptar parámetros de consulta
   - Pasar parámetros a métodos de base de datos
   - Filtrar resultados

### 7.2 Prioridad Media

1. **Página de desarrollo de ciudades:**
   - Mostrar líneas, estaciones y proyectos relacionados cuando se filtra por ciudad

2. **Mapa de estaciones:**
   - Implementar visualización por provincias

### 7.3 Prioridad Baja

1. **Mejoras de UX:**
   - Mensajes cuando no hay resultados
   - Contadores de resultados
   - Paginación en listados filtrados

---

## 8. Ejemplo de Implementación Sugerida

### 8.1 Actualizar modelo Line

```python
# En database.py, agregar campo gauge_type a LineModel
gauge_type = Column(String(50))  # 'iberico', 'metrico', 'internacional'
```

### 8.2 Actualizar método get_lines()

```python
def get_lines(self, skip: int = 0, limit: int = 100, 
              gauge_type: Optional[str] = None, 
              status: Optional[str] = None) -> List[Line]:
    db = self.get_db()
    try:
        query = db.query(LineModel)
        if gauge_type:
            query = query.filter(LineModel.gauge_type == gauge_type)
        if status:
            query = query.filter(LineModel.status == status)
        lines = query.offset(skip).limit(limit).all()
        # ... resto del código
```

### 8.3 Actualizar ruta /lines

```python
@app.get("/lines", response_class=HTMLResponse)
async def list_lines(
    request: Request,
    type: Optional[str] = None,
    status: Optional[str] = None
):
    lines = db.get_lines(gauge_type=type, status=status)
    return templates.TemplateResponse(
        "lines.html",
        {
            "request": request,
            "lines": lines,
            "is_admin": is_authenticated(request),
            "filter_type": type,
            "filter_status": status,
        },
    )
```

---

## 9. Conclusión

Los enlaces están correctamente formados en los templates HTML, pero **la funcionalidad de filtrado no está implementada** en las rutas ni en los métodos de base de datos. Es necesario:

1. Agregar campos faltantes a los modelos
2. Actualizar métodos de base de datos para aceptar parámetros de filtrado
3. Actualizar rutas para procesar parámetros de consulta
4. Implementar funcionalidades específicas (mapa de estaciones, página de desarrollo de ciudades)

**Estado general:** ⚠️ **ENLACES CORRECTOS, FUNCIONALIDAD PARCIAL**

---

*Última actualización: Diciembre 2024*

