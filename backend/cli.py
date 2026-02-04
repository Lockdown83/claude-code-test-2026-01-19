#!/usr/bin/env python3
"""VC Dashboard CLI - Command-line interface for the VC Dashboard API."""
import click
import json
from cli_config import load_config, save_config
from cli_api import APIClient
from cli_formatters import (
    console, format_error, format_success, format_info, format_table,
    format_stats_panel, format_job_detail, format_startup_detail,
    format_application_detail, format_dealflow_detail, format_compact_summary
)


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """VC Dashboard CLI - Manage jobs and dealflow from the terminal.

    A command-line interface for tracking VC job applications and dealflow sourcing.
    """
    pass


# =============================================================================
# DASHBOARD COMMANDS
# =============================================================================

@cli.group()
def dashboard():
    """View dashboard statistics and summaries."""
    pass


@dashboard.command('stats')
@click.option('--format', 'output_format', type=click.Choice(['full', 'compact', 'json']),
              default='full', help='Output format')
def dashboard_stats(output_format):
    """Show complete dashboard statistics."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])
        stats = client.get_dashboard_stats()

        if output_format == 'json':
            console.print_json(data=stats)
        elif output_format == 'compact':
            console.print(f"\n{format_compact_summary(stats)}\n")
        else:
            # Full formatted display
            jobs_panel, dealflow_panel = format_stats_panel(stats)
            console.print()
            console.print(jobs_panel)
            console.print(dealflow_panel)
            console.print()

    except Exception as e:
        format_error(str(e))


@dashboard.command('summary')
def dashboard_summary():
    """Quick one-line dashboard summary."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])
        stats = client.get_dashboard_stats()
        console.print(f"\n{format_compact_summary(stats)}\n")
    except Exception as e:
        format_error(str(e))


# =============================================================================
# JOBS COMMANDS
# =============================================================================

@cli.group()
def jobs():
    """Manage job postings and searches."""
    pass


@jobs.command('list')
@click.option('--limit', default=20, help='Number of jobs to show')
@click.option('--source', help='Filter by source')
@click.option('--company', help='Filter by company name')
@click.option('--search', help='Search in title/description')
def jobs_list(limit, source, company, search):
    """List job postings with optional filters."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])

        filters = {}
        if source:
            filters['source'] = source
        if company:
            filters['company'] = company
        if search:
            filters['search'] = search

        result = client.list_jobs(limit=limit, **filters)
        jobs_data = result.get('jobs', [])

        if not jobs_data:
            format_info("No jobs found matching your criteria.")
            return

        table = format_table(jobs_data, columns=[
            {'name': 'ID', 'key': 'id', 'style': 'cyan'},
            {'name': 'Title', 'key': 'title'},
            {'name': 'Company', 'key': 'company', 'style': 'green'},
            {'name': 'Location', 'key': 'location'},
            {'name': 'Type', 'key': 'job_type'},
            {'name': 'Posted', 'key': 'posted_date'}
        ])

        console.print(f"\n[bold]Found {result.get('total', 0)} jobs[/bold]")
        console.print(table)
        console.print()

    except Exception as e:
        format_error(str(e))


@jobs.command('show')
@click.argument('job_id', type=int)
def jobs_show(job_id):
    """Show detailed information for a specific job."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])
        job = client.get_job(job_id)

        console.print()
        console.print(format_job_detail(job))
        console.print()

    except Exception as e:
        format_error(str(e))


@jobs.command('stats')
def jobs_stats():
    """Show job statistics and metrics."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])
        stats = client.get_job_stats()

        console.print(f"\n[bold magenta]Job Statistics[/bold magenta]\n")
        console.print(f"Total Jobs Found: {stats.get('total_jobs_found', 0)}")
        console.print(f"Active Jobs: {stats.get('active_jobs', 0)}")
        console.print(f"Jobs Last 7 Days: {stats.get('jobs_last_7_days', 0)}")

        console.print(f"\n[bold]Jobs by Source:[/bold]")
        for source, count in stats.get('jobs_by_source', {}).items():
            console.print(f"  {source}: {count}")

        console.print(f"\n[bold]Top Companies:[/bold]")
        for company, count in list(stats.get('jobs_by_company', {}).items())[:10]:
            console.print(f"  {company}: {count}")
        console.print()

    except Exception as e:
        format_error(str(e))


# =============================================================================
# APPLICATIONS COMMANDS
# =============================================================================

@cli.group()
def apps():
    """Track and manage job applications."""
    pass


@apps.command('list')
@click.option('--limit', default=20, help='Number of applications to show')
@click.option('--status', type=click.Choice(['saved', 'applied', 'interviewing', 'rejected', 'offer', 'accepted']),
              help='Filter by status')
def apps_list(limit, status):
    """List job applications with optional filters."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])

        filters = {}
        if status:
            filters['status'] = status

        result = client.list_applications(limit=limit, **filters)
        apps_data = result.get('applications', [])

        if not apps_data:
            format_info("No applications found matching your criteria.")
            return

        table = format_table(apps_data, columns=[
            {'name': 'ID', 'key': 'id', 'style': 'cyan'},
            {'name': 'Job Title', 'key': 'job_title'},
            {'name': 'Company', 'key': 'company', 'style': 'green'},
            {'name': 'Status', 'key': 'status', 'style': 'yellow'},
            {'name': 'Applied', 'key': 'applied_date'},
            {'name': 'Interviews', 'key': 'interview_count'}
        ])

        console.print(f"\n[bold]Found {result.get('total', 0)} applications[/bold]")
        console.print(table)
        console.print()

    except Exception as e:
        format_error(str(e))


@apps.command('show')
@click.argument('app_id', type=int)
def apps_show(app_id):
    """Show detailed information for a specific application."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])
        app = client.get_application(app_id)

        console.print()
        console.print(format_application_detail(app))
        console.print()

    except Exception as e:
        format_error(str(e))


@apps.command('create')
@click.argument('job_id', type=int)
@click.option('--status', default='saved',
              type=click.Choice(['saved', 'applied', 'interviewing']),
              help='Initial status')
@click.option('--notes', help='Application notes')
def apps_create(job_id, status, notes):
    """Create a new job application."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])

        data = {
            'job_id': job_id,
            'status': status
        }
        if notes:
            data['notes'] = notes

        app = client.create_application(data)
        format_success(f"Created application #{app['id']} for job #{job_id}")

    except Exception as e:
        format_error(str(e))


@apps.command('update')
@click.argument('app_id', type=int)
@click.option('--status', type=click.Choice(['saved', 'applied', 'interviewing', 'rejected', 'offer', 'accepted']),
              help='Update status')
@click.option('--notes', help='Update notes')
@click.option('--resume', help='Resume version used')
@click.option('--cover-letter', help='Cover letter path')
def apps_update(app_id, status, notes, resume, cover_letter):
    """Update an existing job application."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])

        data = {}
        if status:
            data['status'] = status
        if notes:
            data['notes'] = notes
        if resume:
            data['resume_version'] = resume
        if cover_letter:
            data['cover_letter_path'] = cover_letter

        if not data:
            format_error("No update parameters provided.")
            return

        app = client.update_application(app_id, data)
        format_success(f"Updated application #{app_id}")

    except Exception as e:
        format_error(str(e))


@apps.command('delete')
@click.argument('app_id', type=int)
@click.confirmation_option(prompt='Are you sure you want to delete this application?')
def apps_delete(app_id):
    """Delete a job application."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])
        client.delete_application(app_id)
        format_success(f"Deleted application #{app_id}")
    except Exception as e:
        format_error(str(e))


@apps.command('stats')
def apps_stats():
    """Show application statistics and metrics."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])
        stats = client.get_application_stats()

        console.print(f"\n[bold magenta]Application Statistics[/bold magenta]\n")
        console.print(f"Total Applications: {stats.get('total', 0)}")

        console.print(f"\n[bold]By Status:[/bold]")
        for status, count in stats.get('by_status', {}).items():
            console.print(f"  {status}: {count}")

        console.print(f"\n[bold]Success Metrics:[/bold]")
        console.print(f"  Response Rate: {stats.get('response_rate', 0):.1%}")
        console.print(f"  Interview Rate: {stats.get('interview_rate', 0):.1%}")
        console.print(f"  Offer Rate: {stats.get('offer_rate', 0):.1%}")
        console.print()

    except Exception as e:
        format_error(str(e))


# =============================================================================
# STARTUPS COMMANDS
# =============================================================================

@cli.group()
def startups():
    """Manage startup/company information."""
    pass


@startups.command('list')
@click.option('--limit', default=20, help='Number of startups to show')
@click.option('--stage', help='Filter by funding stage')
@click.option('--industry', help='Filter by industry')
@click.option('--search', help='Search in name/description')
def startups_list(limit, stage, industry, search):
    """List startups with optional filters."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])

        filters = {}
        if stage:
            filters['funding_stage'] = stage
        if industry:
            filters['industry'] = industry
        if search:
            filters['search'] = search

        result = client.list_startups(limit=limit, **filters)
        startups_data = result.get('startups', [])

        if not startups_data:
            format_info("No startups found matching your criteria.")
            return

        table = format_table(startups_data, columns=[
            {'name': 'ID', 'key': 'id', 'style': 'cyan'},
            {'name': 'Name', 'key': 'name', 'style': 'green'},
            {'name': 'Industry', 'key': 'industry'},
            {'name': 'Stage', 'key': 'funding_stage'},
            {'name': 'Funding', 'key': 'funding_amount'},
            {'name': 'Source', 'key': 'source'}
        ])

        console.print(f"\n[bold]Found {result.get('total', 0)} startups[/bold]")
        console.print(table)
        console.print()

    except Exception as e:
        format_error(str(e))


@startups.command('show')
@click.argument('startup_id', type=int)
def startups_show(startup_id):
    """Show detailed information for a specific startup."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])
        startup = client.get_startup(startup_id)

        console.print()
        console.print(format_startup_detail(startup))
        console.print()

    except Exception as e:
        format_error(str(e))


# =============================================================================
# DEALFLOW COMMANDS
# =============================================================================

@cli.group()
def dealflow():
    """Manage dealflow pipeline and sourcing."""
    pass


@dealflow.command('list')
@click.option('--limit', default=20, help='Number of dealflow items to show')
@click.option('--status',
              type=click.Choice(['sourced', 'researching', 'contacted', 'meeting', 'shared', 'progressing', 'closed']),
              help='Filter by status')
def dealflow_list(limit, status):
    """List dealflow applications with optional filters."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])

        filters = {}
        if status:
            filters['status'] = status

        result = client.list_dealflow(limit=limit, **filters)
        dealflow_data = result.get('applications', [])

        if not dealflow_data:
            format_info("No dealflow items found matching your criteria.")
            return

        table = format_table(dealflow_data, columns=[
            {'name': 'ID', 'key': 'id', 'style': 'cyan'},
            {'name': 'Startup', 'key': 'startup_name', 'style': 'green'},
            {'name': 'Status', 'key': 'status', 'style': 'yellow'},
            {'name': 'First Contact', 'key': 'first_contact_date'},
            {'name': 'Emails', 'key': 'emails_sent'},
            {'name': 'Meetings', 'key': 'meetings_held'}
        ])

        console.print(f"\n[bold]Found {result.get('total', 0)} dealflow items[/bold]")
        console.print(table)
        console.print()

    except Exception as e:
        format_error(str(e))


@dealflow.command('show')
@click.argument('app_id', type=int)
def dealflow_show(app_id):
    """Show detailed information for a specific dealflow item."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])
        dealflow_item = client.get_dealflow(app_id)

        console.print()
        console.print(format_dealflow_detail(dealflow_item))
        console.print()

    except Exception as e:
        format_error(str(e))


@dealflow.command('create')
@click.argument('startup_id', type=int)
@click.option('--notes', help='Initial notes')
@click.option('--research', help='Research summary')
def dealflow_create(startup_id, notes, research):
    """Add a startup to the dealflow pipeline."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])

        data = {
            'startup_id': startup_id,
            'status': 'sourced'
        }
        if notes:
            data['notes'] = notes
        if research:
            data['research_summary'] = research

        app = client.create_dealflow(data)
        format_success(f"Created dealflow item #{app['id']} for startup #{startup_id}")

    except Exception as e:
        format_error(str(e))


@dealflow.command('update')
@click.argument('app_id', type=int)
@click.option('--status',
              type=click.Choice(['sourced', 'researching', 'contacted', 'meeting', 'shared', 'progressing', 'closed']),
              help='Update status')
@click.option('--notes', help='Update notes')
@click.option('--research', help='Update research summary')
@click.option('--outcome',
              type=click.Choice(['passed', 'invested', 'lost_to_competitor', 'no_response', 'not_a_fit']),
              help='Set outcome (for closed status)')
def dealflow_update(app_id, status, notes, research, outcome):
    """Update an existing dealflow item."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])

        data = {}
        if status:
            data['status'] = status
        if notes:
            data['notes'] = notes
        if research:
            data['research_summary'] = research
        if outcome:
            data['outcome'] = outcome

        if not data:
            format_error("No update parameters provided.")
            return

        app = client.update_dealflow(app_id, data)
        format_success(f"Updated dealflow item #{app_id}")

    except Exception as e:
        format_error(str(e))


@dealflow.command('contact')
@click.argument('app_id', type=int)
@click.option('--type', 'contact_type', required=True,
              type=click.Choice(['email', 'meeting']),
              help='Type of contact')
def dealflow_contact(app_id, contact_type):
    """Log a contact (email or meeting) for a dealflow item."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])
        result = client.log_contact(app_id, contact_type)

        format_success(f"Logged {contact_type} for dealflow item #{app_id}")
        console.print(f"Total Emails: {result.get('emails_sent', 0)}")
        console.print(f"Total Meetings: {result.get('meetings_held', 0)}\n")

    except Exception as e:
        format_error(str(e))


@dealflow.command('delete')
@click.argument('app_id', type=int)
@click.confirmation_option(prompt='Are you sure you want to delete this dealflow item?')
def dealflow_delete(app_id):
    """Delete a dealflow item."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])
        client.delete_dealflow(app_id)
        format_success(f"Deleted dealflow item #{app_id}")
    except Exception as e:
        format_error(str(e))


@dealflow.command('stats')
def dealflow_stats():
    """Show dealflow pipeline statistics and metrics."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])
        stats = client.get_dealflow_stats()

        console.print(f"\n[bold magenta]Dealflow Statistics[/bold magenta]\n")
        console.print(f"Total in Pipeline: {stats.get('total_in_pipeline', 0)}")

        console.print(f"\n[bold]Pipeline Breakdown:[/bold]")
        for status, count in stats.get('pipeline_breakdown', {}).items():
            console.print(f"  {status}: {count}")

        console.print(f"\n[bold]Network Growth:[/bold]")
        console.print(f"  Total Emails Sent: {stats.get('total_emails_sent', 0)}")
        console.print(f"  Total Meetings: {stats.get('total_meetings_held', 0)}")
        console.print(f"  Intros Made: {stats.get('total_intros_made', 0)}")

        console.print(f"\n[bold]Outcomes:[/bold]")
        for outcome, count in stats.get('outcomes', {}).items():
            console.print(f"  {outcome}: {count}")
        console.print()

    except Exception as e:
        format_error(str(e))


# =============================================================================
# SCRAPING COMMANDS
# =============================================================================

@cli.group()
def scrape():
    """Run scraping operations for jobs and dealflow."""
    pass


@scrape.command('jobs')
@click.argument('query')
@click.option('--limit', default=50, help='Number of results to scrape')
def scrape_jobs(query, limit):
    """Scrape jobs with a search query."""
    try:
        config = load_config()
        client = APIClient(config['api_url'])

        with console.status(f"[bold green]Scraping jobs for: {query}..."):
            result = client.scrape_jobs(query, limit)

        console.print(f"\n[bold green]✓ Scraping complete![/bold green]")
        console.print(f"Found: {result.get('jobs_found', 0)}")
        console.print(f"New: {result.get('jobs_new', 0)}")
        console.print(f"Updated: {result.get('jobs_updated', 0)}")
        console.print(f"Duration: {result.get('duration_seconds', 0):.1f}s\n")

    except Exception as e:
        format_error(str(e))


@scrape.command('firms')
@click.argument('firms')
@click.option('--each', default=10, help='Results per firm')
def scrape_firms(firms, each):
    """Scrape jobs from VC firms (comma-separated).

    Example: vc-dashboard scrape firms "Sequoia,a16z,Greylock" --each 10
    """
    try:
        config = load_config()
        client = APIClient(config['api_url'])
        firm_list = [f.strip() for f in firms.split(',')]

        with console.status(f"[bold green]Scraping {len(firm_list)} firms..."):
            result = client.scrape_firms(firm_list, each)

        console.print(f"\n[bold green]✓ Scraping complete![/bold green]")
        console.print(f"Found: {result.get('jobs_found', 0)}")
        console.print(f"New: {result.get('jobs_new', 0)}")
        console.print(f"Duration: {result.get('duration_seconds', 0):.1f}s\n")

    except Exception as e:
        format_error(str(e))


@scrape.command('accelerator')
@click.argument('name')
@click.argument('batch')
@click.option('--limit', default=30, help='Number of results to scrape')
def scrape_accelerator(name, batch, limit):
    """Scrape startups from an accelerator batch.

    Example: vc-dashboard scrape accelerator "Y Combinator" "W24" --limit 30
    """
    try:
        config = load_config()
        client = APIClient(config['api_url'])

        with console.status(f"[bold green]Scraping {name} {batch}..."):
            result = client.scrape_accelerator(name, batch, limit)

        console.print(f"\n[bold green]✓ Scraping complete![/bold green]")
        console.print(f"Found: {result.get('startups_found', 0)}")
        console.print(f"New: {result.get('startups_new', 0)}")
        console.print(f"Updated: {result.get('startups_updated', 0)}")
        console.print(f"Duration: {result.get('duration_seconds', 0):.1f}s\n")

    except Exception as e:
        format_error(str(e))


@scrape.command('sectors')
@click.argument('sectors')
@click.option('--each', default=20, help='Results per sector')
def scrape_sectors(sectors, each):
    """Scrape startups from sectors (comma-separated).

    Example: vc-dashboard scrape sectors "fintech,AI,biotech" --each 20
    """
    try:
        config = load_config()
        client = APIClient(config['api_url'])
        sector_list = [s.strip() for s in sectors.split(',')]

        with console.status(f"[bold green]Scraping {len(sector_list)} sectors..."):
            result = client.scrape_sectors(sector_list, each)

        console.print(f"\n[bold green]✓ Scraping complete![/bold green]")
        console.print(f"Found: {result.get('startups_found', 0)}")
        console.print(f"New: {result.get('startups_new', 0)}")
        console.print(f"Duration: {result.get('duration_seconds', 0):.1f}s\n")

    except Exception as e:
        format_error(str(e))


# =============================================================================
# CONFIG COMMANDS
# =============================================================================

@cli.group()
def config():
    """Manage CLI configuration settings."""
    pass


@config.command('show')
def config_show():
    """Show current configuration."""
    try:
        cfg = load_config()
        console.print("\n[bold magenta]Current Configuration[/bold magenta]\n")
        console.print_json(data=cfg)
        console.print()
    except Exception as e:
        format_error(str(e))


@config.command('set-api-url')
@click.argument('url')
def config_set_api_url(url):
    """Set the API base URL."""
    try:
        cfg = load_config()
        cfg['api_url'] = url.rstrip('/')
        save_config(cfg)
        format_success(f"API URL set to: {url}")
    except Exception as e:
        format_error(str(e))


if __name__ == '__main__':
    cli()
