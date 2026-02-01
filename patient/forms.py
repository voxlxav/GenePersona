from django import forms
from .models import Patient, TherapyCycle, Diagnosis, MedicalDocument, Appointment, Mutation

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'pesel', 'date_of_birth', 'gender', 'address_street', 'address_zip_code', 'address_city', 'phone_number']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'pesel': forms.TextInput(attrs={'class': 'form-control'}),
            'address_street': forms.TextInput(attrs={'class': 'form-control'}), # POPRAWKA
            'address_zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'address_city': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
        }

class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = [
            'icd_code', 'name', 'diagnosis_date', 'tumor_stage',
            'node_stage', 'metastasis_stage', 'status', 'description'
        ]
        widgets = {
            'diagnosis_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'icd_code': forms.Select(
                attrs={'id': 'id_icd_code_select', 'class': 'form-select'}
            ),
            'name': forms.TextInput(
                attrs={'id': 'id_diagnosis_name', 'class': 'form-control'}
            ),
            'tumor_stage': forms.Select(attrs={'class': 'form-select'}),
            'node_stage': forms.Select(attrs={'class': 'form-select'}),
            'metastasis_stage': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }

class TherapyCycleForm(forms.ModelForm):
    class Meta:
        model = TherapyCycle
        fields = ['diagnosis', 'scheme_name', 'start_date', 'end_date', 'status']
        widgets = {
            'start_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'end_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'diagnosis': forms.Select(attrs={'class': 'form-select'}),
            'scheme_name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        patient = kwargs.pop('patient', None)
        super(TherapyCycleForm, self).__init__(*args, **kwargs)

        if patient:
            self.fields['diagnosis'].queryset = Diagnosis.objects.filter(
                patient=patient
            )

            if self.fields['diagnosis'].queryset.count() == 1:
                self.fields['diagnosis'].initial = (
                    self.fields['diagnosis'].queryset.first()
                )
        else:
            self.fields['diagnosis'].queryset = Diagnosis.objects.none()

class MedicalDocumentForm(forms.ModelForm):
    class Meta:
        model = MedicalDocument
        # Dodalem pole 'name', bo w bazie jest wymagane
        fields = ['name', 'file', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'purpose', 'notes', 'status']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class MutationForm(forms.ModelForm):
    class Meta:
        model = Mutation
        fields = ['gene_name', 'mutation_type', 'result', 'test_date', 'notes']
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gene_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mutation_type': forms.TextInput(attrs={'class': 'form-control'}),
            'result': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }