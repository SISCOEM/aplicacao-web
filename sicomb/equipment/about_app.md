Este app é responsável pela gerencia dos models do equimapento e dos modelos de equimapento. Um equipamento é formado por um numero de série, uma tag e um modelo, o modelo é formado por uma imagem, o nome do modelo e informações adicionais de acordo com o tipo de modelo. Existem 3 tipos de modelo, o armamento, o vestimento e o acessório, além desses, existe também a munição que é um tipo a parte.

Na estrutura do app temos um arquivo chamado por apis.py, nele estão os métodos responsáveis pelas respostas chamadas do javascript que age como uma view mas com respostas em JSON (pesquisar sobre apis rest).

As mesmas são feitas com um sistema de segurança onde é passado alguns dados para o js que serve como "chave" (esse é um sistema précário e deve ser trocado por um sistema de geração de tokens que possam expirar, pesquisar sobre access token e refresh token). Esse sistema é verificado através de um decorador de função nomeado por require_user_pass, nesse método é feito a validação manual do token passado, lembrando que a requisição deve conter os campos das chaves.



return das rotas da api em equipment:

equipamento/bullets/get/ POST 
{
	"0": {
		"id": 5,
		"activator": 3,
		"activated": 1,
		"amount": 1150,
		"image_path": "/media/Modelos/municoes/45acp.png",
		"caliber": ".45 ACP",
		"description": "Munição ACP"
	},
	"1": {
		"id": 6,
		"activator": 3,
		"activated": 1,
		"amount": 0,
		"image_path": "/media/Modelos/municoes/municao-9mm.jpg",
		"caliber": "9mm",
		"description": "Munição 9mm"
	}
}

equipamento/get/<str:serial_number> POST
{
	"equipment": {
		"date_register": "2024-01-19T14:38:44.380Z",
		"activator": 3,
		"activated": 1,
		"serial_number": "SVH58737",
		"uid": "3000E280699500004003762771ACC343",
		"status": "12H",
		"model_type": 22,
		"model_id": 6
	},
	"registred": "armament",
	"model": {
		"id": 6,
		"activator": 3,
		"activated": 1,
		"model": "TAURUS PT100",
		"caliber": ".40 S&W",
		"description": "Pistola - TAURUS PT100",
		"image_path": "/media/Modelos/armamentos/TaurusPT100.png"
	}
}

equipamento/get_disponivel POST
{
	"uid": "456",
	"confirmCargo": false,
	"equipment": {
		"date_register": "2024-01-17T03:58:05.764Z",
		"activator": 3,
		"activated": 1,
		"serial_number": "45656485",
		"uid": "456",
		"status": "Disponível",
		"model_type": 21,
		"model_id": 3
	},
	"registred": "accessory",
	"model": {
		"id": 3,
		"activator": 3,
		"activated": 1,
		"model": "Bastão",
		"description": "Bastão",
		"image_path": "/media/Modelos/acessorios/bastao.jpg"
	}
}


equipamento/get_indisponivel/112/ POST
{
	"uid": "3000E280699500004003762771ACC343",
	"confirmCargo": false,
	"equipment": {
		"date_register": "2024-01-19T14:38:44.380Z",
		"activator": 3,
		"activated": 1,
		"serial_number": "SVH58737",
		"uid": "3000E280699500004003762771ACC343",
		"status": "12H",
		"model_type": 22,
		"model_id": 6
	},
	"registred": "armament",
	"model": {
		"id": 6,
		"activator": 3,
		"activated": 1,
		"model": "TAURUS PT100",
		"caliber": ".40 S&W",
		"description": "Pistola - TAURUS PT100",
		"image_path": "/media/Modelos/armamentos/TaurusPT100.png"
	}
}