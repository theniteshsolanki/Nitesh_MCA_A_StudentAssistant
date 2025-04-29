import customtkinter
import google.generativeai as genai
from fpdf import FPDF
from tkinter import filedialog
import os
from PyPDF2 import PdfReader
import threading
import time


genai.configure(api_key="AIzaSyATgIcVDv30yWupwpsKUbmnwtmWHAE-q7s") 

class AssignmentGeneratorApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("🚀 Practical Assignment Generator")
        self.geometry("950x750")
        self.minsize(850, 700)

        # Set initial theme
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("blue")
        self.current_theme = "Dark"

        # --- Layout Management ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(8, weight=1)

        # --- UI Components ---
        
        # Button to switch between light and dark themes
        self.theme_button = customtkinter.CTkButton(self, text="Switch Theme 🌗", command=self.switch_theme)
        self.theme_button.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="e")

        # App title label
        self.title_label = customtkinter.CTkLabel(self, text="🧠 Assignment Generator", font=customtkinter.CTkFont(size=28, weight="bold"))
        self.title_label.grid(row=1, column=0, padx=20, pady=(5, 10))

        # Button to upload a PDF file
        self.upload_button = customtkinter.CTkButton(self, text="📄 Upload Notes PDF", command=self.upload_pdf)
        self.upload_button.grid(row=2, column=0, padx=20, pady=(5, 5), sticky="ew")

        # "OR" separator label
        self.or_label = customtkinter.CTkLabel(self, text="OR", font=customtkinter.CTkFont(size=14, slant="italic"))
        self.or_label.grid(row=3, column=0, pady=(5, 5))

        # Text input for entering topic manually
        self.topic_entry = customtkinter.CTkEntry(self, placeholder_text="Enter Topic or Paste Notes...", height=45)
        self.topic_entry.grid(row=4, column=0, padx=20, pady=(5, 10), sticky="ew")

        # Button to generate assignment
        self.generate_button = customtkinter.CTkButton(self, text="⚙️ Generate Assignment", command=self.generate_assignment_thread)
        self.generate_button.grid(row=5, column=0, padx=20, pady=(5, 10), sticky="ew")

        # Loading label for animation
        self.loading_label = customtkinter.CTkLabel(self, text="", font=customtkinter.CTkFont(size=16))
        self.loading_label.grid(row=6, column=0, padx=20, pady=(5, 5))

        # Label for assignment output
        self.assignment_label = customtkinter.CTkLabel(self, text="📜 Generated Assignment", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.assignment_label.grid(row=7, column=0, padx=20, pady=(10, 5), sticky="w")

        # Textbox to display generated assignment
        self.assignment_textbox = customtkinter.CTkTextbox(self, state="disabled", font=("Courier New", 14), wrap="word")
        self.assignment_textbox.grid(row=8, column=0, padx=20, pady=10, sticky="nsew")

        # Button to download the assignment as a PDF
        self.download_button = customtkinter.CTkButton(self, text="💾 Download as PDF", command=self.download_pdf, state="disabled")
        self.download_button.grid(row=9, column=0, padx=20, pady=20, sticky="ew")

        # --- Internal State ---
        self.generated_assignment_text = ""  # Stores generated assignment text
        self.loading = False  # Flag to control loading animation

    def switch_theme(self):
        # Switch between Light and Dark mode
        if self.current_theme == "Dark":
            customtkinter.set_appearance_mode("Light")
            self.current_theme = "Light"
        else:
            customtkinter.set_appearance_mode("Dark")
            self.current_theme = "Dark"

    def generate_assignment_thread(self):
        # Run assignment generation in a separate thread (to avoid freezing the UI)
        thread = threading.Thread(target=self.generate_assignment)
        thread.start()

    def animate_loading(self):
        # Simple animated "Generating..." text effect while assignment is being created
        self.loading = True
        dots = ""
        while self.loading:
            dots += "."
            if len(dots) > 3:
                dots = ""
            self.loading_label.configure(text=f"Generating{dots}")
            time.sleep(0.5)

    def generate_assignment(self):
        # Main logic to generate the assignment using Gemini API
        user_input = self.topic_entry.get()
        if not user_input.strip():
            self.show_text("⚠️ Please enter a topic or notes.")
            return

        self.generate_button.configure(state="disabled", text="⏳ Generating...")
        self.download_button.configure(state="disabled")
        self.loading_label.configure(text="Generating...")

        # Start loading animation in a background thread
        loading_thread = threading.Thread(target=self.animate_loading)
        loading_thread.start()

        # Crafting a careful prompt for the AI model
        prompt = f"""
You are a teaching assistant designing practical computer programming assignments.
Given the topic or notes: "{user_input}",
Generate:
- 2 practical questions.
- First: Easy level.
- Second: Intermediate level.
- Encourage logical thinking and real-world applicability.
- If the input is not about computer programming, ask the user politely to rephrase.
"""
        try:
            # Initialize Gemini model and request content
            model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
            response = model.generate_content(prompt)
            self.generated_assignment_text = response.text

            # Show the generated assignment
            self.show_text(self.generated_assignment_text)
            self.download_button.configure(state="normal")

        except Exception as e:
            # Handle API or network errors gracefully
            self.show_text(f"An error occurred:\n{e}")
            self.download_button.configure(state="disabled")

        finally:
            # Always stop the loading animation
            self.loading = False
            self.loading_label.configure(text="")
            self.generate_button.configure(state="normal", text="⚙️ Generate Assignment")

    def upload_pdf(self):
        # Open file dialog to choose a PDF and extract its text
        file_path = filedialog.askopenfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'rb') as pdf_file:
                    pdf_reader = PdfReader(pdf_file)
                    text = ""
                    for page in pdf_reader.pages:
                        extracted_text = page.extract_text()
                        if extracted_text:
                            text += extracted_text + "\n"

                # Fill the topic entry with the extracted text
                self.topic_entry.delete(0, customtkinter.END)
                self.topic_entry.insert(0, text.strip())
                customtkinter.CTkMessagebox(title="Success", message="PDF loaded successfully.", icon="check")

            except Exception as e:
                # Handle issues during PDF reading
                customtkinter.CTkMessagebox(title="Error", message=f"PDF error:\n{e}", icon="cancel")

    def download_pdf(self):
        # Save the generated assignment as a PDF file
        if not self.generated_assignment_text:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )

        if file_path:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Courier", size=12)
            for line in self.generated_assignment_text.split('\n'):
                pdf.cell(0, 10, txt=line, ln=1, align='L')

            try:
                pdf.output(file_path)
                customtkinter.CTkMessagebox(title="Success", message="Assignment saved successfully.", icon="check")
            except Exception as e:
                # Handle errors while saving the file
                customtkinter.CTkMessagebox(title="Error", message=f"Failed to save PDF:\n{e}", icon="cancel")

    def show_text(self, text):
        # Update the assignment output textbox
        self.assignment_textbox.configure(state="normal")
        self.assignment_textbox.delete("1.0", "end")
        self.assignment_textbox.insert("1.0", text)
        self.assignment_textbox.configure(state="disabled")

# --- Start the app ---
if __name__ == "__main__":
    app = AssignmentGeneratorApp()
    app.mainloop()