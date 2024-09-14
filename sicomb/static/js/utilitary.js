// Array para armazenar mensagens exibidas em pop-ups
var messages = [];

// Função para resetar o sensor RFID fazendo uma requisição Ajax
var reset_rfid = function() {
    console.log("Resetando sensor RFID");
    $.ajax({
        url: "/carga/api/reset_rfid/",
        type: "POST",
        dataType: "json",
        data: {
            user: user,
            pass: pass,
        },
        success: function () {
            // Exibe uma mensagem de sucesso ao resetar a conexão
            popUp("Conexão resetada!", {timer: 2000, overlay: false});
        }
    });
};

// Função para exibir pop-ups com mensagens
var popUp = function (message, options = {}) {
    // Verifica se a mensagem já foi exibida anteriormente
    if (messages.includes(message)) {
        console.log(message + ' já exibida.');
        return;
    } else {
        // Adiciona a mensagem ao array de mensagens exibidas
        messages.push(message);
        console.log('Exibindo mensagem: ' + message);
    }

    // Configurações padrão para o pop-up
    const defaultOptions = {
        closeBtn: true,
        yn: false,
        adicional: "",
        timer: null,
        yesFunction: () => {},
        noFunction: () => {},
        overlay: true,
        textArea: false,
        contentTextarea: "",
    };

    // Mescla as opções padrão com as opções fornecidas
    const settings = { ...defaultOptions, ...options };

    // Cria elementos HTML para o pop-up
    const overlay = $("<a id='overlay'></a>");
    if (settings.overlay) {
        overlay.addClass("popup-overlay");
    }

    const popUpElement = $("<div></div>");
    popUpElement.css("opacity", "0");
    popUpElement.addClass("popup");

    // Adiciona um botão de fechar ao pop-up, se necessário
    if (settings.closeBtn) {
        const closeButton = $("<button>x</button>");
        closeButton.addClass("close-button");
        closeButton.on("click", () => {
            // Remove o pop-up e a mensagem do array de mensagens
            if (settings.overlay) {
                overlay.remove();
                messages = messages.filter(item => item !== message);
            }
            else {
                popUpElement.css("opacity", "0");
                setTimeout(() => {
                    messages = messages.filter(item => item !== message);
                    popUpElement.remove();
                }, 300); // Ajuste conforme necessário
            }
        });
        popUpElement.append(closeButton);
    }

    // Adiciona a mensagem ao pop-up
    const messageElement = $("<p></p>");
    messageElement.text(message);
    popUpElement.append(messageElement);

    // Adiciona conteúdo adicional, se fornecido
    if (settings.adicional) {
        popUpElement.append($(settings.adicional));
    }

    // Adiciona botões de sim e não, se necessário
    if (settings.yn) {
        // Botão SIM
        const yesButton = $("<button>SIM</button>");
        yesButton.addClass("popup-button green");
        yesButton.on("click", () => {
            // Executa a função SIM e remove o pop-up
            if (settings.overlay) {
                overlay.remove();
                messages = messages.filter(item => item !== message);
            }
            else {
                popUpElement.css("opacity", "0");
                setTimeout(() => {
                    popUpElement.remove();
                    messages = messages.filter(item => item !== message);
                }, 300);
            }
            settings.yesFunction();
        });

        // Botão NÃO
        const noButton = $("<button>NÃO</button>");
        noButton.addClass("popup-button red");
        noButton.on("click", () => {
            // Executa a função NÃO e remove o pop-up
            if (settings.overlay) {
                overlay.remove();
                messages = messages.filter(item => item !== message);
            }
            else {
                popUpElement.css("opacity", "0");
                setTimeout(() => {
                    popUpElement.remove();
                    messages = messages.filter(item => item !== message);
                }, 300); // Ajuste conforme necessário
            }
            settings.noFunction();
        });

        // Adiciona os botões ao pop-up
        popUpElement.append(yesButton);
        popUpElement.append(noButton);
    }

    // Adiciona o pop-up à página
    if (settings.overlay) {
        overlay.append(popUpElement);
        $("body").append(overlay);
    } else $("#messages").append(popUpElement);

    // Exibe gradualmente o pop-up
    setTimeout(() => {
        if (settings.overlay) {
            overlay.css("opacity", "1");
            popUpElement.css("opacity", "1");
        } else popUpElement.css("opacity", "1");
    }, 10);

    // Adiciona um campo de texto, se necessário
    if (settings.textArea) {
        const textArea = $("<textarea>" + settings.contentTextarea + "</textarea>");
        textArea.attr("rows", 10);
        textArea.attr("cols", 60);

        // Estilo para o campo de texto
        textArea.css("border", "solid 1px #685949");
        textArea.css("border-radius", "5px");
        textArea.css("background-color", "#efe5da");
        textArea.css("margin-top", "10px");
        textArea.css("padding", "10px");

        // Botão de confirmação para o campo de texto
        const button = $("<button>CONFIRMAR</button>");
        button.addClass("popup-button");
        button.css("background-color", "#685949");
        button.css("color", "#fff");
        button.on("click", () => {
            // Executa a função associada ao botão de confirmação e remove o pop-up
            if (settings.overlay) {
                overlay.remove();
                messages = messages.filter(item => item !== message);
            }
            else {
                popUpElement.css("opacity", "0");
                setTimeout(() => {
                    popUpElement.remove();
                    messages = messages.filter(item => item !== message);
                }, 300); 
            }
            settings.function_textarea(settings.parm1, settings.parm2, textArea.val());
        });

        // Adiciona o campo de texto e o botão ao pop-up
        popUpElement.append(textArea);
        popUpElement.append(button);
        popUpElement.css("display", "grid");
    }

    // Configura um temporizador para fechar o pop-up, se necessário
    if (settings.timer) {
        setTimeout(() => {
            if (settings.overlay) {
                overlay.remove();
                messages = messages.filter(item => item !== message);
            }
            else {
                popUpElement.css("opacity", "0");
                setTimeout(() => {
                    popUpElement.remove();
                    messages = messages.filter(item => item !== message);
                }, 300); 
            }
        }, settings.timer);
    }

    // Exibe gradualmente o pop-up
    setTimeout(() => {
        popUpElement.css("opacity", "1").addClass('show');
    }, 10);

    // Retorna um objeto contendo o overlay, a função de fechar o pop-up e a mensagem exibida
    return {"overlay": overlay, "close_function": () => {
        if (settings.overlay) {
            overlay.remove();
        }
        else $("#messages").find(popUpElement).remove();
        messages = messages.filter(item => item !== message);
    }, "message": message};
}

// Função para lidar com a seleção de arquivos
function handleFileSelection(event) {
    const fileInput = event.target;
    const fileSelectedMessage = document.querySelector("#fileSelectedMessage");
    console.log(fileSelectedMessage);
    if (fileInput.files && fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        fileSelectedMessage.textContent = `Arquivo: ${fileName}`;
    } else {
        fileSelectedMessage.textContent = "Nenhum arquivo selecionado";
    }
}

// Evento que é acionado quando o documento HTML está carregado
$(document).ready(function () {
    console.log($(".input-image"));
    // Evento acionado quando o input de imagem é alterado
    $(".input-image").on("change" ,function() {
        console.log("running");
        // Verifique se um arquivo foi selecionado
        if (this.files.length > 0) {
            // Adicione a classe .file-selected para destacar a borda
            $(".file-label").addClass("file-selected");
            // Exiba o nome do arquivo na div .file-name
            $(".file-label").text("ARQUIVO: " + this.files[0].name);
        } else {
            // Caso contrário, remova a classe .file-selected e limpe o nome do arquivo
            $(".file-label").removeClass("file-selected");
            $(".file-label").text("UPLOAD DE ARQUIVO +");
        }
    });
});
