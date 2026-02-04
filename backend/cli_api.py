"""API client for VC Dashboard CLI."""
import requests
from typing import Optional, Dict, List, Any


class APIClient:
    """Client for making requests to the VC Dashboard API."""

    def __init__(self, base_url: str):
        """Initialize API client.

        Args:
            base_url: Base URL of the API (e.g., http://localhost:8000).
        """
        self.base_url = base_url.rstrip('/')

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            endpoint: API endpoint path.
            **kwargs: Additional arguments to pass to requests.

        Returns:
            JSON response from the API.

        Raises:
            Exception: If the request fails.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")

    # Dashboard
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get unified dashboard statistics."""
        return self._request('GET', '/api/dashboard/stats')

    # Jobs
    def list_jobs(self, skip: int = 0, limit: int = 20, **filters) -> Dict[str, Any]:
        """List job postings with optional filters."""
        params = {'skip': skip, 'limit': limit, **filters}
        return self._request('GET', '/api/jobs/', params=params)

    def get_job(self, job_id: int) -> Dict[str, Any]:
        """Get details for a specific job."""
        return self._request('GET', f'/api/jobs/{job_id}')

    def get_job_stats(self) -> Dict[str, Any]:
        """Get job statistics."""
        return self._request('GET', '/api/jobs/stats')

    # Applications
    def list_applications(self, skip: int = 0, limit: int = 20, **filters) -> Dict[str, Any]:
        """List job applications with optional filters."""
        params = {'skip': skip, 'limit': limit, **filters}
        return self._request('GET', '/api/applications/', params=params)

    def create_application(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new job application."""
        return self._request('POST', '/api/applications/', json=data)

    def update_application(self, app_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing job application."""
        return self._request('PUT', f'/api/applications/{app_id}', json=data)

    def get_application(self, app_id: int) -> Dict[str, Any]:
        """Get details for a specific application."""
        return self._request('GET', f'/api/applications/{app_id}')

    def delete_application(self, app_id: int) -> Dict[str, Any]:
        """Delete a job application."""
        return self._request('DELETE', f'/api/applications/{app_id}')

    def get_application_stats(self) -> Dict[str, Any]:
        """Get application statistics."""
        return self._request('GET', '/api/applications/stats')

    # Startups
    def list_startups(self, skip: int = 0, limit: int = 20, **filters) -> Dict[str, Any]:
        """List startups with optional filters."""
        params = {'skip': skip, 'limit': limit, **filters}
        return self._request('GET', '/api/startups/', params=params)

    def get_startup(self, startup_id: int) -> Dict[str, Any]:
        """Get details for a specific startup."""
        return self._request('GET', f'/api/startups/{startup_id}')

    def create_startup(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new startup entry."""
        return self._request('POST', '/api/startups/', json=data)

    def update_startup(self, startup_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing startup."""
        return self._request('PUT', f'/api/startups/{startup_id}', json=data)

    def delete_startup(self, startup_id: int) -> Dict[str, Any]:
        """Delete a startup."""
        return self._request('DELETE', f'/api/startups/{startup_id}')

    # Dealflow
    def list_dealflow(self, skip: int = 0, limit: int = 20, **filters) -> Dict[str, Any]:
        """List dealflow applications with optional filters."""
        params = {'skip': skip, 'limit': limit, **filters}
        return self._request('GET', '/api/dealflow/', params=params)

    def get_dealflow(self, app_id: int) -> Dict[str, Any]:
        """Get details for a specific dealflow application."""
        return self._request('GET', f'/api/dealflow/{app_id}')

    def create_dealflow(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new dealflow application."""
        return self._request('POST', '/api/dealflow/', json=data)

    def update_dealflow(self, app_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing dealflow application."""
        return self._request('PUT', f'/api/dealflow/{app_id}', json=data)

    def delete_dealflow(self, app_id: int) -> Dict[str, Any]:
        """Delete a dealflow application."""
        return self._request('DELETE', f'/api/dealflow/{app_id}')

    def log_contact(self, app_id: int, contact_type: str) -> Dict[str, Any]:
        """Log a contact (email or meeting) for a dealflow application."""
        return self._request('POST', f'/api/dealflow/{app_id}/contact',
                           json={'contact_type': contact_type})

    def get_dealflow_stats(self) -> Dict[str, Any]:
        """Get dealflow pipeline statistics."""
        return self._request('GET', '/api/dealflow/stats')

    # Scraping - Jobs
    def scrape_jobs(self, query: str, num_results: int = 50) -> Dict[str, Any]:
        """Start job scraping with a search query."""
        return self._request('POST', '/api/scraping/start',
                           json={'query': query, 'num_results': num_results})

    def scrape_firms(self, firms: List[str], num_per_firm: int = 10) -> Dict[str, Any]:
        """Scrape jobs from specific VC firms."""
        return self._request('POST', '/api/scraping/search-firms',
                           json={'firms': firms, 'num_per_firm': num_per_firm})

    def scrape_role(self, role: str, num_results: int = 50) -> Dict[str, Any]:
        """Scrape jobs for a specific role."""
        return self._request('POST', '/api/scraping/search-role',
                           json={'role': role, 'num_results': num_results})

    def get_scraping_logs(self, limit: int = 10) -> Dict[str, Any]:
        """Get recent scraping logs."""
        return self._request('GET', '/api/scraping/logs', params={'limit': limit})

    def get_scraping_status(self) -> Dict[str, Any]:
        """Get latest scraping status."""
        return self._request('GET', '/api/scraping/status')

    # Scraping - Dealflow
    def scrape_dealflow(self, query: str, num_results: int = 30) -> Dict[str, Any]:
        """Start dealflow scraping with a search query."""
        return self._request('POST', '/api/dealflow-scraping/start',
                           json={'query': query, 'num_results': num_results})

    def scrape_accelerator(self, accelerator: str, batch_name: str, num_results: int = 30) -> Dict[str, Any]:
        """Scrape startups from an accelerator batch."""
        return self._request('POST', '/api/dealflow-scraping/accelerator',
                           json={'accelerator': accelerator, 'batch_name': batch_name,
                                'num_results': num_results})

    def scrape_sectors(self, sectors: List[str], num_per_sector: int = 20) -> Dict[str, Any]:
        """Scrape startups from specific sectors."""
        return self._request('POST', '/api/dealflow-scraping/sectors',
                           json={'sectors': sectors, 'num_per_sector': num_per_sector})

    def get_dealflow_scraping_logs(self, limit: int = 10) -> Dict[str, Any]:
        """Get recent dealflow scraping logs."""
        return self._request('GET', '/api/dealflow-scraping/logs', params={'limit': limit})

    def get_dealflow_scraping_status(self) -> Dict[str, Any]:
        """Get latest dealflow scraping status."""
        return self._request('GET', '/api/dealflow-scraping/status')
