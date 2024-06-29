import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Inserciones para el modelo Barrio

barrios = [
    ('Barrio Norte',),
    ('Palermo',),
    ('Recoleta',),
    ('San Telmo',),
    ('Belgrano',)
]
cursor.executemany('INSERT INTO main_app_barrio (nombre) VALUES (?)', barrios)

# Inserciones para el modelo Vecino
vecinos = [
    ('12345678', 'Juan', 'Pérez', 'Calle Falsa 123', 1),
    ('87654321', 'María', 'Gómez', 'Avenida Siempre Viva 456', 2),
    ('11223344', 'Carlos', 'López', 'Boulevard de los Sueños 789', 3),
    ('22334455', 'Ana', 'Martínez', 'Calle Primavera 123', 1),
    ('33445566', 'Luis', 'Fernández', 'Avenida Otoño 456', 2),
    ('44556677', 'Elena', 'García', 'Calle Verano 789', 3),
    ('55667788', 'Roberto', 'Mendoza', 'Avenida Invierno 101', 1),
    ('66778899', 'Isabel', 'Ramírez', 'Calle Sol 202', 2),
    ('77889900', 'Sergio', 'Álvarez', 'Avenida Luna 303', 3),
    ('88990011', 'Natalia', 'Santos', 'Calle Estrella 404', 1),
    ('99001122', 'Miguel', 'Reyes', 'Avenida Cielo 505', 2),
    ('00112233', 'Laura', 'Herrera', 'Calle Viento 606', 3),
    ('11223345', 'Jorge', 'Morales', 'Avenida Tierra 707', 1),
    ('22334456', 'Patricia', 'Castro', 'Calle Agua 808', 2),
    ('33445567', 'Alberto', 'Suárez', 'Avenida Fuego 909', 3),
    ('44556678', 'Andrea', 'Silva', 'Calle Metal 111', 1),
    ('55667789', 'Gustavo', 'Ortiz', 'Avenida Madera 222', 2),
    ('66778891', 'Claudia', 'Navarro', 'Calle Piedra 333', 3),
    ('77889902', 'Fernando', 'Iglesias', 'Avenida Cristal 444', 1),
    ('88990013', 'Lucía', 'Pérez', 'Calle Espejo 555', 2)
]
cursor.executemany('INSERT INTO main_app_vecino (documento, nombre, apellido, direccion, codigo_barrio) VALUES (?, ?, ?, ?, ?)', vecinos)

# Inserciones para el modelo Rubro
rubros = [
    ('Electricidad',),
    ('Plomería',),
    ('Carpintería',)
]
cursor.executemany('INSERT INTO main_app_rubro (descripcion) VALUES (?)', rubros)

# Inserciones para el modelo Desperfecto
desperfectos = [
    ('Problema eléctrico general', 1),
    ('Problema de plomería general', 2),
    ('Problema de carpintería general', 3)
]
cursor.executemany('INSERT INTO main_app_desperfecto (descripcion, rubro_id) VALUES (?, ?)', desperfectos)

# Inserciones para el modelo Personal
personales = [
    ('LEG001', 'Ana', 'Martínez', '29837465', 'Mantenimiento', 'Técnico', '2020-01-15', '123'),
    ('LEG002', 'Luis', 'Fernández', '30598472', 'Administración', 'Supervisor', '2018-03-22', '123'),
    ('LEG003', 'Elena', 'García', '31784930', 'Seguridad', 'Guardia', '2019-06-10', '123'),
    ('LEG004', 'Roberto', 'Mendoza', '32837465', 'Limpieza', 'Operario', '2021-02-10', '123'),
    ('LEG005', 'Isabel', 'Ramírez', '33987456', 'Mantenimiento', 'Técnico', '2017-07-05', '123'),
    ('LEG006', 'Sergio', 'Álvarez', '34598712', 'Administración', 'Analista', '2016-04-18', '123'),
    ('LEG007', 'Natalia', 'Santos', '35678901', 'Recursos Humanos', 'Asistente', '2019-11-11', '123'),
    ('LEG008', 'Miguel', 'Reyes', '36789012', 'Mantenimiento', 'Supervisor', '2018-08-08', '123'),
    ('LEG009', 'Laura', 'Herrera', '37890123', 'Limpieza', 'Operario', '2020-03-25', '123'),
    ('LEG010', 'Jorge', 'Morales', '38901234', 'Seguridad', 'Guardia', '2017-10-15', '123'),
    ('LEG011', 'Patricia', 'Castro', '39912345', 'Administración', 'Jefe de Sector', '2016-05-30', '123'),
    ('LEG012', 'Alberto', 'Suárez', '40923456', 'Mantenimiento', 'Técnico', '2015-12-01', '123'),
    ('LEG013', 'Andrea', 'Silva', '41934567', 'Limpieza', 'Supervisor', '2018-07-19', '123'),
    ('LEG014', 'Gustavo', 'Ortiz', '42945678', 'Recursos Humanos', 'Analista', '2019-02-20', '123'),
    ('LEG015', 'Claudia', 'Navarro', '43956789', 'Mantenimiento', 'Supervisor', '2017-06-06', '123'),
    ('LEG016', 'Fernando', 'Iglesias', '44967890', 'Seguridad', 'Guardia', '2018-01-10', '123'),
    ('LEG017', 'Lucía', 'Pérez', '45978901', 'Administración', 'Jefe de Sector', '2019-09-09', '123'),
    ('LEG018', 'Carlos', 'López', '46989012', 'Limpieza', 'Operario', '2020-11-12', '123'),
    ('LEG019', 'María', 'Gómez', '47990123', 'Recursos Humanos', 'Asistente', '2017-03-27', '123'),
    ('LEG020', 'Santiago', 'Paredes', '48901234', 'Mantenimiento', 'Técnico', '2016-08-16', '123')
]
cursor.executemany('INSERT INTO main_app_personal (legajo, nombre, apellido, documento, sector, categoria, fechaIngreso, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', personales)

# Inserciones para el modelo Sitio
sitios = [
    (-34.603722, -58.381592, 'Calle Corrientes', 123, 'Entre Ríos', 'San Juan', 'Sitio de prueba en el centro', 'Juan Pérez', '2023-01-01', None, 'Sin comentarios'),
    (-34.609722, -58.379167, 'Avenida Santa Fe', 456, 'Callao', 'Pueyrredón', 'Sitio en el barrio norte', 'María Gómez', '2023-02-15', '2023-06-30', 'Comentarios adicionales'),
    (-34.615722, -58.374167, 'Calle Lavalle', 789, 'Paraná', 'Montevideo', 'Sitio en el microcentro', 'Carlos López', '2023-03-20', None, 'Trabajos en progreso'),
    (-34.620722, -58.369167, 'Avenida Córdoba', 101, 'Florida', 'Maipú', 'Sitio en el centro financiero', 'Ana Martínez', '2023-04-25', None, 'Proyectos a futuro'),
    (-34.625722, -58.364167, 'Calle Sarmiento', 202, 'Esmeralda', 'Suipacha', 'Sitio en el casco histórico', 'Luis Fernández', '2023-05-10', '2023-11-10', 'Obras finalizadas')
]
cursor.executemany('INSERT INTO main_app_sitio (latitud, longitud, calle, numero, entreCalleA, entreCalleB, descripcion, aCargoDe, apertura, cierre, comentarios) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', sitios)



# Confirmar los cambios
conn.commit()

# Cerrar la conexión
conn.close()
