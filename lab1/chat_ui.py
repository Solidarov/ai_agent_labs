import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from chat_service import ChatSession, MODEL, SYSTEM_PROMPT

console = Console()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def run_chat():
    session = ChatSession()
    current_temp = 0.5
    history = []

    while True:
        try:
            clear_screen()
            console.print(
                Panel(
                    "[bold cyan]Programming Instructor Chat[/bold cyan]\n"
                    "[dim]Type 'exit', 'quit', '/temp <val>', or '/json <prompt>, or '/info''[/dim]",
                    expand=False,
                )
            )

            # Re-render conversation history
            for sender, msg in history:
                if sender == "You":
                    console.print(f"\n[bold green]You:[/bold green] {msg}")
                elif sender == "System":
                    console.print(f"\n[bold yellow]System:[/bold yellow] {msg}")
                else:
                    console.print("\n[bold magenta]Instructor:[/bold magenta]")
                    # Markdown component renders model code blocks with syntax highlighting
                    console.print(Markdown(msg))

            # Prompt user input
            user_input = Prompt.ask("\n[bold green]You[/bold green]").strip()

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                console.print("\n[yellow]Exiting chat. Happy coding![/yellow]")
                break

            if user_input.startswith("/info"):

                console.print(
                    Panel(
                        f"[bold cyan]Model:[/bold cyan] {MODEL}\n"
                        f"[bold cyan]Temperature:[/bold cyan] {current_temp}\n"
                        f"[bold cyan]System Prompt:[/bold cyan] {SYSTEM_PROMPT}\n"
                        f"[bold cyan]Messages in Context:[/bold cyan] {len(session.messages)}",
                        title="[bold yellow]Current Session Configuration[/bold yellow]",
                        expand=False,
                    )
                )
                Prompt.ask("\n[dim]Press Enter to continue...[/dim]")
                continue

            if user_input.startswith("/temp "):
                history.append(("You", user_input))
                try:
                    current_temp = float(user_input.split()[1])
                    history.append(
                        (
                            "System",
                            f"Temperature changed to {current_temp}",
                        ),
                    )
                except ValueError:
                    history.append(
                        (
                            "System",
                            "Invalid temperature format. Use e.g. /temp 0.2",
                        ),
                    )
                continue

            is_json = user_input.startswith("/json ")
            clean_prompt = (
                user_input.replace("/json ", "", 1) if is_json else user_input
            )
            history.append(("You", user_input))

            # Clear screen before showing thinking state & response
            clear_screen()
            console.print(
                Panel(
                    "[bold cyan]Programming Instructor Chat[/bold cyan]",
                    expand=False,
                )
            )
            for sender, msg in history:
                if sender == "You":
                    console.print(f"\n[bold green]You:[/bold green] {msg}")
                else:
                    console.print("\n[bold magenta]Instructor:[/bold magenta]")
                    console.print(Markdown(msg))

            # Show status spinner while model processes request
            with console.status(
                "[bold yellow]Instructor is writing code...[/bold yellow]",
                spinner="dots",
            ):
                if is_json:
                    response = session.ask_structured(
                        clean_prompt, temperature=current_temp
                    )
                else:
                    response = session.ask(clean_prompt, temperature=current_temp)

            history.append(("Instructor", response))

        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Session ended.[/yellow]")
            sys.exit(0)
