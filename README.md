# CvCrafter
CvCrafter is a web application that intelligently customizes CVs and cover letters based on job descriptions using GPT-4. The application automatically adapts the content and language of your CV and cover letter to match the job requirements and description language.

## Features
* Web interface for easy document upload and generation
* Intelligent CV customization based on job descriptions
* Automatic cover letter generation that complements your CV
* PDF CV processing and text extraction
* LaTeX output format for professional formatting
* Multi-language support (automatically matches job description language)
* API endpoints for programmatic access

## Requirements
* Python 3.6 or higher
* FastAPI
* PyPDF2
* python-dotenv
* requests
* uvicorn (for running the server)
* Node.js 18.18 or later

## Setup
1. Clone the repository
2. Install the required dependencies:
   ```bash
   cd backend/app
   pip install -r requirements.txt
   ```

3. Set up your OpenRouter API key:
   - Create a `.env` file in the project root directory
   - Add your OpenRouter API key:
     ```
     API_KEY=your_api_key_here
     ```
4. Build the Frontend:
   - Install Node dependencies and run the server
     ```
     cd frontend/my-app
     npm install
     npm run build
     ```

## Usage
1. Start the backend:
   ```bash
   uvicorn app.main:app --reload
   ```
2. Start the frontend:
   ```bash
   npm run start
   ```
3. Open your web browser and navigate to `http://localhost:3000`

4. Through the web interface:
   - Upload your CV in PDF format
   - Paste the job description
   - Generate your customized CV and/or cover letter
   - Download the generated LaTeX files