from django import forms
from patient.models import (
    Patient, 
    MedicalDocument, 
    TherapyCycle, 
    Diagnosis, 
    Appointment, 
    Mutation, 
    AdverseEvent, 
    Response
)

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "first_name", "last_name", "pesel", "date_of_birth",
            "gender", "address_street", "address_zip_code", "address_city",
            "phone_number", "email"
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class TherapyCycleForm(forms.ModelForm):
    class Meta:
        model = TherapyCycle
        fields = ["protocol_name", "diagnosis", "start_date", "end_date", "status"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
    
    # Opcjonalnie: Filtrowanie diagnoz tylko dla tego pacjenta (wymaga przekazania pacjenta do __init__)
    # Na razie zostawiamy standardowo dla prostoty.

class MedicalDocumentForm(forms.ModelForm):
    class Meta:
        model = MedicalDocument
        fields = ["name", "file", "description"]

# --- NOWE FORMULARZE ---

class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ["icd_code", "name", "diagnosis_date", "tumor_stage", "node_stage", "metastasis_stage", "status", "description"]
        widgets = {
            "diagnosis_date": forms.DateInput(attrs={"type": "date"}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["doctor", "date_time", "appointment_type", "status", "notes"]
        widgets = {
            "date_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

class MutationForm(forms.ModelForm):
    class Meta:
        model = Mutation
        fields = ["gene", "mutation_type", "vaf", "chromosome_location"]

# Formularze dla zagnieżdżonych elementów (opcjonalne, jeśli chcesz je edytować z poziomu karty pacjenta)
class AdverseEventForm(forms.ModelForm):
    class Meta:
        model = AdverseEvent
        fields = ["therapy_cycle", "event_date", "severity", "description", "action_taken"]
        widgets = {
            "event_date": forms.DateInput(attrs={"type": "date"}),
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ["response_cycle_id", "assessment_date", "recist_result", "notes"]
        widgets = {
            "assessment_date": forms.DateInput(attrs={"type": "date"}),
        }