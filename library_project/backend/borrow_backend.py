import sqlite3
from typing import List
from library_project.backend.backend_common import NavigationState
from library_project.backend.library_classes import Book


class borrowState(NavigationState):
    """State management for the borrow page."""
    books_data: List[dict] = []  # list of all books data , used for UI to display
    books_objects: List[Book] = [] # list of Book objects corresponding to all books as book objects ready for borrow operation
    selected_books: List[int] = [] # list of selected book ids for borrowing , from UI checkbox selection
    
    
    def set_username_from_query(self):
        """Set username from URL query parameter and load books."""
        super().set_username_from_query()
        self.load_books()
    
    def load_books(self):
        """Load books from database with availability status."""
        try:
            conn = sqlite3.connect('librarydb.db')
            cursor = conn.cursor()
            
            # Get all books with their availability status
            query = """
            SELECT books.id, books.title, books.author,
                CASE 
                    WHEN borrowed.book_id IS NULL THEN 'Available'
                    ELSE 'Unavailable'
                END as availability
            FROM books 
            LEFT JOIN borrowed ON books.id = borrowed.book_id
            ORDER BY books.title
            """
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # Clear existing data
            self.books_data = []
            self.books_objects = []
            
            # Create Book objects and convert to dictionaries
            for row in rows:
                book = Book(
                    id=row[0],
                    title=row[1],
                    author=row[2],
                    availability=row[3]
                )
                self.books_objects.append(book)
                self.books_data.append(book.to_dict())
            
            conn.close()
        except Exception as e:
            print(f"Error loading books: {e}")
            self.books_data = []
            self.books_objects = []
    
    def toggle_book_selection(self, book_id: int):
        """Toggle book selection for borrowing."""
        if book_id in self.selected_books:
            self.selected_books.remove(book_id)
        else:
            self.selected_books.append(book_id)
    
    def confirm_borrows(self):
        """Handle confirm borrows button click."""
        if not self.selected_books:
            print("No books selected to borrow")
            return
        
        print(f"User {self.username} confirming borrows for {len(self.selected_books)} book(s)")
        
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
                # Call the borrow method
                if book_obj.borrow(self.username):
                    success_count += 1
                else:
                    failed_count += 1
            else:
                print(f"Error: Book with id {book_id} not found")
                failed_count += 1
        
        print(f"Borrow complete: {success_count} successful, {failed_count} failed")
        
        # Clear selections and reload books to update availability
        self.selected_books = []
        self.load_books()