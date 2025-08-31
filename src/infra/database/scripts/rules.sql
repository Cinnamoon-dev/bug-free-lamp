-- Tipo Usuário
INSERT INTO tipo_usuario (id, nome) VALUES (1, 'admin');
ALTER SEQUENCE tipo_usuario_id_seq RESTART WITH 2;

-- Usuário
-- senha: 1234
INSERT INTO usuario (id, email, senha, tipo_usuario_id) VALUES (1, 'admin@email.com', '$6$xvhoMyeu7TlurX6Z$.j4NQGAvbEzu3IKSJAWU8IzTqAGVW8RZ2sUWmJSzJY2QR0VJhm26rOC/0.7UXT3c8YrwoS3y4pUdbWJV7GEZG1', 1);
ALTER SEQUENCE usuario_id_seq RESTART WITH 2;

-- Controllers
INSERT INTO controllers (id, nome) VALUES (1, 'usuario');
INSERT INTO controllers (id, nome) VALUES (2, 'tipo_usuario');

-- Admin Rules
-- admin + usuario controller
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (1, 1, 1, 'all', True);
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (2, 1, 1, 'view', True);
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (3, 1, 1, 'add', True);
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (4, 1, 1, 'edit', True);
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (5, 1, 1, 'delete', True);

-- admin + tipo_usuario controller
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (6, 2, 1, 'all', True);
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (7, 2, 1, 'view', True);
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (8, 2, 1, 'add', True);
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (9, 2, 1, 'edit', True);
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (10, 2, 1, 'delete', True);