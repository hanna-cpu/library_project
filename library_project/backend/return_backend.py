import sqlite3
from typing import List
from library_project.backend.backend_common import NavigationState
from library_project.backend.library_classes import Book

# this is the main return state handler , whcich is a child class of NavigationState

class returnState(NavigationState):
    """State management for the return page."""
    books_data: List[dict] = []   # list of borrowed books data , used for UI to display
    books_objects: List[Book] = [] # list of Book objects corresponding to borrowed books as book objetcs ready for return operation
    selected_books: List[int] = []  # list of selected book ids for returning , from UI checkbox selection
    
    def set_username_from_query(self):
        """Set username from URL query parameter and load books."""
        super().set_username_from_query()
        self.load_borrowed_books(str(self.username))
    
    def load_borrowed_books(self, username: str = None):
        """Load borrowed books from database."""
        try:
            conn = sqlite3.connect('librarydb.db')
            cursor = conn.cursor()
            
            # Get user id from username
            get_user_query = "SELECT users.id FROM users WHERE username = ?"
            cursor.execute(get_user_query, (username,))
            rows = cursor.fetchall()
            
            if not rows:
                conn.close()
                return False
            userid = rows[0][0]

            # Get all borrowed books of the user
            query = """
            SELECT books.id, books.title, books.author
            FROM books 
            INNER JOIN borrowed ON books.id = borrowed.book_id
            WHERE borrowed.user_id = ?
            ORDER BY books.title
            """
            cursor.execute(query, (userid,))
            rows = cursor.fetchall()
            
            # Clear existing data
            self.books_data = []
            self.books_objects = []
            
            # Create Book objects and convert to dictionaries
            for row in rows:
                book = Book(
                    id=row[0],
                    title=row[1],
                    author=row[2]
                )
                self.books_objects.append(book)
                self.books_data.append(book.to_dict())
            
            conn.close()
            
        except Exception as e:
            print(f"Error loading books: {e}")
            import traceback
            traceback.print_exc()
            self.books_data = []
            self.books_objects = []
    
    def toggle_book_selection(self, book_id: int):
        """Toggle book selection for returning."""
        if book_id in self.selected_books:
            self.selected_books.remove(book_id)
        else:
            self.selected_books.append(book_id)
    
    def confirm_returns(self):
        """Handle confirm returns button click."""
        if not self.selected_books:
            print("No books selected to return")
            return
        
        success_count = 0
        failed_count = 0
        
        # Process each selected book
        for book_id in self.selected_books:
            # Find the book object with matching id
            book_obj = None
            for book in self.books_objects:
                if book.id == book_id:
                    book_obj = book
                    break
            
            if book_obj:
                # Call the return method
                if book_obj.return_book(self.username):
                    success_count += 1
                else:
                    failed_count += 1
            else:
                failed_count += 1
        
        # Clear selections and reload books to update list
        self.selected_books = []
        self.load_borrowed_books(self.username)