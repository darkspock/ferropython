# Migración de Base de Datos - Agregar Columnas Faltantes

## Problema
Las columnas `gauge_type` (en tabla `lines`) y `station_type`, `province` (en tabla `stations`) no existen en la base de datos, causando errores al intentar filtrar.

## Solución

### Opción 1: Ejecutar Migración de Alembic (Recomendado)

Si el contenedor Docker está corriendo:
```bash
docker-compose exec blog_app alembic upgrade head
```

Si estás ejecutando localmente:
```bash
alembic upgrade head
```

### Opción 2: Ejecutar SQL Directamente

Si Alembic no está disponible, ejecuta estos comandos SQL directamente en tu base de datos MySQL:

```sql
-- Agregar gauge_type a la tabla lines
ALTER TABLE `lines` ADD COLUMN `gauge_type` VARCHAR(50) NULL AFTER `status`;

-- Agregar station_type y province a la tabla stations
ALTER TABLE `stations` ADD COLUMN `station_type` VARCHAR(50) NULL AFTER `accessibility`;
ALTER TABLE `stations` ADD COLUMN `province` VARCHAR(100) NULL AFTER `station_type`;
```

### Verificación

Después de ejecutar la migración, verifica que las columnas existen:

```sql
DESCRIBE lines;
DESCRIBE stations;
```

Deberías ver:
- En `lines`: columna `gauge_type`
- En `stations`: columnas `station_type` y `province`

## Nota

El archivo SQL también está disponible en `add_missing_columns.sql` para referencia.

