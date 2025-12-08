import sqlite3
import logging
from config import Config

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path=Config.DB_PATH):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_tables()
    
    def init_tables(self):
        """Initialize database tables"""
        # Groups table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id TEXT UNIQUE,
                group_name TEXT,
                welcome_msg TEXT DEFAULT '👋 Welcome {user} to {group}!',
                rules_msg TEXT DEFAULT 'Be respectful!',
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Promotions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS promotions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message TEXT,
                photo_id TEXT,
                status TEXT DEFAULT 'pending',
                sent_to INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        logger.info("Database initialized")
    
    def add_group(self, group_id, group_name):
        """Add a new group to database"""
        try:
            self.cursor.execute('''
                INSERT OR IGNORE INTO groups (group_id, group_name)
                VALUES (?, ?)
            ''', (str(group_id), group_name))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error adding group: {e}")
            return False
    
    def get_all_groups(self):
        """Get all active groups"""
        self.cursor.execute('SELECT group_id, group_name FROM groups WHERE is_active = 1')
        return self.cursor.fetchall()
    
    def update_welcome(self, group_id, welcome_msg):
        """Update welcome message for group"""
        self.cursor.execute('''
            UPDATE groups SET welcome_msg = ? WHERE group_id = ?
        ''', (welcome_msg, str(group_id)))
        self.conn.commit()
    
    def update_rules(self, group_id, rules_msg):
        """Update rules for group"""
        self.cursor.execute('''
            UPDATE groups SET rules_msg = ? WHERE group_id = ?
        ''', (rules_msg, str(group_id)))
        self.conn.commit()
    
    def add_promotion(self, user_id, message, photo_id=None):
        """Add new promotion"""
        self.cursor.execute('''
            INSERT INTO promotions (user_id, message, photo_id)
            VALUES (?, ?, ?)
        ''', (user_id, message, photo_id))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def close(self):
        """Close database connection"""
        self.conn.close()

# Create global instance
db = Database()