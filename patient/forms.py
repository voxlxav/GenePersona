from django import forms

import patient
from patient.models import Patient, MedicalDocument, Appointment, Mutation, TherapyCycle, Diagnosis


class PatientForm(forms.ModelForm):
  class Meta:
        model = Patient
        fields = [
          "first_name", "last_name", "pesel", "date_of_birth",
          "gender","address_street","address_zip_code","address_city",
          "phone_number","email"
        ]
        widgets = {
          "date_of_birth": forms.DateInput(attrs={'type':'date','class':'form-control'},format='%Y-%m-%d'),
          "first_name": forms.TextInput(attrs={'class':'form-control'}),
          "last_name": forms.TextInput(attrs={'class':'form-control'}),
          "pesel": forms.TextInput(attrs={'class':'form-control'}),
          "address_street": forms.TextInput(attrs={'class':'form-control'}),
          "address_zip_code": forms.TextInput(attrs={'class':'form-control'}),
          "address_city": forms.TextInput(attrs={'class':'form-control'}),
          "email": forms.EmailInput(attrs={'class':'form-control'}),
          "phone_number": forms.TextInput(attrs={'class':'form-control'}),
          "gender": forms.Select(attrs={'class':'form-select'}),
        }

class DiagnosisForm(forms.ModelForm):
  class Meta:
    model = Diagnosis
    fields = ["icd_code","name","diagnosis_date","tumor_stage",
              "node_stage","metastasis_stage","description","status"
              ]
    widgets = {
      "diagnosis_date": forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'),
      "icd_code": forms.Select(attrs={'class':'form-select'}),
      "name": forms.TextInput(attrs={'class':'form-control'}),
      "tumor_stage": forms.Select(attrs={'class':'form-select'}),
      "node_stage": forms.Select(attrs={'class':'form-select'}),
      "metastasis_stage": forms.Select(attrs={'class':'form-select'}),
      "status": forms.Select(attrs={'class':'form-select'}),
      "description": forms.Textarea(attrs={'class':'form-control','rows':'3'}),
    }

class TherapyCycleForm(forms.ModelForm):
    class Meta:
        model = TherapyCycle
        fields = ["protocol_name", "diagnosis", "start_date", "end_date", "status"]
        widgets = {
          "start_date": forms.DateInput(attrs={"type": "date"},format='%Y-%m-%d'),
          "end_date": forms.DateInput(attrs={"type":"date"},format='%Y-%m-%d'),
          "diagnosis": forms.Select(attrs={'class':'form-select'}),
          "protocol_name": forms.TextInput(attrs={'class':'form-control'}),
          "status": forms.Select(attrs={'class':'form-select'}),
        }
    def __init__(self, *args, **kwargs):
      self.patient_obj = kwargs.pop('patient', None)
      patient_id = kwargs.pop('patient_id', None)

      super(TherapyCycleForm, self).__init__(*args, **kwargs)

      if self.patient_obj:
        self.fields['diagnosis'].queryset = Diagnosis.objects.filter(patient=self.patient_obj)
      elif patient_id:
        self.fields['diagnosis'].queryset = Diagnosis.objects.filter(patient_id=patient_id)
      else:
        # Jeśli to edycja istniejącego cyklu, pobierz pacjenta z instancji
        if self.instance and self.instance.pk:
          self.fields['diagnosis'].queryset = Diagnosis.objects.filter(patient=self.instance.patient)
        else:
          self.fields['diagnosis'].queryset = Diagnosis.objects.none()

class MedicalDocumentForm(forms.ModelForm):
    class Meta:
        model = MedicalDocument
        fields = ["name","file","description"]
        widgets = {
          "name": forms.TextInput(attrs={'class':'form-control'}),
          "file": forms.FileInput(attrs={'class':'form-control'}),
          "description": forms.Textarea(attrs={'class':'form-control','rows':'2'}),
        }

class AppointmentForm(forms.ModelForm):
  class Meta:
    model = Appointment
    fields = ["date_time","appointment_type","notes","status"]
    widgets = {
      "date_time": forms.DateTimeInput(
        attrs={'class':'form-control','type': 'datetime-local'},
        format='%Y-%m-%dT%H:%M'
      ),
      "appointment_type": forms.Select(attrs={'class':'form-control'}),
      "notes": forms.Textarea(attrs={'class':'form-control','rows':'2'}),
      "status": forms.Select(attrs={'class':'form-select'})
    }

class MutationForm(forms.ModelForm):
  class Meta:
    model = Mutation
    fields = ["gene","mutation_type"]