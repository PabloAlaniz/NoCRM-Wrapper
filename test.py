import asyncio
import os
import pytest
from dotenv import load_dotenv
from src.config import NoCRMConfig
from src.models import Lead
from src.repositories import LeadRepository
from datetime import datetime


@pytest.mark.asyncio
async def test_wrapper():
    try:
        # 1. Configuración
        print("1. Inicializando configuración...")
        load_dotenv()
        api_key = os.getenv("NOCRM_API_KEY")
        subdomain = os.getenv("NOCRM_SUBDOMAIN")
        user_id = os.getenv("NOCRM_USER_ID")

        if not api_key or not subdomain or not user_id:
            pytest.skip("NOCRM_API_KEY, NOCRM_SUBDOMAIN o NOCRM_USER_ID no encontrados en .env")

        config = NoCRMConfig(api_key=api_key, subdomain=subdomain)
        print(f"✓ Configuración inicializada con subdominio: {subdomain}")

        # 2. Crear repositorio
        print("\n2. Creando repositorio de leads...")
        lead_repo = LeadRepository(config)
        print("✓ Repositorio creado")

        # 3. Crear un nuevo lead
        print("\n3. Creando nuevo lead...")
        new_lead = Lead(
            title="Test Lead from Wrapper",
            status="new",
            contact_name="John Doe",
            amount=1000.0,
            description="Test lead creation",
            expected_closing_date=datetime.now()
        )
        created_lead = await lead_repo.create(new_lead)
        print(f"✓ Lead creado con ID: {created_lead.id}")

        # 4. Obtener el lead creado
        print("\n4. Obteniendo lead por ID...")
        fetched_lead = await lead_repo.get(created_lead.id)
        print(f"✓ Lead obtenido: {fetched_lead.title}")
        assert fetched_lead.id == created_lead.id

        # 5. Actualizar el lead (solo campos permitidos)
        print("\n5. Actualizando lead...")
        update_lead = Lead(
            title="Updated Test Lead",
            status=fetched_lead.status,  # Mantenemos el status original
            contact_name="Jane Doe",
            amount=2000.0,
            description="Updated description"
        )
        updated_lead = await lead_repo.update(fetched_lead.id, update_lead)
        print(f"✓ Lead actualizado: {updated_lead.title}")
        assert updated_lead.title == "Updated Test Lead"

        # 6. Obtener pipelines disponibles
        print("\n6. Obteniendo pipelines disponibles...")
        pipelines = await lead_repo.list_pipelines()
        print(f"✓ Pipelines disponibles: {len(pipelines)}")

        # 7. Obtener estados disponibles
        print("\n7. Obteniendo estados disponibles...")
        steps = await lead_repo.list_steps()
        print(f"✓ Estados disponibles: {len(steps)}")

        # 8. Asignar el lead
        print("\n8. Asignando lead...")
        assigned_lead = await lead_repo.assign_lead(created_lead.id, int(user_id))
        print(f"✓ Lead asignado a usuario: {user_id}")

        # 9. Cambiar estado del lead
        print("\n9. Cambiando estado del lead...")
        if steps and len(steps) > 0:
            first_step = steps[0]
            status_updated_lead = await lead_repo.change_status(
                id=created_lead.id,
                step_id_or_name=first_step['name']
            )
            print(f"✓ Estado actualizado a: {status_updated_lead.status}")
            assert status_updated_lead is not None

        # 10. Listar leads
        print("\n10. Listando leads...")
        leads = await lead_repo.list()
        print(f"✓ Leads encontrados: {len(leads)}")
        assert isinstance(leads, list)

        # 11. Eliminar lead
        print("\n11. Eliminando lead...")
        deleted = await lead_repo.delete(created_lead.id)
        print(f"✓ Lead eliminado: {deleted}")
        assert deleted is True

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise