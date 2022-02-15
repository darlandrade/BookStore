import json

import connection_postgre

with open('livros_aleatorios.json', 'w', encoding="utf-8") as file:
    cursor = connection_postgre.get_connection().cursor()
    cursor.execute("SELECT titulo, autor FROM livros ORDER BY random () limit 50")

    livros = {}
    contador = 0
    for titulo, autor in cursor.fetchall():
        contador += 1
        livros[f"{contador}"] = (titulo, autor)


    obj = json.dumps(livros, ensure_ascii=False)
    file.write(obj)

    print(livros)
