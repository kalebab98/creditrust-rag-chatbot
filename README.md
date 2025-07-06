## 🧹 Preprocessing Pipeline

### ✅ Initial Cleaning
- Loaded full dataset with `pandas`
- Identified and handled missing values:
  - `Consumer complaint narrative`: **6.6M missing**
  - `Tags`, `Consent`, `Public response`: heavily sparse

### 🔍 Filtering Criteria
- Selected rows where:
  - `Product` is in:
    ```
    ['Credit card', 'Personal loan', 'Buy Now, Pay Later (BNPL)', 'Savings account', 'Money transfers']
    ```
  - `Consumer complaint narrative` is **not null**

### 🧼 Text Cleaning
- Lowercased all narratives
- Removed punctuation, newlines, and extra spaces
- Calculated word counts per narrative (`narrative_length`)

### 📤 Output
- Saved cleaned and filtered data to:
  - `filtered_complaints.csv` (~200 MB)
- Total filtered rows: **~2.9M**

---
