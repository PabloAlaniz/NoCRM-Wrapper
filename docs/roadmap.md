# Roadmap — NoCRM-Wrapper

> Última actualización: 2026-02-20

## ✅ Implementado

### Core
- **CRUD de Leads** — Create, Read, Update, Delete completo
- **Arquitectura N-tier** — Separación clara: Models → Repositories → Services
- **Tipado estático** — Type hints en todo el codebase
- **Validaciones de negocio** — Título mínimo, montos no negativos, probabilidad 0-100%, fechas válidas

### Pipeline Management
- **List pipelines** — Obtener pipelines disponibles
- **List steps** — Obtener estados del pipeline
- **Pipeline status** — Info completa del lead en su pipeline actual

### Operaciones Avanzadas
- **Assign lead** — Asignar lead a usuario
- **Change status** — Cambiar estado del lead
- **Process lead** — Operación compuesta (asignar + cambiar estado)
- **Search leads** — Búsqueda con filtros (status, monto, fechas)

### Infraestructura
- **Tests unitarios** — Models, repositories, services
- **Tests de integración** — Workflow completo
- **CI/CD** — GitHub Actions (lint + tests)
- **setup.py** — Instalable via pip

## 🚧 En progreso

*Sin items en progreso actualmente.*

## 📋 Backlog

- [ ] **Publicación en PyPI** — Disponibilizar como `pip install nocrm-wrapper`
- [ ] **CI estricto** — Remover `continue-on-error` de lint y tests
- [ ] **Coverage reporting** — Agregar badge y reporte de cobertura
- [ ] **Requirements-dev.txt** — Separar deps de desarrollo

## 💡 Ideas

- **Más recursos de NoCRM** — Users, Activities, Custom Fields, Teams
- **Async context manager** — `async with NoCRMClient(...) as client:`
- **Rate limiting** — Manejo de límites de la API
- **Retry logic** — Reintentos automáticos con backoff
- **Documentación Sphinx/MkDocs** — Docs generados del código
- **Caché de pipelines/steps** — Evitar requests repetidos

---
*Generado por Brújula 🧭*
