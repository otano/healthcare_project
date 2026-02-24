import pytest
from src.medication import Medication
import time


@pytest.mark.load
class TestMedicationLoad:
    def test_prescribe_one_medication_many_patients(self):
        """Test de charge: prescrire un médicament à un très grand nombre de patients différents"""
        medication_mgr = Medication()
        nb_patients = 10000
        med_name = "TestMed"
        start = time.time()
        for patient_id in range(10000, 10000 + nb_patients):
            medication_mgr.prescribe_medication(patient_id, med_name, "10mg", "1x/jour")
        end = time.time()
        # Vérification
        count = sum(
            1
            for pid in range(10000, 10000 + nb_patients)
            if medication_mgr.get_medication_history(pid)
        )
        assert count == nb_patients
        print(f"Temps pour {nb_patients} patients : {end - start:.2f} secondes")
        assert (end - start) < 10
