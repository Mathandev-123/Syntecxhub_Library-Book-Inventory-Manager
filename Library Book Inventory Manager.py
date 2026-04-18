import json
import os

class Book:
    def __init__(self, title, author, is_issued=False):
        self.title = title
        self.author = author
        self.is_issued = is_issued

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "is_issued": self.is_issued
        }

class Library:
    def __init__(self, storage_file="library_data.json"):
        self.storage_file = storage_file
        # Dict acts as a HashMap (Key: Title, Value: Book Object)
        self.books = {}
        self.load_data()

    def add_book(self, title, author):
        if title.lower() in self.books:
            print(f"Error: '{title}' already exists.")
            return
        new_book = Book(title, author)
        self.books[title.lower()] = new_book
        self.save_data()
        print(f"Book '{title}' added successfully!")

    def issue_book(self, title):
        book = self.books.get(title.lower())
        if book:
            if not book.is_issued:
                book.is_issued = True
                self.save_data()
                print(f"You have issued '{book.title}'.")
            else:
                print("Book is already issued.")
        else:
            print("Book not found.")

    def return_book(self, title):
        book = self.books.get(title.lower())
        if book:
            if book.is_issued:
                book.is_issued = False
                self.save_data()
                print(f"Returned '{book.title}' successfully.")
            else:
                print("This book was not issued.")
        else:
            print("Book not found.")

    def search(self, query):
        print(f"\n--- Search Results for '{query}' ---")
        found = False
        for book in self.books.values():
            if query.lower() in book.title.lower() or query.lower() in book.author.lower():
                status = "Issued" if book.is_issued else "Available"
                print(f"Title: {book.title} | Author: {book.author} | Status: {status}")
                found = True
        if not found:
            print("No books matches your search.")

    def show_report(self):
        total = len(self.books)
        issued = sum(1 for b in self.books.values() if b.is_issued)
        print("\n--- Library Report ---")
        print(f"Total Books: {total}")
        print(f"Books Issued: {issued}")
        print(f"Books Available: {total - issued}")

    def save_data(self):
        with open(self.storage_file, 'w') as f:
            data = {title: b.to_dict() for title, b in self.books.items()}
            json.dump(data, f)

    def load_data(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                try:
                    data = json.load(f)
                    for title, info in data.items():
                        self.books[title] = Book(info['title'], info['author'], info['is_issued'])
                except json.JSONDecodeError:
                    self.books = {}

def main():
    lib = Library()
    
    while True:
        print("\n=== Library Manager ===")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. View Report")
        print("6. Exit")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            t = input("Enter Title: ")
            a = input("Enter Author: ")
            lib.add_book(t, a)
        elif choice == '2':
            q = input("Enter Title or Author to search: ")
            lib.search(q)
        elif choice == '3':
            t = input("Enter Title to issue: ")
            lib.issue_book(t)
        elif choice == '4':
            t = input("Enter Title to return: ")
            lib.return_book(t)
        elif choice == '5':
            lib.show_report()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()