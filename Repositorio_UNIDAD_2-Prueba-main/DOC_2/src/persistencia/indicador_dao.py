SQL_GUARDAR = """ 
INSERT INTO indicador_api
    (fuente, codigo, fecha, valor, unidad, verificado_en) 
VALUES (?, ?, ?, ?, ?, ?) 
ON CONFLICT (fuente, codigo, fecha) DO UPDATE SET 
    valor = excluded.valor, 
    unidad = excluded.unidad, 
    verificado_en = excluded.verificado_en
"""