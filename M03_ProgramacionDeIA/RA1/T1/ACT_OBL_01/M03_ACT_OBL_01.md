# EJERCICIO 5

## Objetivo del proyecto

Crear una aplicación multiplataforma que permita a los usuarios construir y mantener hábitos saludables a través de un sistema de recompensas, combinando tecnología, datos de salud e integraciones de inteligencia artificial.

## Características principales

- Creación de rutinas personalizadas (ejercicio, nutrición, bienestar)
- Recordatorios inteligentes basados en horarios, ubicación y comportamiento
- Visualización del progreso mediante gráficos y métricas
- Sistema de competición entre usuarios (opcional)
- Recompensas con descuentos y promociones
- Integración con wearables
- Recomendaciones personalizadas mediante IA

---

## Metodología Scrum

### Product Owner
- Representar a clientes y stakeholders
- Priorizar el Product Backlog
- Proponer mejoras basadas en feedback
- Gestionar patrocinadores y promociones

### Scrum Master
- Facilitar el proceso Scrum
- Eliminar impedimentos
- Fomentar comunicación y autonomía del equipo

### Equipo de Desarrollo
- Implementación del producto
- Decisiones técnicas y arquitectura
- Testing, corrección de errores y optimización

---

## Plan de Sprints

### Sprint 1: Fundamentos y sistema de usuarios
**Duración:** 2 semanas

**Historias de usuario:**
- Arquitectura base
- Registro y autenticación
- Onboarding
- Navegación principal
- Base de datos de usuarios

**MVP:**
- Login/registro funcional
- Navegación básica operativa

---

### Sprint 2: Creación de rutinas
**Duración:** 2 semanas

**Historias de usuario:**
- CRUD de rutinas
- Biblioteca de ejercicios
- Categorías
- Perfil de usuario
- Guardado de rutinas

**MVP:**
- Gestión completa de rutinas

---

### Sprint 3: Recordatorios y seguimiento
**Duración:** 2 semanas

**Historias de usuario:**
- Notificaciones push
- Calendario
- Registro de rutinas completadas
- Dashboard con estadísticas
- Gráficas de progreso
- Sistema de logros

---

## Eventos Scrum

### Daily Stand-up
- Duración: 15 min
- Preguntas clave:
  - ¿Qué hice ayer?
  - ¿Qué haré hoy?
  - ¿Bloqueos?

**Importancia:**
- Sincronización
- Detección temprana de problemas

---

### Sprint Review
- Duración: 2 horas
- Demo del producto
- Feedback de stakeholders
- Ajuste del backlog

---

### Sprint Retrospective
- Duración: 1.5 horas
- Evaluación del sprint
- Mejora continua

---

# EJERCICIO 6

## Propósito del programa

StoreManager es un sistema de gestión de inventario para pequeñas tiendas, orientado a optimizar el control de stock y mejorar la toma de decisiones basada en datos.

---

## Funcionalidades principales

- Gestión de stock
- Alertas de bajo inventario
- Análisis de ventas
- Generación de informes

---

## Estructura del programa

### 1. Módulo de Inventario
- CRUD de productos
- Control de stock
- Categorías
- Proveedores

### 2. Módulo de Alertas
- Monitorización de stock
- Notificaciones
- Umbrales configurables

### 3. Módulo de Ventas
- Registro de ventas
- Actualización de inventario
- Historial
- Análisis

### 4. Módulo de Informes
- Reportes
- Rotación de productos
- Exportación de datos

---

## Interrelación entre módulos

- Inventario ↔ Alertas  
- Ventas --> Inventario  
- Ventas --> Informes  
- Inventario --> Informes  
- Alertas --> Informes  

---

## Flujo de trabajo

1. Usuario inicia sesión
2. Accede al dashboard
3. Realiza una venta:
   - Consulta inventario
   - Registra transacción
   - Actualiza stock
   - Genera alerta si es necesario
4. Genera informe:
   - Consulta datos de ventas e inventario
   - Calcula rotación
   - Exporta informe

---

## Plan de implementación

### Etapa 1: Requisitos (2 semanas)
- Entrevistas
- Casos de uso
- Historias de usuario

---

### Etapa 2: Diseño (3 semanas)
- Modelo de datos
- Arquitectura (MVC)
- Wireframes

---

### Etapa 3: Implementación (8 semanas)
- Sprint 1-2: Inventario
- Sprint 3-4: Ventas
- Sprint 5: Alertas
- Sprint 6-7: Informes
- Sprint 8: Integración

---

### Etapa 4: Pruebas (3 semanas)
- Unitarias
- Integración
- Sistema
- Aceptación

---

### Etapa 5: Despliegue (2 semanas)
- Configuración producción
- Instalación piloto
- Formación de usuarios