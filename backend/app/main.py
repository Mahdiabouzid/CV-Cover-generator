from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Annotated
import requests
import io
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY= os.getenv('API_KEY')

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generateCV(cv: str, job_description: str):
    detailed_prompt = f"""
    Task: Create a professionally tailored CV in LaTeX format.

    Input Materials:
    Original CV: {cv}
    Job Description: {job_description}

    Required Actions:
    1. Language Analysis:
       - Detect the primary language of the job description 
       - Ensure all CV content matches this language for example if it is german the cv should also be german
       - Maintain any specific industry terminology

    2. Skills Alignment:
       - Identify key requirements from the job description
       - Prioritize matching skills and experiences from the original CV
       - Add relevant keywords from the job posting
       - Quantify achievements where possible (%, numbers, metrics)

    3. Content Optimization:
       - Reorganize sections to highlight most relevant experiences first
       - Focus on achievements rather than just responsibilities
       - Remove or minimize irrelevant experiences
       - Ensure chronological order within sections

    4. Professional Formatting:
       - Use modern LaTeX CV template
       - Include clear section headers
       - Maintain consistent formatting
       - Optimize spacing and layout
       - Keep to maximum 2 pages

    5. Essential Sections:
       - Professional Summary (tailored to position)
       - Technical Skills (matched to job requirements)
       - Professional Experience
       - Education
       - Certifications (if relevant)
       - Projects (if applicable)
       - Languages (if relevant)

    6. Style Guidelines:
       - Use active voice and power verbs
       - Be concise and impactful
       - Maintain professional tone
       - Include industry-specific keywords
       - Ensure ATS compatibility

    Output Requirements:
    - Provide complete LaTeX code
    - Include all necessary LaTeX packages
    - Ensure compilable code
    - Add comments for key sections
    """

    # Rest of the function remains the same, just update the 'text' field
    data = {
        "model": "openai/gpt-4o-2024-11-20",
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": detailed_prompt}]
            }
        ]
    }
    api_url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
    }
    response = requests.post(api_url, headers=headers, json=data)
    response_json = response.json()
    # Extract LaTeX code from the response
    content = response_json['choices'][0]['message']['content']

    # Parse LaTeX code between ```latex and ```
    import re
    latex_match = re.search(r'```latex\n(.*?)```', content, re.DOTALL)
    
    return latex_match.group(1).strip() if latex_match else content

def generateCoverLetter(cv: str, job_description: str):
    detailed_prompt = f"""
    Task: Create a compelling cover letter in LaTeX format that perfectly complements the provided CV.

    Input Materials:
    Customized CV: {cv}
    Job Description: {job_description}

    Required Actions:
    1. Language and Tone:
       - Match the language of the job description for example if it is german the cover letter should also be german
       - Adopt the company's communication style
       - Maintain professional yet engaging tone
       - Show enthusiasm and confidence

    2. Structure (3-4 paragraphs):
       Opening:
       - Strong attention-grabbing introduction
       - Mention the specific position and company
       - Reference how you learned about the opportunity
       - Brief statement of why you're the ideal candidate

       Body (1-2 paragraphs):
       - Highlight 2-3 key achievements that directly relate to the role
       - Connect your experience to company needs
       - Demonstrate knowledge of the company/industry
       - Use specific examples and metrics
       - Reference key requirements from job description

       Closing:
       - Reiterate interest in the position
       - Request an interview
       - Thank the reader
       - Include your contact information

    3. Content Requirements:
       - Address specific points from job description
       - Show understanding of company culture
       - Demonstrate research about the organization
       - Include relevant keywords
       - Keep to one page maximum

    4. Formatting:
       - Use matching LaTeX style to CV
       - Include proper business letter formatting
       - Add current date
       - Include proper spacing and margins
       - Ensure consistent font and styling

    5. Additional Considerations:
       - Avoid repeating CV content verbatim
       - Show personality while maintaining professionalism
       - Address any potential concerns (gaps, career changes)
       - Customize for company culture
       - Include any relevant referrals or connections

    Output Requirements:
    - Provide complete LaTeX code
    - Include all necessary LaTeX packages
    - Ensure compilable code
    - Add comments for key sections
    """

    # Rest of the function remains the same, just update the 'text' field
    data = {
        "model": "openai/gpt-4o-2024-11-20",
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": detailed_prompt}]
            }
        ]
    }
    api_url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
    }
    response = requests.post(api_url, headers=headers, json=data)
    response_json = response.json()
    # Extract LaTeX code from the response
    content = response_json['choices'][0]['message']['content']
    
    # Parse LaTeX code between ```latex and ```
    import re
    latex_match = re.search(r'```latex\n(.*?)```', content, re.DOTALL)
    if latex_match:
        return latex_match.group(1).strip()
    else:
        return content


@app.post("/api/generate-cv")
async def generateCVController(
    cv: Annotated[UploadFile, File()],
    job_description: Annotated[str, Form()]
):
    try:
        text = ''
        reader = PdfReader(cv.file)
        for page in reader.pages:
            text += page.extract_text() or ""

        latex_content = generateCV(cv=text, job_description=job_description)

        latex_file = io.BytesIO(latex_content.encode("utf-8"))

        # Return StreamingResponse without saving locally
        return StreamingResponse(
            latex_file, 
            media_type="application/x-tex", 
            headers={"Content-Disposition": 'attachment; filename="generated_cv.tex"'}
        )

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    
@app.post("/api/generate-cover-letter")
def generateCoverLetterController(
    cv: Annotated[UploadFile, File()],
    job_description: Annotated[str, Form()]
):
    try:
        text = ''
        reader = PdfReader(cv.file)

        for page in reader.pages:
            text += page.extract_text() or ""
        
        latex_content = generateCoverLetter(cv=text, job_description=job_description)

        latex_file = io.BytesIO(latex_content.encode("utf-8"))

        # Return StreamingResponse without saving locally
        return StreamingResponse(
            latex_file, 
            media_type="application/x-tex", 
            headers={"Content-Disposition": 'attachment; filename="generated_coverLetter.tex"'}
        )

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)