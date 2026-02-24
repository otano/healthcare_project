import pytest
from src.medication import Medication


@pytest.mark.unit
class TestMedicationUnit:
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

    def test_get_medication_history(self, medication_mgr):
        """Test: récupération de l'historique des prescriptions"""
        patient_id = 30
        # Historique vide au départ
        assert medication_mgr.get_medication_history(patient_id) == []
        # Ajout d'une prescription
        medication_mgr.prescribe_medication(patient_id, "Ibuprofen", "200mg", "1x/jour")
        history = medication_mgr.get_medication_history(patient_id)
        assert len(history) == 1
        assert history[0]["name"] == "Ibuprofen"
        assert history[0]["dosage"] == "200mg"
        assert history[0]["frequency"] == "1x/jour"
        assert history[0]["status"] == "active"

    def test_stop_medication(self, medication_mgr):
        """Test: arrêt d'un médicament pour un patient"""
        patient_id = 40
        med_name = "Aspirin"
        # Prescription initiale
        medication_mgr.prescribe_medication(patient_id, med_name, "100mg", "1x/jour")
        # Arrêt du médicament
        result = medication_mgr.stop_medication(patient_id, med_name)
        assert result is True
        history = medication_mgr.get_medication_history(patient_id)
        assert len(history) == 1
        assert history[0]["name"] == med_name
        assert history[0]["status"] == "stopped"
        # Arrêt d'un médicament non prescrit
        result2 = medication_mgr.stop_medication(patient_id, "NonExistant")
        assert result2 is False

    def test_get_active_medications(self, medication_mgr):
        """Test: récupération des médicaments actifs"""
        patient_id = 50
        # Aucun médicament actif au départ
        assert medication_mgr.get_active_medications(patient_id) == []
        # Ajout de deux prescriptions
        medication_mgr.prescribe_medication(patient_id, "Amlodipine", "5mg", "1x/jour")
        medication_mgr.prescribe_medication(
            patient_id, "Simvastatin", "20mg", "1x/jour"
        )
        actives = medication_mgr.get_active_medications(patient_id)
        assert len(actives) == 2
        names = [med["name"] for med in actives]
        assert "Amlodipine" in names
        assert "Simvastatin" in names
        # On arrête un médicament
        medication_mgr.stop_medication(patient_id, "Amlodipine")
        actives2 = medication_mgr.get_active_medications(patient_id)
        assert len(actives2) == 1
        assert actives2[0]["name"] == "Simvastatin"
