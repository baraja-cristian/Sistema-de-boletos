CREATE DATABASE Systema_integracion CHARACTER SET utf8 COLLATE utf8_general_ci;

USE Systema_integracion;



CREATE TABLE Rol_usuario(
    ID_rol_usuario VARCHAR(15) PRIMARY KEY,
    Tipo_rol VARCHAR(25)
);

CREATE TABLE Usuario (
    ID_estudiante VARCHAR(15) PRIMARY KEY,
    Usuario_cedula VARCHAR(10) NOT NULL,
    Usuario_nombre1 VARCHAR(45) NOT NULL,
    Usuario_nombre2 VARCHAR(45) NOT NULL,
    Usuario_apellido1 VARCHAR(45) NOT NULL,
    Usuario_apellido2 VARCHAR(45) NOT NULL,
    Usuario_correo VARCHAR(100) NULL,
    Usuario_clave VARCHAR(45) NOT NULL,
    Usuario_ID_rol VARCHAR(25) NOT NULL,
    FOREIGN KEY (Usuario_ID_rol) REFERENCES Rol_usuario(ID_rol_usuario) ON DELETE CASCADE
);



CREATE TABLE Metodo_pago(
    ID_metodo_pago VARCHAR(15) PRIMARY KEY,
    Metodo_pago VARCHAR(25) NOT NULL
);



CREATE TABLE Boleto_tipo (
    ID_boleto_tipo VARCHAR(15) PRIMARY KEY,
    Tipo_boleto_tipo VARCHAR(25) NOT NULL,
    Precio_boleto_tipo FLOAT NOT NULL
);



CREATE TABLE Compra_boleto (
    ID_compra_boleto VARCHAR(15) PRIMARY KEY,
    Fecha_boleto DATE,
    Usuario_ID_cliente VARCHAR(15) NOT NULL,
    Usuario_ID_vendedor VARCHAR(15) NOT NULL,
    Metodo_ID_pago VARCHAR(15) NOT NULL,
    FOREIGN KEY (Usuario_ID_cliente) REFERENCES Usuario(ID_estudiante) ON DELETE CASCADE,
    FOREIGN KEY (Usuario_ID_vendedor) REFERENCES Usuario(ID_estudiante) ON DELETE CASCADE,
    FOREIGN KEY (Metodo_ID_pago) REFERENCES Metodo_pago(ID_metodo_pago) ON DELETE CASCADE
);


CREATE TABLE Factura(
    ID_factura VARCHAR (15),
    Compra_ID_boleto VARCHAR(15) NOT NULL,
    Boleto_ID_tipo VARCHAR(15) NOT NULL,
    FOREIGN KEY (Compra_ID_boleto) REFERENCES Compra_boleto(ID_compra_boleto) ON DELETE CASCADE,
    FOREIGN KEY (Boleto_ID_tipo) REFERENCES Boleto_tipo(ID_boleto_tipo) ON DELETE CASCADE
);