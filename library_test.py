from library import *
import unittest

class CalendarTest(unittest.TestCase):

    def setUp(self):
        global time
        time = Calendar()

    def test_calendar_init(self):
        self.assertEqual(time.date, 0)

    def test_calendar_advance(self):        
        time.advance()
        time.advance()
        self.assertEqual(time.date, 2)

class BookTest(unittest.TestCase):

    def setUp(self):
        global time
        global a
        time = Calendar()
        a = Book('3', "Harry Potter", "J.K rowling")
    
    def test_book_init(self):
        self.assertEqual(a.id, '3')
        self.assertEqual(a.author, "J.K rowling")
        self.assertEqual(a.title, "Harry Potter")

    def test_check_out(self):
        self.assertEqual(a.due_date, None)
        a.check_out(8)
        self.assertEqual(a.due_date, 8)

    def test_check_in(self):
        a.check_in()
        self.assertEqual(a.due_date, None)

    def test_str_(self):
        self.assertEqual(str(a), "3 : Harry Potter , by J.K rowling")

class PatronTest(unittest.TestCase):

    def setUp(self):
        global time
        global pat
        global lib
        global a
        global b
        time = Calendar()
        lib = Library()
        pat = Patron('jim', 'lib')
        a = Book(5, 'A Bend in the River', 'V. S. Naipaul')
        b = Book(11, 'A Dark-Adapted Eye','Barbara Vine')

    def test_patron_init(self):
        self.assertEqual(pat.library, 'lib')
        self.assertEqual(pat.name, 'jim')

    def test_check_out(self):
        pat.check_out(a)
        self.assertEqual(pat.set_of_books, {a})
        pat.check_out(b)
        self.assertEqual(pat.set_of_books, {a, b})

    def test_give_back(self):
        pat.check_out(a)
        pat.give_back(a)
        self.assertEqual(pat.set_of_books, set([]))
        pat.check_out(b)
        pat.check_out(a)
        pat.give_back(b)
        self.assertEqual(pat.set_of_books, set([a]))

class LibraryTest(unittest.TestCase):

    def setUp(self):
        global time
        global pat
        global lib
        global a
        global b
        time = Calendar()
        lib = Library()
        pat = Patron('jim', 'lib')
        a = Book(5, 'A Bend in the River', 'V. S. Naipaul')
        b = Book(11, 'A Dark-Adapted Eye','Barbara Vine')
        lib.open()

    
    def test_init_(self):
        lib.close()
        self.assertTrue(not lib.is_open)

    def test_open(self):
        self.assertTrue(lib.is_open)

    def test_find_all_overdue_books(self):
        lib.find_all_overdue_books()
        self.assertEqual(lib.find_all_overdue_books(), None)

    def test_issue_card(self):
        self.assertEqual(lib.issue_card('jim'), None)               
    
    def test_serve(self):
        lib.issue_card('jim')
        lib.serve('jim')
        self.assertEqual(lib.serve('jim'), None)

    def test_find_overdue_books(self):
        lib.issue_card('jim')
        lib.serve('jim')
        lib.find_overdue_books()
        self.assertEqual(lib.find_overdue_books(), None)
        
    def test_check_in(self):
        lib.issue_card('jim')
        lib.serve('jim')
        lib.check_out('5')
        self.assertEqual(lib.check_in('5'), None)

    def test_search(self):
        self.assertEqual(lib.search('make'), None)

    def test_check_out(self):
        lib.issue_card('jim')
        lib.serve('jim')
        self.assertEqual(lib.check_out('5'), None)
         
    def test_renew(self):
        lib.issue_card('jim')
        lib.serve('jim')
        lib.check_out('5')
        lib.close()
        lib.open()
        lib.close()
        lib.open()
        lib.close()
        lib.open()
        lib.close()
        lib.open()
        lib.close()
        lib.open()
        lib.close()
        lib.open()
        lib.close()
        lib.open()
        lib.close()
        lib.open()
        lib.close()
        lib.open()
        lib.serve('jim')
        self.assertEqual(lib.renew('5'), None)

    def test_close(self):
        lib.close()
        self.assertFalse(lib.is_open)

    def test_quit(self):
        self.assertEqual(lib.quit(), None)




        
unittest.main()
