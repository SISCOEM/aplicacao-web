// Variáveis para armazenar dados sobre os equipamentos e a carga
var list_equipment = []; // Lista de equipamentos disponíveis para devolução
var square_equipment; // Equipamento atual em destaque
var list_returned_equipment = []; // Lista de equipamentos devolvidos
var id_cargo; // ID da carga atual
var done_svg = '<svg fill="green" height="24" viewBox="0 -960 960 960" width="24"><path d="M382-240 154-468l57-57 171 171 367-367 57 57-424 424Z"/></path></svg>'; // Ícone de confirmação de devolução
window.obs_seted = false; // Flag para indicar se a observação foi definida

// Define a data e hora atual no formato adequado
function set_date() {
    var dataAtual = new Date();
    var dia = dataAtual.getDate();
    var mes = dataAtual.getMonth() + 1;
    var ano = dataAtual.getFullYear();
    var diaFormatado = dia < 10 ? "0" + dia : dia;
    var mesFormatado = mes < 10 ? "0" + mes : mes;
    var time = dataAtual.getHours() + ":" + dataAtual.getMinutes();
    var data = diaFormatado + "/" + mesFormatado + "/" + ano;

    // Insere os valores nos elementos HTML correspondentes
    $("#date").text(data);
    $("#time").text(time);

    // Atualiza os botões da página
    $("#cancel_btn")
        .prop("disabled", false)
        .removeClass("btn_disabled")
        .addClass("btn_cancel");
}

// Define o ID da carga atual e adiciona inputs hidden ao formulário
function set_carga_id(id) {
    id_cargo = id;

    // Adiciona inputs hidden com os dados da carga ao formulário
    var inputHidden = $("<input>").attr({
        type: "hidden",
        name: "turn_type",
        value: "descarga",
    });
    $("#form-equipment").append(inputHidden);

    inputHidden = $("<input>").attr({
        type: "hidden",
        name: "load_id",
        value: id,
    });
    $("#form-equipment").append(inputHidden);

    // Altera o texto do botão de inserção
    $("#insert_btn").val("DEVOLVER");

    // Faz uma requisição para obter os equipamentos da carga atual
    $.ajax({
        url: "/carga/get/" + id_cargo + "/",
        type: "POST",
        dataType: "json",
        data: {
            user: user,
            pass: pass,
        },
        success: function (data_cargo) {
            // Para cada equipamento da carga, insere na lista e na tabela
            $.each(data_cargo.equipment_loads, function (cargo, equipment) {
                equipment["Equipment&model"]["observation"] = equipment['observation'];
                insertLine(equipment["Equipment&model"], false);
                list_equipment.push(equipment["Equipment&model"]);
            });
            $(document).ready(function () {
                // Verifica se há equipamentos devolvidos previamente
                $.ajax({
                    url: "/carga/lista_equipamentos_atual/get",
                    type: "POST",
                    dataType: "json",
                    data: {
                        user: user,
                        pass: pass,
                    },
                    success: function (data) {
                        // Para cada equipamento devolvido, atualiza a tabela
                        var table_itens = $("#body_table_itens");
                        var lines = table_itens.find("tr");

                        lines.each(function (j, line) {
                            var camps = $(line).find("td");
                            $.each(data, function (key, eq) {
                                let amount_input = eq.amount;

                                if (camps.eq(1).text() == "-") {
                                    var line_serial_number = camps.eq(4).text();
                                } else {
                                    var line_serial_number = camps.eq(1).text();
                                }

                                if (line_serial_number == key) {
                                    if (
                                        parseInt(camps.eq(5).text()) >
                                        amount_input
                                    ) {
                                        var ultimaLinha = $(line).clone(true);
                                        camps.eq(5).text(amount_input);

                                        ultimaLinha
                                            .find("td")
                                            .eq(5)
                                            .html(
                                                parseInt(
                                                    ultimaLinha
                                                        .find("td")
                                                        .eq(5)
                                                        .text()
                                                ) - amount_input
                                            );

                                        table_itens.append(ultimaLinha);
                                        updateRowNumbers(false);
                                    }

                                    list_returned_equipment.push(
                                        square_equipment
                                    );

                                    camps.eq(8).html(done_svg);
                                }

                            });
                        });
                    },
                    error: function (error) {
                        console.log("Erro de requisição: " + error);
                        popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
                    }
                });
            });
        },
        error: function (error) {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        }
    });
}

// Define os eventos de clique nos botões de pesquisa
$(document).ready(function () {
    $("#search-btn").on("click", search);

    $(".search-bullet").on("click", (e) => {
        fetchUnvalibleEquipmentData("bullet::" + e.target.value, "search");
    });
});

// Função de pesquisa de equipamentos
function search() {
    var search = $("#search-camp");
    fetchUnvalibleEquipmentData(search.val(), "search");
    search.val("");
}

// Cria um intervalo para atualizar os dados dos equipamentos indisponíveis
interval = setInterval(fetchUnvalibleEquipmentData, 1000);

// Função para fazer requisição dos dados de um equipamento indisponível
function fetchUnvalibleEquipmentData(serial_number, type = "none") {
    // Define a URL da requisição com base no número de série fornecido
    let url = "/equipamento/get_indisponivel/" + id_cargo + "/";

    if (!(serial_number == null || serial_number == undefined)) {
        url =
            "/equipamento/get_indisponivel/" +
            id_cargo +
            "/?type=equipment&pk=" +
            serial_number;
    }

    // Faz a requisição Ajax para obter os dados do equipamento
    $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data: {
            user: user,
            pass: pass,
        },
        success: function (data) {
            // Verifica se o equipamento é válido e trata conforme necessário
            if (data.uid !== "") {
                $.each(list_equipment, function (i, equipment) {
                    serial_number = equipment.equipment["serial_number"];
                    caliber = equipment.equipment["caliber"];

                    if (
                        serial_number != undefined &&
                        serial_number === data.equipment.serial_number
                    ) {
                        addToSquare(data);
                        square_equipment = data;
                        if (type != "search") {
                            check_cargo_square(type);
                        }
                        return false;
                    } else if (
                        caliber != undefined &&
                        caliber === data.equipment.caliber
                    ) {
                        addToSquare(data);
                        square_equipment = data;
                        if (type != "search") {
                            check_cargo_square(type);
                        }
                        return false;
                    }
                });
            } else if (data.confirmCargo) {
                $("#submit_btn")
                    .prop("disabled", false)
                    .removeClass("btn_disabled")
                    .addClass("btn_confirm");
            }
            if ("msm" in data) {
                popUp(data.msm, {timer: 2000, overlay: false});
            }
        },
        error: function (error) {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        }
    });
}

// Função para fazer requisição dos dados dos equipamento disponíveis passasdos
function fetchEquipmentData(serial_number, type = "none") {
    // Define a URL da requisição com base no número de série fornecido
    let url =
        serial_number == null || serial_number == undefined
            ? "/equipamento/get_disponivel"
            : "/equipamento/get/" + serial_number;

    // Faz a requisição Ajax para obter os dados do equipamento
    $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data: {
            user: user,
            pass: pass,
        },
        success: function (data) {
            // Verifica se o equipamento é válido e trata conforme necessário
            if (data.uid !== "") {
                if (
                    data.equipment.serial_number != null &&
                    data.equipment.serial_number != undefined
                ) {
                    let equipAlreadyInList = list_equipment.find(function (
                        equipment
                    ) {
                        return (
                            equipment.equipment.serial_number ==
                            data.equipment.serial_number
                        );
                    });

                    if (equipAlreadyInList) {
                        // popUp("Equipamento já na lista!", {timer: 2000, overlay: false});
                        return;
                    }
                }

                if (data.campo !== false) {
                    list_awate_equipment.push(data);
                    checkAwateList(type);
                }
            }
            if (data.msm != null) {
                popUp(data.msm, {timer: 2000, overlay: false});
            }
        },
        error: function (error) {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        }
    });
}

// Verifica se há equipamentos em espera e os adiciona à lista
function checkAwateList(type = "none") {
    if (list_awate_equipment.length > 0) {
        let equipmentData = list_awate_equipment.pop();
        addToSquare(equipmentData);
        if (type != "search") {
            check_cargo_square();
        }
        if (semaphore) {
            semaphore = false;
        }
    }
}

// Verifica se o equipamento está na lista de devolução e atualiza a tabela
function check_cargo_square() {
    var table_itens = $("#body_table_itens");
    var amount_input = $("#amount_input").val();
    var serialNumberInput = $("#serial_number").text();

    if (serialNumberInput == "-") {
        serialNumberValue = square_equipment["equipment"]["caliber"];
    } else {
        serialNumberValue = serialNumberInput;
    }

    var lines = table_itens.find("tr");

    lines.each(function (j, line) {
        var camps = $(line).find("td");
        var status = camps.eq(8).html();

        if (serialNumberInput == "-" && camps.eq(1).text() == "-") {
            var line_serial_number = camps.eq(4).text();
        } else {
            var line_serial_number = camps.eq(1).text();
        }

        if (line_serial_number == serialNumberValue && status !== done_svg) {
            if (parseInt(camps.eq(5).text()) > amount_input) {
                var ultimaLinha = $(line).clone(true);
                camps.eq(5).text(amount_input);

                ultimaLinha
                    .find("td")
                    .eq(5)
                    .html(
                        parseInt(ultimaLinha.find("td").eq(5).text()) -
                            amount_input
                    );

                table_itens.append(ultimaLinha);
                updateRowNumbers(false);
            }

            list_returned_equipment.push(square_equipment);

            camps.eq(8).html(done_svg);

            // Adiciona o equipamento devolvido à lista no servidor
            var serialNumber =
                square_equipment.equipment["serial_number"] ??
                "bullet::" + square_equipment.equipment["caliber"] ??
                "";

            // Faz a requisição Ajax para adicionar o equipamento devolvido
            $.ajax({
                url: "/carga/lista_equipamentos/add/",
                type: "POST",
                dataType: "json",
                data: {
                    serialNumber: serialNumber,
                    // observation: observation ?? "-",
                    observation: "-",
                    amount: amount_input,
                    user: user,
                    pass: pass,
                },
                success: function (data) {
                    clearSquare();
                    square_equipment = null;
                },
                error: function (error) {
                    console.log("Erro de requisição: " + error);
                    popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
                }
            });
            return false;
        }
    });
}

// Verifica se há equipamentos devolvidos para confirmar a carga
function confirmCargo() {
    if (list_returned_equipment.length > 0 || window.obs_seted)
        document.getElementById("form-equipment").submit();
    else popUp("Lista vazia!", {timer: 2000, overlay: false});
}
