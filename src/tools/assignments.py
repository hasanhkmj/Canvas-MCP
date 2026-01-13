from typing import List, Optional
import json
from fastmcp import FastMCP
from ..client import client

def register_tools(mcp: FastMCP):
    # --- Assignments ---
    @mcp.tool()
    async def list_assignments(
        course_id: str,
        search_term: Optional[str] = None,
        bucket: Optional[str] = None,
        order_by: Optional[str] = None,
        include: Optional[List[str]] = None,
        per_page: int = 50,
        max_pages: int = 5,
        max_items: Optional[int] = None
    ) -> str:
        """
        List assignments for a course.
        
        Args:
            bucket: Filter by bucket (past, overdue, undated, etc).
            order_by: Order by (position, due_at, name, etc).
        """
        params = {
            "search_term": search_term,
            "bucket": bucket,
            "order_by": order_by,
            "include": include,
            "per_page": per_page
        }
        try:
            data = await client.request(
                f"/api/v1/courses/{course_id}/assignments",
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
    async def get_assignment(
        course_id: str,
        assignment_id: str,
        include: Optional[List[str]] = None
    ) -> str:
        """Get details for a single assignment."""
        try:
            data = await client.request(
                f"/api/v1/courses/{course_id}/assignments/{assignment_id}",
                params={"include": include}
            )
            return json.dumps(data, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    # --- Quizzes ---
    @mcp.tool()
    async def list_quizzes(
        course_id: str,
        search_term: Optional[str] = None,
        per_page: int = 50,
        max_pages: int = 5,
        max_items: Optional[int] = None
    ) -> str:
        """List quizzes for a course."""
        try:
            data = await client.request(
                f"/api/v1/courses/{course_id}/quizzes",
                params={"search_term": search_term, "per_page": per_page},
                paginate=True,
                max_pages=max_pages
            )
            if max_items and isinstance(data, list):
                data = data[:max_items]
            return json.dumps(data, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    async def get_quiz(course_id: str, quiz_id: str) -> str:
        """Get a single quiz."""
        try:
            data = await client.request(f"/api/v1/courses/{course_id}/quizzes/{quiz_id}")
            return json.dumps(data, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})
