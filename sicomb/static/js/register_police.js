// Função para realizar a busca por matrícula
function search() {
    var matriculaInput = document.querySelector('#matricula-input');
    var matricula = matriculaInput.value;
    if (matricula != '') {
        // Redireciona para a página de busca com a matrícula fornecida
        window.location.href = '/police/search/' + matricula + '/';
    } else {
        var messageText = "Insira uma matrícula";
        popUp(messageText, {timer: 2000, overlay: false});
    }
}

$(document).ready(function() {
    $("#delete-digital").on("click", function () {
        // Exibe um pop-up de confirmação para deletar a digital
        popUp("Tem certeza que deseja deletar a digital de " + $("input[name='police_name']").val() + "?", {
            yn: true,
            yesFunction: function () {
                // Realiza uma requisição AJAX para deletar a digital
                $.ajax({
                    url: "/police/fingerprint/delete/" + $("input[name='police_id']").val(),
                    type: "POST",
                    dataType: "json",
                    data: {
                        user: user,
                        pass: pass,
                    },
                    success: function (data) {
                        if(data.status) {
                            // Exibe uma mensagem de sucesso e redireciona após 1 segundo
                            popUp("Deletado com sucesso!", {closeBtn: false});
                            setTimeout(function () {
                                window.location="/police/filter/";
                            }, 1000);
                        } else {
                            // Exibe a mensagem de erro retornada pelo servidor
                            popUp(data.message, {timer: 2000, overlay: false});
                        }
                    },
                    error: function (error) {
                        console.log("Erro de requisição: " + error);
                        popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
                    }
                });
            }
        });
    });

    // Evento de registrar a digital
    $(document).ready(function () {
        $("#register-fingerprint").on("click", function (e) {
            // Realiza uma requisição AJAX para requisitar o registro de uma nova digital
            $.ajax({
                url: "/police/register/fingerprint/" + $("input[name='police_id']").val() + "/",
                type: "POST",
                dataType: "json",
                data: {
                    user: user,
                    pass: pass,
                },
                success: function (data) {
                    // Exibe a mensagem retornada pela requisição
                    popUp(data['message']);
                },
                error: function (error) {
                    console.log("Erro de requisição: " + error);
                    popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
                }
            });
        });
    });
});
