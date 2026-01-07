import reflex as rx
import sqlite3


class NavigationState(rx.State):
    """Base state class with common navigation methods."""
    username: str = "Guest"
    
    def set_username_from_query(self):
        """Set username from URL query parameter."""
        username = self.router.page.params.get("username", "Guest")
        self.username = username
    
    def navigate_to_borrow(self):
        """Navigate to borrow books page."""
        return rx.redirect(f"/borrow?username={self.username}")
    
    def navigate_to_return(self):
        """Navigate to return books page."""
        return rx.redirect(f"/return?username={self.username}")
    
    def navigate_to_homepage(self):
        """Navigate to homepage."""
        return rx.redirect(f"/homepage?username={self.username}")

    def navigate_to_loginpage(self):
        """Navigate to loginpage."""
        return rx.redirect("/")


# This is a common function that can be used across different modules
# to get user id from username , as we also store userid in users and borrowed tables

def get_user_id_from_username(username: str):
    """Get user ID from username."""
    try:
        conn = sqlite3.connect('librarydb.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT users.id FROM users WHERE username = ?",
            (username,)
        )
        rows = cursor.fetchall()
        
        if not rows:
            print(f"Error: User {username} not found")
            conn.close()
            return None
            
        userid = rows[0][0]
        conn.close()
        return userid
        
    except Exception as e:
        print(f"Error getting user id: {e}")
        return None