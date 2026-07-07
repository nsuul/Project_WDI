# Project_WDI — Academic Project for Introduction to Programming for Bioinformatics course

A simple Python program that takes two input files containing parental genotypes (Mendelian letter notation, e.g. `AaBb`) and generates all possible offspring genotype combinations, following Mendel's laws of inheritance.

## Assignment brief

This project was written for the **"Introduction to Programming"** course (Bioinformatics, academic year 2025/2026). The assignment required using only the **basic, elementary layer** of the language (no advanced libraries). 

### Task statement

Design a Python script that, given the genotypes of two individuals, generates all possible genotype combinations of their offspring according to Mendel's laws.

Genotypes follow Mendelian letter notation, e.g. `AaBb`, where:
- `Aa` is one trait (e.g. seed color; other possible states: `aa`, `AA`),
- `Bb` is a second trait (e.g. flower color; other possible states: `bb`, `BB`),
- each trait is represented by exactly two letters (two alleles).

## How it works

1. **Load files** — the program reads two text files containing the parents' genotypes.
2. **Validation** — checks that each file contains only letters and that every trait has a complete pair of alleles.
3. **Trait comparison** — checks whether both files describe the same set of traits (case-insensitive). If not, the program stops.
4. **Crossing** — for each trait separately, the 4 possible allele combinations are generated (a classic Punnett square), then combined into complete offspring genotypes.
5. **Counting** — the resulting genotypes are counted to produce the deduplicated version with occurrence counts.
6. **Save results** — the output is written to a text file in the `Results` folder.

## Repository structure

```
Project_WDI/
├── genetic_crosses.py   # main (and only) script
├── Data_samples/         # example input files with genotypes
└── Results/              # generated output files land here
```

## Input data

Input file paths are declared as variables at the top of the script, so changing the input files doesn't require searching through the whole script.

Since genotype data only ever consists of Latin letters, plain `.txt` files were chosen as the input format. An input file should:
- contain only text, **with no headers**,
- contain only letters representing alleles — no spaces, commas, or special characters,
- be of any length and describe any number of traits,
- describe each trait with **exactly two** letters (alleles) — no more, no less.

Example content: `AaBbcc`

## Output data

Results are written to a newly created text file, whose path is partially declared at the start of the script — so the output always lands in the same directory as the script and its input data, without the user having to search for it. The `os` module (the only imported module in the whole program) is used to build the file and its path correctly regardless of the operating system.

The output file has two sections:
1. The full list of all possible genotypes, including repeated ones.
2. The list of unique genotypes, each followed by its number of occurrences in parentheses.

## Algorithm

The program is split into three main parts, to make it easier to navigate and extend:

1. **Loading files** — validation and data cleanup.
2. **Genetic crosses** — the main computational part.
3. **Output file generation** — collecting the results into a human-readable file.

### 1. Loading files

**Validity checks.** Before processing any data, the program runs a series of checkpoints to make sure the input is actually valid — this prevents "falsely correct" results that would otherwise be indistinguishable from genuinely correct ones. It checks:
- that the file paths are valid,
- that the file contains only letters,
- that the file is complete (every trait has both of its alleles).

Failing any checkpoint stops the program immediately, with a message telling the user what went wrong, rather than continuing to run on bad data.

**Data cleanup.** The program expects that input files may not be perfectly formatted — e.g. someone might accidentally hit space, or not know the formatting rules and add a space after every trait. To handle this, whitespace is stripped from every input file before validation.

**Trait compatibility check.** Before crossing, the program checks whether the two genotypes actually describe the same traits, so it never blindly crosses individuals that couldn't realistically be crossed. This is done by building a set of unique letters (case-insensitive) for each genotype and comparing the two sets.

### 2. Genetic crosses

Each genotype string is converted into a list where each element is a pair of alleles — one trait.

For each trait separately, a crossing loop runs: the first allele of parent 1's genotype is paired in turn with the first and second allele of parent 2's genotype, then the same is done for parent 1's second allele. This produces the 4 combinations of a classic Punnett square for that trait.

The result for a full genotype is a list of lists — one list per trait. To build complete offspring genotypes, these lists are combined: the first element of the first trait's list is appended with each option from the second trait's list, then the same is done for the second element of the first list, and so on. For 2 traits this gives 16 combinations (4×4); for 3 traits, 64 (4×4×4).

**Counting.** To make the results more readable and analyzable, genotypes are counted — i.e. how many times each unique genotype occurs among all offspring.

## Usage

1. Place the two parental genotype files in the `data_samples` folder.
2. In `genetic_crosses.py`, set `input_female` and `input_male` to point to your input files.
3. Run the script:

```bash
python genetic_crosses.py
```

4. If both parents' genotypes describe the same traits, a file named `Wyniki_krzyżowania_<mother>_x_<father>.txt` is created in the `Results` folder, containing the full and deduplicated offspring genotype lists described above.

## Sample datasets (`data_samples/`)

| File | Description |
|---|---|
| `human_female.txt`, `human_male.txt` | ✅ Valid pair, 4 traits |
| `pea_plant_female.txt`, `pea_plant_male.txt` | ✅ Valid pair, 3 traits |
| `pea_one_allele_short.txt` | ❌ Invalid — missing one allele |
| `pea_one_trait_short.txt` | ❌ Invalid — missing one whole trait (two letters short vs. the valid `pea_plant` file) |
| `pea_with_numbers.txt` | ❌ Invalid — contains digits |
| `pea_with_spaces.txt` | ❕ Valid after cleanup — contains spaces |
| `pea_with_other_trait.txt` | ❌ Invalid — same number of traits as the valid `pea_plant` file, but one trait doesn't match |

## Results / testing

The program was tested on both correctly and intentionally incorrectly constructed datasets, to exercise both the computational part and the validation checkpoints.

**Valid datasets**

- **`human` pair** (`DdEeFfGg` × `ddeeffgg`): 256 total genotypes generated, 16 unique, each repeated 16 times. One parent is heterozygous for all 4 traits, the other is fully recessive homozygous, so every trait splits 1:1 (2 possible states) — giving 2⁴ = 16 unique combinations, and 4 Punnett-square outcomes per trait to the power of 4 traits = 256 total, matching the program's output.
- **`pea_plant` pair** (`AABbCc` × `AaBbCC`): 64 total genotypes, 12 unique. Some genotypes occur 8 times, others 4 times — because traits A and C are homozygous in one parent (1:1 ratio, as in the `human` case), while trait B is heterozygous in both parents (1:2:1 ratio).

**Intentionally invalid datasets**

- Digits in the file (`AaBb12`) → program correctly rejects it with a message that the file contains disallowed characters and only Latin letters are allowed, then stops.
- Missing allele (`AaBbC`) → program correctly reports that the data is incomplete (not every trait has both alleles), then stops.
- One trait short (`AaBb`) crossed with a valid 3-trait file → files load fine, but the trait-compatibility check reports the traits don't match, and generation is refused.
- Files describing different traits (`Aa Bb Zz`) → same as above, incompatibility is correctly detected.
- File with spaces (`Aa Bb Cc`) → whitespace is correctly stripped; the program proceeds normally and produces the same genotype count as the equivalent clean dataset, confirming the cleanup step works as intended.

## Design notes

- The program is intentionally written using elementary language constructs (basic data types, loops, functions, dictionaries, sets) and imports only the `os` module — per the assignment's requirement to stick to the basic layer of the language.
- The project was built as a two-day sprint, then went through a code review with the course instructor.

## Author

Natalia Sulima — [nsuul](https://github.com/nsuul)
