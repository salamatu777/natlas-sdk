import click
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from natlas import NAtlasClient
from natlas.orthography import NigerianOrthographyEngine
from natlas.guardrails import SovereignCulturalGuardrail
from natlas.harness.eval import SovereignBenchmarkHarness
import os
import sys

# Ensure UTF-8 output on legacy Windows consoles
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console(force_terminal=True)

@click.group()
def app():
    """N-ATLAS Developer Harness (DSH) & Sovereign AI Toolkit"""
    pass

@app.command()
@click.argument('message', required=False)
@click.option('--language', '-l', default='en', help='Language code (en, yo, ha, ig)')
def chat(message, language):
    """Start an interactive chat REPL or send a one-shot message."""
    client = NAtlasClient()
    
    if message:
        response = client.chat(message, language=language)
        console.print(Markdown(response.text))
        return
        
    console.print(f"[bold green]Starting interactive chat ({language}). Type 'exit' to quit.[/bold green]")
    while True:
        try:
            user_input = console.input("[bold blue]You:[/bold blue] ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            response = client.chat(user_input, language=language)
            console.print(f"[bold purple]N-ATLAS:[/bold purple] ", end="")
            console.print(Markdown(response.text))
        except KeyboardInterrupt:
            break

@app.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--language', '-l', default=None, help='Force language code')
def transcribe(file_path, language):
    """Transcribe an audio file using N-ATLAS Whisper ASR."""
    client = NAtlasClient()
    console.print("[yellow]Transcribing audio...[/yellow]")
    result = client.transcribe(file_path, language=language)
    console.print(f"[green]Detected Language: {result.language}[/green]")
    console.print(f"[bold]Transcript:[/bold] {result.text}")

@app.command()
@click.option('--port', default=8000, help='Port to bind to')
def harness(port):
    """Launch the Visual N-ATLAS Developer Harness Workbench in browser."""
    import uvicorn
    console.print(f"[bold green]🚀 Launching N-ATLAS Developer Harness at http://localhost:{port}/harness ...[/bold green]")
    uvicorn.run("natlas.server:app", host="0.0.0.0", port=port, reload=True)

@app.command()
@click.option('--port', default=8000, help='Port to bind to')
def serve(port):
    """Start the API server (OpenAI-compatible)."""
    import uvicorn
    console.print(f"[bold green]Starting N-ATLAS API Server on port {port}...[/bold green]")
    uvicorn.run("natlas.server:app", host="0.0.0.0", port=port, reload=True)

@app.command(name="eval")
@click.option('--suite', default='all', help='Suite to run (all, ha_bias, yo_ortho, ig_syntax)')
def evaluate(suite):
    """Run the Sovereign Benchmark Evaluation Suite across Nigerian languages."""
    client = NAtlasClient()
    harness_instance = SovereignBenchmarkHarness(client)
    console.print("[bold yellow]Running Sovereign N-ATLAS Benchmark Diagnostic...[/bold yellow]")
    
    report = harness_instance.run_suite(suite)
    
    table = Table(title=f"N-ATLAS Sovereign Benchmark Diagnostic [Composite: {report.overall_score}/5.0]")
    table.add_column("Task Name", style="cyan")
    table.add_column("Language", style="magenta")
    table.add_column("Score", justify="right")
    table.add_column("Status", justify="center")
    table.add_column("Diagnostic Details", style="white")

    for t in report.task_results:
        status_str = "[bold green]PASS[/bold green]" if t.passed else "[bold yellow]NEEDS TUNING[/bold yellow]"
        table.add_row(t.task_name, t.target_language, f"{t.score} / 5.0", status_str, t.details)

    console.print(table)

@app.command()
@click.argument('text')
def guard(text):
    """Audit prompt against Sovereign Cultural Safety & Ethnic Bias rules."""
    result = SovereignCulturalGuardrail.check_safety(text)
    if result.is_safe:
        console.print(f"[bold green][CLEARED][/bold green] {result.explanation}")
    else:
        console.print(f"[bold red][FLAGGED - Risk: {result.risk_level}][/bold red] {result.explanation}")
        console.print(f"[yellow]Mitigated Action:[/yellow] {result.mitigated_prompt}")

@app.command()
@click.argument('text')
@click.option('--language', '-l', default='yo', help='Language (yo or ig)')
def fertility(text, language):
    """Analyze token fertility and diacritic fragmentation ratio."""
    report = NigerianOrthographyEngine.analyze_token_fertility(text, language)
    console.print(f"[bold]Language:[/bold] {report.language}")
    console.print(f"[bold]Words:[/bold] {report.word_count} | [bold]Estimated Tokens:[/bold] {report.estimated_token_count}")
    console.print(f"[bold cyan]Fertility Ratio:[/bold cyan] {report.fertility_ratio} tokens/word (English baseline ~1.3)")
    console.print(f"[bold yellow]Recommendation:[/bold yellow] {report.recommendation}")

@app.command()
@click.argument('query')
@click.option('--language', '-l', default='ha', help='Target language (ha, yo, ig, en)')
def agent(query, language):
    """Run autonomous sovereign agent reasoning against Nigerian tools."""
    from natlas.harness.agent import SovereignAgentHarness
    client = NAtlasClient()
    harness = SovereignAgentHarness(client)
    console.print(f"[bold cyan]🤖 Initiating Sovereign Agent Harness ({language})...[/bold cyan]")
    result = harness.run(query, language=language)
    
    if not result.guardrail_passed:
        console.print(f"[bold red]Safety Check:[/bold red] Flagged by sovereign cultural guardrail.")
        console.print(f"[yellow]{result.final_response}[/yellow]")
        return
        
    console.print(f"[bold green]Safety Check:[/bold green] Cleared ✅")
    console.print(f"[bold]Tools Invoked:[/bold] {result.tools_invoked or 'None (Direct Reasoning)'}")
    
    for idx, s in enumerate(result.steps):
        console.print(f"\n[bold blue]--- Step {idx+1} ---[/bold blue]")
        console.print(f"[italic]Thought:[/italic] {s.thought}")
        if s.action:
            console.print(f"[cyan]Action:[/cyan] {s.action}({s.action_input})")
        if s.observation:
            console.print(f"[magenta]Observation:[/magenta] {s.observation}")
            
    console.print(f"\n[bold green]Final Advisory Output ({language}):[/bold green]")
    console.print(Markdown(result.final_response))

@app.command()
def models():
    """List available models."""
    console.print("[bold]Available Sovereign Models:[/bold]")
    console.print("- NCAIR1/N-ATLaS (Llama-3 8B Multilingual SFT)")
    console.print("- NCAIR1/Hausa-ASR (Whisper Small - 120h)")
    console.print("- NCAIR1/Yoruba-ASR (Whisper Small - 627h)")
    console.print("- NCAIR1/Igbo-ASR (Whisper Small - 120h)")
    console.print("- NCAIR1/NigerianAccentedEnglish (Whisper Small - 120h)")

if __name__ == '__main__':
    app()
