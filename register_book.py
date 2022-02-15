from tkinter import messagebox

from connection_postgre import get_connection
from tkinter import *
from generalsettings import label, entry, button, frame, text


class RegisterBook(Tk):
    def __init__(self):
        Tk.__init__(self)
        x = 800
        y = 600
        self.title("Register book")
        self.geometry(f"{x}x{y}")
        self.config(**frame())

        f_info = Frame(self, **frame())
        f_info.pack(pady=20)

        l_info = Label(f_info, text="Please, fill out all fields.", **label())
        l_info.pack()

        f_fields = Frame(self, **frame())
        f_fields.pack()

        l_title = Label(f_fields, text="Title: ", **label())
        l_title.grid(row=0, column=0, )

        self.e_title = Entry(f_fields, **entry(), )
        self.e_title.grid(row=0, column=1, columnspan=4, sticky=EW, padx=10)

        l_author = Label(f_fields, text="Author: ", **label())
        l_author.grid(row=1, column=0)
        self.e_author = Entry(f_fields, **entry())
        self.e_author.grid(row=1, column=1, sticky=EW, padx=10)

        l_publihser = Label(f_fields, text="Publisher: ", **label())
        l_publihser.grid(row=1, column=2, padx=10)
        self.e_publihser = Entry(f_fields, **entry())
        self.e_publihser.grid(row=1, column=3, sticky=EW, padx=10)

        l_genre = Label(f_fields, text="Genre: ", **label())
        l_genre.grid(row=2, column=0)
        self.e_genre = Entry(f_fields, **entry(), )
        self.e_genre.grid(row=2, column=1, columnspan=4, sticky=EW, padx=10)

        f_y_g = Frame(f_fields, **frame())
        f_y_g.grid(row=3, column=0, columnspan=4)

        l_year = Label(f_y_g, text="Year: ", **label(), )
        l_year.grid(row=0, column=0, padx=20)
        self.e_year = Entry(f_y_g, **entry(), width=5)
        self.e_year.grid(row=0, column=1, padx=(14, 0), sticky=W)

        l_pages = Label(f_y_g, text="Pages: ", **label())
        l_pages.grid(row=0, column=2)
        self.e_pages = Entry(f_y_g, **entry(), )
        self.e_pages.grid(row=0, column=3, sticky=EW, padx=10)

        l_language = Label(f_y_g, text="Language: ", **label())
        l_language.grid(row=0, column=4)
        self.e_language = Entry(f_y_g, **entry())
        self.e_language.grid(row=0, column=5, padx=(0, 10))

        l_isbn_10 = Label(f_y_g, text="ISBN: ", **label())
        l_isbn_10.grid(row=1, column=0, )
        self.e_isbn = Entry(f_y_g, **entry())
        self.e_isbn.grid(row=1, column=1, columnspan=3, sticky=W, padx=(14, 0))

        # Description
        f_books_info3 = Frame(self, **frame())
        f_books_info3.pack()
        l_description = Label(f_books_info3, text="Description", **label())
        l_description.pack(pady=20)

        self.t_description_text = Text(f_books_info3, text(), wrap=WORD, height=15)
        self.t_description_text.pack(fill=X, pady=(0, 20))
        # Buttons

        f_buttons = Frame(self, frame())
        f_buttons.pack()
        b_save = Button(f_buttons, text="Save", command=self.save, **button())
        b_save.pack(side=LEFT, padx=(0, 30))

        b_quit = Button(f_buttons, text='Close', command=self.destroy, **button())
        b_quit.pack(side=LEFT)

    def save(self, con=get_connection()):
        cursor = con.cursor()

        titulo = self.e_title.get().capitalize()
        autor = self.e_author.get().title()
        isbn = self.e_isbn.get().upper()
        ano = self.e_year.get()
        paginas = self.e_pages.get()
        idioma = self.e_language.get().capitalize()
        editora = self.e_publihser.get().capitalize()
        descricao = self.t_description_text.get('1.0', END).capitalize()
        genero = self.e_genre.get().capitalize()

        if titulo and autor and isbn and ano and paginas and idioma and editora and descricao and genero:
            if ano.isnumeric() and paginas.isnumeric() and len(isbn) == 10:
                cursor.execute("INSERT INTO livros "
                               "(titulo, autor, id, ano, paginas, idioma, editora, descricao, genero) "
                               f"VALUES ('{titulo}', '{autor}', '{isbn}', '{int(ano)}', '{int(paginas)}', '{idioma}', "
                               f"'{editora}', '{descricao}', '{genero}')")
                con.commit()
                print('ok')
                if messagebox.askyesno("Successfully added", "Book registered. \nAdd another book?"):
                    self.clear_fields()
                else:
                    self.destroy()

        else:
            messagebox.showinfo("Blank field", "Blank fields are not allowed")

    def clear_fields(self):
        self.e_title.delete(0, END)
        self.e_author.delete(0, END)
        self.e_isbn.delete(0, END)
        self.e_year.delete(0, END)
        self.e_pages.delete(0, END)
        self.e_language.delete(0, END)
        self.e_publihser.delete(0, END)
        self.t_description_text.delete('1.0', END)
        self.e_genre.delete(0, END)


if __name__ == '__main__':
    register_book1 = RegisterBook()
    register_book1.mainloop()
