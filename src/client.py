import httpx
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse, parse_qs
from .config import Config

class CanvasClient:
    def __init__(self):
        Config.validate()
        self.base_url = Config.CANVAS_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {Config.CANVAS_TOKEN}",
            "Accept": "application/json",
            "User-Agent": "canvas-mcp-py"
        }
        self.default_per_page = 50
        self.default_max_pages = 5

    async def _request(self, method: str, url: str, params: Optional[Dict] = None) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=self.headers, params=params)
            response.raise_for_status()
            return response

    def _parse_next_link(self, link_header: str) -> Optional[str]:
        if not link_header:
            return None
        
        links = link_header.split(",")
        for link in links:
            parts = link.split(";")
            if len(parts) < 2:
                continue
            
            url_part = parts[0].strip()
            rel_part = parts[1].strip()
            
            if 'rel="next"' in rel_part:
                if url_part.startswith("<") and url_part.endswith(">"):
                    return url_part[1:-1]
                return url_part
        return None

    async def request(self, path: str, method: str = "GET", params: Optional[Dict] = None, paginate: bool = False, max_pages: int = None) -> Union[Dict, List]:
        if not path.startswith("http"):
            url = f"{self.base_url}{path}"
        else:
            url = path

        # Handle array parameters for Canvas (e.g., include[] instead of include)
        processed_params = {}
        if params:
            for key, value in params.items():
                if value is None:
                    continue
                if isinstance(value, list):
                    processed_params[f"{key}[]"] = value
                else:
                    processed_params[key] = value

        response = await self._request(method, url, params=processed_params)
        data = response.json()

        if not paginate or not isinstance(data, list):
            return data

        results = data
        max_p = max_pages if max_pages is not None else self.default_max_pages
        page_count = 1
        
        next_link = self._parse_next_link(response.headers.get("link"))
        
        while next_link and page_count < max_p:
            # next_link usually contains the full URL with params
            response = await self._request("GET", next_link)
            new_data = response.json()
            if isinstance(new_data, list):
                results.extend(new_data)
            else:
                break
                
            next_link = self._parse_next_link(response.headers.get("link"))
            page_count += 1
            
        return results

    async def get_file_content(self, url: str) -> bytes:
        """Download file content (binary)."""
        # Canvas file URLs might require auth, or might be public S3/CDN links.
        # We'll try with auth first.
        try:
             async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers)
                if response.status_code == 403 or response.status_code == 401:
                     # Try without auth headers (e.g. signed S3 url)
                    response = await client.get(url)  
                
                response.raise_for_status()
                return response.content
        except Exception as e:
            # Fallback: try blindly without auth if first attempt failed differently or as retry logic
             async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.content

client = CanvasClient()
