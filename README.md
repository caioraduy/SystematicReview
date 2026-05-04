# Systematic Literature Review — Update Pipeline (2021 → 2024)

A Python pipeline to support **Systematic Literature Review (SLR) updates**, comparing search results across multiple academic databases between two time periods to identify newly published articles relevant to the research scope.

This repository was developed as part of the literature review process for my **PhD research in Process Mining and Process Drift Detection** at the Software Agents Laboratory (PUCPR), and follows the principles of [Kitchenham’s SLR guidelines](https://www.elsevier.com/__data/promis_misc/525444systematicreviewsguide.pdf).

---

## 🎯 Problem

Systematic Literature Reviews need to be **periodically updated** to remain relevant. When an SLR originally executed in 2021 needs to be refreshed in 2024 across multiple databases (Scopus, Springer, ACM, IEEE), the researcher must answer:

- Which papers are **new** (appear in 2024 but not in 2021)?
- Which papers **disappeared** from the search string results?
- Which **duplicates** exist across the four databases?
- What is the **clean list of new titles** that needs to go through the inclusion/exclusion criteria (CI01, CI02)?

Doing this by hand across thousands of records is slow and error-prone. This pipeline automates it.

---

## 🛠️ What it does

1. **Loads** CSV exports from 4 academic databases for 2021 and 2024:
   - Scopus (`SCOPUS2021.csv`, `SCOPUS2024.csv`)
   - Springer (`SPRINGER2021.csv`, `SPRINGER2024.csv`)
   - ACM (`ACM2021.csv`, `ACM2024.csv`)
   - IEEE (`IEEE2021.csv`, `IEEE2024.csv`)
2. **Normalizes** article titles (removes punctuation, extra whitespace, case-folds) so that minor formatting differences across databases don’t produce false mismatches.
3. **Compares** each base’s 2021 vs 2024 export using a dictionary-based delta detection algorithm:
   - Counts occurrences of each title in both periods
   - Flags new articles, removed articles, and increased-frequency entries
4. **Exports** the new articles per database (`novos_arquivos_*.csv`).
5. **Cross-deduplicates** the four bases to produce a single consolidated list (`Novos_titulos.csv`) ready for screening against inclusion criteria.

---

## 📂 Repository structure

```
SystematicReview/
├── compara.py                    # Main pipeline
├── ACM2021.csv / ACM2024.csv     # Raw search exports (ACM)
├── IEEE2021.csv / IEEE2024.csv   # Raw search exports (IEEE)
├── SCOPUS2021.csv / SCOPUS2024.csv
├── SPRINGER2021.csv / SPRINGER2024.csv
├── novos_arquivos_ACM.csv        # New articles found in ACM (2024 vs 2021)
├── novos_arquivos_IEEE.csv       # New articles found in IEEE
├── novos_arquivos_scopus.csv     # New articles found in Scopus
├── novos_arquivos_springer.csv   # New articles found in Springer
└── Novos_titulos.csv             # Consolidated, deduplicated list of new titles
```

---

## 🚀 How to run

### Requirements
- Python 3.8+
- `pandas`

### Install

```bash
pip install pandas
```

### Configure paths

Open `compara.py` and update the absolute paths inside `__main__` to point to your local copies of the CSV files. Example:

```python
NOVOS_SCOPUS = compara_base_2021_2024(
    "path/to/SCOPUS2024.csv",
    "path/to/SCOPUS2021.csv",
    "Title",
    "novos_arquivos_scopus.csv"
)
```

> ⚠️ The current paths are hardcoded to a local Windows environment. A future iteration will move these to a config file or CLI arguments.

### Run

```bash
python compara.py
```

Outputs are written to the working directory:
- One `novos_arquivos_<base>.csv` per database
- One consolidated `Novos_titulos.csv` with all unique new titles across the four bases

---

## 🔑 Key technical points

- **Title normalization** uses regex to strip non-alphanumeric characters and collapse whitespace, then lowercases for comparison — a small but essential step to avoid false negatives across databases with inconsistent formatting.
- **Set-style delta detection** is implemented manually with dictionaries to also track *frequency changes* (e.g. a paper that appeared once in 2021 but three times in 2024 contributes a delta of two, not zero).
- **Cross-base deduplication** runs after per-base comparison so that the final list reflects unique papers across all four sources.
- **Column names per database** are not standardized (`Title`, `Item Title`, `Document Title`), so the pipeline is parameterized to accept the column name per source.

---

## 📚 Research context

This pipeline supported the literature review phase of my PhD research at the **Software Agents Laboratory (PUCPR)**, focused on:

- Process Mining
- Process Drift Detection in event streams
- Online process monitoring and adaptive analysis

Related publication (from my MSc research in the same laboratory):

> Raduy, C., et al. *Benchmarking Process Drift Detection Tools.* International Conference on Artificial Intelligence and Soft Computing (ICAISC), Lecture Notes in Computer Science, Springer, 2023.
> [link.springer.com/chapter/10.1007/978-3-031-23480-4_12](https://link.springer.com/chapter/10.1007/978-3-031-23480-4_12)

---

## 👤 Author

**Caio Raduy** 
🔗 [LinkedIn](https://www.linkedin.com/in/caio-raduy/) · [GitHub](https://github.com/caioraduy)
📩 raduycaio@gmail.com
