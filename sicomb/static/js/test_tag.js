// Array para armazenar os dados das tags
let tags = [];

// Intervalo para chamar a função fetchTagData a cada 2 segundos
let interval = setInterval(fetchTagData, 2000);

// Função para limpar os dados das tags
function clearData() {
    tags = [];
    refreshTable();
}

// Função para fazer a requisição dos dados das tags
function fetchTagData() {
    // URL da rota de teste de tag
    let url = '/equipamento/tag/api/test/';

    // Faz a requisição para a rota de teste de tag para recuperar a lista de tags passadas
    fetch(url, {
            method: 'POST', // Método HTTP POST para enviar dados
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
            let uid = data.uid;
            // Verifica se a UID é uma string não vazia
            if (typeof uid === 'string' && uid.trim() !== '') {
                let is_in = false;
                // Define um valor padrão para 'read' caso não esteja presente nos dados
                data['read'] = data['read'] ?? 1;

                // Verifica se a tag já está na lista
                tags.forEach((tag) => {
                    if (uid == tag.uid) {
                        tag.read += 1; // Incrementa o contador de leituras
                        refreshTable(); // Atualiza a tabela
                        is_in = true;
                    }
                    return;
                });
                // Se a tag não estiver na lista, adiciona-a
                if (!is_in) {
                    tags.push(data);
                    refreshTable(); // Atualiza a tabela
                }
            }
        })
        .catch(error => {
            console.log("Erro de requisição: " + error);
            // Exibe uma mensagem de erro caso ocorra um erro na requisição
            popUp("Conexão com o sistema perdida!", {
                timer: 2000,
                overlay: false
            });
        });
}

// Função para atualizar a tabela HTML com os dados das tags
function refreshTable() {
    let body_table = '';

    // Verifica se há tags na lista
    if(tags.length > 0) {
        tags.forEach((tag) => {
            console.log(tag);
            // Monta as linhas da tabela com os dados das tags
            body_table += `<tr><td>${tag.equipment?.serial_number ?? '-'}</td>
            <td>${tag.equipment?.status ?? '-'}</td>
            <td>${tag.type ?? '-'}</td>
            <td>${tag.model?.model ?? '-'}</td>
            <td>${tag.equipment?.activated ?? '-'}</td>
            <td>${tag.uid ?? '-'}</td>
            <td>${tag.equipment?.activator ?? '-'}</td>
            <td>${tag.read ?? '-'}</td></tr>`;
        });
    } else {
        // Se não houver tags, exibe uma mensagem na tabela
        body_table = `<tr><td colspan="100%">Nenhuma tag passada</td></tr>`;
    }

    // Atualiza o corpo da tabela com as novas linhas
    $('#body_table').html(body_table);
}
