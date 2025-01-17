import pytest
from datetime import datetime
from nocrm_wrapper.models import Lead

@pytest.mark.integration
@pytest.mark.asyncio
async def test_lead_workflow(lead_repository, user_id):
    """Test del flujo completo de trabajo con leads"""
    created_lead = None
    try:
        # 1. Crear un nuevo lead
        print("\n1. Creando nuevo lead...")
        new_lead = Lead(
            title="Test Lead from Wrapper",
            status="new",
            contact_name="John Doe",
            amount=1000.0,
            description="Test lead creation",
            expected_closing_date=datetime.now()
        )
        created_lead = await lead_repository.create(new_lead)
        print(f"✓ Lead creado con ID: {created_lead.id}")

        # 2. Obtener el lead creado
        print("\n2. Obteniendo lead por ID...")
        fetched_lead = await lead_repository.get(created_lead.id)
        print(f"✓ Lead obtenido: {fetched_lead.title}")
        assert fetched_lead.id == created_lead.id

        # 3. Actualizar el lead (solo campos permitidos)
        print("\n3. Actualizando lead...")
        update_lead = Lead(
            title="Updated Test Lead",
            status=fetched_lead.status,  # Mantenemos el status original
            contact_name="Jane Doe",
            amount=2000.0,
            description="Updated description"
        )
        updated_lead = await lead_repository.update(fetched_lead.id, update_lead)
        print(f"✓ Lead actualizado: {updated_lead.title}")
        assert updated_lead.title == "Updated Test Lead"

        # 4. Obtener pipelines disponibles
        print("\n4. Obteniendo pipelines disponibles...")
        pipelines = await lead_repository.list_pipelines()
        print(f"✓ Pipelines disponibles: {len(pipelines)}")
        assert len(pipelines) > 0

        # 5. Obtener estados disponibles
        print("\n5. Obteniendo estados disponibles...")
        steps = await lead_repository.list_steps()
        print(f"✓ Estados disponibles: {len(steps)}")
        assert len(steps) > 0

        # 6. Asignar el lead
        print("\n6. Asignando lead...")
        assigned_lead = await lead_repository.assign_lead(created_lead.id, user_id)
        print(f"✓ Lead asignado a usuario: {user_id}")
        assert assigned_lead is not None

        # 7. Cambiar estado del lead
        print("\n7. Cambiando estado del lead...")
        if steps and len(steps) > 0:
            first_step = steps[0]
            status_updated_lead = await lead_repository.change_status(
                id=created_lead.id,
                step_id_or_name=first_step['name']
            )
            print(f"✓ Estado actualizado a: {status_updated_lead.status}")
            assert status_updated_lead is not None

        # 8. Listar leads
        print("\n8. Listando leads...")
        leads = await lead_repository.list()
        print(f"✓ Leads encontrados: {len(leads)}")
        assert isinstance(leads, list)
        assert len(leads) > 0

    except Exception as e:
        print(f"\n❌ Error durante el test: {str(e)}")
        raise

    finally:
        # Limpieza: Asegurar que el lead se elimine incluso si el test falla
        if created_lead:
            try:
                print("\n9. Limpieza - Eliminando lead...")
                deleted = await lead_repository.delete(created_lead.id)
                print(f"✓ Lead eliminado: {deleted}")
                assert deleted is True
            except Exception as e:
                print(f"\n❌ Error durante la limpieza: {str(e)}")
                raise