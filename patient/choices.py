from django.db import models

class ICD10Choices(models.TextChoices):
  # === C00–C14 NOWOTWORY ZŁOŚLIWE WARGI, JAMY USTNEJ I GARDŁA ===
  C00_0 = 'C00.0', 'C00.0 - Nowotwór złośliwy wargi górnej (powierzchnia zewnętrzna)'
  C00_1 = 'C00.1', 'C00.1 - Nowotwór złośliwy wargi dolnej (powierzchnia zewnętrzna)'
  C00_3 = 'C00.3', 'C00.3 - Nowotwór złośliwy wargi górnej (powierzchnia wewnętrzna)'
  C00_4 = 'C00.4', 'C00.4 - Nowotwór złośliwy wargi dolnej (powierzchnia wewnętrzna)'
  C01 = 'C01', 'C01 - Nowotwór złośliwy nasady języka'
  C02_0 = 'C02.0', 'C02.0 - Nowotwór złośliwy powierzchni grzbietowej języka'
  C02_1 = 'C02.1', 'C02.1 - Nowotwór złośliwy brzegu języka'
  C02_2 = 'C02.2', 'C02.2 - Nowotwór złośliwy dolnej powierzchni języka'
  C03_0 = 'C03.0', 'C03.0 - Nowotwór złośliwy dziąsła górnego'
  C03_1 = 'C03.1', 'C03.1 - Nowotwór złośliwy dziąsła dolnego'
  C04_0 = 'C04.0', 'C04.0 - Nowotwór złośliwy przedniej części dna jamy ustnej'
  C05_0 = 'C05.0', 'C05.0 - Nowotwór złośliwy podniebienia twardego'
  C05_1 = 'C05.1', 'C05.1 - Nowotwór złośliwy podniebienia miękkiego'
  C06_0 = 'C06.0', 'C06.0 - Nowotwór złośliwy błony śluzowej policzka'
  C07 = 'C07', 'C07 - Nowotwór złośliwy ślinianki przyusznej'
  C08_0 = 'C08.0', 'C08.0 - Nowotwór złośliwy ślinianki podżuchwowej'
  C09_0 = 'C09.0', 'C09.0 - Nowotwór złośliwy dołka migdałkowego'
  C09_9 = 'C09.9', 'C09.9 - Nowotwór złośliwy migdałka, nieokreślony'
  C10_0 = 'C10.0', 'C10.0 - Nowotwór złośliwy doliny nagłośniowej'
  C11_1 = 'C11.1', 'C11.1 - Nowotwór złośliwy ściany tylnej nosogardła'
  C13_0 = 'C13.0', 'C13.0 - Nowotwór złośliwy okolicy zapierściennej'
  C14_0 = 'C14.0', 'C14.0 - Nowotwór złośliwy gardła, nieokreślony'

  # === C15–C26 NOWOTWORY ZŁOŚLIWE NARZĄDÓW TRAWIENNYCH ===
  C15_3 = 'C15.3', 'C15.3 - Nowotwór złośliwy górnej części przełyku'
  C15_4 = 'C15.4', 'C15.4 - Nowotwór złośliwy środkowej części przełyku'
  C15_5 = 'C15.5', 'C15.5 - Nowotwór złośliwy dolnej części przełyku'

  C16_0 = 'C16.0', 'C16.0 - Nowotwór złośliwy wpustu żołądka'
  C16_1 = 'C16.1', 'C16.1 - Nowotwór złośliwy dna żołądka'
  C16_2 = 'C16.2', 'C16.2 - Nowotwór złośliwy trzonu żołądka'
  C16_3 = 'C16.3', 'C16.3 - Nowotwór złośliwy ujścia odźwiernika'
  C16_9 = 'C16.9', 'C16.9 - Nowotwór złośliwy żołądka, nieokreślony'

  C18_0 = 'C18.0', 'C18.0 - Nowotwór złośliwy kątnicy'
  C18_2 = 'C18.2', 'C18.2 - Nowotwór złośliwy jelita grubego wstępującego'
  C18_4 = 'C18.4', 'C18.4 - Nowotwór złośliwy jelita grubego poprzecznego'
  C18_6 = 'C18.6', 'C18.6 - Nowotwór złośliwy jelita grubego zstępującego'
  C18_7 = 'C18.7', 'C18.7 - Nowotwór złośliwy esicy'
  C19 = 'C19', 'C19 - Nowotwór złośliwy zgięcia esiczo-odbytniczego'
  C20 = 'C20', 'C20 - Nowotwór złośliwy odbytnicy'

  C22_0 = 'C22.0', 'C22.0 - Rak komórek wątroby (HCC)'
  C22_1 = 'C22.1', 'C22.1 - Rak przewodów żółciowych wewnątrzwątrobowych'

  C25_0 = 'C25.0', 'C25.0 - Nowotwór złośliwy głowy trzustki'
  C25_1 = 'C25.1', 'C25.1 - Nowotwór złośliwy trzonu trzustki'
  C25_2 = 'C25.2', 'C25.2 - Nowotwór złośliwy ogona trzustki'

  # === C30–C39 UKŁAD ODDECHOWY ===
  C32_0 = 'C32.0', 'C32.0 - Nowotwór złośliwy głośni'
  C32_1 = 'C32.1', 'C32.1 - Nowotwór złośliwy nagłośni'

  C34_0 = 'C34.0', 'C34.0 - Nowotwór złośliwy oskrzela głównego'
  C34_1 = 'C34.1', 'C34.1 - Nowotwór złośliwy płata górnego, oskrzela płatowego górnego'
  C34_2 = 'C34.2', 'C34.2 - Nowotwór złośliwy płata środkowego, oskrzela płatowego środkowego'
  C34_3 = 'C34.3', 'C34.3 - Nowotwór złośliwy płata dolnego, oskrzela płatowego dolnego'
  C34_8 = 'C34.8', 'C34.8 - Zmiana przekraczająca granice w obrębie oskrzela i płuca'
  C34_9 = 'C34.9', 'C34.9 - Nowotwór złośliwy oskrzela lub płuca, nieokreślony'

  C38_4 = 'C38.4', 'C38.4 - Nowotwór złośliwy opłucnej'

  # === C43–C44 SKÓRA ===
  C43_0 = 'C43.0', 'C43.0 - Czerniak złośliwy wargi'
  C43_5 = 'C43.5', 'C43.5 - Czerniak złośliwy tułowia'
  C43_6 = 'C43.6', 'C43.6 - Czerniak złośliwy kończyny górnej'
  C43_7 = 'C43.7', 'C43.7 - Czerniak złośliwy kończyny dolnej'
  C43_9 = 'C43.9', 'C43.9 - Czerniak złośliwy skóry, nieokreślony'

  C44_0 = 'C44.0', 'C44.0 - Rak skóry wargi'
  C44_3 = 'C44.3', 'C44.3 - Rak skóry innych i nieokreślonych części twarzy'

  # === C50 PIERŚ (SUTEK) ===
  C50_0 = 'C50.0', 'C50.0 - Nowotwór złośliwy brodawki i otoczki'
  C50_1 = 'C50.1', 'C50.1 - Nowotwór złośliwy centralnej części sutka'
  C50_2 = 'C50.2', 'C50.2 - Nowotwór złośliwy ćwiartki górnej wewnętrznej sutka'
  C50_3 = 'C50.3', 'C50.3 - Nowotwór złośliwy ćwiartki dolnej wewnętrznej sutka'
  C50_4 = 'C50.4', 'C50.4 - Nowotwór złośliwy ćwiartki górnej zewnętrznej sutka'
  C50_5 = 'C50.5', 'C50.5 - Nowotwór złośliwy ćwiartki dolnej zewnętrznej sutka'
  C50_6 = 'C50.6', 'C50.6 - Nowotwór złośliwy części pachowej sutka'
  C50_8 = 'C50.8', 'C50.8 - Zmiana przekraczająca granice sutka'
  C50_9 = 'C50.9', 'C50.9 - Nowotwór złośliwy sutka, nieokreślony'

  # === C51–C58 NARZĄDY PŁCIOWE ŻEŃSKIE ===
  C53_0 = 'C53.0', 'C53.0 - Nowotwór złośliwy błony śluzowej szyjki macicy'
  C53_1 = 'C53.1', 'C53.1 - Nowotwór złośliwy błony zewnętrznej szyjki macicy'
  C53_9 = 'C53.9', 'C53.9 - Nowotwór złośliwy szyjki macicy, nieokreślony'

  C54_1 = 'C54.1', 'C54.1 - Nowotwór złośliwy błony śluzowej macicy (endometrium)'
  C54_2 = 'C54.2', 'C54.2 - Nowotwór złośliwy mięśniówki macicy'

  C56 = 'C56', 'C56 - Nowotwór złośliwy jajnika'

  # === C60–C63 NARZĄDY PŁCIOWE MĘSKIE ===
  C61 = 'C61', 'C61 - Nowotwór złośliwy gruczołu krokowego (prostaty)'
  C62_0 = 'C62.0', 'C62.0 - Nowotwór złośliwy jądra niezstąpionego'
  C62_1 = 'C62.1', 'C62.1 - Nowotwór złośliwy jądra zstąpionego'

  # === C64–C68 UKŁAD MOCZOWY ===
  C64 = 'C64', 'C64 - Nowotwór złośliwy nerki (z wyjątkiem miedniczki)'
  C67_0 = 'C67.0', 'C67.0 - Nowotwór złośliwy trójkąta pęcherza moczowego'
  C67_9 = 'C67.9', 'C67.9 - Nowotwór złośliwy pęcherza moczowego, nieokreślony'

  # === C70–C72 OUN ===
  C71_0 = 'C71.0', 'C71.0 - Nowotwór złośliwy mózgu, z wyjątkiem płatów i komór'
  C71_1 = 'C71.1', 'C71.1 - Nowotwór złośliwy płata czołowego'
  C71_2 = 'C71.2', 'C71.2 - Nowotwór złośliwy płata skroniowego'
  C71_3 = 'C71.3', 'C71.3 - Nowotwór złośliwy płata ciemieniowego'
  C71_4 = 'C71.4', 'C71.4 - Nowotwór złośliwy płata potylicznego'
  C71_9 = 'C71.9', 'C71.9 - Nowotwór złośliwy mózgu, nieokreślony'

  # === C73–C75 TARCZYCA I GRUCZOŁY ===
  C73 = 'C73', 'C73 - Nowotwór złośliwy tarczycy'

  # === C81–C96 UKŁAD CHŁONNY I KRWIOTWÓRCZY ===
  C81_9 = 'C81.9', 'C81.9 - Chłoniak Hodgkina, nieokreślony'
  C90_0 = 'C90.0', 'C90.0 - Szpiczak mnogi'
  C91_0 = 'C91.0', 'C91.0 - Ostra białaczka limfoblastyczna (ALL)'
  C91_1 = 'C91.1', 'C91.1 - Przewlekła białaczka limfocytowa (CLL)'
  C92_0 = 'C92.0', 'C92.0 - Ostra białaczka szpikowa (AML)'
  C92_1 = 'C92.1', 'C92.1 - Przewlekła białaczka szpikowa (CML)'

  # === D00–D09 NOWOTWORY IN SITU ===
  D05_0 = 'D05.0', 'D05.0 - Rak in situ zrazików sutka'
  D05_1 = 'D05.1', 'D05.1 - Rak in situ przewodów wewnątrz sutka'
  D06_9 = 'D06.9', 'D06.9 - Rak in situ szyjki macicy, nieokreślony'

  # === D10–D36 NOWOTWORY ŁAGODNE ===
  D12_6 = 'D12.6', 'D12.6 - Nowotwór łagodny okrężnicy, nieokreślony'
  D17_9 = 'D17.9', 'D17.9 - Tłuszczak, nieokreślony'
  D24 = 'D24', 'D24 - Nowotwór łagodny sutka'
  D25_9 = 'D25.9', 'D25.9 - Mięśniak gładkokomórkowy macicy, nieokreślony'

  # === D37–D48 NOWOTWORY O NIEPEWNYM CHARAKTERZE ===
  D37_1 = 'D37.1', 'D37.1 - Nowotwór o niepewnym charakterze żołądka'
  D37_4 = 'D37.4', 'D37.4 - Nowotwór o niepewnym charakterze okrężnicy'
  D39_1 = 'D39.1', 'D39.1 - Nowotwór o niepewnym charakterze jajnika'
  D43_2 = 'D43.2', 'D43.2 - Nowotwór o niepewnym charakterze mózgu'
  D47_1 = 'D47.1', 'D47.1 - Przewlekła choroba mieloproliferacyjna'
  D48_9 = 'D48.9', 'D48.9 - Nowotwór o niepewnym charakterze, nieokreślony'

  OTHER = 'INNE', 'Inny kod ICD-10 (spoza listy)'

class TNM_T_Choices(models.TextChoices):
  TX = 'TX', 'TX - Guz pierwotny nie może być oceniony'
  TIS = 'Tis', 'Tis - Rak przedinwazyjny (in situ)'
  T0 = 'T0', 'T0 - Brak dowodów na istnienie guza pierwotnego'
  T1 = 'T1', 'T1 - Guz <= 3 cm'
  T2 = 'T2', 'T2 - Guz > 3 cm, ale <= 5 cm'
  T3 = 'T3', 'T3 - Guz > 5 cm lub nacieka'
  T4 = 'T4', 'T4 - Guz nacieka inne narządy (serce, przełyk)'


# === Klasyfikacja TNM - Cecha N (Węzły chłonne) ===
class TNM_N_Choices(models.TextChoices):
  NX = 'NX', 'NX - Regionalne węzły chłonne nie mogą być ocenione'
  N0 = 'N0', 'N0 - Brak przerzutów do regionalnych węzłów chłonnych'
  N1 = 'N1', 'N1 - Przerzuty do węzłów okołooskrzelowych/wnęk'
  N2 = 'N2', 'N2 - Przerzuty do węzłów śródpiersia'
  N3 = 'N3', 'N3 - Przerzuty do węzłów przeciwległych'


# === Klasyfikacja TNM - Cecha M (Przerzuty odległe) ===
class TNM_M_Choices(models.TextChoices):
  M0 = 'M0', 'M0 - Brak przerzutów odległych'
  M1 = 'M1', 'M1 - Występują przerzuty odległe'