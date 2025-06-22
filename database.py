import sqlite3
from PyQt5.QtWidgets import QMessageBox

class DatabaseManager:
    def __init__(self, db_name='selection_db.sqlite'):
        self.db_name = db_name
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS candidates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    ipk REAL NOT NULL,
                    jaringan_komputer INTEGER NOT NULL,
                    bahasa_pemrograman INTEGER NOT NULL,
                    komunikasi_tim INTEGER NOT NULL,
                    disiplin_tanggungjawab INTEGER NOT NULL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_id INTEGER NOT NULL,
                    final_score REAL NOT NULL,
                    ranking INTEGER,
                    FOREIGN KEY (candidate_id) REFERENCES candidates (id)
                )
            ''')
            conn.commit()
    
    def add_candidate(self, data):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO candidates 
                    (name, ipk, jaringan_komputer, bahasa_pemrograman, komunikasi_tim, disiplin_tanggungjawab)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', data)
                conn.commit()
            return True
        except Exception as e:
            QMessageBox.critical(None, "Database Error", str(e))
            return False
    
    def delete_candidate(self, name):
        """Delete a candidate by name"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM candidates WHERE name=?", (name,))
                cursor.execute("""
                    DELETE FROM results 
                    WHERE candidate_id IN (
                        SELECT id FROM candidates WHERE name=?
                    )
                """, (name,))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting candidate: {e}")
            QMessageBox.critical(None, "Database Error", f"Gagal menghapus kandidat: {e}")
            return False
    
    def get_all_candidates(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM candidates')
            return cursor.fetchall()
    
    def save_results(self, results):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                cursor.execute('DELETE FROM results')
                
                # Simpan hasil baru
                for result in results:
                    cursor.execute('''
                        INSERT INTO results (candidate_id, final_score, ranking)
                        VALUES (?, ?, ?)
                    ''', (result['id'], result['final_score'], result['ranking']))
                
                conn.commit()
            return True
        except Exception as e:
            QMessageBox.critical(None, "Database Error", str(e))
            return False
    
    def get_results(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.id, c.name, c.ipk, c.jaringan_komputer, c.bahasa_pemrograman, 
                       c.komunikasi_tim, c.disiplin_tanggungjawab, r.final_score, r.ranking
                FROM candidates c
                JOIN results r ON c.id = r.candidate_id
                ORDER BY r.ranking
            ''')
            return cursor.fetchall()