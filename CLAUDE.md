# aem-modbus-simulator

Arquivo de instruções deste repositório para o assistente.

## Paralelismo com subagentes é o padrão, não a exceção

**Regra geral, válida para toda sessão e toda tarefa:** antes de começar
qualquer tarefa, avalie explicitamente como executá-la da forma mais eficiente —
e a primeira pergunta dessa avaliação é sempre "dá para paralelizar isto com
subagentes?". É passo de planejamento, feito antes da primeira ferramenta rodar,
não otimização a posteriori.

Sempre que o trabalho puder ser dividido em frentes independentes, dispare
subagentes em paralelo (várias chamadas da ferramenta Agent na MESMA mensagem)
em vez de fazer tudo em série na sessão principal. Em mensagens separadas elas
viram série de novo.

Vale para varredura ampla (mais de ~3 buscas vai para um agente `Explore`),
coleta por site/marca/domínio, e frentes independentes da mesma tarefa. Use
`run_in_background: true` para não travar a sessão.

**Não paralelize** passos com dependência real entre si, nem escrita concorrente
no mesmo arquivo ou na mesma branch (dois agentes editando o mesmo `.md` se
sobrescrevem — divida por arquivo, ou deixe a escrita para a sessão principal).

Cada agente precisa receber no prompt o contexto que não tem como descobrir
sozinho, o entregável esperado e se pode escrever (padrão: investigação é
somente leitura). O relatório do subagente não é mostrado ao usuário — a sessão
principal relata o que importa.

### Custo×benefício: qual modelo usar em cada agente

Ao disparar um subagente, escolha o `model` (parâmetro da ferramenta Agent) pela
complexidade real da tarefa, não por hábito. Faixa aceita nesta conta: piso
**Sonnet 5**, teto **Fable 5** — nunca Haiku para tarefa que envolva julgamento.

- **Tarefa mecânica/repetitiva** (editar o mesmo arquivo em N repos, aplicar um
  patch padronizado, rodar o mesmo comando N vezes): **Sonnet 5**. É
  leitura+escrita direta, sem julgamento editorial — pagar mais não muda o
  resultado.
- **Tarefa que exige julgamento** (decidir vencedor de par duplicado por
  evidência, escrever ou revisar conteúdo, sintetizar uma recomendação a partir
  de dados ambíguos): **Opus 5** ou **Fable 5**, conforme a profundidade exigida.
- Na dúvida, comece em Sonnet 5 e só suba de nível se o resultado voltar raso ou
  errado — não o contrário. Subir de nível "por garantia" em tarefa mecânica é
  custo sem ganho.
