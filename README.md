# NoCRM API Wrapper

Un wrapper modular y estructurado para la API de NoCRM, implementado en Python siguiendo principios SOLID y arquitectura N-tier.

## Características

- ✨ Implementación completa de operaciones CRUD para leads
- 🏗️ Arquitectura N-tier con clara separación de responsabilidades
- 🎯 Diseño basado en principios SOLID
- 🚀 Operaciones asíncronas para mejor rendimiento
- 🔒 Manejo robusto de errores
- 📝 Validación de datos en múltiples capas
- 🔍 Tipado estático
- 🧪 Tests unitarios y de integración

## Estructura del Proyecto

```
nocrm_wrapper/
├── src/
│   ├── __init__.py
│   ├── nocrm_client.py           # Cliente principal
│   │
│   ├── config/                   # Configuración
│   │   ├── __init__.py
│   │   └── config.py
│   │
│   ├── exceptions/               # Excepciones personalizadas
│   │   ├── __init__.py
│   │   └── nocrm_exceptions.py
│   │
│   ├── models/                   # Modelos de datos
│   │   ├── __init__.py
│   │   └── lead.py
│   │
│   ├── repositories/             # Capa de acceso a datos
│   │   ├── __init__.py
│   │   ├── base_repository.py
│   │   └── lead_repository.py
│   │
│   └── services/                 # Capa de lógica de negocio
│       ├── __init__.py
│       ├── base_service.py
│       └── lead_service.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Configuración de tests
│   │
│   ├── test_integration/        # Tests de integración
│   │   ├── __init__.py
│   │   └── test_workflow.py
│   │
│   └── test_unit/              # Tests unitarios
│       ├── __init__.py
│       ├── test_models.py
│       ├── test_repositories.py
│       └── test_services.py
```

## Arquitectura

### 1. Capa de Modelos (Models)
- Definición de entidades de negocio
- Validación de datos
- Serialización/Deserialización
- Ejemplo: `Lead`

### 2. Capa de Repositorios (Repositories)
- Acceso a datos
- Operaciones CRUD básicas
- Manejo de peticiones HTTP
- Ejemplo: `LeadRepository`

### 3. Capa de Servicios (Services)
- Lógica de negocio
- Validaciones complejas
- Operaciones compuestas
- Ejemplo: `LeadService`

### 4. Capa de Excepciones (Exceptions)
- Manejo de errores específicos
- Jerarquía de excepciones
- Ejemplo: `NoCRMValidationError`

## Requisitos

- Python 3.8 o superior
- NoCRM API Key
- Dependencias listadas en requirements.txt

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/PabloAlaniz/NoCRM-Wrapper.git
cd nocrm-wrapper
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales:
# NOCRM_API_KEY=tu_api_key
# NOCRM_SUBDOMAIN=tu_subdominio
# NOCRM_USER_ID=tu_user_id
```

## Uso

### Como Biblioteca Python

1. **Configuración Básica**:
```python
from src.config import NoCRMConfig
from src.nocrm_client import NoCRMClient

config = NoCRMConfig(
    api_key="tu_api_key",
    subdomain="tu_subdominio"
)
client = NoCRMClient(config)
```

2. **Operaciones con Leads**:
```python
# Crear lead
new_lead = Lead(
    title="Nueva Oportunidad",
    status="new",
    contact_name="John Doe",
    amount=10000.0
)
created_lead = await client.lead_service.create_lead(new_lead)

# Obtener lead
lead = await client.lead_service.get_lead(created_lead.id)

# Actualizar lead
lead.amount = 15000.0
updated_lead = await client.lead_service.update_lead(lead.id, lead)

# Procesar lead (asignar y cambiar estado)
processed_lead = await client.lead_service.process_lead(
    id=lead.id,
    user_id=123,
    step_name="Contactado"
)

# Búsqueda avanzada
leads = await client.lead_service.search_leads(
    status="new",
    min_amount=5000,
    max_amount=20000,
    date_from=datetime.now() - timedelta(days=30)
)
```

## Testing

### Configuración de Tests
1. Configurar variables de entorno para testing:
```bash
cp .env.example .env.test
# Editar .env.test con credenciales de prueba
```

2. Ejecutar tests:
```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_integration/  # Solo integración
pytest tests/test_unit/        # Solo unitarios
pytest -v                      # Modo verbose
pytest -s                      # Con print statements
```

## Características Detalladas

### Manejo de Errores
```python
try:
    lead = await client.lead_service.get_lead(999)
except NoCRMValidationError as e:
    print(f"Error de validación: {e}")
except NoCRMAuthenticationError as e:
    print(f"Error de autenticación: {e}")
except NoCRMAPIError as e:
    print(f"Error de API: {e}")
```

### Validaciones
- Título obligatorio (mínimo 3 caracteres)
- Monto no negativo
- Probabilidad entre 0 y 100
- Fecha de cierre no en el pasado

### Operaciones Compuestas
```python
# Procesar lead completo
status = await client.lead_service.get_lead_pipeline_status(lead_id)
print(f"Pipeline: {status['current_pipeline']['name']}")
print(f"Paso actual: {status['current_step']['name']}")
```

## Buenas Prácticas

1. **Uso de Tipos**:
- Usar tipado estático
- Definir tipos genéricos cuando sea apropiado
- Documentar tipos en docstrings

2. **Manejo de Errores**:
- Usar excepciones específicas
- Propagar errores apropiadamente
- Documentar posibles excepciones

3. **Testing**:
- Escribir tests unitarios
- Incluir tests de integración
- Usar fixtures de pytest
- Mantener tests independientes

4. **Documentación**:
- Documentar todas las clases y métodos
- Incluir ejemplos de uso
- Mantener README actualizado
