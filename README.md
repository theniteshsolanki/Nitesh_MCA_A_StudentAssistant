# Nitesh_MCA_A_StudentAssistant

## Project Description
This is a desktop application designed to help educators and students quickly generate practical programming assignments. The application takes a topic or notes as input (either typed in or uploaded as a PDF) and uses the Gemini AI model to create an assignment with two questions: one easy and one intermediate. The generated assignment can then be downloaded as a PDF. The application features a user-friendly graphical interface with a light/dark theme toggle.

## Technologies Used
Python
CustomTkinter (for the GUI)
Google Generative AI (Gemini)
fpdf (for PDF generation)
PyPDF2 (for PDF text extraction)
Steps to Run/Execute the Project

## Prerequisites:
Python 3.8 or higher
Ensure you have pip installed.
Install Dependencies:
Clone the repository to your local machine.
Open a terminal or command prompt in the project directory.
Run the following command to install the required Python packages:
pip install customtkinter google-generativeai fpdf PyPDF2


You will also need a Google Gemini API key. Obtain one and replace the placeholder in the code.
Set up API Key:
Locate the line in main.py that says:
genai.configure(api_key="YOUR_API_KEY")  # Replace with your actual API key


Replace "YOUR_API_KEY" with your actual Gemini API key.
Run the Application:
In the same terminal, run the following command:
python main.py


The application window will appear.
How to Use the Application:
Upload PDF: Click the "Upload Notes PDF" button to upload a PDF file containing your notes. The text from the PDF will be extracted and placed in the topic entry.
Enter Topic/Notes: Type your topic or notes directly into the "Enter Topic or Paste Notes..." text entry field.
Generate Assignment: Click the "⚙️ Generate Assignment" button. The application will use the Gemini API to generate an assignment based on your input. The generated assignment will be displayed in the text box.
Download PDF: Once the assignment is generated, the "💾 Download as PDF" button will become enabled. Click it to save the assignment to a PDF file.
Switch Theme: Click the "Switch Theme 🌗" button to toggle between light and dark mode.
