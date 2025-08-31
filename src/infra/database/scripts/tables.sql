CREATE TABLE IF NOT EXISTS tipo_usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS usuario (
    id SERIAL PRIMARY KEY,
    email VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(200) NOT NULL,
    tipo_usuario_id INTEGER NOT NULL,

    CONSTRAINT fk_tipo_usuario FOREIGN KEY (tipo_usuario_id)
    REFERENCES tipo_usuario (id)
);

CREATE TABLE IF NOT EXISTS controllers (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS regras (
    id SERIAL PRIMARY KEY,
    acao VARCHAR(50) NOT NULL,
    permitir BOOLEAN NOT NULL,
    controller_id INTEGER NOT NULL,
    tipo_usuario_id INTEGER NOT NULL,
    
    CONSTRAINT fk_controller FOREIGN KEY (controller_id)
    REFERENCES controllers (id),
    CONSTRAINT fk_tipo_usuario FOREIGN KEY (tipo_usuario_id)
    REFERENCES tipo_usuario (id)
);