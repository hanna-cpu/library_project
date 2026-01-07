import sqlite3
from library_project.backend.backend_common import get_user_id_from_username


class Book:
    """Book model class."""
    # These are Book properties
    id: int
    title: str
    author: str
    availability: str | None = None


    # These are Book methods
    def __init__(self, id: int, title: str, author: str, availability: str = None):
        self.id = id
        self.title = title
        self.author = author
        self.availability = availability
   
    def to_dict(self):
        # Convert book object to dictionary. This is used for showing the list of books in UI in a table format
        result = {
            "id": self.id,
            "title": self.title,
            "author": self.author
        }
        if self.availability is not None:
            result["availability"] = self.availability
        return result
    
    def borrow(self, username: str):
        # this function is used to mark the book as borrowed by a user and insert into borrowed table
        try:
            # Get user id from username using common function
            userid = get_user_id_from_username(username)
            if userid is None:
                return False
            
            conn = sqlite3.connect('librarydb.db')
            cursor = conn.cursor()

            # Insert into borrowed table       
            cursor.execute(
                "INSERT INTO borrowed (book_id, user_id) VALUES (?, ?)",
                (self.id, userid)
            )
            conn.commit()
            conn.close()
            print(f"Book '{self.title}' successfully borrowed by user {username}")
            return True
            
        except Exception as e:
            print(f"Error borrowing book: {e}")
            return False
    
    def return_book(self, username: str):
        # this function is for returning a book by a user and delete from borrowed table
        try:
            # Get user id from username using common function
            userid = get_user_id_from_username(username)
            if userid is None:
                return False
            
            conn = sqlite3.connect('librarydb.db')
            cursor = conn.cursor()

            # Delete from borrowed table (book is returned, so remove from borrowed)
            query = "DELETE FROM borrowed WHERE book_id = ? AND user_id = ?"
            cursor.execute(query, (self.id, userid))
            conn.commit()
            conn.close()

            print(f"Book '{self.title}' successfully returned by user {username}")
            return True
            
        except Exception as e:
            print(f"Error returning book: {e}")
            return False