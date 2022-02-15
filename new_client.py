from tkinter import *
from tkinter import messagebox

import connection_postgre
from generalsettings import label, entry, button, frame, radio


class NewCLient(Tk):
    def __init__(self):
        Tk.__init__(self)

        x = 600
        y = 130

        self.geometry(f"{x}x{y}")
        self.title("Register new client")
        self.config(frame())

        f_main = Frame(self, frame())
        f_main.pack()

        f_linha1 = Frame(f_main, frame())
        f_linha1.pack(pady=(10, 0))
        l_id = Label(f_linha1, text="ID: ", **label(), )
        l_id.pack(side=LEFT, )
        self.l_id_number = Label(f_linha1, text="", **label(), width=6)
        self.l_id_number['background'] = "#202D20"
        self.l_id_number['relief'] = "sunken"
        self.l_id_number.pack(side=LEFT)

        f_nome = Frame(f_main, frame())
        f_nome.pack()
        l_nome = Label(f_linha1, text='Nome: ', **label(), )
        l_nome.pack(side=LEFT, padx=10)
        self.e_nome = Entry(f_linha1, **entry(), width=40)
        self.e_nome.pack(side=LEFT)

        f_linha2 = Frame(f_main, frame())
        f_linha2.pack(pady=10)
        l_telefone = Label(f_linha2, text='Telefone: ', **label())
        l_telefone.pack(side=LEFT)
        self.e_telefone = Entry(f_linha2, **entry(), )
        self.e_telefone.pack(side=LEFT)

        l_idade = Label(f_linha2, text="Idade:", **label(), )
        l_idade.pack(side=LEFT, padx=10)
        self.e_idade = Entry(f_linha2, **entry(), width=3)
        self.e_idade.pack(side=LEFT)

        self.sex = StringVar(value="M")
        l_sexo = Label(f_linha2, text="Sexo:", **label(), )
        l_sexo.pack(side=LEFT, padx=10)
        self.r_sexom = Radiobutton(f_linha2, text="M", variable=self.sex, value="M", **radio())
        self.r_sexom.pack(side=LEFT)
        self.r_sexof = Radiobutton(f_linha2, text="F", variable=self.sex, value="F", **radio())
        self.r_sexof.pack(side=LEFT)

        f_button = Frame(f_main, frame())
        f_button.pack()
        b_save = Button(f_button, text='Save', **button(), command=self.save_new_client)
        b_save.pack(side=LEFT, padx=(0, 20))
        b_quit = Button(f_button, text='Close', **button(), command=self.destroy)
        b_quit.pack(side=LEFT, )
        self.load_new_id()

    def load_new_id(self, con=connection_postgre.get_connection()):
        cursor = con.cursor()
        cursor.execute(f"SELECT max(id_cliente) FROM cliente")
        proximo_id = cursor.fetchone()[0] + 1

        self.l_id_number['text'] = proximo_id

    def save_new_client(self, con=connection_postgre.get_connection()):
        cursor = con.cursor()

        if self.e_nome.get() and self.e_telefone.get() and self.e_idade.get():
            cursor.execute(f"INSERT INTO cliente "
                           f"VALUES ({int(self.l_id_number['text'])}, '{self.e_nome.get()}', '{self.e_telefone.get()}',"
                           f" '{self.e_idade.get()}', '{self.sex.get()}')")

            con.commit()

            if messagebox.askyesno("Registered", "Success. Add another?"):
                self.e_nome.delete(0, END)
                self.e_idade.delete(0, END)
                self.e_telefone.delete(0, END)
                self.load_new_id()
            else:
                self.destroy()
        else:
            messagebox.showinfo("Blank field", "No blank fields allowed")



if __name__ == '__main__':
    new_client = NewCLient()
    new_client.mainloop()