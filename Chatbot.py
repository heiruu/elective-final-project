import datetime
import json
import PYPDF2
import os
# Function to respond based on user input
def respond(user_input):
    user_input = user_input.lower()
    if user_input == "hello":
        return "Hello! How can I assist you today? If you have any questions or need a recipe, just let me know! 😊"
    elif user_input == "how are you":
        return "I'm here and ready to help you! How about you? If you have any questions or need assistance with something, feel free to ask! 😊"
    elif user_input == "what's your name":
        return "I don’t have a personal name, but you can call me your friendly assistant! How can I help you today? If you’re looking for recipes or cooking tips, just let me know! 😊"
    elif user_input == "what can you do":
        return ("I can help you with Filipino recipes and cooking tips! If you have a specific dish in mind or need suggestions," 
                "/n just let me know, and I’ll be happy to assist you. What are you interested in cooking today? 😊")
    elif user_input == "bye":
        return "Goodbye! If you ever need assistance again, feel free to reach out. Have a wonderful day! 😊"
    else:
        return "It looks like there might have been a typo in your message. If you meant to ask about something specific, please clarify, and I'll do my best to assist you! 😊"
# Main function to handle the chat
def main():
    print("🍴 Kumusta! Craving Filipino food? I’m here to help you cook authentic dishes like adobo, sinigang, and more! Just ask for a recipe, and I’ll guide you step by step. Tara, luto tayo! 🌟")
    while True:
        user_input = input("\nYou: ").strip()
        # Check if the user wants to exit
        if user_input.lower() == "bye":
            response = respond(user_input)
            print(f"\Tito Jose: {response}")
            break
        # Respond to the input
        response = respond(user_input)
        print(f"\Tito Jose: {response}")
    print("Goodbye! If you ever need assistance again, feel free to reach out. Have a wonderful day! 😊")

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    """
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text
def generate_training_data(text, output_path):
    """
    Process the extracted text to create a simple question-answer training dataset for the chatbot.
    Example: Use recipe titles as questions and their details as answers.
    """
    lines = text.split("\n")
    training_data = {} 
    current_title = None
    for line in lines:
        if line.strip() == "":
            continue
        if "Ingredients" in line or "Instructions" in line:
            # Collect the data as the answer
            if current_title and current_title not in training_data:
                training_data[current_title] = training_data.get(current_title, "") + "\n" + line.strip()
            continue

        if any(keyword in line for keyword in ["Recipe", "Prep Time", "Cook Time", "Servings"]):
            current_title = line.strip()
        else:
            if current_title:
                training_data[current_title] = training_data.get(current_title, "") + "\n" + line.strip()   
    # Save the training data to a JSON file
    with open(output_path, "w") as json_file:
        json.dump(training_data, json_file, indent=4)
    print(f"Training data saved to {output_path}")
def main():
    # Paths to the PDFs and output JSON
    pdf_files = [
        "/mnt/data/chatbot-cook-book-2.en.tl (1).pdf",
        "/mnt/data/chatbot-cook-book-2.pdf"
    ]
    output_json = "chatbot_training_data.json"
    combined_text = ""
    for pdf in pdf_files:
        combined_text += extract_text_from_pdf(pdf)   
    # Generate training data
    generate_training_data(combined_text, output_json)

if __name__ == "__main__":
    main()
