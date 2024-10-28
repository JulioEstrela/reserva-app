CREATE TABLE Usuario (

	usuario_id int PRIMARY KEY AUTO_INCREMENT,
    usuario_nome varchar(255),
    usuario_email varchar(255),
    usuario_senha varchar(255)
);

CREATE TABLE Sala (

	sala_id int PRIMARY KEY AUTO_INCREMENT,
    sala_tipo varchar(255),
    sala_capacidade int,
    sala_desc varchar(255)    

);

CREATE TABLE Reserva (

	reserva_id int PRIMARY KEY AUTO_INCREMENT,
    reserva_horario_inicio datetime,
    reserva_horario_fim datetime,
    reserva_usuario_id int,
    reserva_sala_id int,
    
    FOREIGN KEY(reserva_usuario_id) REFERENCES Usuario(usuario_id),
	FOREIGN KEY(reserva_sala_id) REFERENCES Sala(sala_id)

);