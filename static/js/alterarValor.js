function alterarValor(botao, delta) {
    const input = botao.parentElement.querySelector('input[name="quantidade"]');
    let valorAtual = parseInt(input.value) || 0;
    let novoValor = valorAtual + delta;
    if (novoValor >= 0) {
      input.value = novoValor;
    }
  }