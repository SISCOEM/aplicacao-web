let table_itens = $("#actually_load");
let list_equipment;

// Define um intervalo para atualizar a lista de equipamentos e obter informações sobre a carga
setInterval(() => {
    fetchList();
    getInfoLoad();
}, 1000);

// Função para obter a lista de equipamentos carregados
function fetchList() {
    $.ajax({
        url: '/carga/lista_equipamentos_atual/get',
        type: 'POST',
        dataType: 'json',
        data: {
            user: user,
            pass: pass
        },
        success: function (data) {
            // Limpa a tabela antes de adicionar novas linhas
            table_itens.empty();
            list_equipment = data;
            // Itera sobre os dados recebidos e insere uma linha para cada equipamento na tabela
            $.each(data, function (key, line) {
                insertLine(line);
            });
        },
        error: function (error) {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        }
    });
}

// Função para obter informações sobre a carga
function getInfoLoad() {
    $.ajax({
        url: '/carga/info/get',
        type: 'POST',
        dataType: 'json',
        data: {
            user: user,
            pass: pass
        },
        success: function (data) {
            console.log(data);
            // Redireciona para a página de login se a matrícula for nula
            if (data.matricula == null) {
                window.location = "/police/login/";
            }
        },
        error: function (error) {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        }
    });
}

// Função para inserir uma linha na tabela de itens carregados
function insertLine(line) {
    var newRow = $("<tr>").append(
        $("<td></td>"),
        $("<td>").text(line.equipment.serial_number || "-"),
        $("<td>").text(line.model.model || "-"),
        $("<td>").text(line.campo || "-"),
        $("<td>").text(line.model.caliber || "-"),
        $("<td>").text(line.amount || "1"),
        $("<td>").text(line.registred === 'wearable' ? line.model.size : "-"),
        $("<td>").text(line.equipment.observation || "-"),
        $("<td></td>")
    );
    table_itens.append(newRow);

    updateRowNumbers();
}

// Função para atualizar os números das linhas na tabela de itens carregados
function updateRowNumbers() {
    var rows = table_itens.find("tr");
    rows.each(function (index) {
        $(this).find("td:first").text(index + 1);
    });
}

// Função para confirmar o carregamento da carga
function confirmCargo(self) {
    // Altera o estilo do botão para indicar que foi clicado
    self.style.backgroundColor = "#9999";
    self.style.color = "black";
    $.ajax({
        url: '/equipamento/allow_cargo',
        type: 'POST',
        data: {
            user: user,
            pass: pass
        },
        error: function (error) {
            console.log("Erro de requisição: " + error);
            // Exibe uma mensagem de erro de conexão com o sistema
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        }
    });
}
