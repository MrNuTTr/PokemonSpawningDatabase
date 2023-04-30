from datetime import datetime

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


@app.route('/booking/')
def bookings():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(f'SELECT booking_id, room_num, poke_id, date_in, date_out, name '
                f'FROM Booking NATURAL JOIN Pokemon '
                f'WHERE date_out is null;')
    books = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('bookings.html', bookings=books)

@app.route('/booking/past/')
def bookings_past():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(f'SELECT booking_id, room_num, poke_id, date_in, date_out, name '
                f'FROM Booking NATURAL JOIN Pokemon '
                f'WHERE date_out is not null;')
    books = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('past_bookings.html', bookings=books)

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
        poke_id = random.randint(a=10000, b=99999)
        owner = request.form['owner_id']
        dex = request.form['pokedex']
        name = request.form['name']
        level = request.form['level']
        gender = request.form['gender']
        dob = request.form['dob']
        is_child = bool(request.form['is_child'])

        cur.execute('INSERT INTO Pokemon '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (poke_id, owner, dex, name, level, gender, dob))
        conn.commit()
        cur.close()
        conn.close()

        if is_child:
            return redirect(url_for('add_child', client_id=owner, pokemon_id=poke_id))
        else:
            return redirect(url_for('pokemon', pokemon_id=poke_id))

    cur.execute('SELECT * FROM Client;')
    owners = cur.fetchall()

    cur.execute('SELECT * FROM Pokedex;')
    dex = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('add_pokemon.html', owners=owners, pokedex=dex)


@app.route('/client/<client_id>/add/child/<pokemon_id>/', methods=('GET', 'POST'))
def add_child(client_id, pokemon_id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        father = request.form['father']
        mother = request.form['mother']

        cur.execute('INSERT INTO Family VALUES (%s, %s, %s)',
                    (pokemon_id, father, mother))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('pokemon', pokemon_id=pokemon_id))

    cur.execute(f"SELECT * FROM Pokemon WHERE owner_id={client_id} and poke_id<>{pokemon_id} and gender='M'")
    males = cur.fetchall()

    cur.execute(f"SELECT * FROM Pokemon WHERE owner_id={client_id} and poke_id<>{pokemon_id} and gender='F'")
    females = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('add_child.html', males=males, females=females)


@app.route('/booking/add/', methods=('GET', 'POST'))
def select_client():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        client_id = request.form['owner_id']
        return redirect(url_for('add_booking', client_id=client_id))

    cur.execute('SELECT * FROM Client;')
    owners = cur.fetchall()

    return render_template('select_client.html', owners=owners)


@app.route('/booking/add/<client_id>/', methods=('GET', 'POST'))
def add_booking(client_id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        booking_id = random.randint(a=10000, b=99999)
        room_num = request.form['room_num']
        poke_id = request.form['pokemon']
        date_in = request.form['date_in']
        date_out = request.form['date_out'] or None

        cur.execute('INSERT INTO Booking '
                    'VALUES (%s, %s, %s, %s, %s);',
                    (booking_id, room_num, poke_id, date_in, date_out))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('bookings'))

    cur.execute(f'SELECT room_num FROM storage '
                f'EXCEPT '
                f'SELECT room_num '
                f'FROM Storage NATURAL JOIN Booking '
                f'WHERE date_out is null')
    open_rooms = cur.fetchall()

    cur.execute(f'SELECT poke_id, owner_id, pokedex_num, name, level, gender, dob '
                f'FROM Pokemon WHERE owner_id = {client_id} '
                f'EXCEPT '
                f'SELECT poke_id, owner_id, pokedex_num, name, level, gender, dob '
                f'FROM Pokemon NATURAL JOIN Booking WHERE date_out is null')
    poke = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('add_booking.html', rooms=open_rooms, pokemon=poke)


@app.route('/booking/update/<booking_id>/', methods=['GET', 'POST'])
def update_booking(booking_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(f'SELECT * FROM Booking WHERE booking_id={booking_id}')
    booking = cur.fetchone()

    if booking[4] is not None:
        return render_template('error.html', errortext="Cannot update an entry for past resident.")

    if request.method == "POST":
        date_out = request.form['date_out']
        cur.execute('UPDATE Booking '
                    'SET date_out=%s '
                    'WHERE booking_id=%s',
                    (date_out, booking_id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('bookings'))

    cur.close()
    conn.close()
    return render_template('update_booking.html')


app.run(debug=True)
