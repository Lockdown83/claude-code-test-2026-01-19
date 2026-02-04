"""Output formatting utilities for VC Dashboard CLI using Rich."""
from typing import Dict, List, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box


console = Console()


def format_error(message: str) -> None:
    """Format and print an error message.

    Args:
        message: Error message to display.
    """
    console.print(f"\n[bold red]Error:[/bold red] {message}\n")


def format_success(message: str) -> None:
    """Format and print a success message.

    Args:
        message: Success message to display.
    """
    console.print(f"\n[bold green]✓[/bold green] {message}\n")


def format_info(message: str) -> None:
    """Format and print an info message.

    Args:
        message: Info message to display.
    """
    console.print(f"\n[bold cyan]ℹ[/bold cyan] {message}\n")


def format_table(data: List[Dict[str, Any]], columns: List[Dict[str, str]]) -> Table:
    """Create a Rich table from data.

    Args:
        data: List of dictionaries containing row data.
        columns: List of column definitions with 'name', 'key', and optional 'style'.

    Returns:
        Formatted Rich Table object.
    """
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)

    for col in columns:
        table.add_column(col['name'], style=col.get('style', ''))

    for row in data:
        table.add_row(*[str(row.get(col['key'], '')) for col in columns])

    return table


def format_stats_panel(stats: Dict[str, Any]) -> tuple:
    """Format dashboard stats with panels and colors.

    Args:
        stats: Dashboard statistics dictionary.

    Returns:
        Tuple of (jobs_panel, dealflow_panel).
    """
    # Jobs section
    jobs_data = stats.get('jobs', {})
    jobs_apps = jobs_data.get('applications', {})
    jobs_goal = jobs_data.get('weekly_goal', {})

    jobs_text = f"""
[bold]Activity[/bold]
Total Active Jobs: {jobs_data.get('total_active', 0)}
Total Applications: {jobs_apps.get('total', 0)}

[bold]Success Metrics[/bold]
Response Rate: {jobs_apps.get('response_rate', 0):.1%}
Interview Rate: {jobs_apps.get('interview_rate', 0):.1%}
Offer Rate: {jobs_apps.get('offer_rate', 0):.1%}

[bold]Goals & Consistency[/bold]
Weekly Goal: {jobs_goal.get('current', 0)}/{jobs_goal.get('target', 10)}
Current Streak: {jobs_data.get('current_streak', 0)} days 🔥
    """

    # Dealflow section
    dealflow_data = stats.get('dealflow', {})
    dealflow_goal = dealflow_data.get('weekly_goal', {})
    dealflow_network = dealflow_data.get('network_growth', {})

    dealflow_text = f"""
[bold]Pipeline[/bold]
Total Startups: {dealflow_data.get('total_startups', 0)}
In Pipeline: {dealflow_data.get('total_in_pipeline', 0)}

[bold]Network Growth[/bold]
Emails Sent: {dealflow_network.get('total_emails_sent', 0)}
Meetings Held: {dealflow_network.get('total_meetings_held', 0)}
Intros Made: {dealflow_network.get('total_intros_made', 0)}

[bold]Goals & Consistency[/bold]
Weekly Goal: {dealflow_goal.get('current', 0)}/{dealflow_goal.get('target', 5)}
Current Streak: {dealflow_data.get('current_streak', 0)} days 🔥
    """

    jobs_panel = Panel(jobs_text.strip(), title="📊 Job Applications", border_style="green", padding=(1, 2))
    dealflow_panel = Panel(dealflow_text.strip(), title="🚀 Dealflow", border_style="blue", padding=(1, 2))

    return jobs_panel, dealflow_panel


def format_job_detail(job: Dict[str, Any]) -> Panel:
    """Format detailed job information as a panel.

    Args:
        job: Job data dictionary.

    Returns:
        Formatted Rich Panel.
    """
    details = f"""
[bold cyan]Title:[/bold cyan] {job.get('title', 'N/A')}
[bold cyan]Company:[/bold cyan] {job.get('company', 'N/A')}
[bold cyan]Location:[/bold cyan] {job.get('location', 'N/A')}
[bold cyan]Type:[/bold cyan] {job.get('job_type', 'N/A')}
[bold cyan]Seniority:[/bold cyan] {job.get('seniority_level', 'N/A')}
[bold cyan]Salary:[/bold cyan] {job.get('salary_range', 'N/A')}
[bold cyan]Source:[/bold cyan] {job.get('source', 'N/A')}
[bold cyan]URL:[/bold cyan] {job.get('source_url', 'N/A')}

[bold cyan]Description:[/bold cyan]
{job.get('description', 'No description available')[:500]}...
    """

    return Panel(details.strip(), title=f"Job #{job.get('id')}", border_style="green", padding=(1, 2))


def format_startup_detail(startup: Dict[str, Any]) -> Panel:
    """Format detailed startup information as a panel.

    Args:
        startup: Startup data dictionary.

    Returns:
        Formatted Rich Panel.
    """
    details = f"""
[bold cyan]Name:[/bold cyan] {startup.get('name', 'N/A')}
[bold cyan]Website:[/bold cyan] {startup.get('website', 'N/A')}
[bold cyan]Industry:[/bold cyan] {startup.get('industry', 'N/A')}
[bold cyan]Funding Stage:[/bold cyan] {startup.get('funding_stage', 'N/A')}
[bold cyan]Funding Amount:[/bold cyan] {startup.get('funding_amount', 'N/A')}
[bold cyan]Valuation:[/bold cyan] {startup.get('valuation', 'N/A')}
[bold cyan]Source:[/bold cyan] {startup.get('source', 'N/A')}

[bold cyan]Description:[/bold cyan]
{startup.get('description', 'No description available')[:500]}...

[bold cyan]Founders:[/bold cyan]
{startup.get('founders', 'N/A')}

[bold cyan]Traction:[/bold cyan]
{startup.get('traction_metrics', 'N/A')}
    """

    return Panel(details.strip(), title=f"Startup #{startup.get('id')}", border_style="blue", padding=(1, 2))


def format_application_detail(application: Dict[str, Any]) -> Panel:
    """Format detailed application information as a panel.

    Args:
        application: Application data dictionary.

    Returns:
        Formatted Rich Panel.
    """
    job = application.get('job', {})

    details = f"""
[bold cyan]Job:[/bold cyan] {job.get('title', 'N/A')} at {job.get('company', 'N/A')}
[bold cyan]Status:[/bold cyan] {application.get('status', 'N/A')}
[bold cyan]Applied Date:[/bold cyan] {application.get('applied_date', 'N/A')}
[bold cyan]Last Contact:[/bold cyan] {application.get('last_contact_date', 'N/A')}
[bold cyan]Next Follow-up:[/bold cyan] {application.get('next_follow_up_date', 'N/A')}
[bold cyan]Interviews:[/bold cyan] {application.get('interview_count', 0)}

[bold cyan]Notes:[/bold cyan]
{application.get('notes', 'No notes')}

[bold cyan]Interview Notes:[/bold cyan]
{application.get('interview_notes', 'No interview notes')}
    """

    return Panel(details.strip(), title=f"Application #{application.get('id')}", border_style="yellow", padding=(1, 2))


def format_dealflow_detail(dealflow: Dict[str, Any]) -> Panel:
    """Format detailed dealflow application information as a panel.

    Args:
        dealflow: Dealflow application data dictionary.

    Returns:
        Formatted Rich Panel.
    """
    startup = dealflow.get('startup', {})

    details = f"""
[bold cyan]Startup:[/bold cyan] {startup.get('name', 'N/A')}
[bold cyan]Status:[/bold cyan] {dealflow.get('status', 'N/A')}
[bold cyan]First Contact:[/bold cyan] {dealflow.get('first_contact_date', 'N/A')}
[bold cyan]Last Contact:[/bold cyan] {dealflow.get('last_contact_date', 'N/A')}
[bold cyan]Emails Sent:[/bold cyan] {dealflow.get('emails_sent', 0)}
[bold cyan]Meetings Held:[/bold cyan] {dealflow.get('meetings_held', 0)}
[bold cyan]Intro Made To:[/bold cyan] {dealflow.get('intro_made_to', 'N/A')}
[bold cyan]Outcome:[/bold cyan] {dealflow.get('outcome', 'In Progress')}

[bold cyan]Research Summary:[/bold cyan]
{dealflow.get('research_summary', 'No research summary')}

[bold cyan]Notes:[/bold cyan]
{dealflow.get('notes', 'No notes')}
    """

    return Panel(details.strip(), title=f"Dealflow #{dealflow.get('id')}", border_style="cyan", padding=(1, 2))


def format_compact_summary(stats: Dict[str, Any]) -> str:
    """Format a compact one-line dashboard summary.

    Args:
        stats: Dashboard statistics dictionary.

    Returns:
        Formatted summary string.
    """
    jobs_data = stats.get('jobs', {})
    dealflow_data = stats.get('dealflow', {})
    combined = stats.get('combined', {})

    return (
        f"📊 Jobs: {jobs_data.get('applications', {}).get('total', 0)} apps | "
        f"🚀 Dealflow: {dealflow_data.get('total_startups', 0)} startups | "
        f"🔥 Streak: {combined.get('overall_streak', 0)} days"
    )
