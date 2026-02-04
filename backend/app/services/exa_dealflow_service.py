from exa_py import Exa
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.config import settings
import logging
import re

logger = logging.getLogger(__name__)


class ExaDealflowService:
    """Service for searching startups/companies using Exa API."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Exa client."""
        self.api_key = api_key or settings.exa_api_key
        if not self.api_key:
            raise ValueError("Exa API key is required. Set EXA_API_KEY in your .env file")

        self.client = Exa(api_key=self.api_key)

    async def search_accelerator_batch(
        self,
        accelerator: str,
        batch_name: str,
        num_results: int = 50
    ) -> List[Dict]:
        """
        Search for startups from a specific accelerator batch.

        Args:
            accelerator: Accelerator name (e.g., "Y Combinator", "Techstars")
            batch_name: Batch identifier (e.g., "W24", "2024")
            num_results: Number of results to return

        Returns:
            List of startup dictionaries
        """
        query = f"{accelerator} {batch_name} batch startups companies"
        return await self.search_startups(query=query, num_results=num_results)

    async def search_by_sector(
        self,
        sector: str,
        num_results: int = 50,
        funding_stage: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for startups in a specific sector/industry.

        Args:
            sector: Industry sector (e.g., "fintech", "AI", "biotech")
            num_results: Number of results to return
            funding_stage: Optional funding stage filter (e.g., "seed", "series-a")

        Returns:
            List of startup dictionaries
        """
        stage_text = f"{funding_stage} stage" if funding_stage else ""
        query = f"{sector} startups {stage_text} 2024 2025 funding"
        return await self.search_startups(query=query, num_results=num_results)

    async def search_by_funding_stage(
        self,
        stage: str,
        num_results: int = 50
    ) -> List[Dict]:
        """
        Search for startups at a specific funding stage.

        Args:
            stage: Funding stage (e.g., "seed", "series-a", "series-b")
            num_results: Number of results to return

        Returns:
            List of startup dictionaries
        """
        query = f"{stage} stage startups fundraising 2024 2025"
        return await self.search_startups(query=query, num_results=num_results)

    async def search_startups(
        self,
        query: str,
        num_results: int = 50,
        start_published_date: Optional[str] = None,
        use_autoprompt: bool = True
    ) -> List[Dict]:
        """
        Generic startup search using Exa API.

        Args:
            query: Search query
            num_results: Number of results to return (max 100)
            start_published_date: Filter by publication date (ISO format)
            use_autoprompt: Use Exa's autoprompt for better results

        Returns:
            List of startup dictionaries
        """
        try:
            # Default to last 90 days if no start date provided
            if not start_published_date:
                ninety_days_ago = datetime.now() - timedelta(days=90)
                start_published_date = ninety_days_ago.strftime("%Y-%m-%d")

            logger.info(f"Searching Exa for startups: '{query}' (limit: {num_results})")

            # Perform search with content retrieval
            search_response = self.client.search_and_contents(
                query=query,
                num_results=min(num_results, 100),  # Exa max is 100
                use_autoprompt=use_autoprompt,
                start_published_date=start_published_date,
                text=True,  # Get text content
                highlights=True  # Get relevant highlights
            )

            logger.info(f"Found {len(search_response.results)} results from Exa")

            # Transform results
            startups = []
            for result in search_response.results:
                startup_data = self._transform_exa_result(result)
                if startup_data:
                    startups.append(startup_data)

            return startups

        except Exception as e:
            logger.error(f"Error searching Exa API: {str(e)}")
            raise

    def _transform_exa_result(self, result) -> Optional[Dict]:
        """Transform Exa search result into startup format."""
        try:
            title = result.title or "Untitled Company"
            url = result.url
            text_content = result.text or ""
            highlights = result.highlights or []
            published_date = result.published_date

            # Extract company name from title or URL
            name = self._extract_company_name(url, title)

            # Extract industry/sector
            industry = self._extract_industry(text_content, highlights)

            # Extract funding stage
            funding_stage = self._extract_funding_stage(text_content, highlights)

            # Extract funding amount
            funding_amount = self._extract_funding_amount(text_content, highlights)

            # Build description from highlights
            description = self._build_description(text_content, highlights)

            # Build startup dictionary
            startup_data = {
                "name": name[:255],
                "website": url,
                "description": description,
                "funding_stage": funding_stage,
                "funding_amount": funding_amount,
                "industry": industry,
                "source": "exa",
                "source_url": url,
                "source_id": result.id,
                "last_funding_date": self._parse_date(published_date),
                "tags": "exa,dealflow"
            }

            return startup_data

        except Exception as e:
            logger.error(f"Error transforming Exa result: {str(e)}")
            return None

    def _extract_company_name(self, url: str, title: str) -> str:
        """Extract company name from URL or title."""
        # Try to get company from domain
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            company = domain.replace("www.", "").replace(".com", "").replace(".ai", "").replace(".io", "")
            company = company.split(".")[0]
            company = company.replace("-", " ").replace("_", " ").title()

            if company and len(company) > 2:
                return company
        except:
            pass

        # Fallback: use title
        # Remove common prefixes
        title = re.sub(r'^(About|Company|Startup|)\s*[-:]\s*', '', title, flags=re.IGNORECASE)
        return title.split("|")[0].split("-")[0].strip()

    def _extract_industry(self, text: str, highlights: List[str]) -> Optional[str]:
        """Extract industry/sector from content."""
        search_text = " ".join(highlights[:3]) if highlights else text[:1000]

        # Common industry keywords
        industries = [
            "fintech", "finance", "financial", "banking",
            "AI", "artificial intelligence", "machine learning", "ML",
            "biotech", "healthcare", "health tech", "medical",
            "edtech", "education", "learning",
            "saas", "software", "enterprise",
            "e-commerce", "retail", "marketplace",
            "crypto", "blockchain", "web3",
            "climate tech", "cleantech", "sustainability"
        ]

        for industry in industries:
            if re.search(rf'\b{industry}\b', search_text, re.IGNORECASE):
                return industry.lower()

        return None

    def _extract_funding_stage(self, text: str, highlights: List[str]) -> Optional[str]:
        """Extract funding stage from content."""
        search_text = " ".join(highlights[:3]) if highlights else text[:1000]

        # Funding stage patterns
        stages = {
            "seed": r'\bseed\s+(round|funding|stage)\b',
            "series-a": r'\bseries\s+a\b',
            "series-b": r'\bseries\s+b\b',
            "series-c": r'\bseries\s+c\b',
            "pre-seed": r'\bpre-seed\b'
        }

        for stage, pattern in stages.items():
            if re.search(pattern, search_text, re.IGNORECASE):
                return stage

        return None

    def _extract_funding_amount(self, text: str, highlights: List[str]) -> Optional[str]:
        """Extract funding amount from content."""
        search_text = " ".join(highlights[:3]) if highlights else text[:1000]

        # Pattern: $X million, $XM, $X.YM
        pattern = r'\$\s*(\d+(?:\.\d+)?)\s*(million|billion|M|B)\b'
        match = re.search(pattern, search_text, re.IGNORECASE)

        if match:
            amount = match.group(1)
            unit = match.group(2).upper()
            if unit in ["MILLION", "M"]:
                return f"${amount}M"
            elif unit in ["BILLION", "B"]:
                return f"${amount}B"

        return None

    def _build_description(self, text: str, highlights: List[str]) -> str:
        """Build company description from text and highlights."""
        if highlights:
            return "\n\n".join(highlights[:5])  # Top 5 highlights
        else:
            return text[:2000]  # First 2000 chars

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string to datetime."""
        if not date_str:
            return None

        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except:
            try:
                from dateutil import parser
                return parser.parse(date_str)
            except:
                return None
