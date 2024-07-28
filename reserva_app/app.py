from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask("Reservas")

@app.route("/cadastrar-sala")
def cadastrar_sala():

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

            with open("csvs/users.csv", "r") as csvfile:

                csvreader = csv.reader(csvfile)
        
                for row in csvreader:

                    if row[0].strip() == email:

                        return render_template("cadastro.html")
                
                csvfile.close()
                    
                with open("csvs/users.csv", "a", newline="") as csvfile:

                    csvwriter = csv.writer(csvfile, lineterminator='\n')

                    csvwriter.writerow([email, password])

                    csvfile.close()
                
                return redirect(url_for("login"))
            
    
    else:
        
        return render_template("cadastro.html")



@app.route("/listar-salas")
def lista_salas():

    with open("csvs/salas.csv", "r") as csvfile:

        csvreader = csv.reader(csvfile)

        return render_template("/listar-salas.html", salas = csvreader)



@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        if (email == '' or password == ''):

            return render_template("login.html")
        
        else:

            with open("csvs/users.csv", "r") as csvfile:
                csvreader = csv.reader(csvfile)

                if csvreader:

                    for row in csvreader:

                        if row[0].strip() == email and row[1].strip() == password:

                            return redirect(url_for("reservas"))
                    
                    csvfile.close()
                    
                    return render_template("login.html")
    
    else:

        return render_template("login.html")



@app.route("/reservar-sala")
def reserva_sala():

    return render_template("/reservar-sala.html")



@app.route("/reservas")
def reservas():

    with open("csvs/salas.csv", "r") as csvfile:

        csvreader = csv.reader(csvfile)

        return render_template("/reservas.html", salas = csvreader)



@app.route("/reserva/detalhe-reserva")
def detalhes_reserva():

    return render_template("reserva/detalhe-reserva.html")

