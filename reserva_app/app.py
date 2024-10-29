from flask import Flask, render_template, request, redirect, url_for, flash
from reserva_app.conexao_bd import conexao_fechar, conexao_abrir

app = Flask("Reservas")
app.secret_key = "senha"

db_connection_dict = {
    "host": "",
    "usuario": "",
    "senha": "",
    "banco": ""
}

with app.app_context():

    db = conexao_abrir(**db_connection_dict)
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS Reserva")
    cursor.execute("DROP TABLE IF EXISTS Sala")
    cursor.execute("DROP TABLE IF EXISTS Usuario")
    cursor.execute("CREATE TABLE Usuario (usuario_id int PRIMARY KEY AUTO_INCREMENT,usuario_nome varchar(255),usuario_email varchar(255),usuario_senha varchar(255));")
    cursor.execute("CREATE TABLE Sala (sala_id int PRIMARY KEY AUTO_INCREMENT,sala_tipo varchar(255),sala_capacidade int,sala_desc varchar(255));")
    cursor.execute("CREATE TABLE Reserva (reserva_id int PRIMARY KEY AUTO_INCREMENT,reserva_horario_inicio datetime,reserva_horario_fim datetime,reserva_usuario_id int,reserva_sala_id int,FOREIGN KEY(reserva_usuario_id) REFERENCES Usuario(usuario_id),FOREIGN KEY(reserva_sala_id) REFERENCES Sala(sala_id));")
    cursor.close()
    conexao_fechar(db)

@app.route("/cadastrar-sala", methods=["POST", "GET"])
def cadastrar_sala():

    if request.method == "POST":

        tipo = request.form["tipo"]
        capacidade = request.form["capacidade"]
        descricao = request.form["descricao"]

        if (tipo == '' or capacidade == '' or descricao == ''):
            return render_template("/cadastrar-sala.html")
        
        db = conexao_abrir(**db_connection_dict)
        cursor = db.cursor()
        sql = "INSERT INTO sala (sala_tipo, sala_capacidade, sala_desc) VALUE (%s, %s, %s)"
        cursor.execute(sql, (tipo, capacidade, descricao))
        db.commit()
        cursor.close()
        conexao_fechar(db)

        return redirect(url_for("listar_salas"))
    
    else:

        return render_template("/cadastrar-sala.html")


@app.route("/cadastrar-usuario", methods=["POST", "GET"])
def cadastrar_usuario():

    if request.method == "POST":

        name = request.form["nome"]
        email = request.form["email"]
        password = request.form["password"]

        if (name == '' or email == '' or password == ''):
            flash("credenciais em branco")
            return render_template("cadastrar-usuario.html")

        else:

            db = conexao_abrir(**db_connection_dict)
            cursor = db.cursor()
            cursor.execute("select usuario_email from usuario")
            emails = cursor.fetchall()

            for e in emails:
                if(email in e):
                    flash("email já cadastrado")
                    conexao_fechar(db)
                    return render_template("cadastrar-usuario.html")

            cursor.execute("INSERT INTO Usuario (usuario_nome, usuario_email, usuario_senha) VALUES (%s, %s, %s)", (name, email, password))
            db.commit()
            cursor.close()
            conexao_fechar(db)

            return redirect(url_for("login"))        
    
    else:
        
        return render_template("cadastrar-usuario.html")



@app.route("/listar-salas")
def listar_salas():

    db = conexao_abrir(**db_connection_dict)
    cursor = db.cursor()
    sql = "SELECT * FROM sala"
    cursor.execute(sql)
    salas = cursor.fetchall()
    cursor.close()
    return render_template("/listar-salas.html", salas = salas)



@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        if (email == '' or password == ''):
            flash("credenciais em branco")
            return render_template("login.html")
        
        else:

            db = conexao_abrir(**db_connection_dict)
            cursor = db.cursor()
            cursor.execute("SELECT usuario_email, usuario_senha FROM Usuario")
            dados = cursor.fetchall()

            for tuplas in dados:

                if tuplas[0] == email and tuplas[1] == password:

                    return redirect(url_for("reservas"))
            
            cursor.close()
            conexao_fechar(db)
            flash("email ou senha incorretos")
            return render_template("login.html")
    
    else:

        return render_template("login.html")
    

@app.route("/reservar-sala", methods=["POST", "GET"])
def reservar_sala():

    if request.method == "POST":

        room = request.form["room"]
        inicio = request.form["inicio"]
        fim = request.form["fim"]

        if (room == '' or inicio == '' or fim == ''):

            return render_template("/reservar-sala.html")


        # cadastrar reserva
        db = conexao_abrir(**db_connection_dict)
        cursor = db.cursor()
        sql = "INSERT INTO reserva (reserva_horario_inicio, reserva_horario_fim, reserva_sala_id) VALUE (%s, %s, %s)"
        cursor.execute(sql, (inicio, fim, room))
        db.commit()
        cursor.close()
        conexao_fechar(db)

        return redirect(url_for("reservas"))
    
    else:

        db = conexao_abrir(**db_connection_dict)
        cursor = db.cursor()
        sql = "SELECT * FROM sala"
        cursor.execute(sql)
        salas = cursor.fetchall()
        cursor.close()
        conexao_fechar(db)

        return render_template("/reservar-sala.html", salas = salas)

@app.route("/reservas")
def reservas():

    db = conexao_abrir(**db_connection_dict)
    sql = 'SELECT * FROM reserva'
    cursor = db.cursor()

    cursor.execute(sql)

    reservas = cursor.fetchall()

    cursor.close()
    conexao_fechar(db)
    return render_template("/reservas.html", reservas = reservas)



@app.route("/reserva/detalhe-reserva")
def detalhes_reserva():
    
    db = conexao_abrir(**db_connection_dict)

    sql = 'SELECT * FROM reserva'
    cursor = db.cursor()

    cursor.execute(sql)

    reservas = cursor.fetchall()

    cursor.close()
    conexao_fechar(db)

    return render_template("reserva/detalhe-reserva.html", reservas = reservas[-1])