"""
Notes Tool
Save, retrieve, update, and delete notes using SQLite

Features:
- Create notes with title and content
- Search notes by keyword
- List all notes
- Update existing notes
- Delete notes
- Tag support
"""

import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotesTool:
    """
    Notes management tool using SQLite.
    
    Provides CRUD operations for notes storage.
    """
    
    def __init__(self, db_path: str = "agent_notes.db"):
        """
        Initialize notes tool with database.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self._connect()
        self._create_tables()
        
        logger.info(f"NotesTool initialized with database: {db_path}")
    
    def _connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Error connecting to database: {str(e)}")
            raise
    
    def _create_tables(self):
        """Create notes table if it doesn't exist"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    tags TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create index for faster searches
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_notes_title 
                ON notes(title)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_notes_content 
                ON notes(content)
            """)
            
            self.conn.commit()
            logger.info("Notes table created/verified")
            
        except Exception as e:
            logger.error(f"Error creating tables: {str(e)}")
            raise
    
    def create_note(self, title: str, content: str, tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Create a new note.
        
        Args:
            title: Note title
            content: Note content
            tags: Optional list of tags
            
        Returns:
            Dict with created note data
        """
        try:
            cursor = self.conn.cursor()
            
            # Convert tags list to comma-separated string
            tags_str = ','.join(tags) if tags else ''
            
            cursor.execute("""
                INSERT INTO notes (title, content, tags)
                VALUES (?, ?, ?)
            """, (title, content, tags_str))
            
            self.conn.commit()
            note_id = cursor.lastrowid
            
            logger.info(f"Created note with ID: {note_id}")
            
            # Retrieve the created note
            note = self.get_note(note_id)
            
            return {
                'success': True,
                'note': note,
                'explanation': f"Note created: '{title}' (ID: {note_id})"
            }
            
        except Exception as e:
            logger.error(f"Error creating note: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'explanation': 'Failed to create note'
            }
    
    def get_note(self, note_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific note by ID.
        
        Args:
            note_id: Note ID
            
        Returns:
            Note data or None if not found
        """
        try:
            cursor = self.conn.cursor()
            
            cursor.execute("""
                SELECT id, title, content, tags, created_at, updated_at
                FROM notes
                WHERE id = ?
            """, (note_id,))
            
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting note: {str(e)}")
            return None
    
    def list_notes(self, limit: int = 10) -> Dict[str, Any]:
        """
        List all notes.
        
        Args:
            limit: Maximum number of notes to return
            
        Returns:
            Dict with list of notes
        """
        try:
            cursor = self.conn.cursor()
            
            cursor.execute("""
                SELECT id, title, content, tags, created_at, updated_at
                FROM notes
                ORDER BY updated_at DESC
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            notes = [dict(row) for row in rows]
            
            if not notes:
                explanation = "No notes found. You can create a note using the create_note action."
            else:
                explanation = f"Found {len(notes)} notes:\n\n"
                for note in notes[:5]:  # Show first 5
                    explanation += f"• {note['title']} (ID: {note['id']})\n"
                    explanation += f"  {note['content'][:100]}...\n\n"
            
            return {
                'success': True,
                'notes': notes,
                'total_count': len(notes),
                'explanation': explanation
            }
            
        except Exception as e:
            logger.error(f"Error listing notes: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'notes': [],
                'total_count': 0,
                'explanation': 'Failed to list notes'
            }
    
    def search_notes(self, keyword: str) -> Dict[str, Any]:
        """
        Search notes by keyword in title or content.
        
        Args:
            keyword: Search keyword
            
        Returns:
            Dict with matching notes
        """
        try:
            cursor = self.conn.cursor()
            
            search_pattern = f"%{keyword}%"
            
            cursor.execute("""
                SELECT id, title, content, tags, created_at, updated_at
                FROM notes
                WHERE title LIKE ? OR content LIKE ?
                ORDER BY updated_at DESC
            """, (search_pattern, search_pattern))
            
            rows = cursor.fetchall()
            notes = [dict(row) for row in rows]
            
            if not notes:
                explanation = f"No notes found matching '{keyword}'"
            else:
                explanation = f"Found {len(notes)} notes matching '{keyword}':\n\n"
                for note in notes[:5]:
                    explanation += f"• {note['title']} (ID: {note['id']})\n"
                    explanation += f"  {note['content'][:100]}...\n\n"
            
            return {
                'success': True,
                'notes': notes,
                'total_count': len(notes),
                'keyword': keyword,
                'explanation': explanation
            }
            
        except Exception as e:
            logger.error(f"Error searching notes: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'notes': [],
                'total_count': 0,
                'explanation': f'Failed to search notes for: {keyword}'
            }
    
    def update_note(self, note_id: int, title: Optional[str] = None, 
                   content: Optional[str] = None, tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Update an existing note.
        
        Args:
            note_id: Note ID
            title: New title (optional)
            content: New content (optional)
            tags: New tags (optional)
            
        Returns:
            Dict with update result
        """
        try:
            # Check if note exists
            existing_note = self.get_note(note_id)
            if not existing_note:
                return {
                    'success': False,
                    'error': f'Note with ID {note_id} not found',
                    'explanation': f'Cannot update note {note_id} - not found'
                }
            
            cursor = self.conn.cursor()
            
            # Build update query dynamically
            updates = []
            params = []
            
            if title is not None:
                updates.append("title = ?")
                params.append(title)
            
            if content is not None:
                updates.append("content = ?")
                params.append(content)
            
            if tags is not None:
                updates.append("tags = ?")
                params.append(','.join(tags))
            
            updates.append("updated_at = CURRENT_TIMESTAMP")
            
            params.append(note_id)
            
            query = f"UPDATE notes SET {', '.join(updates)} WHERE id = ?"
            
            cursor.execute(query, params)
            self.conn.commit()
            
            logger.info(f"Updated note ID: {note_id}")
            
            # Retrieve updated note
            updated_note = self.get_note(note_id)
            
            return {
                'success': True,
                'note': updated_note,
                'explanation': f"Note updated: '{updated_note['title']}' (ID: {note_id})"
            }
            
        except Exception as e:
            logger.error(f"Error updating note: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'explanation': f'Failed to update note {note_id}'
            }
    
    def delete_note(self, note_id: int) -> Dict[str, Any]:
        """
        Delete a note.
        
        Args:
            note_id: Note ID
            
        Returns:
            Dict with deletion result
        """
        try:
            # Check if note exists
            existing_note = self.get_note(note_id)
            if not existing_note:
                return {
                    'success': False,
                    'error': f'Note with ID {note_id} not found',
                    'explanation': f'Cannot delete note {note_id} - not found'
                }
            
            cursor = self.conn.cursor()
            
            cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            self.conn.commit()
            
            logger.info(f"Deleted note ID: {note_id}")
            
            return {
                'success': True,
                'deleted_id': note_id,
                'explanation': f"Note deleted: '{existing_note['title']}' (ID: {note_id})"
            }
            
        except Exception as e:
            logger.error(f"Error deleting note: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'explanation': f'Failed to delete note {note_id}'
            }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")


# LangChain Tool wrapper
def get_notes_tool_for_langchain():
    """
    Create LangChain-compatible notes tool.
    
    Returns a function that handles various note operations.
    """
    notes_tool = NotesTool()
    
    def notes_wrapper(action: str, **kwargs) -> str:
        """
        Manage notes.
        
        Args:
            action: Action to perform (create, list, search, update, delete)
            **kwargs: Arguments for the action
                - title: Note title (for create, update)
                - content: Note content (for create, update)
                - note_id: Note ID (for get, update, delete)
                - keyword: Search keyword (for search)
                - limit: Number of notes to list (for list)
            
        Returns:
            Result as string
        """
        action = action.lower()
        
        if action == 'create':
            result = notes_tool.create_note(
                kwargs.get('title', ''),
                kwargs.get('content', ''),
                kwargs.get('tags')
            )
        elif action == 'list':
            result = notes_tool.list_notes(kwargs.get('limit', 10))
        elif action == 'search':
            result = notes_tool.search_notes(kwargs.get('keyword', ''))
        elif action == 'update':
            result = notes_tool.update_note(
                kwargs.get('note_id'),
                kwargs.get('title'),
                kwargs.get('content'),
                kwargs.get('tags')
            )
        elif action == 'delete':
            result = notes_tool.delete_note(kwargs.get('note_id'))
        elif action == 'get':
            note = notes_tool.get_note(kwargs.get('note_id'))
            if note:
                result = {
                    'success': True,
                    'explanation': f"Note: {note['title']}\n{note['content']}"
                }
            else:
                result = {
                    'success': False,
                    'explanation': 'Note not found'
                }
        else:
            result = {
                'success': False,
                'explanation': f'Unknown action: {action}'
            }
        
        return result['explanation']
    
    return notes_wrapper


# Example usage and testing
if __name__ == "__main__":
    notes = NotesTool("test_notes.db")
    
    print("🧪 Testing Notes Tool\n")
    
    # Test 1: Create note
    print("1️⃣ Creating note:")
    result = notes.create_note(
        "Python Tips",
        "Use list comprehensions for better performance",
        ["python", "coding"]
    )
    print(f"   {result['explanation']}\n")
    note_id = result['note']['id']
    
    # Test 2: Create another note
    print("2️⃣ Creating another note:")
    result = notes.create_note(
        "AI Resources",
        "Check out LangChain documentation for agent development",
        ["ai", "resources"]
    )
    print(f"   {result['explanation']}\n")
    
    # Test 3: List notes
    print("3️⃣ Listing all notes:")
    result = notes.list_notes()
    print(f"   {result['explanation']}")
    
    # Test 4: Search notes
    print("4️⃣ Searching for 'Python':")
    result = notes.search_notes("Python")
    print(f"   {result['explanation']}")
    
    # Test 5: Update note
    print("5️⃣ Updating note:")
    result = notes.update_note(
        note_id,
        content="Use list comprehensions and generators for better performance and memory efficiency"
    )
    print(f"   {result['explanation']}\n")
    
    # Test 6: Delete note
    print("6️⃣ Deleting note:")
    result = notes.delete_note(note_id)
    print(f"   {result['explanation']}\n")
    
    notes.close()
    
    # Clean up test database
    os.remove("test_notes.db")
    
    print("✅ All tests completed!")