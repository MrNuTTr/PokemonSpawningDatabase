import psycopg2
import random
from flask import Flask, render_template, request, url_for, redirect


app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='pokemon',
                            user='postgres',
                            password='postgres')
    return conn


@app.route('/')
def index():
    return redirect(url_for("pokemon"))


@app.route('/pokemon/', defaults={'pokemon_id': None})
@app.route('/pokemon/<pokemon_id>/')
def pokemon(pokemon_id):
    text = "All Pokemon"
    conn = get_db_connection()
    cur = conn.cursor()

    if pokemon_id is None:
        cur.execute('SELECT * FROM Pokemon;')
    else:
        cur.execute(f'SELECT * FROM Pokemon WHERE poke_id = {pokemon_id};')
        text = ""
    poke = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('pokemon.html', header_text=text, pokemon=poke)


@app.route('/parents/<pokemon_id>/')
def parents(pokemon_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(f'SELECT name FROM Pokemon WHERE poke_id = {pokemon_id}')
    name = cur.fetchone()

    cur.execute(f'SELECT parent_m, parent_f '
                f'FROM Family WHERE child = {pokemon_id}')
    parent = cur.fetchone()

    if parent is None:
        return render_template('error.html', errortext=f"No parents found for {name[0]}")

    cur.execute(f'SELECT * FROM Pokemon WHERE poke_id = {parent[0]} or poke_id = {parent[1]}')
    family = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('pokemon.html', header_text=f"{name[0]}'s Parents", pokemon=family)


@app.route('/children/<pokemon_id>/')
def children(pokemon_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(f'SELECT name FROM Pokemon WHERE poke_id = {pokemon_id};')
    p_name = cur.fetchone()

    cur.execute(f'SELECT poke_id, owner_id, pokedex_num, name, gender, dob '
                f'FROM Pokemon INNER JOIN Family ON Pokemon.poke_id = Family.child '
                f'WHERE Family.parent_f = {pokemon_id} OR Family.parent_m = {pokemon_id};')
    poke = cur.fetchall()

    if poke is None:
        return render_template('error.html', errortext=f"No children found for {p_name[0]}")

    cur.close()
    conn.close()

    return render_template('pokemon.html', header_text=f"{p_name[0]}'s Children", pokemon=poke)


@app.route('/client/')
def clients():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM Client;')
    client_info = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('clients.html', clients=client_info)


@app.route('/client/<client_id>/')
def client(client_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM Pokemon WHERE owner_id = {client_id};')
    poke = cur.fetchall()

    cur.execute(f'SELECT * FROM Client WHERE owner_id = {client_id};')
    client_info = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('client.html', client=client_info, pokemon=poke)


@app.route('/bookings/')
def bookings():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(f'SELECT booking_id, room_num, poke_id, date_in, date_out, name '
                f'FROM Booking NATURAL JOIN Pokemon;')
    books = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('bookings.html', bookings=books)


@app.route('/pokedex/', defaults={'dex_num': None})
@app.route('/pokedex/<dex_num>/')
def pokedex(dex_num):
    conn = get_db_connection()
    cur = conn.cursor()

    if dex_num is None:
        cur.execute(f'SELECT * FROM Pokedex;')
    else:
        cur.execute(f'SELECT * FROM Pokedex WHERE dex_num = {dex_num};')
    dex = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('pokedex.html', header_text="PokeDex", pokedex=dex)


@app.route('/create/', methods=('GET', 'POST'))
def add_pokemon():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        print(request.form)

        poke_id = random.randint(a=10000, b=99999)
        owner = request.form['owner_id']
        dex = request.form.get('pokedex')
        name = request.form['name']
        level = int(request.form['level'])
        gender = request.form.get('gender')

        cur.execute('INSERT INTO Pokemon '
                    'VALUES (%s, %s, %s, %s, %s, %s)',
                    (poke_id, owner, dex, name, level, gender))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    cur.execute('SELECT * FROM Client;')
    owners = cur.fetchall()

    cur.execute('SELECT * FROM Pokedex;')
    dex = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('add_pokemon.html', owners=owners, pokedex=dex)


app.run(debug=True)
