CREATE SCHEMA dw;
CREATE TABLE dw.fat_principal (data date NOT NULL, chv_produto bigint, chv_unidade text, flg_tipo_fato text, valor_liq numeric, lucro_liq numeric, qtde_cliente numeric, qtde_liq numeric);
CREATE TABLE dw.dim_produto_unidade_total (chv_produto bigint, chv_unidade text);
CREATE TABLE dw.dim_grupo_produto_quebra_total (chv_produto bigint, dsc_clas_departamento text, dsc_clas_setor text, dsc_clas_categoria text);
INSERT INTO dw.fat_principal VALUES ('2026-01-10', 1, '001', 'fat_venda_det_tipovenda', 100, 20, 0, 5), ('2026-01-10', 1, '001', 'fat_qtde_clientes', 0, 0, 2, 0);
INSERT INTO dw.dim_produto_unidade_total VALUES (1, '001');
INSERT INTO dw.dim_grupo_produto_quebra_total VALUES (1, 'Mercearias', 'Mercearia Doce', 'Biscoitos');
