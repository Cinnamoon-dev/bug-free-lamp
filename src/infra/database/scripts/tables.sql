CREATE TABLE IF NOT EXISTS tipo_usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS usuario (
    id SERIAL PRIMARY KEY,
    email VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(200) NOT NULL,
    tipo_id INTEGER NOT NULL,

    CONSTRAINT fk_tipo_usuario FOREIGN KEY (tipo_id)
    REFERENCES tipo_usuario (id)
);