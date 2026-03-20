-- Script de Base de Datos - Semana 14
-- Estudiante: William Zapata

CREATE DATABASE IF NOT EXISTS la_estacion_db;
USE la_estacion_db;

-- Tabla de usuarios con la columna 'email' como pide la tarea
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Insertar un usuario de prueba para el docente
INSERT INTO usuarios (nombre, email, password) 
VALUES ('William Zapata', 'william@correo.com', '201624');

-- Tabla de productos (Semana 13)
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre_producto VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    descripcion TEXT
);