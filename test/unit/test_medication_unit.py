import pytest
from src.medication import Medication


@pytest.mark.unit
class TestMedicationUnit:
    """Test individual Patient methods in isolation"""

    @pytest.fixture
    def medication_mgr(self):
        return Medication()

    def test_read_interactions(self, medication_mgr):
        """Test: les interactions sont bien lues"""
        result = medication_mgr.interactions_df
        assert result.shape[0] > 2

    def test_prescribe_medication(self, medication_mgr):
        """Test: prescription d'un médicament sans interaction"""
        patient_id = 10
        med_name = "Paracetamol"
        # Prescription sans interaction connue
        result = medication_mgr.prescribe_medication(
            patient_id, med_name, "500mg", "2x/jour"
        )
        assert result is True
        history = medication_mgr.get_medication_history(patient_id)
        assert len(history) == 1
        assert history[0]["name"] == med_name
        assert history[0]["status"] == "active"

    def test_prescribe_medication_with_interaction(self, medication_mgr):
        """Test: prescription avec interaction détectée"""
        patient_id = 20
        # On prescrit d'abord Metformin
        medication_mgr.prescribe_medication(patient_id, "Metformin", "500mg", "2x/jour")
        # Puis Lisinopril qui interagit avec Metformin
        result = medication_mgr.prescribe_medication(
            patient_id, "Lisinopril", "10mg", "1x/jour"
        )
        assert result is False
        history = medication_mgr.get_medication_history(patient_id)
        assert len(history) == 2
        assert history[1]["name"] == "Lisinopril"
        assert history[1]["status"] == "active"
