CREATE TABLE IF NOT EXISTS mascotas_sql (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    raza VARCHAR(50) NOT NULL,
    edad INT NOT NULL
);

-- Datos iniciales en SQL para el Ejercicio 21
INSERT INTO mascotas_sql (nombre, raza, edad) VALUES
('Kira', 'Pastor Alemán', 4),
('Thor', 'Bulldog', 2),
('Bimba', 'Dálmata', 5);