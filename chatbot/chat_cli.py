from client import init_chat
import asyncio
from colorama import init, Fore, Style

init(autoreset=True)  # Enable color support


# Box constants
BOX_TOP = "┌─ " + "─ " * 25 + "┐"
BOX_BOTTOM = "└─ " + "─ " * 25 + "┘"


async def cli_chat_loop():
    print(Fore.CYAN + "╔" + "═" * 55 + "╗")
    print(Fore.CYAN + "║{:^55}║".format("Welcome to the CLI AI Chat!"))
    print(
        Fore.CYAN + "║{:^55}║".format("Type your message below. Type 'exit' to quit.")
    )
    print(Fore.CYAN + "╚" + "═" * 55 + "╝" + Style.RESET_ALL)

    user_id = input(f"{Fore.LIGHTWHITE_EX}🔐 Enter your User ID: ").strip()
    print(f"{Fore.LIGHTBLACK_EX}User ID set to: {user_id}")

    while True:
        print(Fore.BLUE + "\n" + "=" * 60 + Style.RESET_ALL)
        user_input = input(Fore.GREEN + "🤠 You: " + Style.RESET_ALL).strip()

        if user_input.lower() in ["exit", "quit"]:
            print(Fore.CYAN + "\n╔" + "═" * 55 + "╗")
            print(Fore.CYAN + "║{:^55}║".format("Thank you for chatting! Goodbye!"))
            print(Fore.CYAN + "╚" + "═" * 55 + "╝" + Style.RESET_ALL)
            break

        # Thinking Box
        print(Fore.YELLOW + BOX_TOP)
        print(Fore.WHITE + "  AI is thinking...")
        print(Fore.YELLOW + BOX_BOTTOM + Style.RESET_ALL)

        try:
            ai_response = await init_chat(user_input, user_id)

            # Response Box
            print(Fore.MAGENTA + BOX_TOP)
            print(Fore.WHITE + "  " + str(ai_response))  # Single-line, raw text
            print(Fore.MAGENTA + BOX_BOTTOM + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + BOX_TOP)
            print(Fore.RED + "  An error occurred: " + str(e))
            print(Fore.RED + BOX_BOTTOM + Style.RESET_ALL)


# Run
if __name__ == "__main__":
    asyncio.run(cli_chat_loop())
