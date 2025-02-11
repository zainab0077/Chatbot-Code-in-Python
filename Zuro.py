## Code Commented

import subprocess  # Importing the subprocess module to execute shell commands
import sys  # Importing the sys module to access system-specific parameters and functions

def install(package):
    """
    Install a package using pip.
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])  # Execute pip install command for the specified package

try:
    import rich  # Attempting to import the rich library for enhanced console output
    import art  # Attempting to import the art library for ASCII art generation
    import fakefarsi  # Attempting to import the fakefarsi library for generating fake information
except ImportError:  # If any of the imports fail
    install('rich')  # Install the rich library
    install('art')  # Install the art library
    install('fakefarsi')  # Install the fakefarsi library

from art import text2art  # Importing the text2art function from the art library
from rich.console import Console  # Importing the Console class from the rich library for styled console output
from rich.prompt import Prompt  # Importing the Prompt class from the rich library for user input prompts
from fakefarsi import fakefarsi  # Importing the fakefarsi module for generating fake information

console = Console()  # Creating an instance of Console for styled output

def print_ai():
    """
    Print the AI art representation.
    """
    ai_art = text2art("AI", font="block")  # Generate ASCII art for the text "AI"
    console.print(ai_art, style="bold red")  # Print the ASCII art in bold red style

def chatbot():
    """
    Run the chatbot interaction.
    """
    print_ai()  # Call the function to print the AI art representation
    console.print("[bold green]Chatbot:[/] Hi! I am your chatbot. You can ask me anything! Type 'what you can' to see features.")  # Greet the user

    while True:  # Start an infinite loop for continuous interaction
        user_input = Prompt.ask("[bold blue]You[/]").lower()  # Prompt the user for input and convert it to lowercase
        handle_user_input(user_input)  # Pass the user input to the handler function

def handle_user_input(user_input):
    """
    Handle user input and provide appropriate responses.
    """
    responses = {  # Dictionary mapping user inputs to chatbot responses
        # Welcome conversation
        "hello": "[bold green]Chatbot:[/] Hello! How can I help you?",
        "hi": "[bold green]Chatbot:[/] Hi! How can I help you?",
        "hey": "[bold green]Chatbot:[/] Hey! How can I help you?",
        "how are you": "[bold green]Chatbot:[/] I'm just a program, but I'm doing great! How about you?",
        "who are you": "[bold green]Chatbot:[/] I am Zuro, your friendly chatbot. How can I assist you?",

        # Finuture
        "what you can": "[bold green]Chatbot:[/]\n\ntype 'Encrypt' to encrypt your text \n\ntype 'Decrypt' to decrypt your text \n\ntype 'fake' to generate a fake information \n\nand you can ask me 'anythings' :) \n\ntype 'bye' to exit.",

        # Name
        "name": "[bold green]Chatbot:[/] My name is Zuro. How can I help you?",
        "what's your name": "[bold green]Chatbot:[/] My name is Zuro. I am chat-bot build by Python. How can I help you?",

        # End conversation
        "bye": "[bold green]Chatbot: Goodbye! Have a great day!"  # Response for exiting the chatbot
    }
    if "bye" in user_input:  # Check if the user wants to exit
        console.print(responses["bye"])  # Print the goodbye message
        sys.exit()  # Exit the program
    elif user_input in responses:  # If the user input matches a predefined response
        console.print(responses[user_input])  # Print the corresponding response
    elif "encrypt" in user_input:  # If the user wants to encrypt text
        encrypt_text()  # Call the encryption function
    elif "decrypt" in user_input:  # If the user wants to decrypt text
        decrypt_text()  # Call the decryption function
    elif "fake" in user_input:  # If the user wants to generate fake information
        generate_fake_info()  # Call the function to generate fake information
    else:  # If the user input does not match any known commands
        console.print("[bold green]Chatbot:[/] I'm not sure I understand.\nCan you ask something else?")  # Prompt for clarification

    return False  # Return False to indicate the function has completed

def encrypt_text():
    """
    Encrypt the user's text input.
    """
    input_text = Prompt.ask("[bold blue]Enter your text to encrypt:[/]")  # Prompt the user for text to encrypt
    encrypted_text = input_text.encode("utf-8").hex()  # Encrypt the text by encoding it to UTF-8 and converting to hex
    console.print(f"[bold green]Chatbot:[/] Here is your encrypted text: {encrypted_text}")  # Print the encrypted text

def decrypt_text():
    """
    Decrypt the user's hex input.
    """
    input_text = Prompt.ask("[bold blue]Enter your text to decrypt:[/]")  # Prompt the user for hex text to decrypt
    try:
        decrypted_text = bytes.fromhex(input_text).decode("utf-8")  # Attempt to convert hex back to UTF-8 text
        console.print(f"[bold green]Chatbot:[/] Here is your decrypted text: {decrypted_text}")  # Print the decrypted text
    except ValueError:  # If the input is not a valid hex string
        console.print("[bold green]Chatbot:[/] Invalid hex string. Please enter a valid hex string.")  # Inform the user of the error

def generate_fake_info():
    """
    Generate and display fake information.
    """
    fake_info = fakefarsi.complete()  # Generate fake information using the fakefarsi library
    console.print(f"[bold green]Chatbot:[/] Here is your fake information: \n{fake_info}")  # Print the generated fake information

# Run the chatbot
if __name__ == "__main__":  # Check if the script is being run directly
    chatbot()  # Start the chatbot interaction
