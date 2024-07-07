import sys
import os
import re
import requests
from docx import Document
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def read_file_content(file_path):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == '.docx':
        doc = Document(file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    elif file_extension == '.pdf':
        reader = PdfReader(file_path)
        return '\n'.join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def generate_document(prompt):
    system_prompt = f"""
    Ești un manager de proiect și dezvoltator IT expert. Sarcina ta este să analizezi solicitarea clientului, care este "{prompt}" și să generezi o propunere, neaparat in limba romanaa, de proiect detaliată, demonstrând cunoștințe avansate atât în gestionarea proiectelor, cât și în dezvoltarea software, propunerea neaparat sa includa urmatoareale 5 sectiuni:

    I. Scopul documentului:
    Oferiți o prezentare generală detaliată a proiectului și definiți scopul documentului. Includeți:
    - Introducerea proiectului
    - Obiectivele principale
    - Etapele de planificare (identificarea cerințelor, analiza riscurilor, planificarea resurselor)
    - Diagramele logice și ER
    - Considerațiile inițiale de design (UI/UX, arhitectură software)
    - Importanța acestor etape pentru succesul proiectului

    II. Propunere structură:
    Conturați structura propusă și sarcinile detaliate necesare pentru dezvoltarea aplicației. Acest lucru ar trebui să acopere toate aspectele dezvoltării:
    - Backend: Limbaje de programare, framework-uri, servere, arhitectura de microservicii
    - Frontend: Framework-uri și librării (React, Angular), structura componentelor, responsive design
    - Baza de date: Tipuri de baze de date (SQL, NoSQL), structura tabelelor, relații, diagrame ER
    - Integrarea API-urilor: API-uri externe utilizate, metode de autentificare, fluxuri de date, exemple de endpoint-uri
    - Alte caracteristici: Sistem de notificări, autentificare și autorizare, optimizări de performanță

    III. Detalii Tehnice:
    A. Backend:
    - Descrierea tehnologiilor utilizate (Node.js, Python, Java)
    - Arhitectura propusă (microservicii, monolit)
    - Framework-uri și librării utilizate (Express.js, Django, Spring Boot)
    - Gestionarea datelor și comunicarea între servicii (RabbitMQ, Kafka)
    B. Frontend:
    - Descrierea tehnologiilor utilizate (React, Angular, Vue.js)
    - Arhitectura propusă (SPA, PWA)
    - Framework-uri și librării utilizate (Redux, Vuex)
    - Tehnici de optimizare a performanței (lazy loading, code splitting)
    C. Baza de date:
    - Modelul de date detaliat
    - Tipul de baze de date (PostgreSQL, MongoDB)
    - Diagrame ER detaliate
    - Backup și strategii de restaurare
    D. Integrarea API-urilor:
    - API-uri externe utilizate (Google Maps API, Stripe)
    - Metode de autentificare (OAuth2, JWT)
    - Fluxuri de date detaliate și exemple de endpoint-uri
    - Gestionarea rate limiting și caching

    IV. Sugestii suplimentare:
    Oferiți sugestii sau module suplimentare care ar putea îmbunătăți proiectul:
    - Module pentru raportare și analiză
    - Funcționalități avansate de căutare
    - Integrarea cu alte sisteme (CRM, ERP)
    - Îmbunătățiri ale securității (2FA, audit logs)
    - Module pentru suport multi-limbă și localizare

    V. Pret și timp de implementare:
    Estimați costurile și timpul necesar pentru implementare:
    - Defalcare a costurilor pe etape de dezvoltare
    - Timp estimat de livrare pentru fiecare etapă
    - Metodologia de calcul a estimărilor (complexitatea proiectului, resurse necesare)
    - Riscuri potențiale și planuri de atenuare

    De asemenea, asigurați-vă că următoarele cerințe sunt luate în considerare:
    - Secțiunea financiară: cum restaurantele solicită bani de la administratorii aplicației.
    - Modalități de plată pentru rideri.
    - Generarea automată a facturilor și posibilitatea clientului de a descărca factura generată.
    """

    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3",
        "prompt": system_prompt,
        "stream": False
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        return result['response']
    else:
        raise Exception(f"Error: Received status code {response.status_code}")

def create_pdf(content, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Register a font that supports Romanian diacritics
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    custom_style = ParagraphStyle(name='CustomStyle', fontName='DejaVuSans', fontSize=12)
    
    story = []
    sections = content.split('\n\n')
    for section in sections:
        lines = section.split('\n')
        for line in lines:
            if line.startswith("I.") or line.startswith("II.") or line.startswith("III.") or line.startswith("IV."):
                story.append(Paragraph(f"<b>{line.strip()}</b>", custom_style))
                story.append(Spacer(1, 12))
            else:
                story.append(Paragraph(line.strip(), custom_style))
                story.append(Spacer(1, 12))

    doc.build(story)

def extract_description(prompt):
    keywords = re.findall(r'\b(?:construire|consultanta|CRM|facturare|gestiune|site|ticket|programari|problema|solicita)\b', prompt, re.IGNORECASE)
    description = "_".join(keywords[:5]).lower()
    return description if description else "proposal"

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <client_request_file>")
        sys.exit(1)

    client_request_file = sys.argv[1]

    try:
        client_request = read_file_content(client_request_file)
    except Exception as e:
        print(f"Error reading client request file: {e}")
        sys.exit(1)

    try:
        document_content = generate_document(client_request)
    except Exception as e:
        print(f"Error generating document: {e}")
        sys.exit(1)

    brief_description = extract_description(client_request)
    output_pdf_path = f'{brief_description}.pdf'
    create_pdf(document_content, output_pdf_path)

    print(f"Detailed proposal has been saved to '{output_pdf_path}'")

if __name__ == "__main__":
    main()
