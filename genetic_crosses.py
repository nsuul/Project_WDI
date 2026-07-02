# PRZYGOTOWANIE PLIKÓW

### Wczytanie pliku
def load_genotype_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read() #zwraca odczytany poprawny plik
        
    except FileNotFoundError:
        print("Nie znaleziono pliku. Sprawdź, czy ścieżka pliku jest poprawna.")
    except TypeError:
        print("Niepoprawna ścieżka pliku. Sprawdź, czy ścieżka pliku jest poprawna.")
        
    return None


### Walidacja poprawnosci pliku, przygotowanie
def prepare_genotype_file(raw_file):
    
    genotype = "".join(raw_file.split()) #usuniecie bialych znakow
    
    if genotype.isalpha() == False: #walidacja czy plik to litery
        print("Plik zawiera niedozwolone znaki. Dozwolone znaki to wyłącznie litery alfabetu.")
        return None
    
    if len(genotype) % 2 != 0:
        print("Plik zawiera niekompletne dane - nie wszystkie cechy są opisane przez oba allele") #walidacja czy plik jest kompletny
        return None
    
    return genotype


### Porównanie plików - czy cechy są zgodne
def compare_genotypes(genotype1, genotype2):
    
    if genotype1 is None or genotype2 is None: #walidacja wczytania plikow
        print("Nie wczytano jednego z plików - nie można porównać genotypów.")
        return False
    
    # zbiory bez powtórzeń - eliminacja powtórzeń z drugiego allelu
    traits1 = set(char.upper() for char in genotype1)
    traits2 = set(char.upper() for char in genotype2)
        
    return traits1 == traits2 #jesli True to sa zgodne


# Ścieżki inputów
raw_file_male = load_genotype_file("")
raw_file_female = load_genotype_file("")

# Gotowe genotypy
genotype_male = prepare_genotype_file(raw_file_male)
genotype_female = prepare_genotype_file(raw_file_female)


# ZGODNOŚĆ CECH
compatibility = compare_genotypes(genotype_female, genotype_male)
if compatibility:
    print("Cechy są zgodne dla obu osobników. Można generować potomstwo")
else:
    print("Cechy nie są zgodne. Nie można wygenerować potomstwa.")


# KRZYŻÓWKI

# Rozdzielenie string na pary alleli
def splitting_traits(genotype):
    traits_list = []
    
    for a in range(0, len(genotype), 2):
        trait = genotype[a:a+2]
        traits_list.append(trait)
    traits_list.sort(key=str.upper) # Sortowanie, na wypadek, jakby cechy nie były alfabetycznie w obu plikach
    return traits_list
    

# Krzyżowanie w obrębie jednej cechy
#    Wynik: 4 kombinacje
def cross_single_trait(pair1, pair2):
    crossed_trait = []
    
    for allele1 in pair1: #po allelu od pierwszego osobnika
        
        for allele2 in pair2: #łączony po kolei z allelami drugiego osobnika
            genotype = "".join(sorted([allele1, allele2], key=str.islower)) #wielkie litery mają pierwszeństwo
            crossed_trait.append(genotype)
            
    return crossed_trait


# Połączenie krzyżowania wielu cech - pełne genotypy potomstwa
def combine_traits(traits_crossing_result_list):
    combined = [""] # pusty string - genotyp do którego dopisujemy cechy
    
    for trait_options in traits_crossing_result_list:
        new_combined = []
        
        for existing_genotype in combined:
            
            for option in trait_options:
                new_combined.append(existing_genotype + option)
                
        combined = new_combined
    
    return combined


# Zliczanie genotypów - do opcji bez powtórzeń
def count_offspring(all_offspring):
    counts = {}
    
    for genotype in all_offspring:
        if genotype in counts:
            counts[genotype] += 1
        else:
            counts[genotype] = 1 #nowe pojawienie w słowniku, wartość startowa zliczeń=1
                
        




    
traits_list_male = splitting_traits(genotype_male)
traits_list_female = splitting_traits(genotype_female)