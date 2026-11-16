import os
import sys
import getpass
import subprocess
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


def get_api_key() -> str:
    """Retrieves the Gemini API key via environment variable or interactive BYOK prompt."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("🔑 GEMINI_API_KEY not found in environment.")
        print("Get a free API key at: https://google.com")
        api_key = getpass.getpass("Enter your Gemini API Key (hidden): ").strip()
    
    if not api_key:
        print("❌ Error: An API key is required to run this agent.", file=sys.stderr)
        sys.exit(1)
        
    return api_key


def execute_linux_command(command: str) -> str:
    """Executes a bash command on the local Linux system after explicit user approval.

    Args:
        command: The exact bash command to execute.

    Returns:
        The stdout/stderr output of the command or a permission denial message.
    """
    print(f"\n⚠️  [Agent Proposed Command]: \033[93m{command}\033[0m")
    confirmation = input("Allow execution? [y/N]: ").strip().lower()

    if confirmation != "y":
        return "Execution denied by the user. Ask for an alternative approach or clarify requirements."

    try:
        result = subprocess.run(
            command,
            shell=True,
            text=True,
            capture_output=True,
            timeout=60
        )
        output = result.stdout.strip()
        error = result.stderr.strip()

        if result.returncode == 0:
            return output if output else "Command executed successfully with no output."
        else:
            return f"Command failed (Exit Code {result.returncode}):\n{error or output}"

    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 60 seconds."
    except Exception as e:
        return f"System execution error: {str(e)}"


def main() -> None:
    """Initializes and runs the interactive Agentic Linux CLI."""
    api_key = get_api_key()
    client = genai.Client(api_key=api_key)

    system_instruction = (
        "You are an autonomous Senior Linux Systems Administrator agent. "
        "Your goal is to diagnose, manage, and automate tasks on the user's Linux machine "
        "using the 'execute_linux_command' tool. "
        "Rules:\n"
        "1. Prefer non-destructive, read-only commands first when investigating.\n"
        "2. Execute one logical step at a time and analyze the output before proceeding.\n"
        "3. Never attempt to bypass user confirmation or obfuscate commands.\n"
        "4. Provide a clear, concise summary once the objective is achieved."
    )

    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[execute_linux_command],
            temperature=0.1,
        )
    )

    print("\n🐧 Linux Agentic CLI initialized (Powered by your BYOK)")
    print("Type 'exit' or 'quit' to terminate the session.\n")

    while True:
        try:
            user_input = input("\033[92muser@agentic-linux\033[0m:~$ ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Session terminated.")
                break

            response = chat.send_message(user_input)
            print(f"\n🤖 \033[96mAgent:\033[0m\n{response.text}\n")

        except KeyboardInterrupt:
            print("\nSession interrupted by user.")
            break
        except Exception as e:
            print(f"\n❌ API or Runtime Error: {str(e)}\n", file=sys.stderr)


if __name__ == "__main__":
    main()
