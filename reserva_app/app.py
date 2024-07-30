from flask import Flask, render_template, request, redirect, url_for, flash
import csv

app = Flask("Reservas")
app.secret_key = "senha"

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

            return render_template("cadastro.html")

        else:

            with open("csvs/users.csv", "a+") as csvfile:

                csvreader = csv.reader(csvfile)
        
                for row in csvreader:

                    if row[0].strip() == email:

                        return render_template("cadastro.html")
                    
                with open("csvs/users.csv", "a+", newline="") as csvfile:

                    csvwriter = csv.writer(csvfile, lineterminator='\n')

                    csvwriter.writerow([email, password])
                
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

            return render_template("login.html")
        
        else:

            with open("csvs/users.csv", "a+") as csvfile:
                csvreader = csv.reader(csvfile)

                if csvreader:

                    for row in csvreader:

                        if row[0].strip() == email and row[1].strip() == password:

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

