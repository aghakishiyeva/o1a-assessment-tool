# O-1A Visa Qualification Assessment Tool

This AI application assesses how qualified a person is for an O-1A immigration visa based on their CV. It evaluates the 8 O-1A criteria and provides:
  1. A rating (low, medium, high) on the likelihood of qualifying for the O-1A visa.
  2. A list of achievements that meet the criteria.

Here is the sample video:

[![O1A Assessment Tool](https://img.youtube.com/vi/AO8yiENGRlE/0.jpg)](https://www.youtube.com/watch?v=AO8yiENGRlE)

## Design Decisions

### **System Design**
1. **CV Parsing**:
   - Used `pdfminer` to extract text from uploaded PDFs.
   - Ensures compatibility with most CV formats.

2. **Criteria Matching**:
   - **Semantic Matching**: Used `SentenceTransformer` (all-mpnet-base-v2) to compute embeddings and match CV text to O-1A criteria.
   - **Keyword Matching**: Fallback to keyword matching if semantic matching fails.
   - Threshold for semantic matching set to `0.4` to balance precision and recall.

3. **Rating Logic**:
   - **High**: 5+ criteria matched.
   - **Medium**: 3-4 criteria matched.
   - **Low**: Fewer than 3 criteria matched.

4. **API Design**:
   - Built with **FastAPI** for simplicity and performance (also as requested).
   - Endpoint `/upload/` accepts a CV file and returns:
     - Achievements matching O-1A criteria.
     - Overall qualification rating.

### **Why These Choices?**
- **Semantic Matching**: Captures nuanced relationships between CV text and criteria.
- **Keyword Matching**: Ensures robustness when semantic matching fails.
- **FastAPI**: Lightweight, fast, and easy to use for building APIs.

## Evaluation Guide

### **How to Evaluate the Output**
1. **Achievements**:
   - Check if the listed achievements align with the 8 O-1A criteria:
     - Awards, Membership, Press, Judging, Original Contribution, Scholarly Articles, Critical Employment, High Remuneration.
   - Ensure the sentences extracted from the CV are relevant to the criteria.

2. **Qualification Rating**:
   - **High**: 5+ criteria matched.
   - **Medium**: 3-4 criteria matched.
   - **Low**: Fewer than 3 criteria matched.

3. **Testing**:
   - Upload sample CVs to the `/upload/` endpoint.
   - Verify the output matches expectations based on the CV content.

### **Example Output**
```json
{
  "qualifications": {
    "Awards": [{"score": 0.85, "text": "Received 'Best Researcher Award' in 2022."}],
    "Scholarly Articles": [{"score": 0.78, "text": "Published 10 papers in top-tier journals."}]
  },
  "O-1A Qualification Rating": "High"
}
```


## How to Run

1. Clone the repository - `git clone https://github.com/aghakishiyeva/o1a-assessment-tool`
2. Navigate to the directory - `cd o1a-assessment-tool`
3. Create the virtual environment - `python -m venv venv`
4. Activate the virtual environment <br>
   4.1 `source venv/bin/activate`  # On macOS/Linux <br>
   4.2 `venv\Scripts\activate `    # On Windows
5. Install dependencies - `pip install -r requirements.txt`
6. Run the app - `uvicorn app.main:app --reload`
7. Try it! - `http://127.0.0.1:8000`
