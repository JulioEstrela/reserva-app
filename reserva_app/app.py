from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import mysql.connector

app = Flask("Reservas")
app.secret_key = "senha"

def conexao_abrir():

    return mysql.connector.connect(host="", user="", password="", database="")

def conexao_fechar(con):
    con.close

with app.app_context():

    db = conexao_abrir()
    mycursor = db.cursor()
    mycursor.execute("DROP TABLE IF EXISTS Reserva")
    mycursor.execute("DROP TABLE IF EXISTS Sala")
    mycursor.execute("DROP TABLE IF EXISTS Usuario")
    mycursor.execute("CREATE TABLE Usuario (usuario_id int PRIMARY KEY AUTO_INCREMENT,usuario_nome varchar(255),usuario_email varchar(255),usuario_senha varchar(255));")
    mycursor.execute("CREATE TABLE Sala (sala_id int PRIMARY KEY AUTO_INCREMENT,sala_tipo varchar(255),sala_capacidade int,sala_desc varchar(255));")
    mycursor.execute("CREATE TABLE Reserva (reserva_id int PRIMARY KEY AUTO_INCREMENT,reserva_horario_inicio datetime,reserva_horario_fim datetime,reserva_usuario_id int,reserva_sala_id int,FOREIGN KEY(reserva_usuario_id) REFERENCES Usuario(usuario_id),FOREIGN KEY(reserva_sala_id) REFERENCES Sala(sala_id));")
    conexao_fechar(db)

@app.route("/cadastrar-sala", methods=["POST", "GET"])
def cadastrar_sala():

    if request.method == "POST":

        with open("csvs/id.csv", "a+") as idezinha:

            csvwriter = csv.writer(idezinha, lineterminator='\n')
            csvwriter.writerow("o")

        with open("csvs/id.csv", "a+") as idezinho:

            csvreader = csv.reader(idezinho)
            id = len(list(csvreader))  

        tipo = request.form["tipo"]
        capacidade = request.form["capacidade"]
        descricao = request.form["descricao"]

        if (tipo == '' or capacidade == '' or descricao == ''):

            return render_template("/cadastrar-sala.html")
        
        else:

            with open("./csvs/salas.csv", "a+") as csvfile:

                csvwriter = csv.writer(csvfile, lineterminator='\n')

                csvwriter.writerow([id, tipo, descricao, capacidade, "Sim"])

                return redirect(url_for("lista_salas"))
    
    else:

        return render_template("/cadastrar-sala.html")


@app.route("/cadastro", methods=["POST", "GET"])
def cadastro():

    if request.method == "POST":

        name = request.form["nome"]
        email = request.form["email"]
        password = request.form["password"]

        if (name == '' or email == '' or password == ''):
            flash("credenciais em branco")
            return render_template("cadastro.html")

        else:

            db = conexao_abrir()
            mycursor = db.cursor()
            mycursor.execute("select usuario_email from usuario")
            emails = mycursor.fetchall()

            for e in emails:
                if(email in e):
                    flash("email já cadastrado")
                    conexao_fechar(db)
                    return render_template("cadastro.html")

            mycursor.execute("INSERT INTO Usuario (usuario_nome, usuario_email, usuario_senha) VALUES (%s, %s, %s)", (name, email, password))
            db.commit()
            mycursor.close()
            conexao_fechar(db)

            return redirect(url_for("login"))        
    
    else:
        
        return render_template("cadastro.html")



@app.route("/listar-salas")
def lista_salas():

    roomlist = []

    with open("csvs/salas.csv", "a+") as csvfile:

        for room in csvfile:

            this_room = room.strip().split(",")
            roomlist.append(this_room)

        return render_template("/listar-salas.html", salas = roomlist)



@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        if (email == '' or password == ''):
            flash("credenciais em branco")
            return render_template("login.html")
        
        else:

            db = conexao_abrir()
            mycursor = db.cursor()
            mycursor.execute("SELECT usuario_email, usuario_senha FROM Usuario")
            dados = mycursor.fetchall()

            for tuplas in dados:

                if tuplas[0] == email and tuplas[1] == password:

                    return redirect(url_for("reservas"))
                    
            flash("usuário inválido")
            return render_template("login.html")
    
    else:

        return render_template("login.html")
    

@app.route("/reservar-sala", methods=["POST", "GET"])
def reserva_sala():

    if request.method == "POST":

        room = request.form["room"]
        inicio = request.form["inicio"]
        fim = request.form["fim"]

        if (room == '' or inicio == '' or fim == ''):

            return render_template("/reservar-sala.html")

        else:

            with open("csvs/reservas.csv", "a+") as file:

                csvwriter = csv.writer(file, lineterminator='\n')

                csvwriter.writerow([room, inicio, fim])

            return redirect(url_for("detalhes_reserva"))
    
    else:

        roomlist = []

        with open("csvs/salas.csv", "a+") as csvfile:

            for room in csvfile:

                this_room = room.strip().split(",")
                roomlist.append(this_room)

        return render_template("/reservar-sala.html", salas = roomlist)



@app.route("/reservas")
def reservas():

    with open("csvs/salas.csv", "a+") as csvfile:

        csvreader = csv.reader(csvfile)

        return render_template("/reservas.html", salas = csvreader)



@app.route("/reserva/detalhe-reserva")
def detalhes_reserva():

    with open("csvs/reservas.csv", "a+") as file:

        csvreader = csv.reader(file)

        reservaslista = list(csvreader)

    return render_template("reserva/detalhe-reserva.html", reservas = reservaslista[-1])