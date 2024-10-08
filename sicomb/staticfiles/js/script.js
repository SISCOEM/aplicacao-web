
function verificarTamanhoTela() {
    var larguraTela = window.innerWidth;
    var elemento = document.querySelector('.text-nav');

    if (elemento !== null) {
        console.log(elemento.textContent);
        console.log(larguraTela);

        if (larguraTela <= 768) { // Por exemplo, remova o texto quando a largura for inferior a 768 pixels
            elemento.textContent = "SISCOEM";
        } else {
            elemento.textContent = "SISCOEM - Sistema de Controle de Equipamentos Militares"; // Restaura o texto se a largura for maior ou igual a 768 pixels
        }
    }
}

// Evento de redimensionamento da janela
window.addEventListener("resize", verificarTamanhoTela);

// Verificar o tamanho da tela ao carregar a página
verificarTamanhoTela();

