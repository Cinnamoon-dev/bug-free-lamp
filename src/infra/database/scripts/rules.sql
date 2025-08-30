-- Tipo Usuário
INSERT INTO tipo_usuario (id, nome) VALUES (1, 'admin');

-- Controllers
INSERT INTO controllers (id, nome) VALUES (1, 'usuario');
INSERT INTO controllers (id, nome) VALUES (2, 'tipo_usuario');

-- Admin Rules
-- admin + usuario controller
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (1, 1, 1, 'all', True);
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (2, 1, 1, 'view', False);
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (3, 1, 1, 'add', True);
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (4, 1, 1, 'edit', True);
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (5, 1, 1, 'delete', True);

-- admin + tipo_usuario controller
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (6, 2, 1, 'all', True);
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (7, 2, 1, 'view', True);
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (8, 2, 1, 'add', True);
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (9, 2, 1, 'edit', True);
INSERT INTO regras (id, controller_id, tipo_usuario_id, acao, permitir) VALUES (10, 2, 1, 'delete', True);