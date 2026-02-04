from exa_py import Exa
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class ExaService:
    """Service for searching job postings using Exa API."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Exa client."""
        self.api_key = api_key or settings.exa_api_key
        if not self.api_key:
            raise ValueError("Exa API key is required. Set EXA_API_KEY in your .env file")

        self.client = Exa(api_key=self.api_key)

    async def search_vc_jobs(
        self,
        query: str = "venture capital jobs hiring",
        num_results: int = 50,
        start_published_date: Optional[str] = None,
        use_autoprompt: bool = True,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Search for VC job postings using Exa API.

        Args:
            query: Search query for jobs
            num_results: Number of results to return (max 100)
            start_published_date: Filter by publication date (ISO format)
            use_autoprompt: Use Exa's autoprompt for better results
            include_domains: List of domains to include
            exclude_domains: List of domains to exclude

        Returns:
            List of job postings as dictionaries
        """
        try:
            # If no start date provided, default to last 30 days
            if not start_published_date:
                thirty_days_ago = datetime.now() - timedelta(days=30)
                start_published_date = thirty_days_ago.strftime("%Y-%m-%d")

            logger.info(f"Searching Exa for: '{query}' (limit: {num_results})")

            # Perform search with content retrieval
            search_response = self.client.search_and_contents(
                query=query,
                num_results=min(num_results, 100),  # Exa max is 100
                use_autoprompt=use_autoprompt,
                start_published_date=start_published_date,
                include_domains=include_domains,
                exclude_domains=exclude_domains,
                text=True,  # Get text content
                highlights=True  # Get relevant highlights
            )

            logger.info(f"Found {len(search_response.results)} results from Exa")

            # Transform results
            jobs = []
            for result in search_response.results:
                job_data = self._transform_exa_result(result)
                if job_data:
                    jobs.append(job_data)

            return jobs

        except Exception as e:
            logger.error(f"Error searching Exa API: {str(e)}")
            raise

    def _transform_exa_result(self, result) -> Optional[Dict]:
        """Transform Exa search result into job format."""
        try:
            # Extract key information from the result
            title = result.title or "Untitled Position"
            url = result.url
            text_content = result.text or ""
            highlights = result.highlights or []
            published_date = result.published_date

            # Try to extract company from URL or title
            company = self._extract_company(url, title)

            # Try to extract location from content
            location = self._extract_location(text_content, highlights)

            # Build job dictionary
            job_data = {
                "title": title[:255],  # Truncate to fit DB field
                "company": company[:255],
                "location": location,
                "description": self._build_description(text_content, highlights),
                "source": "exa",
                "source_url": url,
                "source_job_id": result.id,
                "posted_date": self._parse_date(published_date),
                "is_vc_related": True,  # Assuming VC-related since we searched for VC jobs
                "tags": "exa,ai-search"
            }

            return job_data

        except Exception as e:
            logger.error(f"Error transforming Exa result: {str(e)}")
            return None

    def _extract_company(self, url: str, title: str) -> str:
        """Extract company name from URL or title."""
        # Try to get company from domain
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc

            # Remove common prefixes and suffixes
            company = domain.replace("www.", "").replace(".com", "").replace(".ai", "")
            company = company.split(".")[0]

            # Capitalize
            company = company.replace("-", " ").replace("_", " ").title()

            if company and len(company) > 2:
                return company
        except:
            pass

        # Fallback: try to extract from title (e.g., "Software Engineer at Sequoia")
        if " at " in title:
            parts = title.split(" at ")
            if len(parts) > 1:
                return parts[-1].strip()

        if " @ " in title:
            parts = title.split(" @ ")
            if len(parts) > 1:
                return parts[-1].strip()

        return "Unknown Company"

    def _extract_location(self, text: str, highlights: List[str]) -> Optional[str]:
        """Extract location from text content."""
        import re

        # Common location patterns
        location_patterns = [
            r'(?:located in|based in|office in|location:)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z]{2})',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z]{2})',  # City, State format
            r'(San Francisco|New York|Los Angeles|Boston|Austin|Seattle|Remote)',
        ]

        # Check highlights first (more relevant)
        search_text = " ".join(highlights) if highlights else text[:1000]

        for pattern in location_patterns:
            match = re.search(pattern, search_text, re.IGNORECASE)
            if match:
                return match.group(1) if match.lastindex else match.group(0)

        return None

    def _build_description(self, text: str, highlights: List[str]) -> str:
        """Build job description from text and highlights."""
        if highlights:
            # Use highlights as they contain the most relevant info
            description = "\n\n".join(highlights[:5])  # Top 5 highlights
        else:
            # Use first 2000 chars of text
            description = text[:2000]

        return description

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string to datetime."""
        if not date_str:
            return None

        try:
            # Try ISO format
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except:
            try:
                # Try other common formats
                from dateutil import parser
                return parser.parse(date_str)
            except:
                return None

    async def search_specific_companies(
        self,
        companies: List[str],
        num_results_per_company: int = 10
    ) -> List[Dict]:
        """Search for jobs at specific VC firms."""
        all_jobs = []

        for company in companies:
            query = f"jobs at {company} venture capital hiring"
            jobs = await self.search_vc_jobs(
                query=query,
                num_results=num_results_per_company
            )
            all_jobs.extend(jobs)

        return all_jobs

    async def search_by_role(
        self,
        role: str,
        num_results: int = 50
    ) -> List[Dict]:
        """Search for specific role types in VC."""
        query = f"{role} venture capital jobs hiring"
        return await self.search_vc_jobs(query=query, num_results=num_results)
