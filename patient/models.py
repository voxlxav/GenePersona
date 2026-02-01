from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def validate_pesel(value):
    if len(value) != 11:
        raise ValidationError('PESEL musi mieć 11 znaków.')
    if not value.isdigit():
        raise ValidationError('PESEL musi składać się wyłącznie z cyfr.')

    wages = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    control_sum = sum(int(value[i]) * wages[i] for i in range(10))
    control_value = (10 - (control_sum % 10)) % 10
    if int(value[-1]) != control_value:
        raise ValidationError('Nieprawidłowa suma kontrolna numeru PESEL.')

def patient_directory_path(instance, filename):
    return f"medical_docs/patient{instance.patient.id}/{filename}"

class Doctor(models.Model):
    class Specialization(models.TextChoices):
        ONCOLOGIST = 'ONKOLOG','Onkolog kliniczny'
        ONKOGENETICIST = 'ONKOGENETYK', 'Onkogenetyk'
        RADIOLOGIST = 'RADIOLOG', 'Radiolog'
        PATHOMORPHOLOGIST = 'PATOMORFOLOG', 'Patomorfolog'
        SURGEON = 'CHIRURG', 'Chirurg onkologiczny'
        OTHER = 'INNY', 'Inna specjalizacja'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        null=True,
        blank=True,
        verbose_name='Konto użytkownika'
    )

    first_name = models.CharField(max_length=100,verbose_name='Imię')
    last_name = models.CharField(max_length=100,verbose_name='Nazwisko')
    pwz_number = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Numer PWZ',
        help_text='7-cyfrowy numepr prawa wykonywania zawodu'
    )
    specialization = models.CharField(
        max_length=50,
        choices=Specialization.choices,
        default=Specialization.ONCOLOGIST,
        verbose_name='Specializacja'
    )
    email = models.EmailField(verbose_name='Email służbowy', blank=True, null=True)
    phone = models.CharField(max_length=15,verbose_name='Telefon kontaktowy',blank=True, null=True)

    def __str__(self):
        return f'lek. {self.first_name} {self.last_name} ({self.specialization})'

    class Meta:
        verbose_name = 'Lekarz'
        verbose_name_plural = 'Lekarze'

class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = 'Mężczyzna','Mężczyzna'
        FEMALE = 'Kobieta','Kobieta'
        OTHER = 'Inna','Inna'

    first_name = models.CharField(max_length=100, verbose_name='Imię')
    last_name = models.CharField(max_length=100,verbose_name='Nazwisko')
    pesel = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
        validators=[validate_pesel],
        verbose_name='PESEL',
        help_text='11-cyfrowy numer identyfikacyjny'
    )
    date_of_birth = models.DateField(verbose_name='Data urodzenia')
    gender = models.CharField(
        max_length=15,
        choices=Gender.choices,
        default=Gender.MALE,
        verbose_name='Płeć'
    )
    address_street = models.CharField(max_length=200, verbose_name='Ulica i nr domu', blank=True, null=True)
    address_zip_code = models.CharField(
        max_length=6,
        verbose_name='Kod pocztowy',
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\d{2}-\d{3}$', 'Format kodu: XX-XXX')]
    )
    address_city = models.CharField(max_length=100, verbose_name='Miejscowość', blank=True, null=True)

    phone_number = models.CharField(max_length=15, verbose_name='Numer telefonu', blank=True, null=True)
    email = models.EmailField(verbose_name='Email', blank=True, null=True)

    attending_doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_patients',
        verbose_name='Lekarz Prowadzący',
    )
    consulting_doctors = models.ManyToManyField(
        Doctor,
        blank=True,
        related_name='consultation_patients',
        verbose_name='Lekarze konsultujący'
    )

    initial_diagnosis = models.CharField(max_length=250, verbose_name='Wstępna diagnoza (ARCHIWALNE)', blank=True, null=True)
    diagnosis_date = models.DateField(verbose_name='Data diagnozy (ARCHIWALNE)', blank=True, null=True)

    def __str__(self):
        identifier = self.pesel if self.pesel else self.date_of_birth
        return f'{self.first_name} {self.last_name} ({identifier})'

    class Meta:
        verbose_name = 'Pacjent'
        verbose_name_plural = 'Pacjenci'

class Diagnosis(models.Model):
    class StageT(models.TextChoices):
        TX = 'TX', 'TX - Nie można ocenić guza'
        T0 = 'T0', 'T0 - Brak dowodów na obecność guza'
        TIS = 'Tis', 'Tis - Rak przedinwazyjny (in situ)'
        T1 = 'T1', 'T1 - Guz mały (I stopień)'
        T2 = 'T2', 'T2 - Guz średni (II stopień)'
        T3 = 'T3', 'T3 - Guz duży/nacieka (III stopień)'
        T4 = 'T4', 'T4 - Guz bardzo duży/nacieka sąsiednie narządy'

    class StageN(models.TextChoices):
        NX = 'NX', 'NX - Nie można ocenić węzłów'
        N0 = 'N0', 'N0 - Brak przerzutów do węzłów'
        N1 = 'N1', 'N1 - Przerzuty do pojedynczych węzłów'
        N2 = 'N2', 'N2 - Przerzuty do licznych węzłów'
        N3 = 'N3', 'N3 - Rozległe przerzuty węzłowe'

    class StageM(models.TextChoices):
        M0 = 'M0', 'M0 - Brak przerzutów odległych'
        M1 = 'M1', 'M1 - Obecne przerzuty odległe'

    class ICDCodes(models.TextChoices):
        C15 = 'C15', 'C15 - Nowotwór złośliwy przełyku'
        C16 = 'C16', 'C16 - Nowotwór złośliwy żołądka'
        C18 = 'C18', 'C18 - Nowotwór złośliwy jelita grubego'
        C20 = 'C20', 'C20 - Nowotwór złośliwy odbytnicy'
        C22 = 'C22', 'C22 - Nowotwór złośliwy wątroby'
        C25 = 'C25', 'C25 - Nowotwór złośliwy trzustki'
        C34 = 'C34', 'C34 - Nowotwór złośliwy oskrzela i płuca'
        C43 = 'C43', 'C43 - Czerniak złośliwy skóry'
        C50 = 'C50', 'C50 - Nowotwór złośliwy sutka (piersi)'
        C53 = 'C53', 'C53 - Nowotwór złośliwy szyjki macicy'
        C54 = 'C54', 'C54 - Nowotwór złośliwy trzonu macicy'
        C56 = 'C56', 'C56 - Nowotwór złośliwy jajnika'
        C61 = 'C61', 'C61 - Nowotwór złośliwy gruczołu krokowego'
        C64 = 'C64', 'C64 - Nowotwór złośliwy nerki'
        C67 = 'C67', 'C67 - Nowotwór złośliwy pęcherza moczowego'
        C71 = 'C71', 'C71 - Nowotwór złośliwy mózgu'
        C73 = 'C73', 'C73 - Nowotwór złośliwy tarczycy'
        C81 = 'C81', 'C81 - Chłoniak Hodgkina'
        C90 = 'C90', 'C90 - Szpiczak mnogi'
        INNE = 'INNE', 'Inne rozpoznanie'

    class Status(models.TextChoices):
        SUSPECTED = 'PODEJRZENIE', 'Podejrzenie'
        CONFIRMED = 'POTWIERDZONA', 'Potwierdzona histopatologicznie'
        RECURRENCE = 'WZNOWA', 'Wznowa'
        REMISSION = 'REMISJA', 'Remisja (Wyleczona)'
        PALLIATIVE = 'PALIATYWNA', 'Opieka paliatywna'

    patient = models.ForeignKey(
        'Patient',
        on_delete=models.CASCADE,
        related_name='diagnoses',
        verbose_name='Pacjent'
    )

    icd_code = models.CharField(
        max_length=10,
        choices=ICDCodes.choices,
        verbose_name='Kod ICD-10',
        blank=True,
        null=True
    )

    name = models.CharField(max_length=250, verbose_name='Rozpoznanie opisowe')
    diagnosis_date = models.DateField(verbose_name='Data postawienia diagnozy')

    tumor_stage = models.CharField(
        max_length=10,
        choices=StageT.choices,
        default=StageT.TX,
        verbose_name='Cecha T (Guz)',
        blank=True, null=True
    )
    node_stage = models.CharField(
        max_length=10,
        choices=StageN.choices,
        default=StageN.NX,
        verbose_name='Cecha N (Węzły)',
        blank=True, null=True
    )
    metastasis_stage = models.CharField(
        max_length=10,
        choices=StageM.choices,
        default=StageM.M0,
        verbose_name='Cecha M (Przerzuty)',
        blank=True, null=True
    )

    description = models.TextField(verbose_name='Opis szczegółowy / Wynik hist-pat', blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CONFIRMED,
        verbose_name='Status diagnozy'
    )

    def __str__(self):
        return f"{self.get_icd_code_display()} ({self.diagnosis_date})"

    class Meta:
        verbose_name = "Diagnoza"
        verbose_name_plural = "Historia Chorób (Diagnozy)"
        ordering = ['-diagnosis_date']

class MedicalDocument(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_documents',
        verbose_name='Pacjent'
    )
    name = models.CharField(max_length=250, verbose_name='Nazwa dokumentu (np. Wynik TK)')
    file = models.FileField(upload_to=patient_directory_path, blank=True, null=True)
    upload_date = models.DateField(verbose_name='Data dodania dokumentu', blank=True, null=True)
    description = models.TextField(verbose_name='Komentarz', blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.upload_date}- {self.patient.last_name}"

    class Meta:
        verbose_name = "Dokument medyczny"
        verbose_name_plural = "Dokumentacja medyczna"
        ordering = ['-upload_date']

class Appointment(models.Model):
    patient = models.ForeignKey(
        'Patient', 
        on_delete=models.CASCADE, 
        related_name='appointments',
        verbose_name="Pacjent"
    )
    appointment_date = models.DateTimeField(verbose_name="Data i godzina")
    purpose = models.CharField(max_length=200, verbose_name="Cel wizyty")
    
    notes = models.TextField(verbose_name="Notatki", blank=True, null=True)
    
    class Status(models.TextChoices):
        SCHEDULED = 'Zaplanowana', 'Zaplanowana'
        COMPLETED = 'Odbyta', 'Odbyta'
        CANCELLED = 'Odwołana', 'Odwołana'
    
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.SCHEDULED,
        verbose_name="Status"
    )

    def __str__(self):
        return f"{self.purpose} - {self.appointment_date}"

class TherapyCycle(models.Model):
    patient = models.ForeignKey(
        'Patient',
        on_delete=models.CASCADE,
        related_name='therapy_cycles',
        verbose_name='Pacjent'
    )
    
    diagnosis = models.ForeignKey(
        'Diagnosis', 
        on_delete=models.CASCADE, 
        verbose_name="Leczona choroba (z diagnoz pacjenta)",
        related_name="therapy_cycles",
        null=True,
        blank=True
    )

    scheme_name = models.CharField(
        max_length=100, 
        verbose_name="Nazwa schematu (np. AC, Taxol)"
    )
    
    start_date = models.DateField(verbose_name="Data rozpoczęcia")
    end_date = models.DateField(verbose_name="Data zakończenia", blank=True, null=True)

    class Status(models.TextChoices):
        ONGOING = 'W trakcie', 'W trakcie'
        COMPLETED = 'Zakończona', 'Zakończona'
        PAUSED = 'Wstrzymana', 'Wstrzymana'
        PLANNED = 'Zaplanowana', 'Zaplanowana'
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNED,
        verbose_name='Status terapii'
    )

    def clean(self):
        if self.diagnosis and self.patient:
            try:
                if self.diagnosis.patient != self.patient:
                    raise ValidationError('Wybrana diagnoza nie należy do przypisanego pacjenta!')
            except (Diagnosis.DoesNotExist, AttributeError):
                pass

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.diagnosis:
            try:
                return f'{self.scheme_name} ({self.diagnosis.get_icd_code_display()})'
            except AttributeError:
                pass
        return f'{self.scheme_name}'

    class Meta:
        verbose_name = "Cykl terapii"
        verbose_name_plural = "Cykle terapii"

class Response(models.Model):
    class RECIST_criteria(models.TextChoices):
        CR = "CR", "CR - complete response"
        PR = "PR", "PR - partial response"
        SD = "SD", "SD - stable disease"
        PD = "PD", "PD - progressive disease"

    response_cycle_id = models.ForeignKey(
        TherapyCycle,
        on_delete=models.CASCADE,
        null=True,
        related_name='response_ci',
        verbose_name="Terapia"
    )
    assessment_date = models.DateField(verbose_name='Data oceny reakcji')

    recist_result = models.CharField(
        choices=RECIST_criteria.choices,
        default=RECIST_criteria.SD,
        verbose_name='Kryterium RECIST'
    )

    notes = models.TextField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name='Notatki'
    )

    def __str__(self):
        return f'{self.therapy_cycle} - {self.assessment_date}'

    class Meta:
        verbose_name = "Odpowiedź na leczenie"
        verbose_name_plural = "Odpowiedzi na leczenie"

class AdverseEvent(models.Model):
    class severity_grades(models.TextChoices):
        G1 = "Grade 1", "Grade 1 - Łagodne"
        G2 = "Grade 2", "Grade 2 - Umiarkowane"
        G3 = "Grade 3", "Grade 3 - Ciężkie"
        G4 = "Grade 4", "Grade 4 - Zagrażające życiu"
        G5 = "Grade 5", "Grade 5 - Zgon"

    therapy_cycle = models.ForeignKey(
        TherapyCycle,
        on_delete=models.CASCADE,
        related_name='adverse_events',
        verbose_name="Cykl terapii",
        null=True
    )

    event_date = models.DateField(verbose_name='Data zdarzenia')
    description = models.TextField(
        max_length=1500,
        verbose_name="Opis zdarzenia"
    )

    severity = models.CharField(
        choices=severity_grades.choices,
        default=severity_grades.G1,
        verbose_name="Severity"
    )

    action_taken = models.TextField(
        max_length=1500,
        verbose_name="Podjęte działanie"
    )

    def __str__(self):
        return f'{self.therapy_cycle} - {self.severity}'

    class Meta:
        verbose_name = "Zdarzenie niepożądane"
        verbose_name_plural = "Zdarzenia niepożądane"

class Mutation(models.Model):
    patient = models.ForeignKey(
        'Patient', 
        on_delete=models.CASCADE, 
        related_name='mutations',
        verbose_name="Pacjent"
    )
    gene_name = models.CharField(max_length=50, verbose_name="Nazwa genu")
    mutation_type = models.CharField(max_length=100, verbose_name="Rodzaj mutacji")
    
    class Result(models.TextChoices):
        POSITIVE = 'Pozytywny', 'Pozytywny'
        NEGATIVE = 'Negatywny', 'Negatywny'
        UNKNOWN = 'Niejednoznaczny', 'Niejednoznaczny'

    result = models.CharField(
        max_length=20, 
        choices=Result.choices, 
        verbose_name="Wynik"
    )
    test_date = models.DateField(verbose_name="Data badania", blank=True, null=True)
    notes = models.TextField(verbose_name="Dodatkowe informacje", blank=True, null=True)

    def __str__(self):
        return f"{self.gene_name} ({self.result})"