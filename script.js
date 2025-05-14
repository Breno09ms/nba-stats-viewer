const select = document.getElementById("opcao-tipo"); 
const jogadorSection = document.getElementById("jogador-selection");
const timeSection = document.getElementById("time-selection");
const nomeJogador = document.getElementById("input-jogador").value;
const estatisticaSelecionadaJ = document.getElementById("select-estatistica-jogador").value;


jogadorSection.style.display = "none";
timeSection.style.display = "none";



select.addEventListener("change", function () {
    const valor = select.value;

    if (valor === "jogador") {
        jogadorSection.style.display = "block";
        timeSection.style.display = "none";
    } else if (valor === "time") {
        jogadorSection.style.display = "none";
        timeSection.style.display = "block";
    } else {
        jogadorSection.style.display = "none";
        timeSection.style.display = "none";
    }
});
const jogadorButton = jogadorSection.querySelector("button");

jogadorButton.addEventListener("click", () => {
    const nomeJogador = jogadorSection.querySelector("input").value;
    const estatisticaSelecionadaJ = jogadorSection.querySelectorAll("select")[0].value;
    const respostaDiv = document.getElementById("resposta-servidor");
    respostaDiv.innerHTML = "";

    console.log("Estatística selecionada:", estatisticaSelecionadaJ);

    if (estatisticaSelecionadaJ === "ppg_grafico") {
        // Chama o endpoint do gráfico
        fetch("http://127.0.0.1:5000/grafico", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nome: nomeJogador
            })
        })
        .then(response => response.json())
        .then(data => {

             console.log(data)

            if (data.imagem) {
                const img = document.createElement("img");
                img.src = "data:image/png;base64," + data.imagem;
                img.alt = "Gráfico gerado";
                img.style.maxWidth = "100%";
                respostaDiv.appendChild(img);
            } else {
                respostaDiv.textContent = "Erro: " + data.erro;
            }
        })
        .catch(error => {
            console.error("Erro ao buscar gráfico:", error);
        });
    } else {
        // Chama o endpoint de estatísticas normais
        fetch("http://127.0.0.1:5000/jogador", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nome: nomeJogador,
                estatistica: estatisticaSelecionadaJ
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.erro) {
                respostaDiv.textContent = "Erro: " + data.erro;
            } else if (data.mensagem) {
                respostaDiv.textContent = data.mensagem;
            } else {
                const tabela = document.createElement("table");
                for (const [time, valor] of Object.entries(data)) {
                    const linha = document.createElement("tr");

                    const colTime = document.createElement("td");
                    colTime.textContent = time;

                    const colValor = document.createElement("td");
                    colValor.textContent = valor.toFixed(2);

                    linha.appendChild(colTime);
                    linha.appendChild(colValor);
                    tabela.appendChild(linha);
                }
                respostaDiv.appendChild(tabela);
            }
        })
        .catch(error => {
            console.error("Erro ao buscar estatísticas:", error);
        });
    }
});

const timeButton = document.getElementById("botao-time");


timeButton.addEventListener("click", () => {
    const nomeTime = document.getElementById("select-time").value;
    const estatisticaTime = document.getElementById("select-estatistica-time").value;

    fetch("http://127.0.0.1:5000/time", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            time: nomeTime,
            estatistica: estatisticaTime
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Resposta do servidor:", data);

        const respostaDiv = document.getElementById("resposta-servidor");
        respostaDiv.innerHTML = "";

        if (data.erro) {
            respostaDiv.textContent = "Erro: " + data.erro;
        } else if (data.mensagem) {
            respostaDiv.textContent = data.mensagem;
        } else {
            const tabela = document.createElement("table");
            for (const [chave, valor] of Object.entries(data)) {
                const linha = document.createElement("tr");

                const colChave = document.createElement("td");
                colChave.textContent = chave;

                const colValor = document.createElement("td");
                colValor.textContent = typeof valor === "number" ? valor.toFixed(2) : valor;

                linha.appendChild(colChave);
                linha.appendChild(colValor);
                tabela.appendChild(linha);
            }
            respostaDiv.appendChild(tabela);
        }
    })
    .catch(error => console.error("Erro:", error));
});

