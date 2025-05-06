
import PyPDF2
import pyttsx3
import threading
is_stopped = False
pdf_loaded = False
def pdf_to_audio(pdf_path, page_number):
    global is_stopped, pdf_loaded
    try:
        with open(pdf_path, 'rb') as path:
            pdfReader = PyPDF2.PdfReader(path)
            if page_number < 1 or page_number > len(pdfReader.pages):
                print("Invalid page number.")
                return
            from_page = pdfReader.pages[page_number - 1]
            text = from_page.extract_text()
            if text:
                pdf_loaded = True
                speak = pyttsx3.init()
                def speak_text():
                    global is_stopped
                    speak.say(text)
                    speak.runAndWait()
                    is_stopped = False
                speaking_thread = threading.Thread(target=speak_text)
                speaking_thread.start()
                while speaking_thread.is_alive():
                    command = input("Enter command (type 'stop' to stop reading): ").strip().lower()
                    if command == "stop":
                        is_stopped = True
                        speak.stop()
                        print("Reading stopped.")
                        break
                speaking_thread.join()
            else:
                print("No text could be extracted from this page.")
                pdf_loaded = False
    except FileNotFoundError:
        print("The specified PDF file was not found.")
        pdf_loaded = False
    except Exception as e:
        print(f"An error occurred: {e}")
        pdf_loaded = False
while True:
    pdf_file_path = input("Please enter the PDF file path: ")
    if pdf_file_path.lower().endswith('.pdf'):
        break
    else:
        print("Please enter a valid PDF file path.")
read_option = input("Do you want to read the entire PDF or a specific page? (type 'full' or 'page'): ").strip().lower()

if read_option == "full":
    with open(pdf_file_path, 'rb') as path:
        pdfReader = PyPDF2.PdfReader(path)
        for page_number in range(1, len(pdfReader.pages) + 1):
            pdf_to_audio(pdf_file_path, page_number)"C:\Users\its_i\Downloads\Cloud Computing (100Question's Answers)_250109_190234.pdf"
elif read_option == "page":
    page_to_read = int(input("Please enter the page number to read (1-based): "))
    pdf_to_audio(pdf_file_path, page_to_read)
else:
    print("Invalid option selected. Please restart the program .")

