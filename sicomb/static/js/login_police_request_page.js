// Objeto para armazenar informações relacionadas ao registro de impressões digitais
var reg_fingerprints_assets = {};

// Função para obter a impressão digital passada
function fetchFingerprint() {
    $.ajax({
        url: '/police/get_fingerprint/',
        type: 'POST',
        dataType: 'json',
        data: {
            user: user,
            pass: pass
        },
        success: function(data) {
            if (data.status) {
                // Define os valores dos campos de formulário e envia o formulário de login
                $('input[name="type_login"]').val("fingerprint");
                $('input[name="token"]').val(data.token);
                $('#form_login').submit();
            } else if (data.type) {
                // Se houver um tipo de mensagem específico
                if (data.type == "USERMESSAGE" || data.type == "ERROR" || data.type == "SUCCESS") {
                    // Verifica se há uma popup existente e a fecha
                    if (reg_fingerprints_assets["popUp"]) {
                        reg_fingerprints_assets["popUp"]["close_function"]()
                    }
                    // Exibe uma popup com base no tipo de mensagem recebida
                    if (data.type == "SUCCESS") {
                        reg_fingerprints_assets["popUp"] = popUp(data.message, { timer: 2000 });
                    } else if (data.type == "ERROR") {
                        reg_fingerprints_assets["popUp"] = popUp(data.message);
                    } else {
                        reg_fingerprints_assets["popUp"] = popUp(data.message, { closeBtn: false });
                    }
                } else {
                    // Exibe uma mensagem de popup padrão se não houver um tipo específico
                    if (data.message)
                        popUp(data.message, { timer: 2000, overlay: false });
                }
            }
        },
        error: function (error) {
            console.log("Erro de requisição: " + error);
            // Exibe uma mensagem de erro de conexão com o sistema
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        }
    });
}

// Define um intervalo para obter a lista de impressões digitais
var interval = setInterval(fetchFingerprint, 1000);

$(document).ready(function() {
    // Evento de clique para solicitar uma nova impressão digital
    $("#request_fingerprint").on("click", function () {
        $.ajax({
            url: '/police/request/fingerprint/',
            type: 'POST',
            dataType: 'json',
            data: {
                user: user,
                pass: pass
            },
            success: function(data) {
                // Exibe uma mensagem de popup indicando que a impressão digital está sendo requisitada
                popUp("Requisitando impressão digital...", { overlay: false, timer: 2000 })
            },
            error: function (error) {
                console.log("Erro de requisição: " + error);
                // Exibe uma mensagem de erro de conexão com o sistema
                popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
            }
        });
    });
}); 
