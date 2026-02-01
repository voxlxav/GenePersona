from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .forms import (
    PatientForm,
    TherapyCycleForm,
    MedicalDocumentForm,
    DiagnosisForm,
    AppointmentForm,
    MutationForm
)

from patient.models import (
    Patient,
    Doctor,
    TherapyCycle,
    Diagnosis,
    MedicalDocument,
    Appointment,
    Mutation
)

@login_required(login_url='login')
def home(request):
    user = request.user
    if user.is_superuser:
        patients = Patient.objects.all().order_by('-id')
    else:
        try:
            doctor_profile = user.doctor_profile
            patients = Patient.objects.filter(
                Q(attending_doctor=doctor_profile) |
                Q(consulting_doctors=doctor_profile)
            ).distinct().order_by('-id')
        except Doctor.DoesNotExist:
            patients = Patient.objects.none()

    search_query = request.GET.get('q')
    if search_query:
        patients = patients.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(pesel__startswith=search_query)
        )

    paginator = Paginator(patients, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home_page/home.html', {
        'user': user,
        'patients': page_obj,
        'search_query': search_query or ""
    })

@login_required(login_url='login')
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            try:
                patient.attending_doctor = request.user.doctor_profile
                patient.save()
            except Doctor.DoesNotExist:
                messages.error(request, "Błąd: Twoje konto nie jest powiązane z profilem lekarza.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Błąd w polu {field}: {error}")
            return redirect('home')
    return redirect('home')

@login_required(login_url='login')
def appointments(request):
    user = request.user
    return render(request, "appointments/appointments.html", {'user': user})

# --- GŁÓWNY WIDOK PACJENTA ---
@login_required(login_url='login')
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    editing_patient = request.GET.get("edit") == "1"

    sub_modal_form = None
    sub_modal_title = ""
    action_type = ""
    object_id = ""

    if request.method == "POST":
        post_action = request.POST.get("action_type")
        obj_id = request.POST.get("object_id")

        if not post_action:
            form = PatientForm(request.POST, instance=patient)
            if form.is_valid():
                form.save()
                messages.success(request, "Zaktualizowano dane pacjenta.")
                return redirect("patient_detail", pk=pk)

        elif post_action == "appointment":
            instance = get_object_or_404(Appointment, pk=obj_id) if obj_id else None
            form = AppointmentForm(request.POST, instance=instance)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.patient = patient
                obj.save()
                messages.success(request, "Zapisano wizytę.")
                return redirect("patient_detail", pk=pk)
            else:
                sub_modal_form = form
                sub_modal_title = "Błąd w formularzu wizyty"
                action_type = "appointment"

        elif post_action == "diagnosis":
            instance = get_object_or_404(Diagnosis, pk=obj_id) if obj_id else None
            form = DiagnosisForm(request.POST, instance=instance)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.patient = patient
                obj.save()
                messages.success(request, "Zapisano diagnozę.")
                return redirect("patient_detail", pk=pk)
            else:
                sub_modal_form = form
                sub_modal_title = "Błąd w formularzu diagnozy"
                action_type = "diagnosis"

        elif post_action == "therapy_cycle":
            instance = get_object_or_404(TherapyCycle, pk=obj_id) if obj_id else None

            form = TherapyCycleForm(request.POST, instance=instance, patient=patient)
            
            if form.is_valid():
                obj = form.save(commit=False)
                obj.patient = patient
                obj.save()
                messages.success(request, "Zapisano terapię.")
                return redirect("patient_detail", pk=pk)
            else:
                sub_modal_form = form
                sub_modal_title = "Błąd w formularzu terapii"
                action_type = "therapy_cycle"

        elif post_action == "mutation":
            instance = get_object_or_404(Mutation, pk=obj_id) if obj_id else None
            form = MutationForm(request.POST, instance=instance)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.patient = patient
                obj.save()
                messages.success(request, "Zapisano mutację.")
                return redirect("patient_detail", pk=pk)
            else:
                sub_modal_form = form
                sub_modal_title = "Błąd w formularzu mutacji"
                action_type = "mutation"

    if not sub_modal_form:
        action = request.GET.get("action")
        target_id = request.GET.get("id")

        if action == "add_therapy":
            sub_modal_form = TherapyCycleForm(patient=patient)
            sub_modal_title = "Dodaj cykl terapii"
            action_type = "therapy_cycle"
        elif action == "edit_therapy" and target_id:
            obj = get_object_or_404(TherapyCycle, pk=target_id)
            sub_modal_form = TherapyCycleForm(instance=obj, patient=patient)
            sub_modal_title = "Edytuj cykl terapii"
            action_type = "therapy_cycle"
            object_id = obj.id

        elif action == "add_diagnosis":
            sub_modal_form = DiagnosisForm()
            sub_modal_title = "Dodaj diagnozę"
            action_type = "diagnosis"
        elif action == "edit_diagnosis" and target_id:
            obj = get_object_or_404(Diagnosis, pk=target_id)
            sub_modal_form = DiagnosisForm(instance=obj)
            sub_modal_title = "Edytuj diagnozę"
            action_type = "diagnosis"
            object_id = obj.id

        elif action == "add_appointment":
            sub_modal_form = AppointmentForm()
            sub_modal_title = "Dodaj wizytę"
            action_type = "appointment"
        elif action == "edit_appointment" and target_id:
            obj = get_object_or_404(Appointment, pk=target_id)
            sub_modal_form = AppointmentForm(instance=obj)
            sub_modal_title = "Edytuj wizytę"
            action_type = "appointment"
            object_id = obj.id

        elif action == "add_mutation":
            sub_modal_form = MutationForm()
            sub_modal_title = "Dodaj mutację"
            action_type = "mutation"
        elif action == "edit_mutation" and target_id:
            obj = get_object_or_404(Mutation, pk=target_id)
            sub_modal_form = MutationForm(instance=obj)
            sub_modal_title = "Edytuj mutację"
            action_type = "mutation"
            object_id = obj.id

    main_patient_form = PatientForm(instance=patient)

    return render(request, "home_page/patient_detail.html", {
        "patient": patient,
        "form": main_patient_form,
        "editing": editing_patient,
        "sub_modal_form": sub_modal_form,
        "sub_modal_title": sub_modal_title,
        "action_type": action_type,
        "object_id": object_id,
    })

@login_required(login_url='login')
def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        patient.delete()
        messages.success(request, "Pacjent usunięty.")
        return redirect("home")
    return redirect("patient_detail", pk=pk)

@login_required(login_url='login')
def add_document(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        form = MedicalDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.patient = patient
            document.save()
            messages.success(request, "Dodano dokument.")
            return redirect("patient_detail", pk=patient.pk)
    else:
        form = MedicalDocumentForm()

    return render(request, "home_page/patient_detail.html", {
        'patient': patient,
        'sub_modal_form': form,
        'sub_modal_title': "Dodaj dokumentację medyczną",
        'document_upload_mode': True
    })