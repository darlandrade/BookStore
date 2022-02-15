from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Style
from generalsettings import label, entry, button, frame, labelframe, label_livros, label_livros_info, text, checkbox
from PIL import ImageTk, Image
from connection_postgre import get_connection
from register_book import RegisterBook
from new_client import NewCLient


class Book_Store(Tk):
    def __init__(self):
        Tk.__init__(self)
        # Layout settings
        x = 1600
        y = 720
        self.config(**frame())  # Setting background
        self.geometry(f"{x}x{y}+"
                      f"{int(self.winfo_screenwidth() / 2 - x / 2) + 2000}+"
                      f"{int(self.winfo_screenheight() / 2 - y / 2)}")  # Window size
        self.title("Darlan's Book Store")  # Title

        # ################################################################################################ #
        f_logo_botoes = Frame(self, **frame(), )  # Frame to support button widgets
        f_logo_botoes.pack(side=LEFT, anchor=N, )
        # ################################################################################################ #
        self.img_logo = ImageTk.PhotoImage(Image.open("./images/book_store.png").resize((150, 200)))  # Book image
        l_img_logo = Label(f_logo_botoes, image=self.img_logo, **label())  # Setting image
        l_img_logo.pack(padx=(20, 20), pady=(20, 0))

        # Register Buttons Add/Delete (books, new customer, etc)
        f_g_buttons = Frame(f_logo_botoes, **frame())  # Frame to position buttons
        f_g_buttons.pack(pady=(10, 5))

        l_info_register = Label(f_g_buttons, text="Register", **label())  # Text 'register'
        l_info_register.config(font="Helvetica 18 bold")  # Set font size and 'bold' style
        l_info_register.pack()

        # Buttons Register
        b_register_client = Button(f_g_buttons, text="Client", **button(), command=NewCLient)  # New Client
        b_register_client.pack(pady=(5, 0))
        b_register_client = Button(f_g_buttons, text="Book", **button(), command=RegisterBook)  # New Book
        b_register_client.pack(pady=10)

        # Buttons Rent
        l_info_register = Label(f_g_buttons, text="Books", **label())  # Text for books
        l_info_register.config(font="Helvetica 18 bold")  # Set font size and 'bold' style
        l_info_register.pack()

        b_register_client = Button(f_g_buttons, text="Rent", **button(), command=self.rent_book)  # Rent a book
        b_register_client.pack(pady=(5, 0))
        b_register_client = Button(f_g_buttons, text="Return book", **button(), command=self.return_book)  # Return book
        b_register_client.pack(pady=10)

        # Client info
        l_info_register = Label(f_g_buttons, text="Search client", **label())  # Seach for a client
        l_info_register.config(font="Helvetica 18 bold")  # Set font size and 'bold' style
        l_info_register.pack()

        # Entry to search for a client
        self.e_client_number = Entry(f_g_buttons, **entry())  # Entry point to specify client number
        self.e_client_number.config(justify=CENTER)  # Justify the text to be centered
        self.e_client_number.pack()

        b_loadclient = Button(f_g_buttons, text="Load", **button(),  # Load info about the client
                              command=lambda: self.load_cliente_info())
        b_loadclient.pack(pady=10)

        self.l_nome_cliente = Label(f_g_buttons, **label())  # Client name appears when client number is searched
        self.l_nome_cliente.pack()

        self.l_idade = Label(f_g_buttons, **label())  # Client age appears when client number is searched
        self.l_idade.pack()
        # ################################################################################################ #
        # Split layout
        f_split_logo_title = LabelFrame(self, **labelframe(), width=2, height=y)  # Simple line to split content
        f_split_logo_title.pack(side=LEFT, anchor=N, padx=(0, 10))

        # ################################################################################################ #
        f_books_holder = Frame(self, **frame())  # Frame to hold book tree with a sample of 50 books from our database
        f_books_holder.pack(side=LEFT, anchor=N)  # and also the books our client has or not in its possetion

        f_books = Frame(f_books_holder, **frame())  # To hold books info
        f_books.pack()

        l_book_1_info = Label(f_books, text="Books rented", **label())  # Text books rented
        l_book_1_info.grid(row=0, column=0, columnspan=2, pady=(40, 0), )

        self.l_book_not_rented = Label(f_books, text="", **label_livros())  # If there's no books with the client
        self.l_book_not_rented.grid(row=1, column=0, columnspan=2, )  # this'll show a message

        book_title_width_field = 55  # Set field size for the book titles

        # Here is where books rented are going to appear, with the books there's also a checkbutton
        # This checkbutton is used to return the book
        self.l_book_1_info = Label(f_books, text="", width=book_title_width_field, **label_livros())
        self.l_book_1_info.grid(row=2, column=1, pady=(10, 0))

        self.livro1_checked = IntVar()
        self.check_livro_1 = Checkbutton(f_books, variable=self.livro1_checked, **checkbox(), )

        self.l_book_2_info = Label(f_books, text="", width=book_title_width_field, **label_livros())
        self.l_book_2_info.grid(row=3, column=1, pady=(5, 0))
        self.livro2_checked = IntVar()
        self.check_livro_2 = Checkbutton(f_books, variable=self.livro2_checked, **checkbox())

        self.l_book_3_info = Label(f_books, text="", width=book_title_width_field, **label_livros())
        self.l_book_3_info.grid(row=4, column=1, pady=(5, 0))
        self.livro3_checked = IntVar()
        self.check_livro_3 = Checkbutton(f_books, variable=self.livro3_checked, **checkbox())

        self.check_livro_1.grid(row=2, column=0)
        self.check_livro_2.grid(row=3, column=0)
        self.check_livro_3.grid(row=4, column=0)

        # Start the system with all checkbuttons disabled since there's no client loaded yet.
        self.check_livro_1['state'] = DISABLED
        self.check_livro_2['state'] = DISABLED
        self.check_livro_3['state'] = DISABLED

        # ################################################################################################ #
        f_books_search = Frame(f_books_holder, **frame())  # Hold the tree with book samples
        f_books_search.pack()

        # Info about what each textfield does
        l_search_book = Label(f_books_search, text="Book title ", **label())
        l_search_author = Label(f_books_search, text="Author ", **label())
        l_search_publisher = Label(f_books_search, text="Publisher ", **label())

        l_search_book.grid(row=0, column=0, pady=(5, 0))
        l_search_author.grid(row=0, column=1, pady=(5, 0))
        l_search_publisher.grid(row=0, column=2, pady=(5, 0))

        # Entries to search for a specific book
        self.e_search_book = Entry(f_books_search, **entry())
        self.e_search_author = Entry(f_books_search, **entry())
        self.e_search_publisher = Entry(f_books_search, **entry())

        self.e_search_book.grid(row=1, column=0, pady=(5, 0), padx=5)
        self.e_search_author.grid(row=1, column=1, pady=(5, 0))
        self.e_search_publisher.grid(row=1, column=2, pady=(5, 0), padx=(0, 5))

        # Binds each entry to a function. This function will search for the book and show it on the tree
        self.e_search_author.bind("<KeyRelease>", self.search_book)
        self.e_search_book.bind("<KeyRelease>", self.search_book)
        self.e_search_publisher.bind("<KeyRelease>", self.search_book)
        # ################################################################################################ #
        # Tree showing search result
        self.tree = Treeview(f_books_search, columns=("c1", "c2", "c3"), show="headings", height=20, )
        # Specify column position text position and headings title
        self.tree.column("#1", anchor=CENTER)
        self.tree.heading("#1", text="Title")
        self.tree.column("#2", anchor=CENTER)
        self.tree.heading("#2", text="Author")
        self.tree.column("#3", anchor=CENTER)
        self.tree.heading("#3", text="Publisher")
        self.tree.grid(row=2, column=0, columnspan=3, pady=10)

        # Bind a function to show the book info on their designated fields
        self.tree.bind("<ButtonRelease-1>", self.load_book_info)

        # Using style to change the tree colors, such as background, foreground and background when an item is selected
        style = Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#424D42",
                        foreground="#FFFFFF",
                        fieldbackground="#051C03",
                        font="Helvetica 12")

        # Using style to change headings font size
        style.configure("Treeview.Heading",
                        font="Helvetica 12")
        style.map("Treeview", background=[("selected", "#202D20")], )

        # Load books on the tree
        self.loadbooks()
        self.tree.selection_set("I001")  # Initiate the tree with the first item selected
        # ################################################################################################ #
        f_books_info = Frame(self, **frame())  # Hold widgets for book info
        f_books_info.pack(side=LEFT, anchor=N)

        # Hold all fields to show information about the book selected
        f_books_info2 = Frame(f_books_info, **frame())
        f_books_info2.pack(fill=X)
        l_books_info = Label(f_books_info2, text="Books info", **label())
        l_books_info.grid(row=0, columnspan=4, pady=20)

        l_title = Label(f_books_info2, text="Title: ", **label())
        l_title.grid(row=1, column=0, )
        LARGURA_CAMPO_INFORMACAO = 50
        self.l_title = Label(f_books_info2, text=" ", anchor=W, width=80, **label_livros_info())
        self.l_title.grid(row=1, column=1, columnspan=4)

        l_author = Label(f_books_info2, text="Author: ", **label())
        l_author.grid(row=2, column=0)
        self.l_author = Label(f_books_info2, text=" ", anchor=W, width=LARGURA_CAMPO_INFORMACAO, **label_livros_info())
        self.l_author.grid(row=2, column=1, )

        l_publihser = Label(f_books_info2, text="Publisher: ", **label())
        l_publihser.grid(row=2, column=2, padx=10)
        self.l_publihser = Label(f_books_info2, text="", width=17, anchor=W, **label_livros_info())
        self.l_publihser.grid(row=2, column=3)

        l_year = Label(f_books_info2, text="Year: ", **label(), )
        l_year.grid(row=3, column=0)
        self.l_year = Label(f_books_info2, text=" ", anchor=W, **label_livros_info(), width=LARGURA_CAMPO_INFORMACAO)
        self.l_year.grid(row=3, column=1)

        l_pages = Label(f_books_info2, text="Pages: ", **label())
        l_pages.grid(row=3, column=2)
        self.l_pages = Label(f_books_info2, text=" ", anchor=W, **label_livros_info(), width=17)
        self.l_pages.grid(row=3, column=3)

        l_genre = Label(f_books_info2, text="Genre: ", **label())
        l_genre.grid(row=4, column=0)
        self.l_genre = Label(f_books_info2, text=" ", anchor=W, **label_livros_info(), width=LARGURA_CAMPO_INFORMACAO)
        self.l_genre.grid(row=4, column=1)

        l_language = Label(f_books_info2, text="Language: ", **label())
        l_language.grid(row=4, column=2)
        self.l_language = Label(f_books_info2, text="", width=17, anchor=W, **label_livros_info())
        self.l_language.grid(row=4, column=3)

        # Description
        f_books_info3 = Frame(f_books_info, **frame())  # Hold description
        f_books_info3.pack()
        l_description = Label(f_books_info3, text="Description", **label())
        l_description.pack()
        # Description text field
        self.t_description_text = Text(f_books_info3, text(), wrap=WORD, height=28)
        self.t_description_text.pack(fill=X)
        self.t_description_text['state'] = DISABLED

        # ################################################################################################ #

    # Function used to rent books
    def rent_book(self, con=get_connection()):
        selection = self.tree.selection()  # Get tree selected item
        items = self.tree.item(selection[0]).get('values')  # Get the items from selection

        cursor = con.cursor()
        # Count how many books the client already has and...
        cursor.execute(f"SELECT count(isbn) FROM livros_alugados "
                       f"WHERE alugado_id_cliente = {int(self.e_client_number.get())}")
        quantidae_livros_alugado = cursor.fetchone()[0]
        # if there are 3 books, can't rent
        if quantidae_livros_alugado == 3:
            messagebox.showinfo("Limit reached", "Max number of books per customer reached, "
                                                 "return a book to rent a new one")
        else:  # Otherwise... Add to the database
            cursor.execute(f"SELECT id FROM livros "
                           f"WHERE titulo = '{items[0]}' AND autor = '{items[1]}' AND editora = '{items[2]}'")
            cursor.execute(f"INSERT INTO livros_alugados "
                           f"VALUES ({self.e_client_number.get()}, NOW(), '{cursor.fetchone()[0]}')")
        con.commit()
        self.load_cliente_info()

    # This function returns books
    def return_book(self, con=get_connection()):
        cursor = con.cursor()
        client_id = self.e_client_number.get()  # Get client ID
        # Select ISBNs to remove from the client log
        cursor.execute(f"SELECT isbn FROM livros_alugados WHERE alugado_id_cliente = {client_id}")
        dados_livros = cursor.fetchall()
        # Store books if there is any...
        livros = []
        for livro in dados_livros:
            livros.append(livro)

        # Get wich checkbutton is active...
        s1 = self.livro1_checked.get()
        s2 = self.livro2_checked.get()
        s3 = self.livro3_checked.get()

        # And goes through every situation to remove it
        if livros:
            if s1 and s2 and s3:
                cursor.execute(f"DELETE FROM livros_alugados WHERE alugado_id_cliente = {client_id}")
            elif s1 and s2:
                cursor.execute(f"SELECT id FROM livros "
                               f"WHERE titulo IN ('{self.l_book_1_info['text']}', '{self.l_book_2_info['text']}')")
                isbns = cursor.fetchall()
                cursor.execute(f"DELETE FROM livros_alugados WHERE alugado_id_cliente = {client_id}"
                               f"AND isbn IN ('{isbns[0][0]}', '{isbns[1][0]}')")
            elif s1 and s3:
                cursor.execute(f"SELECT id FROM livros "
                               f"WHERE titulo IN ('{self.l_book_1_info['text']}', '{self.l_book_3_info['text']}')")
                isbns = cursor.fetchall()
                cursor.execute(f"DELETE FROM livros_alugados WHERE alugado_id_cliente = {client_id}"
                               f"AND isbn IN ('{isbns[0][0]}', '{isbns[1][0]}')")
            elif s2 and s3:
                cursor.execute(f"SELECT id FROM livros "
                               f"WHERE titulo IN ('{self.l_book_2_info['text']}', '{self.l_book_3_info['text']}')")
                isbns = cursor.fetchall()
                cursor.execute(f"DELETE FROM livros_alugados WHERE alugado_id_cliente = {client_id}"
                               f"AND isbn IN ('{isbns[0][0]}', '{isbns[1][0]}')")
            elif s1:
                cursor.execute(f"SELECT id FROM livros "
                               f"WHERE titulo IN ('{self.l_book_1_info['text']}')")
                isbns = cursor.fetchone()[0]
                cursor.execute(f"DELETE FROM livros_alugados "
                               f"WHERE alugado_id_cliente = {client_id} AND isbn = '{isbns}'")
            elif s2:
                cursor.execute(f"SELECT id FROM livros "
                               f"WHERE titulo IN ('{self.l_book_2_info['text']}')")
                isbns = cursor.fetchone()[0]
                cursor.execute(f"DELETE FROM livros_alugados "
                               f"WHERE alugado_id_cliente = {client_id} AND isbn = '{isbns}'")
            elif s3:
                cursor.execute(f"SELECT id FROM livros "
                               f"WHERE titulo IN ('{self.l_book_3_info['text']}')")
                isbns = cursor.fetchone()[0]
                cursor.execute(f"DELETE FROM livros_alugados "
                               f"WHERE alugado_id_cliente = {client_id} AND isbn = '{isbns}'")
            else:
                messagebox.showinfo("Nothing selected", "At least one book must be selected")

        con.commit()
        self.livro1_checked.set(0)
        self.livro2_checked.set(0)
        self.livro3_checked.set(0)

        self.load_cliente_info()

    # Search through the databse and load them
    def search_book(self, e, con=get_connection()):
        self.tree.delete(*self.tree.get_children())
        cursor = con.cursor()
        cursor.execute(f"SELECT titulo, autor, editora "
                       f"FROM livros "
                       f"WHERE editora ILIKE '%{self.e_search_publisher.get()}%' "
                       f"AND autor ILIKE '%{self.e_search_author.get()}%' "
                       f"AND titulo ILIKE '%{self.e_search_book.get()}%'")
        print(self.e_search_publisher.get())
        livros = cursor.fetchall()
        for livro in livros:
            self.tree.insert("", END, values=livro)

    # Randomly chooses 30 books to show when system initiate
    def loadbooks(self, con=get_connection()):
        self.tree.delete(*self.tree.get_children())
        cursor = con.cursor()
        cursor.execute("SELECT titulo, autor, editora FROM livros ORDER BY random() limit 30")
        livros = cursor.fetchall()
        for livro in livros:
            self.tree.insert("", END, values=livro)

    # Clear old info
    def clear_last_cliente_info(self):
        self.l_nome_cliente['text'] = ''
        self.l_book_not_rented['text'] = ''
        self.l_book_1_info['text'] = ''
        self.l_book_2_info['text'] = ''
        self.l_book_3_info['text'] = ''

    # Load client info
    def load_cliente_info(self, con=get_connection()):
        self.clear_last_cliente_info()

        cursor = con.cursor()
        cursor.execute(f"SELECT isbn "
                       f"FROM livros_alugados "
                       f"WHERE alugado_id_cliente = {int(self.e_client_number.get())}")
        dados_livros = cursor.fetchall()

        cursor.execute(f"SELECT nome, idade, sexo "
                       f"FROM cliente "
                       f"WHERE id_cliente = {int(self.e_client_number.get())}")
        dados_cliente = cursor.fetchone()

        if dados_cliente:  # If client is found
            nome, idade, sexo = dados_cliente
            self.l_nome_cliente["text"] = nome  # Shows its name
            self.l_idade['text'] = idade + ' anos'  # And age

            if dados_livros:  # And if there is any book...
                quantidade_livros = len(dados_livros)
                livro1, livro2, livro3 = '', '', ''

                # Check its quantity and assign them to their variables
                if quantidade_livros == 3:
                    livro1, livro2, livro3 = dados_livros
                elif quantidade_livros == 2:
                    livro1, livro2 = dados_livros
                elif quantidade_livros == 1:
                    livro1 = dados_livros

                # Accord to the amout of books, perform different task
                if quantidade_livros == 3:
                    cursor.execute(f"SELECT titulo FROM livros "
                                   "WHERE id = ANY('{%s, %s, %s}')"
                                   % (livro1[0], livro2[0], livro3[0]))
                    self.l_book_1_info["text"] = cursor.fetchone()[0]
                    self.l_book_2_info["text"] = cursor.fetchone()[0]
                    self.l_book_3_info["text"] = cursor.fetchone()[0]

                    self.check_livro_1['state'] = NORMAL
                    self.check_livro_2['state'] = NORMAL
                    self.check_livro_3['state'] = NORMAL

                if quantidade_livros == 2:
                    cursor.execute(f"SELECT titulo FROM livros "
                                   "WHERE id = ANY('{%s, %s}')" % (livro1[0], livro2[0]))
                    self.l_book_1_info["text"] = cursor.fetchone()[0]
                    self.l_book_2_info["text"] = cursor.fetchone()[0]

                    self.check_livro_1['state'] = NORMAL
                    self.check_livro_2['state'] = NORMAL
                    self.check_livro_3['state'] = DISABLED

                if quantidade_livros == 1:
                    cursor.execute(f"SELECT titulo FROM livros "
                                   "WHERE id = ANY('{%s}')" % livro1[0])
                    self.l_book_1_info["text"] = cursor.fetchone()[0]
                    self.check_livro_1['state'] = NORMAL
                    self.check_livro_2['state'] = DISABLED
                    self.check_livro_3['state'] = DISABLED

            else:
                self.l_book_not_rented["text"] = "Nenhum livro alugado"
                self.check_livro_1['state'] = DISABLED
                self.check_livro_2['state'] = DISABLED
                self.check_livro_3['state'] = DISABLED
        else:
            if messagebox.askyesno("Not registered",
                                   "Client doesn't exist. Would like to register a new one?") == "yes":
                pass
            else:
                self.e_client_number.delete(0, END)

    # Load every information the book has
    def load_book_info(self, e, con=get_connection()):
        selection = self.tree.focus()
        titulo, autor, editora = self.tree.item(selection).get("values")
        cursor = con.cursor()
        cursor.execute(f"SELECT ano, paginas, idioma, genero, descricao "
                       f"FROM livros "
                       f"WHERE titulo = '{titulo}' AND autor = '{autor}' AND editora = '{editora}'")
        ano, paginas, idioma, genero, descricao = cursor.fetchone()
        largura_genero = len(genero)
        self.l_title['text'] = titulo
        self.l_author['text'] = autor
        self.l_publihser['text'] = editora
        self.l_year['text'] = ano
        self.l_pages['text'] = paginas
        if largura_genero > 50:
            self.l_genre['text'] = genero[:47] + '...'
        else:
            if largura_genero:
                self.l_genre['text'] = genero
            else:
                self.l_genre['text'] = 'Desconhecido'
        self.l_language['text'] = idioma

        cursor.execute("SELECT descricao "
                       "FROM livros "
                       f"WHERE titulo = '{titulo}' AND autor = '{autor}' AND editora = '{editora}'")
        self.t_description_text['state'] = NORMAL
        self.t_description_text.delete('1.0', END)
        self.t_description_text.insert('1.0', cursor.fetchone()[0])
        self.t_description_text['state'] = DISABLED


if __name__ == '__main__':
    book_store = Book_Store()
    book_store.mainloop()
