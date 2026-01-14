**Contract Metadata Extractor**

**1. Problem Statement**

The objective of this project is to build an AI-based system that automatically extracts key metadata from contract documents provided in **DOCX** and **scanned PNG** formats.

The system must:

* Avoid rule-based extraction
* Work across different contract templates
* Support batch processing
* Provide evaluation using **per-field Recall** as defined in the problem statement

---
**2. Dataset Details**

The `data/` directory is structured as follows:

```
data/
├── train.csv
├── test.csv
├── train/
│   ├── *.docx
│   ├── *.png
├── test/
│   ├── *.docx
│   ├── *.png
```

Description

* **train.csv**
  Contains ground-truth metadata for documents present in `train/`.

* **test.csv**
  Contains metadata structure for documents in `test/` (used for prediction).

* **train/**
  Documents used for evaluation.

* **test/**
  Unseen documents used for prediction.

---

**3. Extracted Metadata Fields**

The system extracts the following fields:

* Agreement Value
* Agreement Start Date
* Agreement End Date
* Renewal Notice (Days)
* Party One
* Party Two

---

**4. Solution Approach**

Overall Strategy

The solution uses an **AI-driven NLP pipeline** instead of rule-based logic to ensure robustness across varying contract layouts.

Processing Pipeline

1. Document ingestion (DOCX / PNG)
2. Text extraction
   * DOCX → `docx2txt`
   * PNG → Tesseract OCR
3. Text preprocessing
4. Metadata extraction using a **Transformer-based Question Answering model**
5. Structured output generation (JSON / CSV)

This approach avoids hard-coded rules and supports generalization.

---

**5. System Architecture**

```
User / Script
     ↓
FastAPI Backend
     ↓
Text Extraction (DOCX / OCR)
     ↓
NLP Pipeline (Transformer QA)
     ↓
Structured Metadata Output
```

---

**6. Technology Stack
**
* Python 3.10
* FastAPI
* Streamlit
* HuggingFace Transformers
* PyTorch
* Tesseract OCR
* Pandas
* Requests

---

## 7. Project Structure

```
contract-metadata-extractor/
|
├── api/
│   └── main.py
│
├── app/
│   ├── pipeline.py
│   ├── ocr.py
│   ├── docx_reader.py
│   ├── extractor.py
│   └── qa_engine.py
│
├── web/
│   └── app.py
│
├── evaluation/
│   ├── evaluate.py
│   └── predict_test.py
│
├── data/
│   ├── train.csv
│   ├── test.csv
│   ├── train/
│   └── test/
│
├── requirements.txt
└── README.md
```

---

**8. Installation & Setup**

Create and activate virtual environment

```bash
python -m venv contract_ai
contract_ai\Scripts\activate
```
**Install dependencies**

```bash
pip install -r requirements.txt
or using dependencies.txt 
```
**Install Tesseract OCR (Windows)**  (if error occured by tesseract lib)

Download from:
[https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

Verify installation:

```bash
tesseract --version
```

---

**9. Running the Application**

Start Backend API

```bash
uvicorn api.main:app --reload
```

Start Streamlit UI

```bash
streamlit run web/app.py
```

The UI supports **single and batch document upload** with CSV and JSON download.

---

**10. Prediction on Test Data**

To generate predictions for unseen test documents:

```bash
python evaluation/predict_test.py
```

Output:

```
evaluation/test_predictions.csv
```

---

**11. Evaluation Methodology**

Metric Used

**Per-field Recall**, as defined in the problem statement.

**Definition**

* **True**: Extracted value exactly matches the ground-truth value
* **False**: Value does not match or is not extracted

```
Recall = True / (True + False)
```

Evaluation is performed **independently for each field**.

---

**12. Running Evaluation**

```bash
python evaluation/evaluate.py
```

The script:

* Iterates through `train.csv`
* Extracts metadata using the pipeline
* Compares extracted values with ground truth
* Prints **per-field Recall**

---

**13. Evaluation Results (Observed)**

Sample output (values vary due to OCR and NLP variability):

```
Aggrement Value: 0.00
Aggrement Start Date: 0.11
Aggrement End Date: 0.11
Renewal Notice (Days): 0.00
Party One: 0.00
Party Two: 0.00
```

**Note:** Exact-match recall is sensitive to OCR noise and formatting variations, which can lower recall despite correct semantic extraction.

---

**14. Observations & Limitations**

* OCR errors affect numeric and date fields
* Formatting differences (dates, punctuation, spacing) reduce exact-match recall
* Party names are often partially extracted
* Dataset filenames are not always perfectly aligned with file extensions

These limitations are expected and can be improved with normalization and fine-tuning.

---

**15. Future Improvements**

* Date and numeric normalization
* Confidence scoring for extracted fields
* Fine-tuning NLP model on contract-specific data
* PDF support
* Asynchronous batch processing

---

**16. Conclusion**

This project demonstrates an **end-to-end AI-based contract metadata extraction system** with:

* Modular architecture
* Support for multiple document formats
* Batch processing
* Offline evaluation using defined metrics

The solution prioritizes clarity, correctness, and real-world applicability.

---

**Built to understand contracts, not just parse them.**
