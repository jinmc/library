class Calendar(object):

    def __init__(self):
        self.date = 0

    def get_date(self):
        return self.date

    def advance(self):
        self.date += 1
        return self.date

time = Calendar()

class Book(object):

    global time

    def __init__(self, id, title, author):
        self.id = str(id)
        self.title = title
        self.author = author
        self.due_date = None

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_due_date(self):
        return self.due_date

    def check_out(self, due_date):
        self.due_date = due_date
    
    def check_in(self):     ##returning to the library
        self.due_date = None

    def __str__(self):
        return str(self.id) + " : " + str(self.title) + " , by " + str(self.author)

class Patron(object):

    global time
    
    def __init__(self, name, library):
        self.name = name
        self.library = library
        self.set_of_books = set([])
        self.set_of_overdue_books = set([])

    def get_name(self):
        return self.name

    def check_out(self, book):      ##checking out from the library
        book.check_out(time.get_date() + 7)
        self.set_of_books.add(book)

    def give_back(self, book):      ##returning to the library
        self.set_of_books.discard(book)
        self.set_of_overdue_books.discard(book)
        book.check_in()

    def get_books(self):
        return self.set_of_books

    def get_overdue_books(self):
        """return the number of overdue books"""
        
#        overdue_booklist = []
        for book in self.set_of_books:
            if book.get_due_date() < time.get_date():
                self.set_of_overdue_books.add(book)
        return self.set_of_overdue_books

class Library(object):

    global time  ## check if it should go inside definition of functions
    
    def __init__(self):

        ## self.books are 
        infile = open('collection.txt','r', encoding = 'utf-8')
        self.books = infile.readlines()
        self.list_of_books = []
        for i in range(len(self.books) - 1):
            self.list_of_books.append(Book(i + 1, self.books[i + 1].rstrip().split('"')[1], self.books[i + 1].rstrip().split('"')[3]))
        infile.close()
        self.cal = time
        self.patrons = {}   # key will be names, and values will be patron objects
        self.is_open = False
        self.current_patron = None
        self.overdue_books = set([])
        
    def open(self):
        if self.is_open:
            raise Exception("The library is already open!")
        self.is_open = True
        self.cal.advance()
        n = self.cal.get_date()
        self.current_patron = None

        if self.patrons != {}:    
            for patron in self.patrons:
                self.patrons[patron].get_overdue_books()
     
        print("Today is day " + str(n) + ".")

    def find_all_overdue_books(self):
        """Go over patrons in the library and use for loop to find the overdue books in each patrons.
        """
        overdue_string = ""
        for patron in self.patrons:
            if len(self.patrons[patron].get_overdue_books()) > 0:
                overdue_string += str(patron) + "\n"
                for x in self.patrons[patron].set_of_overdue_books:
                    overdue_string += str(x) + "\n"
                
        if len(overdue_string) == 0:
            print("No books are overdue.")
            return

        print(overdue_string)

    def issue_card(self, name_of_patron):
        """3 cases. First, if the patron already has a library card. Second, the patron does not have a card.
        third, the library is not open."""
        if self.is_open:
            if name_of_patron in self.patrons:
                print(str(name_of_patron) + " already has a library card.")
            else:
                self.patrons[name_of_patron] = Patron(name_of_patron, self)
                print("Library card issued to " + str(name_of_patron))
        else:
#            return "The library is not open."
            raise Exception("The library is not open.")

    def serve(self, name_of_patron):
        """ Make self.current_patron to the patron object.
            Make sure library is open, and patron has library card       """
        if self.is_open:
            if name_of_patron in self.patrons:
                self.current_patron = self.patrons[name_of_patron]
                print("Now serving " + str(name_of_patron) + ".")
            else:
                raise Exception(str(name_of_patron) + " does not have a library card.")
        else:
            raise Exception("The library is not open.")

    def find_overdue_books(self):
        overdue_string = ""
        if self.is_open:
            if self.current_patron != None:
                for book in self.current_patron.get_overdue_books():
                    overdue_string += book.__str__() +"\n"
            else:
                raise Exception("No patron is currently being served")
        else:
            raise Exception("The library is not open.")
        

    def check_in(self, *book_ids):
        """return the books the patron had"""
        return_book_list = []
        return_book_id_list = []
        flag = 0
        if not self.is_open:                                ## exception
            raise Exception("The library is not open.")

        if self.current_patron == None:                 ## exception
            raise Exception("No patron is currently being served.")

        for bookobject in self.current_patron.get_books():   ## Actual loop
            for book_id in book_ids:
#                print(book_id)
                if bookobject.get_id() == book_id:
#                    flag += 1
#                    return_book_id_list.append(bookobject.get_id())
                    return_book_list.append(bookobject)
                    
##        print(self.current_patron.set_of_books)

##        if flag != len(book_ids):
##            raise Exception("the patron does not have book(s)" + str(book_ids).strip("(),") + ".")
##        for b in self.current_patron.set_of_books:
##            print(b.get_id())
##
##        for book_id in book_ids:
##            for b in self.current_patron.set_of_books:
##                
##        
##        for book_id in book_ids:
##            if book_id not in return_book_id_list:
##                raise Exception("the patron does not have book(s)" + str(book_ids).strip("(),") + ".")
##            
##            for book_id in book_ids:
##                if 
##
##        print(self.current_patron.get_books())
##        print(book_ids)
##        print(return_book_list)
        if len(book_ids) != len(return_book_list):      ## exception
            for x in return_book_list:
                list(book_ids).remove(x)
            raise Exception("The patron does not have book(s) " + str(book_ids).strip("(),") + ".")
            return

        for book in return_book_list:           ## again, it is book library here!
            self.current_patron.give_back(book)
            self.list_of_books.append(book)            
        print(str(self.current_patron.get_name()) + " has returned " + str(len(book_ids)) + " book(s).")

    def search(self, string):
        searchliststring = ""
        searchlist = []
        if len(string) < 4:
            print("Search string must contain at least four characters.")
            return None

        for book in self.list_of_books:
            if (string.lower() in book.get_title().lower()) or (string.lower() in book.get_author().lower()):
                searchlist.append(book)
#                searchliststring += str(book) + "\n"
                
        if len(searchlist) == 0:
            print("No books found.")
            return None
    
        for book in searchlist:           ## to handle same books
            for book2 in searchlist:
                if book != book2 and book.title == book2.title and book.author == book2.author:
                    try:
                        searchlist.remove(book2)
                    except ValueError:
                        pass

        for book in searchlist:
            searchliststring += str(book) + "\n"
        
        print(searchliststring)

    def check_out(self, *book_ids):
        books_in_library = []
        if not self.is_open:
            raise Exception("The library is not open")

        if self.current_patron == None:
            raise Exception("No patron is currently being served.")

        if len(book_ids) + len(self.current_patron.get_books()) > 3:
            raise Exception("Patron cannot have more than three books.")
        
        for bookobject in self.list_of_books: ## THIS IS WHERE THE REAL LOOP IS PERFORMED
            for book_id in book_ids:
                if int(bookobject.get_id()) == int(book_id):    ## ACTUAL CASE
                    books_in_library.append(bookobject)
                    
        if len(books_in_library) != len(book_ids):  ##EXCEPTION THAT EVEN IF ONE BOOK IS NOT IN LIBRARY
            for x in books_in_library:
                list(book_ids).remove(x)
            print("The library does not have book(s) " + str(book_ids).strip("(),") + ".")
            return

        for book in books_in_library:       ## remember the the book here is the book object!!
            self.current_patron.check_out(book)
            self.list_of_books.remove(book)
        print(str(len(books_in_library)) + " book(s) have been checked out to " + str(self.current_patron.get_name()) + ".")
      
    def renew(self, *book_ids):
        renewable_books = []
        if not self.is_open:
            raise Exception("The library is not open.")

        if self.current_patron == None:
            raise Exception("No patron is currently being served.")

        for book_id in book_ids:
            for bookobject in self.current_patron.set_of_books:       ## bookobjects
                if book_id == bookobject.get_id():
                    renewable_books.append(bookobject)
                    
#        if len(renewable_books) != len(book_ids):
#            for x in renewable_books:
#                book_ids.remove(x)
#            raise Exception("The patron does not have book(s) " + str(book_ids).strip("()") + ".")

        for bookobject in renewable_books:              ## bookobjects
            for book in self.current_patron.set_of_books:
                if bookobject == book:
                    book.due_date += 7
                    if bookobject in self.current_patron.set_of_overdue_books:
                        self.current_patron.set_of_overdue_books.discard(book)
        print(str(len(renewable_books)) + " book(s) have been renewed from " + str(self.current_patron.get_name()) + ".")          
        

    def close(self):
        if not self.is_open:
            raise Exception("The library is not open.")
        self.is_open = False
        
        print("The library is not open.")

    def quit(self):
        print("The library is now closed for renovations.")
##-------------------------------------------------------
##helper functions for testing


    
def main():
    lib = Library()
    while True:
        command = input("input open, overdue, card, serve, checkin, checkout, renew, search, close, quit : \n")
        com = command.split()
        try:
            if com[0] == "open":
                lib.open()
            elif com[0] == "overdue":
                lib.find_all_overdue_books()
            elif com[0] == "card":
                names = com[1:]
                name = ' '.join(names)
#                lib.patrons[name] = Patron(str(name), lib)      ##putting inside the dictionary
                lib.issue_card(name.lower())
            elif com[0] == "checkin":
                ids = com[1:]
                lib.check_in(*ids)

            elif com[0] == "serve":
                names = com[1:]
                name = ' '.join(names)
                lib.serve(name.lower())
                if lib.current_patron.set_of_books != set([]):
                    print("The patron has these books(or book) borrowed.")
#                    print(lib.current_patron.set_of_books)
                    for x in lib.current_patron.set_of_books:
                        print(x)
                if lib.current_patron.set_of_overdue_books != set([]):
                    print("The patron has these books(or book) overdued.")
                    for y in lib.current_patron.set_of_overdue_books:
                        print(y)
                

            elif com[0] == "checkout":
                ids = com[1:]
                lib.check_out(*ids)
                
            elif com[0] == "renew":
                names = com[1:]
                name = ' '.join(names)
                lib.renew(name)
                
            elif com[0] == "search":
                words = com[1:]
                word = ''.join(words)
                lib.search(word)

            elif com[0] == "close":
                lib.close()

            elif com[0] == "quit":
                lib.quit()
                break
            else:
                print("invalid input!")
                
        except Exception as msg:
            print(msg)



if __name__ == "__main__":
    main()
