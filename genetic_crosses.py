import os 


# ŚCIEŻKI
#   Wejściowe
input_female = ".\\Data_samples\\pea_plant_female.txt"
input_male = ".\\Data_samples\\human_male.txt"

#   Wyjściowe
results_dir = ".\\Results" #output_dir



# PRZYGOTOWANIE PLIKÓW

### Wczytanie pliku
print("Wczytywanie plików...")

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
    
    # zbiory bez powtórzeń - eliminacja powtórzeń z drugiego allelu
    traits1 = set(char.upper() for char in genotype1)
    traits2 = set(char.upper() for char in genotype2)
        
    return traits1 == traits2 #jesli True to sa zgodne


# Załadowanie inputów
raw_file_male = load_genotype_file(input_male)
raw_file_female = load_genotype_file(input_female)


# Gotowe genotypy
genotype_male = prepare_genotype_file(raw_file_male)
genotype_female = prepare_genotype_file(raw_file_female)

if genotype_male is None or genotype_female is None:
    print("Nie można kontynuować. Wybierz poprawne pliki wejściowe.")
    exit()


# ZGODNOŚĆ CECH
print("Sprawdzanie zgodności cech osobników...")

compatibility = compare_genotypes(genotype_female, genotype_male)
if compatibility:
    print("Cechy są zgodne dla obu osobników. Można generować potomstwo")
else:
    print("Cechy nie są zgodne. Nie można wygenerować potomstwa.")
    exit()




# KRZYŻÓWKI

### Rozdzielenie string na pary alleli
print("Krzyżowanie osobników...")

def splitting_traits(genotype):
    traits_list = []
    
    for a in range(0, len(genotype), 2):
        trait = genotype[a:a+2]
        traits_list.append(trait)
    traits_list.sort(key=str.upper) # Sortowanie, na wypadek, jakby cechy nie były alfabetycznie w obu plikach
    return traits_list
    

### Krzyżowanie w obrębie jednej cechy
#      Wynik: 4 kombinacje
def cross_single_trait(pair1, pair2):
    crossed_trait = []
    
    for allele1 in pair1: #po allelu od pierwszego osobnika
        
        for allele2 in pair2: #łączony po kolei z allelami drugiego osobnika
            genotype = "".join(sorted([allele1, allele2], key=str.islower)) #wielkie litery mają pierwszeństwo
            crossed_trait.append(genotype)
            
    return crossed_trait


### Połączenie krzyżowania wielu cech - pełne genotypy potomstwa
def combine_traits(traits_crossing_result_list):
    combined = [""] # pusty string - genotyp do którego dopisujemy cechy
    
    for trait_options in traits_crossing_result_list:
        new_combined = []
        
        for existing_genotype in combined:
            
            for option in trait_options:
                new_combined.append(existing_genotype + option)
                
        combined = new_combined
    
    return combined


### Zliczanie genotypów - do opcji bez powtórzeń
def count_offspring(all_offspring):
    count = {}
    
    for genotype in all_offspring:
        if genotype in count:
            count[genotype] += 1
        else:
            count[genotype] = 1 #nowe pojawienie w słowniku, wartość startowa zliczeń=1
    
    return count
                
        

# Gotowe listy rozdzielonych cech - 1 element to 1 cecha
#   Wynik: [Aa, Bb]    
traits_male = splitting_traits(genotype_male)
traits_female = splitting_traits(genotype_female)

# Gotowe krzyżówki dla 1 cechy
#   Wynik: [[Aa, Aa, AA, aa], [Bb, Bb, bb, BB]] - lista list
trait_crosses = []
for t in range(len(traits_female)): #dla każdej cechy w liście cech
    single_cross = cross_single_trait(traits_female[t], traits_male[t]) #po cesze od matki i ojca
    trait_crosses.append(single_cross)

    
# Łączenie
offspring_all = combine_traits(trait_crosses)

# Zliczanie uniklanych
offspring_unique_count = count_offspring(offspring_all)


# Podsumowanie
print(f"Wygenerowano {len(offspring_all)} możliwych układów genotypowych potomstwa dla podanych osobników.\nZapisywanie wyników do osobnego pliku...")
    
    

# PLIK WYNIKOWY
def creating_results_file(all_offspring, unique_count, output_dir, input_female, input_male):
    
    name_female = os.path.splitext(os.path.basename(input_female))[0] # 0 - nazwa, 1 - rozsz
    name_male = os.path.splitext(os.path.basename(input_male))[0]
    
    file_path = os.path.join(output_dir, f"Wyniki_krzyżowania_{name_female}_x_{name_male}.txt")
    
    with open(file_path, 'w', encoding='utf-8') as file:
        
        file.write("Wszystkie możliwe genotypy potomstwa:\n")
        for genotype in all_offspring:
            file.write(genotype + "\n")
        
        file.write("\nUzyskano następujące unikalne genotypy. W nawiasie podano liczbę wystąpień danego genotypu.\n")
        for genotype, count in unique_count.items():
            file.write(f"{genotype} ({count})\n")
            
    return file_path


# Gotowy plik z wynikami
results_file = creating_results_file(offspring_all, offspring_unique_count, results_dir, input_female, input_male)
print(f"Wyniki zapisano w pliku: {results_file}")