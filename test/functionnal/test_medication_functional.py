import pytest
from src.medication import Medication


@pytest.mark.functional
class TestMedicationFunctional:

    def test_prescribe_medication_functional(self):
        """Test fonctionnel: prescription d'un médicament sans interaction"""
        medication_mgr = Medication()
        patient_id = 100
        med_name = "Paracetamol"
        result = medication_mgr.prescribe_medication(
            patient_id, med_name, "500mg", "2x/jour"
        )
        assert result is True
        history = medication_mgr.get_medication_history(patient_id)
        assert len(history) == 1
        assert history[0]["name"] == med_name
        assert history[0]["status"] == "active"
