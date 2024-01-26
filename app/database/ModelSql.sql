---------------------------------------------------------------------------
-- MySQL 
CREATE TABLE PrioridadNivel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nivel VARCHAR(255) NOT NULL
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    correo VARCHAR(120) NOT NULL,
    contraseña_hash VARCHAR(128) NOT NULL
    suscripcion BOOLEAN NOT NULL DEFAULT FALSE
);



CREATE TABLE ubicaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ComunaUnidad VARCHAR(255),
    latitud DECIMAL(10, 6),   -- Tipo de dato DECIMAL para latitud
    longitud DECIMAL(10, 6)  -- Tipo de dato DECIMAL para longitud
);


CREATE TABLE licitaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    CodigoExterno VARCHAR(120),
    CodigoEstado VARCHAR(120),
    Descriptive_name VARCHAR(120),
    Nombre_del_Organismo VARCHAR(255),  -- Nombre del organismo convocante de la licitación
    Producto VARCHAR(255),             -- Nombre del producto a licitar
    Precio DECIMAL(10, 2),             -- Precio estimado o base de la licitación
    Cantidad INT,                      -- Cantidad de productos a adquirir
    FechaCreacion DATETIME,            -- Fecha de creación de la licitación
    FechaPublicacion DATETIME,         -- Fecha de publicación de la licitación
    FechaCerrada DATETIME,             -- Fecha de cierre de la licitación
    FechaDesierta DATETIME,            -- Fecha de declaración de desierta de la licitación
    FechaRevocada DATETIME,            -- Fecha de revocación de la licitación
    FechaSuspendido DATETIME,          -- Fecha de suspensión de la licitación
    FechaAdjudicacion DATETIME,        -- Fecha de adjudicación de la licitación
    id_ComunaUnidad INT,               -- ID de la comuna o unidad relacionada
    nivel_prioridad INT,               -- Nivel de prioridad de la licitación
    FOREIGN KEY (id_ComunaUnidad) REFERENCES ubicaciones(id),
    FOREIGN KEY (nivel_prioridad) REFERENCES PrioridadNivel(id)
);

CREATE TABLE seguimiento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_licitacion INT,
    id_usuario INT,
    id_prioridad_nivel INT,
    FOREIGN KEY (id_licitacion) REFERENCES licitaciones(id),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_prioridad_nivel) REFERENCES PrioridadNivel(id)
);



----------------------------------------------------------------------
-- PostgreSQL
CREATE TABLE PrioridadNivel (
    id SERIAL PRIMARY KEY,
    nivel VARCHAR(255) NOT NULL
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    correo VARCHAR(120) NOT NULL,
    contraseña_hash VARCHAR(128) NOT NULL,
    suscripcion BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE ubicaciones (
    id SERIAL PRIMARY KEY,
    ComunaUnidad VARCHAR(255),
    latitud DECIMAL(10, 6),   -- Tipo de dato DECIMAL para latitud
    longitud DECIMAL(10, 6)  -- Tipo de dato DECIMAL para longitud
);

CREATE TABLE licitaciones (
    id SERIAL PRIMARY KEY,
    CodigoExterno VARCHAR(120),
    CodigoEstado VARCHAR(120),
    Descriptive_name VARCHAR(120),
    Nombre_del_Organismo VARCHAR(255),
    Producto VARCHAR(255),
    Precio DECIMAL(10, 2),
    Cantidad INT,
    FechaCreacion TIMESTAMPTZ,  -- Utiliza TIMESTAMPTZ para almacenar fechas con zona horaria
    FechaPublicacion TIMESTAMPTZ,
    FechaCerrada TIMESTAMPTZ,
    FechaDesierta TIMESTAMPTZ,
    FechaRevocada TIMESTAMPTZ,
    FechaSuspendido TIMESTAMPTZ,
    FechaAdjudicacion TIMESTAMPTZ,
    id_ComunaUnidad INT,
    tipo_codificación VARCHAR(120),
    FOREIGN KEY (id_ComunaUnidad) REFERENCES ubicaciones(id)
);

CREATE TABLE seguimiento (
    id SERIAL PRIMARY KEY,
    id_licitacion INT,
    id_usuario INT,
    suscripcion_notificaciones BOOLEAN,
    FOREIGN KEY (id_licitacion) REFERENCES licitaciones(id),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);



-- Tabla del Usario sus detalle como ubicacion favotio, Producto o servio etca  prametros_perfil success! parametros_perfil
CREATE TABLE nombre_producto_servicio_favorita (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    nombre_producto_servicio VARCHAR(255) NOT NULL,
    CONSTRAINT fk_usuario_producto_servicio FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE nombre_comuna_favorita (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    nombre_comuna VARCHAR(255) NOT NULL,
    CONSTRAINT fk_usuario_comuna FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE parametros_perfil (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    numero_licitacion INTEGER,
    monto_min DECIMAL(12, 2),
    monto_max DECIMAL(12, 2),
    CONSTRAINT fk_usuario_comuna FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE codificaciones_perfil (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    codificacio VARCHAR(255) NOT NULL,
    CONSTRAINT fk_usuario_comuna FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
