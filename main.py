import sqlite3 
import hashlib

class Bank:
    def __init__(self, db_name = 'Banco.db', table_name = 'users'):
        self.con = sqlite3.connect(db_name)
        self.cursor = self.con.cursor()
        self.table_name = table_name
        self.create_table()
    def create_table(self):
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name}  (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name  TEXT NOT NULL,
        password TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE 
        )
        ''')
        self.con.commit()
        
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
        
    def add_user(self, name, password, cpf):
        password_hashed = self.hash_password(password)
        try:
            self.cursor.execute(f'''INSERT INTO {self.table_name} (name, password, cpf) VALUES (?, ?, ?)
            ''', (name, password_hashed, cpf))
            self.con.commit()
            print(f"User {name} added with success")
        except sqlite3.IntegrityError as e:
            print(f'Error: user  with CPF: {cpf} already exists. {e}')
            
    def show_all(self):
            self.cursor.execute(f"""SELECT * FROM {self.table_name} """)
            all_users = self.cursor.fetchall()
            if not all_users:
                print('[ ! ] No users found')
                
            for users in all_users:
                print(f" ID: {users [ 0 ]} | Nome: {users [ 1 ]} | CPF: {users[ 3 ]}")
                
    def update_user(self, cpf, new_name=None, new_password=None):
         update= False
         
         if new_password:
             hashed = self.hash_password(new_password)
             self.cursor.execute(f'''UPDATE {self.table_name}
         SET password = ? WHERE cpf = ?
           ''', (hashed, cpf))
             print(f"[ - ] Password updated!")
             update = True
         
         if new_name:
             self.cursor.execute(f'''UPDATE {self.table_name}
         SET name = ? WHERE cpf = ?
           ''', (new_name, cpf)
           )
             print('[ - ] Name updated!')
             update = True
             
             if update:
                 self.con.commit()
             else:
                 print(f'[ ! ] No changes provided.')
                 
    def erase_account(self, cpf):
         self.cursor.execute(f"""DELETE FROM  {self.table_name} WHERE  cpf = ? """, (cpf, ))
         self.con.commit()
         
         print(f'User with CPF: {cpf} has had their account deleted')
         
    def close(self):
          self.cursor.close()
          self.con.close()

# Interactive sample menu

def menu():
    bank = Bank()
    try:
        while True:
            print("\n--- User Bank System ---")
            print("1. Add user")
            print("2. Show all users")
            print("3. Update user")
            print("4. Delete user")
            print("5. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                name = input("Name: ")
                password = input("Password: ")
                cpf = input("CPF: ")
                bank.add_user(name, password, cpf)

            elif choice == "2":
                bank.show_all()

            elif choice == "3":
                cpf = input("User CPF to update: ")
                new_name = input("New name (press Enter to keep current): ")
                new_password = input("New password (press Enter to keep current): ")
                bank.update_user(cpf, new_name or None, new_password or None)

            elif choice == "4":
                cpf = input("User CPF to delete: ")
                bank.erase_account(cpf)

            elif choice == "5":
                print("Exiting...")
                break
                
            else:
                print("[!] Invalid option!")

    finally:
        bank.close()


if __name__ == "__main__":
    menu()
