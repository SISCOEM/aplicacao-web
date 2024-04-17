Este app é responsável pela gerencia das cargas e descargas, afinal a descarga nada mais é que uma carga com o tipo descarga. Seus campos principais são os campos de load_unload, que se refere à descarga da carga em questão, o turn_type que se refere ao tipo da carga como 8h, 6h, 12h... caso seja uma descarga ele é setado como "descarga", assim como seu status.

Temos também o model de Equipment_load que nada mais é que uma classe associatica em que vinculamos os equipamento à carga, formando uma relação de 1 carga pra muitas Equipment_load's

TODO: Uma sugestão de algo percebido após o desenvolvimento é da possibilidade de criar um arquivo chamado managers.py e mover o manager do models.py.

Seguindo o mesmo padrão do app equipment, neste app temos o arquivo apis.py responsável pelas rotas de api, que é como uma view mas com retorno do tipo JsonResponse. 
