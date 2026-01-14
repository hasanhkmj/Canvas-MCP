import json
from typing import List, Optional, Union
from fastmcp import FastMCP
from ..client import client
from ..utils import extract_pdf_text

def register_tools(mcp: FastMCP):
    # --- Files ---
    @mcp.tool()
    async def list_files(
        course_id: Optional[str] = None,
        folder_id: Optional[str] = None,
        search_term: Optional[str] = None,
        include: Optional[List[str]] = None,
        per_page: int = 50,
        max_pages: int = 5,
        max_items: Optional[int] = None
    ) -> str:
        """List files for a course, folder, or the current user.
        
        NOTE: If you receive a 403 Forbidden error, the instructor has likely hidden the "Files" tab.
        In that case, try using `list_modules` with `include=['items']` to find course materials.
        """
        if folder_id:
            path = f"/api/v1/folders/{folder_id}/files"
        elif course_id:
            path = f"/api/v1/courses/{course_id}/files"
        else:
            path = "/api/v1/users/self/files"
            
        params = {
            "search_term": search_term,
            "include": include,
            "per_page": per_page
        }
        
        try:
            data = await client.request(path, params=params, paginate=True, max_pages=max_pages)
            if max_items and isinstance(data, list):
                data = data[:max_items]
            return json.dumps(data, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    async def get_file(file_id: str, include: Optional[List[str]] = None) -> str:
        """Get metadata for a file."""
        try:
            data = await client.request(f"/api/v1/files/{file_id}", params={"include": include})
            return json.dumps(data, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    async def read_pdf(file_id: str, max_chars: int = 20000) -> str:
        """Download a PDF file and extract its text."""
        try:
            # 1. Get file metadata
            file_meta = await client.request(f"/api/v1/files/{file_id}")
            if not isinstance(file_meta, dict):
                 return json.dumps({"error": f"Could not retrieve file metadata for id {file_id}"})

            name = file_meta.get("display_name", file_meta.get("filename", "unknown"))
            mime = file_meta.get("content-type", file_meta.get("mime_type", ""))
            
            # Basic validation
            if "pdf" not in mime.lower() and not name.lower().endswith(".pdf"):
                return json.dumps({"error": f"File {name} (type {mime}) does not appear to be a PDF."})

            # 2. Download content
            download_url = file_meta.get("url")
            if not download_url:
                 # Construct API download URL if 'url' not present
                 download_url = f"/api/v1/files/{file_id}/download"
            
            # client handles ensuring download param if needed, but usually the 'url' field works
            # We might need to ensure 'download=1' if using the API endpoint directly.
            # But client.get_file_content handles the request.
            
            buffer = await client.get_file_content(download_url)
            
            # 3. Parse PDF
            text = extract_pdf_text(buffer, max_chars=max_chars)
            
            result = {
                "file": {
                    "id": file_id,
                    "name": name,
                    "mime_type": mime,
                    "size": file_meta.get("size")
                },
                "text": text,
                "truncated": len(text) == max_chars if max_chars > 0 else False
            }
            return json.dumps(result, indent=2)
            
        except Exception as e:
             return json.dumps({"error": f"Error reading PDF: {str(e)}"})

    # --- Folders ---
    @mcp.tool()
    async def list_folders(
        course_id: str,
        per_page: int = 50,
        max_pages: int = 5,
        max_items: Optional[int] = None
    ) -> str:
        """List folders in a course."""
        try:
            data = await client.request(
                f"/api/v1/courses/{course_id}/folders", 
                params={"per_page": per_page}, 
                paginate=True, 
                max_pages=max_pages
            )
            if max_items and isinstance(data, list):
                data = data[:max_items]
            return json.dumps(data, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @mcp.tool()
    async def get_folder(folder_id: str) -> str:
        """Get metadata for a folder."""
        try:
            data = await client.request(f"/api/v1/folders/{folder_id}")
            return json.dumps(data, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    # --- Modules ---
    @mcp.tool()
    async def list_modules(
        course_id: str,
        include: Optional[List[str]] = None,
        per_page: int = 50,
        max_pages: int = 5,
        max_items: Optional[int] = None
    ) -> str:
        """List modules for a course.
        
        TIP: Use `include=['items']` to see all module items, including files.
        This is often the most reliable way to access course materials if `list_files` is restricted.
        """
        try:
            data = await client.request(
                f"/api/v1/courses/{course_id}/modules",
                params={"include": include, "per_page": per_page},
                paginate=True,
                max_pages=max_pages
            )
            if max_items and isinstance(data, list):
                data = data[:max_items]
            return json.dumps(data, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})

    # --- Pages ---
    @mcp.tool()
    async def list_pages(
        course_id: str,
        search_term: Optional[str] = None,
        sort: Optional[str] = None,
        per_page: int = 50,
        max_pages: int = 5,
        max_items: Optional[int] = None
    ) -> str:
        """List pages in a course."""
        params = {
            "search_term": search_term,
            "sort": sort,
            "per_page": per_page
        }
        try:
            data = await client.request(
                f"/api/v1/courses/{course_id}/pages",
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
    async def get_page(
        course_id: str,
        page_url: str,
        include_content: bool = False
    ) -> str:
        """Get a single page by page_url."""
        params = {}
        if include_content:
            params["include"] = ["body"]
            
        try:
            data = await client.request(
                f"/api/v1/courses/{course_id}/pages/{page_url}",
                params=params
            )
            return json.dumps(data, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)})
