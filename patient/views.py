from django.contrib.admindocs.utils import docutils_is_available
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
import json

from .forms import PatientForm, TherapyCycleForm, MedicalDocumentForm, AppointmentForm, DiagnosisForm, MutationForm, \
  ConsultingDoctorsForm, GeneralAppointmentForm
from patient.models import Patient, Doctor, Appointment, TherapyCycle, Diagnosis, Mutation


@login_required(login_url='login')
def home(request):
  user = request.user

  if user.is_superuser:
    patients = Patient.objects.filter(is_active=True).order_by('-id')
  else:
    try:
      doctor_profile = user.doctor_profile
      patients = Patient.objects.filter(
        Q(attending_doctor=doctor_profile) |
        Q(consulting_doctors=doctor_profile)
      ).filter(is_active=True).distinct().order_by('-id')
    except Doctor.DoesNotExist:
      patients = Patient.objects.none()

  # Wyszukiwanie
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

  context = {
    'user': user,
    'patients': page_obj,
    'search_query': search_query or ""
  }

  return render(request, 'home_page/home.html', context)


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
  context = {
    'user': user
  }
  return render(request, "appointments/appointments.html", context=context)


@login_required(login_url='login')
def patient_detail(request, pk):
  patient = get_object_or_404(Patient, pk=pk)
  editing = request.GET.get("edit") == "1"

  sub_modal_form = None
  sub_modal_title = ""
  action_type = ""
  object_id = ""
  document_upload_mode = False
  is_attending_doctor = False

  try:
    if request.user.doctor_profile == patient.attending_doctor:
      is_attending_doctor = True
  except AttributeError:
    pass

  main_patient_form = PatientForm(instance=patient)
  if request.method == "POST":
    post_action = request.POST.get("action_type")
    obj_id = request.POST.get("object_id")

    if not post_action:
      main_patient_form = PatientForm(request.POST, instance=patient)
      if main_patient_form.is_valid():

        main_patient_form.save()
        messages.success(request, "Zaktualizowano dane pacjenta.")
        return redirect("patient_detail", pk=pk)

    elif post_action == "appointment":
      instance = get_object_or_404(Appointment,pk = obj_id) if obj_id else None
      form = AppointmentForm(request.POST, instance=instance)

      if form.is_valid():
        obj = form.save(commit=False)
        obj.patient = patient

        try:
          obj.doctor = request.user.doctor_profile
          obj.save()
          messages.success(request, "Zapisano wizytę.")
          return redirect("patient_detail", pk=pk)
        except AttributeError:
          form.add_error(None, "Błąd: Nie masz przypisanego profilu lekarza.")
          sub_modal_form = form
          sub_modal_title = "Błąd uprawnień"
          action_type = "appointment"

      else:
        sub_modal_form = form
        sub_modal_title = "Błąd w formularzu wizyty"
        action_type = "appointment"

    elif post_action == "diagnosis":
      instance = get_object_or_404(Diagnosis,pk = obj_id) if obj_id else None
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
      instance = get_object_or_404(TherapyCycle,pk = obj_id) if obj_id else None
      form = TherapyCycleForm(request.POST, instance=instance, patient = patient)

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

    elif post_action == "document":
      form = MedicalDocumentForm(request.POST, request.FILES)
      if form.is_valid():
        doc = form.save(commit=False)
        doc.patient = patient
        doc.save()
        messages.success(request, "Dodano dokument.")
        return redirect("patient_detail", pk=pk)
      else:
        sub_modal_form = form
        sub_modal_title = "Błąd dodawania dokumentu"
        action_type = "document"
        document_upload_mode = True

    elif post_action == "consulting_doctors":

      if not is_attending_doctor:
        messages.error(request, "Tylko lekarz prowadzący może zmieniać konsultantów.")
        return redirect("patient_detail", pk=pk)

      form = ConsultingDoctorsForm(request.POST, instance = patient)
      if form.is_valid():
        form.save()
        messages.success(request, "Zaktualizowano listę lekarzy konsultujących.")
        return redirect("patient_detail", pk=pk)
      else:
        sub_modal_form = form
        sub_modal_title = "Zarządzaj konsultantami"
        action_type = "consulting_doctors"

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

    elif action == "add_document":
      sub_modal_form = MedicalDocumentForm()
      sub_modal_title = "Dodaj dokument medyczny"
      action_type = "document"
      document_upload_mode = True

    elif action == "manage_consultants":
      sub_modal_form = ConsultingDoctorsForm(instance=patient)
      sub_modal_title = "Zarządzaj lekarzami konsultującymi"
      action_type = "consulting_doctors"

  return render(request, "home_page/patient_detail.html", {
    "patient": patient,
    "form": main_patient_form,
    "editing": editing,
    "sub_modal_form": sub_modal_form,
    "sub_modal_title": sub_modal_title,
    "action_type": action_type,
    "object_id": object_id,
    "document_upload_mode": document_upload_mode,
    "is_attending_doctor": is_attending_doctor
  })


@login_required(login_url='login')
def delete_patient(request, pk):
  patient = get_object_or_404(Patient, pk=pk)

  if request.method == "POST":
    patient.is_active = False
    patient.save()
    messages.success(request, "Pacjent został usunięty (przeniesiony do archiwum).")
    return redirect("home")

  return redirect("patient_detail", pk=pk)

@login_required(login_url='login')
def add_document(request, pk):
  patient = get_object_or_404(Patient, pk = pk)

  if request.method == "POST":
    form = MedicalDocumentForm(request.POST, request.FILES)
    if form.is_valid():
      document = form.save(commit=False)
      document.patient = patient
      document.save()
      messages.success(request, "Dodano dokument do karty pacjenta")
      return redirect("patient_detail", pk=patient.pk)
  else:
    form = MedicalDocumentForm()

  return render(request, "home_page/patient_detail.html", {'form':form, 'patient':patient})


@login_required(login_url='login')
def appointments(request):
  # 1. Pobieranie danych do kalendarza i tabeli
  upcoming_appointments = []
  past_appointments = []
  events_data = []

  try:
    if hasattr(request.user, 'doctor_profile'):
      doctor = request.user.doctor_profile
      now = timezone.now()

      upcoming_appointments = Appointment.objects.filter(
        doctor=doctor,
        date_time__gte=now,
      ).order_by('date_time')

      past_appointments = Appointment.objects.filter(
        doctor=doctor,
        date_time__lt=now,
      ).order_by('date_time')

      all_appointments = list(upcoming_appointments) + list(past_appointments)

      for app in all_appointments:
        patient_str = str(app.patient)
        type_str = str(app.appointment_type)

        events_data.append({
          'title': f"{patient_str} - {type_str}",
          'start': app.date_time.isoformat(),
          'color': '6c757d' if app.date_time < now else ('#3788d8' if app.appointment_type == 'Konsultacja' else '#28a745')
        })
  except Exception as e:
    print(f"Błąd pobierania wizyt: {e}")

  events_json = json.dumps(events_data, cls=DjangoJSONEncoder)

  if request.method == "POST":
    form = GeneralAppointmentForm(request.user, request.POST)
    if form.is_valid():
      appointment = form.save(commit=False)
      try:
        appointment.doctor = request.user.doctor_profile
        appointment.save()
        messages.success(request, f"Dodano wizytę dla pacjenta: {appointment.patient}")

        return redirect("appointments")
      except AttributeError:
        messages.error(request, "Błąd: Nie masz profilu lekarza.")
    else:
      messages.error(request, "Popraw błędy w formularzu.")
  else:
    form = GeneralAppointmentForm(request.user)

  return render(request, 'home_page/appointments.html', {
    'upcoming_appointments': upcoming_appointments,
    'past_appointments': past_appointments,
    'events_json': events_json,
    'form': form
  })