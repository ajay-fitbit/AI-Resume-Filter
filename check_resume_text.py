"""Check what the resume actually contains"""
import PyPDF2

resume_path = r"uploads\Yuki_Tanaka-resume.pdf"

with open(resume_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

print("=" * 80)
print("FULL RESUME TEXT")
print("=" * 80)
print(text)
print("\n" + "=" * 80)
print(f"Total length: {len(text)} characters")
