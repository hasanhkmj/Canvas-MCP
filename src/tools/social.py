from typing import List, Optional
import json
from fastmcp import FastMCP
from ..client import client

def register_tools(mcp: FastMCP):
    # --- Announcements ---
    @mcp.tool()
    async def list_announcements(
        context_codes: Optional[List[str]] = None,
        course_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        per_page: int = 50,
        max_pages: int = 5,
        max_items: Optional[int] = None
    ) -> str:
        """
        List announcements for a course or context codes.
        
        Args:
            context_codes: List of context codes (e.g. course_123).
            course_id: Alternative to context_codes (will be converted to course_ID).
            start_date: ISO8601 start date.
            end_date: ISO8601 end date.
        """
        codes = context_codes
        if not codes and course_id:
            codes = [f"course_{course_id}"]
            
        params = {
            "context_codes": codes,
            "start_date": start_date,
            "end_date": end_date,
            "per_page": per_page
        }
        try:
            data = await client.request(
                "/api/v1/announcements",
                params=params,
                paginate=True,
                max_pages=max_pages
            )
            if max_items and isinstance(data, list):
                data = data[:max_items]
            return json.dumps(data, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    # --- Discussions ---
    @mcp.tool()
    async def list_discussion_topics(
        course_id: str,
        search_term: Optional[str] = None,
        include: Optional[List[str]] = None,
        per_page: int = 50,
        max_pages: int = 5,
        max_items: Optional[int] = None
    ) -> str:
        """List discussion topics for a course."""
        params = {
            "search_term": search_term,
            "include": include,
            "per_page": per_page
        }
        try:
            data = await client.request(
                f"/api/v1/courses/{course_id}/discussion_topics",
                params=params,
                paginate=True,
                max_pages=max_pages
            )
            if max_items and isinstance(data, list):
                data = data[:max_items]
            return json.dumps(data, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    # --- Calendar ---
    @mcp.tool()
    async def list_calendar_events(
        context_codes: Optional[List[str]] = None,
        type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        per_page: int = 50,
        max_pages: int = 5,
        max_items: Optional[int] = None
    ) -> str:
        """
        List calendar events.
        
        Args:
            type: 'event' or 'assignment'.
        """
        params = {
            "context_codes": context_codes,
            "type": type,
            "start_date": start_date,
            "end_date": end_date,
            "per_page": per_page
        }
        try:
            data = await client.request(
                "/api/v1/calendar_events",
                params=params,
                paginate=True,
                max_pages=max_pages
            )
            if max_items and isinstance(data, list):
                data = data[:max_items]
            return json.dumps(data, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    # --- Todo ---
    @mcp.tool()
    async def list_todo(
        per_page: int = 50,
        max_pages: int = 5,
        max_items: Optional[int] = None
    ) -> str:
        """List the current user's to-do items."""
        try:
            data = await client.request(
                "/api/v1/users/self/todo",
                params={"per_page": per_page},
                paginate=True,
                max_pages=max_pages
            )
            if max_items and isinstance(data, list):
                data = data[:max_items]
            return json.dumps(data, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})
