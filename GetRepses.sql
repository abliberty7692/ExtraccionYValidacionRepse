DECLARE @TAB TABLE(ID INT IDENTITY(1,1), OPERADOR_PERIODO_ID INT, OPERADOR_ID INT, RFC VARCHAR(20), RAZON_SOCIAL VARCHAR(100), MES INT, ANIO INT, DOC_ID INT, PATH_FILE TEXT);


INSERT @TAB
        SELECT op.Id, o.Id, o.Rfc, o.RazonSocial, op.Mes, Op.Ano, d.Id, d.[Path]
        FROM ( SELECT * FROM PORTAL.BM_SERV_ESP.OperadorPeriodo WHERE Activo = 1
            ) op 
       INNER JOIN (SELECT * FROM PORTAL.BM_SERV_ESP.Operador WHERE EmpresaId in --*(115,116,874) --Bandag-Bridgestone
																				--*(227)		  --Takeda
																							  --FemsaServicios (abajo)
																				--*(871,881,888,901,907,908,909,910,911,912,913,914,915,916,917,918,919)
																				--*(815)		  --Banco Invex
																				--*(814)		  --Comercial City Fresko
																				--*(439,442,868,869)	--FEMCO
																				--*(873,878,898)	--Mercedes Benz & Daimler (Financial/Vehiculos)
																				(886)		  --Chemtreat
																				--*(903)		  --Unifin Financiera
																				--*(905)		  --Grupo ABC 
																				
            ) AS o ON o.Id = op.OperadorId
       INNER JOIN (SELECT * FROM PORTAL.BM_SERV_ESP.CategoriaOperador WHERE EmpresaCategoriumId in (
                                SELECT Id FROM PORTAL.BM_SERV_ESP.EmpresaCategoria ec WHERE EmpresaId in --*(115,116,874) --Bandag-Bridgestone 120+
 																										--*(227)		  --Takeda 20+
																										--FemsaServicios (abajo) 80+
																										--*(871,881,888,901,907,908,909,910,911,912,913,914,915,916,917,918,919)
																										--*(815)		  --Banco Invex 60+
																										--*(814)		  --Comercial City Fresko 50+
																										--*(439,442,868,869)	--FEMCO 1500+
																										--*(873,878,898)	--Mercedes Benz & Daimler (Financial/Vehiculos) +30
																										(886)		  --Chemtreat 5+
																										--*(903)		  --Unifin Financiera 10+
																										--*(905)		  --Grupo ABC 15+
								AND CategoriaMaterialidadId = 2 )
                ) AS co ON co.OperadorPeriodoId = op.Id
       INNER JOIN (SELECT * FROM PORTAL.BM_SERV_ESP.CategoriaOperadorTipoDocumento WHERE CatalogoTipoDocumentoId = 4
            ) AS cotd ON cotd.CategoriaOperadorId = co.Id
       INNER JOIN (SELECT * FROM PORTAL.BM_SERV_ESP.Documentos WHERE CatalogoEstatusId = 4  --Estatus 4 para validados 
																							--Estatus 2 para nuevos 
																							AND [PATH] IS NOT NULL 
            ) AS d ON d.CategoriaOperadorTipoDocumentoId = cotd.Id
        ORDER BY o.Rfc, op.Ano, op.Mes

SELECT * 
FROM (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY RFC ORDER BY ID) AS DUPLICADO
            FROM @TAB
        ) AS A
WHERE DUPLICADO = 1
ORDER BY RFC
