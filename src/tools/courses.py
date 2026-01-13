from typing import List, Optional, Union
import json
from fastmcp import FastMCP
from ..client import client

def register_tools(mcp: FastMCP):
    @mcp.tool()
    async def list_courses(
        enrollment_state: Optional[str] = None,
        state: Optional[str] = None,
        search_term: Optional[str] = None,
        include: Optional[List[str]] = None,
        per_page: int = 50,
        max_pages: int = 5,
        max_items: Optional[int] = None
    ) -> str:
        """
        List courses the current user can access.
        
        Args:
            enrollment_state: Filter by enrollment_state (active, invited, etc).
            state: Filter by course state (available, completed, etc).
            search_term: Filter by search term.
            include: Array of extra data to include (e.g. ['term', 'teachers']).
            per_page: Items per page (Canvas max 100).
            max_pages: Max pages to fetch.
            max_items: Max items to return.
        """
        params = {
            "enrollment_state": enrollment_state,
            "state": state,
            "search_term": search_term,
            "include": include,
            "per_page": per_page
        }
        
        try:
            data = await client.request(
                "/api/v1/courses", 
                params=params, 
                paginate=True, 
                max_pages=max_pages
            )
            
            if max_items and isinstance(data, list):
                data = data[:max_items]
                
            return json.dumps(data, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    async def get_course(
        course_id: str,
        include: Optional[List[str]] = None
    ) -> str:
        """
        Get details for a single course.
        
        Args:
            course_id: The ID of the course.
            include: Array of extra data to include.
        """
        params = {"include": include}
        try:
            data = await client.request(f"/api/v1/courses/{course_id}", params=params)
            return json.dumps(data, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})
