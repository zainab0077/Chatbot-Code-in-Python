"""
Zuro - A simple chatbot with encryption, decryption, and fake information generation capabilities.
"""

import hashlib
import subprocess
import sys

# Third-party dependencies
try:
    import rich
    import art
    import fakefarsi
    from Crypto.Cipher import AES
except ImportError:
    # Auto-install missing dependencies
    def install(package):
        """Install a package using pip."""
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    install('rich')
    install('art')
    install('fakefarsi')
    install('pycryptodome')

from art import text2art
from rich.console import Console
from rich.prompt import Prompt
from fakefarsi import fakefarsi

console = Console()

# Create a custom print function for chatbot responses
def chatbot_print(*args, **kwargs):
    """
    Wrapper for console.print that automatically adds the chatbot prefix.
    Preserves all original console.print functionality.
    """
    # If there's a message to print (args has content)
    if args:
        # If the message already starts with the chatbot prefix, print as is
        if isinstance(args[0], str) and args[0].startswith("[bold green]Chatbot:"):
            console.print(*args, **kwargs)
        else:
            # For string arguments, prepend the prefix
            if isinstance(args[0], str):
                message = f"[bold green]Chatbot:[/] {args[0]}"
                console.print(message, *args[1:], **kwargs)
            else:
                # For non-string first arguments (like panels, tables)
                # Print the prefix first, then the content
                console.print("[bold green]Chatbot:[/]", *args, **kwargs)
    else:
        # If no arguments, just print the prefix
        console.print("[bold green]Chatbot:[/]", **kwargs)

def print_ai():
    """Print the AI art representation."""
    ai_art = text2art("AI", font="block")
    console.print(ai_art, style="bold red")  # Keep original as this is not a chatbot message

def chatbot():
    """Run the chatbot interaction loop."""
    print_ai()
    chatbot_print("Hi! I am your chatbot. You can ask me anything! Type 'what can you do' to see features.")

    while True:
        user_input = Prompt.ask("[bold blue]You[/]").lower()
        handle_user_input(user_input)

def handle_user_input(user_input):
    """Handle user input and provide appropriate responses."""
    responses = {
        # Welcome conversation
        "hello": "Hello! How can I help you?",
        "hi": "Hi! How can I help you?",
        "hey": "Hey! How can I help you?",
        "how are you": "I'm just a program, but I'm doing great! How about you?",
        "who are you": "I am Zuro, your friendly chatbot. How can I assist you?",

        # Features
        "what can you do": "\n\ntype 'Encrypt' to encrypt your text \n\ntype 'Decrypt' to decrypt your text \n\ntype 'fake' to generate a fake information \n\nand you can ask me 'anything' :) \n\ntype 'bye' to exit.",

        # Name
        "name": "My name is Zuro. How can I help you?",
        "what's your name": "My name is Zuro. I am chat-bot build by Python. How can I help you?",

        # End conversation
        "bye": "Goodbye! Have a great day!"
    }
    
    # Command handlers dictionary
    commands = {
        "encrypt": encrypt_text,
        "decrypt": decrypt_text,
        "fake": generate_fake_info,
        "bye": lambda: (chatbot_print(responses["bye"]), sys.exit())
    }
    
    # Check for exact matches first
    if user_input in responses:
        chatbot_print(responses[user_input])
        return False
    
    # Check for command keywords
    for cmd, handler in commands.items():
        if cmd in user_input:
            handler()
            return False
    
    # Default response if no match
    chatbot_print("I'm not sure I understand.\nCan you ask something else?")
    return False

def encrypt_text():
    """Encrypt the user's text input using AES-CBC."""
    input_text = Prompt.ask("[bold blue]Enter your text to encrypt[/]")
    KeySeed = Prompt.ask("[bold blue]Enter your password[/]")

    # Generate a 32-byte key from the password
    key = hashlib.sha256(KeySeed.encode()).digest()
    
    # Add verification string to validate successful decryption
    input_text += "EncryptDecryptSigning"

    # Add padding to make text length a multiple of 16 bytes (AES block size)
    while len(input_text) % 16 != 0:
        input_text += " "

    # Generate IV from the key for AES-CBC mode
    # Using CBC instead of ECB for better security with plaintext
    iv = hashlib.sha256(key).digest()[:16]

    # Perform encryption
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_text = cipher.encrypt(input_text.encode())
    encrypted_text = encrypted_text.hex()

    # Display result
    chatbot_print("Here is your encrypted text")
    console.print(f"[bold red]{encrypted_text}[/]")  # Keep original formatting for encrypted text

def decrypt_text():
    """Decrypt the user's hex input using AES-CBC."""
    input_text = Prompt.ask("[bold blue]Enter your text to decrypt[/]")
    KeySeed = Prompt.ask(" \n[bold blue]Enter your password[/]")
    
    # Generate key and IV identical to encryption process
    key = hashlib.sha256(KeySeed.encode()).digest()
    iv = hashlib.sha256(key).digest()[:16]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypted_text = cipher.decrypt(bytes.fromhex(input_text))
        decrypted_text = decrypted_text.decode('utf-8')

        # Verify decryption was successful using the verification string
        if not decrypted_text.__contains__("EncryptDecryptSigning"):
            chatbot_print("Decryption failed. Invalid key or corrupted data.")
            return
            
        # Extract original text by removing verification string
        decrypted_text = decrypted_text.split("EncryptDecryptSigning")[0]
        chatbot_print(f"Here is your decrypted text \n{decrypted_text}")
        
    except ValueError:
        chatbot_print("Decryption failed. Invalid key/text or corrupted data.")
        return

def generate_fake_info():
    """Generate and display fake information."""
    fake_info = fakefarsi.complete()
    chatbot_print(f"Here is your fake information: \n{fake_info}")

# Entry point
if __name__ == "__main__":
    chatbot()