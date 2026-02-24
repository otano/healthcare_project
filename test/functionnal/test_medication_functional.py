import pytest
from src.medication import Medication


@pytest.mark.functional
class TestMedicationFunctional:
    def test_get_active_medications_functional(self):
        """Test fonctionnel: récupération des médicaments actifs"""
        medication_mgr = Medication()
        patient_id = 103
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

    def test_stop_medication_functional(self):
        """Test fonctionnel: arrêt d'un médicament pour un patient"""
        medication_mgr = Medication()
        patient_id = 102
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

    def test_get_medication_history_functional(self):
        """Test fonctionnel: récupération de l'historique des prescriptions"""
        medication_mgr = Medication()
        patient_id = 101
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
