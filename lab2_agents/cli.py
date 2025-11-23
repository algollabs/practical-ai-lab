import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

from lab2_agents.tools import ALL_TOOLS
from lab2_agents.agent import ManualReActAgent

app = typer.Typer()
console = Console()

@app.command()
def main():
    """
    Starts the Performance Review Assistant (Agent) in CLI mode.
    """
    console.print(Panel.fit(
        "[bold blue]Performance Review Assistant[/bold blue]\n"
        "Practical AI Corp - ReAct Agent Lab",
        subtitle="Type 'exit' to quit"
    ))

    # System Prompt
    system_prompt = """
    You are a helpful HR Assistant for Practical AI Corp.
    Your goal is to help managers draft Performance Reviews and OKRs.
    
    You have access to the following tools:
    - read_file: To read existing context or drafts.
    - save_plan: To save the final OKR plan.
    - get_okr_guidelines: To check best practices.
    
    ALWAYS check the guidelines before drafting a plan.
    If asked to create OKRs, reason through the requirements, check guidelines, 
    then draft the plan and save it.
    """

    # Initialize Agent
    console.print("[italic]Initializing Agent...[/italic]")
    try:
        agent = ManualReActAgent(tools=ALL_TOOLS, system_prompt=system_prompt)
        console.print("[green]Agent Ready![/green]\n")
    except Exception as e:
        console.print(f"[bold red]Error initializing agent:[/bold red] {e}")
        return

    # Interaction Loop
    while True:
        user_input = Prompt.ask("[bold cyan]You[/bold cyan]")
        
        if user_input.lower() in ["exit", "quit"]:
            console.print("[yellow]Goodbye![/yellow]")
            break
            
        if not user_input.strip():
            continue

        console.print("\n[italic dim]Agent is thinking...[/italic dim]")
        
        try:
            # We rely on the agent's internal print statements for the ReAct steps
            # so we just print the final result here nicely.
            response = agent.chat(user_input, verbose=True)
            
            console.print("\n[bold green]Assistant[/bold green]:")
            console.print(Markdown(response))
            console.print("\n" + "-"*50 + "\n")
            
        except Exception as e:
            console.print(f"[bold red]An error occurred:[/bold red] {e}")

if __name__ == "__main__":
    app()

