// Declaração das variáveis usadas para armazenar referências aos elementos HTML
var serialNumberInput = document.getElementById("serial_number");
var description = document.getElementById("description");
var type = document.getElementById("type");
var amount = document.getElementById("amount");
var insert_bttn = document.getElementById("insert_btn");
let amount_input = document.getElementById("amount_input");

// Array que armazena os equipamentos a serem cadastrados em formato de dicionário
var list_equipment = []; 

// Variáveis de controle
var semaphore = true; 
var square = false; 
var equipmentData = null; // Equipamento atual em formato global
// Seta a data e a hora atual
set_date();
// => }

// Busca se já existe uma lista no sistema
fetch("/carga/lista_equipamentos/get", {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
        'user': user,
        'pass': pass,
    })})
    .then(response => response.json())
    .then(data => {
        list_equipment = data;
        // Insere cada objeto novamente na tabela
        for (let key in list_equipment) {
            insertLine(list_equipment[key]);
        }
    })
    .catch(error => {
        console.log("Erro de requisição: " + error);
        popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
    });

// Função para requisitar dados do equipamento
function fetchEquipmentData(serial_number, type='none') {
    // Caso a função receba o parâmetro serial_number, ela requisita o equipamento correspondente.
    // Caso contrário, ela requisita o equipamento passado no sensor.
    let url = (serial_number == null || serial_number == undefined ?
        '/equipamento/get_disponivel' :
        '/equipamento/get/' + serial_number);

    // Faz a requisição para a URL especificada
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                'user': user,
                'pass': pass,
            })
        })
        .then(response => response.json())
        .then(data => {
            // Verifica se o equipamento já está na lista
            if (data.uid !== '' && semaphore) {
                if (data.equipment.serial_number != null && data.equipment.serial_number != undefined) {
                    for (let key in list_equipment) {
                        if (key == data.equipment.serial_number) {
                            return;
                        }
                    }
                }

                // Se o equipamento não estiver cadastrado, adiciona-o à lista de equipamentos em espera
                if (data.registred !== false) {
                    list_awate_equipment.push(data);
                    checkAwateList(type);
                }
            } else if (data.confirmCargo) {
                document.getElementById("submit_btn").disabled = false;
                document.getElementById("submit_btn").classList.remove("btn_disabled");
                document.getElementById("submit_btn").classList.add("btn_confirm");

                semaphore = false;
                clearInterval(interval);
            }

            // Exibe mensagem de erro, se houver
            if (data.msm != null) {
                popUp(data.msm);
            }
        })
        .catch(error => {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        });
}

// Cria um intervalo para chamar a função fetchEquipmentData a cada 1 segundo
var interval = setInterval(fetchEquipmentData, 1000);

// Insere um equipamento na lista de equipamentos
function check_cargo_square() {
    if (equipmentData != null) { // se tiver um equipamento no quadro
        equipmentData['amount'] = amount_input.value;
        
        let eq = equipmentData
        let serial_number = eq.equipment.serial_number ?? "bullet::" + eq.model.caliber;
        
        // Faz a requisição para adicionar o equipamento à lista no django
        fetch('/carga/lista_equipamentos/add/', {
            method: 'POST',
            headers: {
                'Content-Type': "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            'serialNumber': serial_number,
            'observation': "-",
            'amount': eq.amount,
            'user': user,
            'pass': pass
        }).toString()
        })
        .then(response => response.json())
        .then(data => {
            // Se houver erro, exibe a mensagem
            if(data.status == "error") {
                popUp(data.message);
                return;
            }

            // Adiciona o equipamento ao array de equipamentos
            list_equipment[eq.equipment.serial_number ?? 'ac' + eq.equipment.id] = {
                'serial_number': eq.equipment.serial_number,
                'observation': "-",
                'amount': amount_input.value,
                'model': {
                    'image_path': document.getElementById('means_room_product').src,
                }
            };

            // Insere a linha na tabela
            insertLine(eq);
        })
        .catch(error => {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        });

        // Reseta os equipamentos atuais e o quadro do equipamento
        equipmentData = null;
        clearSquare();
        clearInterval(interval);
        interval = setInterval(fetchEquipmentData, 1000);
        checkAwateList();
    }
}

// Requisita a remoção de um equipamento da lista
function checkRemoveRow(rowNumber) {
    var rows = table_itens.getElementsByTagName("tr");
    var col = rows[rowNumber].getElementsByTagName("td");

    obs = col[7].innerHTML;
    amount = col[5].innerHTML;

    // Verifica se o equipamento é munição
    if (col[3].innerHTML != 'Munição') {
        serialNum = col[1].innerHTML; // 1 É A POSIÇÃO DO NUMERO DE SÉRIE, ou seja ele pega o numero de série

        popUp("Tem certeza que deseja remover esse equipamento?", {yn: true, closeBtn: false, yesFunction: () => {
            // Faz a requisição para remover o equipamento
            fetch("/carga/lista_equipamentos/remover/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    'user': user,
                    'pass': pass,
                    'serial_number': serialNum,
                    'obs': obs
                })
            })
            .then(response => {
                removeRow(rowNumber);
            }).catch(error => {
                console.log("Erro de requisição: " + error);
                popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
            });
        }});
    } else {
        caliber = col[4].innerHTML;
        popUp("Tem certeza que deseja remover esse equipamento?", {yn: true, closeBtn: false, yesFunction: () => {
            fetch("/carga/lista_equipamentos/remover/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    'user': user,
                    'pass': pass,
                    'serial_number': caliber,
                    'obs': obs
                })
            })
            .then(response => {
                removeRow(rowNumber);
            })
            .catch(error => {
                console.log("Erro de requisição: " + error);
                popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
            });
        }});
    }
}

// Remove a linha da tabela
function removeRow(rowNumber) {
    var rows = table_itens.getElementsByTagName("tr");
    serialNum = rows[rowNumber].getElementsByTagName("td")[1].innerHTML;
    delete list_equipment[serialNum];

    table_itens.deleteRow(rowNumber);
    updateRowNumbers();
}

// Edita um equipamento mandando ele para o quadro
function edit(i) {
    var rows = table_itens.getElementsByTagName("tr");
    serialNum = rows[i].getElementsByTagName("td")[1].innerHTML;
    console.log(rows);
    addToSquare(list_equipment[serialNum]);
    removeRow(i);
}

// Verifica se a lista está vazia antes de confirmar a carga
function confirmCargo() {
    var rows = table_itens.getElementsByTagName("tr");
    if (rows.length > 0) document.getElementById("form-equipment").submit();
    else popUp("Lista vazia!");
}

// Verifica se há equipamentos em espera
function checkAwateList(type='none') {
    console.log(type);
    if (list_awate_equipment.length > 0) {
        equipmentData = list_awate_equipment[list_awate_equipment.length - 1];
        data = list_awate_equipment[list_awate_equipment.length - 1];
        list_awate_equipment.pop();
        addToSquare(data);
        
        // Verifica se é uma busca
        if (type != "search") {
            check_cargo_square();
        }
    }
}

// Busca a lista de espera
function searchWatingList() {
    fetch("/equipamento/lista_espera/get/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                'user': user,
                'pass': pass
            })
        })
        .then(response => response)
        .then(response => response.json())
        .then(data => {
            let wating_list = "";
            for (i in data) {
                wating_list += "<tr>" + data[i] + "</tr>";
            }
            document.getElementById("wating_list").innerHTML = wating_list;
        })
        .catch(error => {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        });
}
searchWatingList();
// var intervalWatingList = setInterval(searchWatingList, 1000);