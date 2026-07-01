### FUNKCJE ---

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
    
### ---


### śCIEŻKI INPUTÓW ---

raw_file_male = load_genotype_file("")
raw_file_female = load_genotype_file("")

genotype_male = prepare_genotype_file(raw_file_male)
genotype_female = prepare_genotype_file(raw_file_male)

compatibility = compare_genotypes(genotype_female, genotype_male)
if compatibility:
    print("Cechy są zgodne dla obu osobników. Można generować potomstwo")
else:
    print("Cechy nie są zgodne. Nie można wygenerować potomstwa.")