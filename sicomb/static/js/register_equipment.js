// Função para registrar uma nova munição
function register_bullet() {
    // Realiza uma requisição AJAX para obter as informações das munições
    $.ajax({
        url: '/equipamento/bullets/get/',
        type: 'POST',
        dataType: 'json',
        data: {
            user: user,
            pass: pass
        },
        success: function (bullets) {
            var bullet_options = '';
            // Verifica se foram retornadas balas
            if (bullets) {
                // Itera sobre as balas retornadas para criar as opções do menu dropdown
                $.each(bullets, function (i, bullet) {
                    bullet_options += '\n<option value="' + bullet['id'] + '">' + bullet['description'] + '</option>';
                });
            }

            var csrf = $('input[type="hidden"][name="csrfmiddlewaretoken"]');
            var bullet_html =
                `
                <form method="post" action="." class="form-element" style="min-height:220px;min-whidth:300px;">
                    <div style="background-color: rgb(91,73,57, 0.9); whidth: 100%; border-radius: 20px; text-align:center; color: #fff; padding:5px;">
                        </div>
                            <h3 class="input-title">
                                CADASTRAR MUNIÇÃO
                            </h3>
                            <div class="input-div">
                            ` + csrf[0].outerHTML + `
                            <div class="input-box">
                                <h4 class="input-title">MUNIÇÕES</h4>
                                <div class="select">
                                    <select name="bullet" class="select-field" id="dropdown_bullets" required>
                ` +
                    bullet_options
                + `
                                    </select>
                                </div>
                            </div>
                            <div class="input-box">
                            <h4 class="input-title">QUANTIDADE</h4>
                                <input name="amount" class="input-data" type="number" id="input_amount" required>
                            </div>
                        <div class="finalize-registration" style="padding-bottom: 0px;">
                        <label><input type="submit" id="submit-btn" class="box-shadow-registration" value="Adicionar"></label>
                    </div>
                </form>
                `;

            // Exibe um pop-up com o formulário de cadastro de munição
            popUp("", { closeBtn: true, adicional: bullet_html });
        },
        error: function (error) {
            console.log("Erro de requisição: " + error);
            popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
        }
    });
}

// Função para lidar com a seleção de tipos e modelos
$(document).ready(function () {
    var choicesTypes = $("#type-choices");
    // Reseta o valor selecionado inicialmente
    choicesTypes.val(""); 

    // Função para obter e validar o UID
    function fetchUid() {
        $.ajax({
            url: '/equipamento/valid_uid',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                var input_uid = $("#input-uid");
                var text_uid = $("#text-uid");

                // Verifica se há uma mensagem a ser exibida
                if (data.msm != null) {
                    popUp(data.msm);
                }
                // Verifica se foi retornado um UID válido
                if (data.uid !== '') {
                    input_uid.val(data.uid);
                    text_uid.text("UID : " + data.uid);

                    clearInterval(interval);
                } else if (input_uid.val() !== '') {
                    text_uid.text("UID : " + input_uid.val());
                    clearInterval(interval);
                }
            },
            error: function (error) {
                console.log("Erro de requisição: " + error);
                // Exibe uma mensagem de erro de conexão com o sistema
                popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
            }
        });
    }

    // Define um intervalo para verificar o UID periodicamente
    var interval = setInterval(fetchUid, 1000);

    // Limpa o UID setado
    $("#clear-btn").on('click', function () {
        var input_uid = $("#input-uid");
        var text_uid = $("#text-uid");

        setInterval(fetchUid, 1000);

        input_uid.val('');
        text_uid.text("Passe a tag no sensor");
    });

    // Checa tudo antes de dar o submit
    $("#submit-btn").on('click', function () {
        console.log("Submit");
        var choices = $(".type-choices-type");
        var selectedIndex = 0;

        choices.each(function () {
            if ($(this).val() !== '') {
                selectedIndex++;
            }
        });

        var serial_num = $("#serial-number-input").val();

        // Verifica se o número de série foi inserido
        if (serial_num === '') {
            popUp("Por favor insira o número de série.");
            return;
        }

        // Verifica se o número de série já existe
        $.ajax({
            url: '/equipamento/valid_serial_number/' + serial_num + '/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                if (data.exists) {
                    popUp("Numero de série já cadastrado!");
                    return;
                }
            },
            error: function (error) {
                console.log("Erro de requisição: " + error);
                popUp("Conexão com o sistema perdida!", {timer: 2000, overlay: false});
            }
        });

        // Verifica se um UID foi passado
        if ($("#input-uid").val() === '') {
            popUp("Por favor passe uma tag no sensor.");
            return;
        }
        // Verifica se uma opção de modelo foi selecionada
        if (selectedIndex === 0) {
            popUp("Por favor selecione uma opção de modelo.");
            return;
        }
        // Submete o formulário se apenas uma opção de modelo foi selecionada
        if (selectedIndex === 1) {
            $("#form-equipment").submit();
        }
    });

    $("#register-bullet-btn").on('click', function () {
        register_bullet();
    });

    // Libera o campo certo com base no tipo selecionado
    function change_field() {
        var selectedValue = choicesTypes.val();
        var choiceModels = $("#type-choices-" + selectedValue);
        var choices = $(".type-choices-type");
        var labelClass = $("#lable-type-input");

        if (labelClass) labelClass.remove();

        choices.prop('disabled', true).hide().val('');

        if (selectedValue !== '') {
            choiceModels.show().prop('disabled', false);
        }
    }

    change_field();
    choicesTypes.on('change', change_field);
});
