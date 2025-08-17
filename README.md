# JobFit-AI

**JobFit-AI** is a Django-based web application that analyzes resumes using AI and provides feedback, skills extraction, job matching, and recommendations based on user preferences. It integrates NLP models from Hugging Face and provides actionable insights for both candidates and recruiters.

---

## Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Screenshots](#screenshots)  
- [Folder Structure](#folder-structure)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Features

- Upload and analyze resumes in multiple formats.  
- AI-powered resume feedback and improvement suggestions.  
- Skills extraction and summary generation.  
- Job matching based on resume, skills, CGPA, and user preferences.  
- Filter jobs by location, experience, job type, and skills.  
- Simple and clean user interface.

---

## Tech Stack

- **Backend:** Python, Django  
- **Frontend:** HTML, CSS, JavaScript  
- **AI/NLP:** Hugging Face Transformers, LangChain, Flan-T5, DistilBART  
- **Database:** SQLite (default, can be replaced with PostgreSQL/MySQL)  
- **Other Libraries:** pandas, numpy, re (regex for parsing), decouple (environment variables)

---

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/DimpiMittal/JobFit-AI.git
    cd JobFit-AI
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - Windows:
      ```bash
      venv\Scripts\activate
      ```
    - macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4. **Install required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Set up environment variables:**
    - Create a `.env` file in the project root:
      ```
      SECRET_KEY=your_django_secret_key
      HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
      DEBUG=True
      ```

6. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

7. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

8. Open your browser and go to:  
    ```
    http://127.0.0.1:8000/
    ```

---

## Usage

1. Upload your resume on the homepage.  
2. View AI-generated feedback, skill extraction, and summary.  
3. Search for jobs based on preferences like location, skills, experience, and job type.  
4. View matched jobs ranked by relevance.  

---

## Folder Structure

