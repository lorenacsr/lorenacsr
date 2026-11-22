# Regras legais e limites da demonstração

Consulta às fontes em 22/11/2026. O contrato municipal não foi analisado.

| Referência | Consequência para o modelo |
| --- | --- |
| Lei 14.133/2021, art. 92, II, III e VII | Cadastrar regime, instrumento e cláusula que definem prazo e entrega. A lei não estabelece 15 dias como prazo geral. |
| Art. 183, caput, I e III e § 2º | Distinguir dias corridos e dias de expediente; excluir início e incluir vencimento; considerar hipóteses de prorrogação do vencimento. O dispositivo trata dos prazos previstos na lei: sua aplicação à cláusula deve ser conferida no instrumento e nas normas aplicáveis. |
| Art. 117 | Registrar ocorrências para apoiar a fiscalização. |
| Art. 140 | Distinguir entrega física de recebimento e aceitação. |
| Art. 162 | Atraso observado não gera multa automática: avaliar justificativa e previsão contratual. |
| Arts. 190 e 191 | Conferir regime dos contratos anteriores e da transição. |

Fonte: [Lei no Planalto](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm).
Complemento: [Cláusulas contratuais — TCU](https://licitacoesecontratos.tcu.gov.br/5-11-1-clausulas/).

## Hipóteses de implementação, não conclusões sobre o município

Lorena informou prazo contratual de 15 dias e marco de envio da AF. Continua pendente conferir se o instrumento exige envio ou recebimento da AF e se especifica dias úteis ou corridos. Essas informações não são substituídas por uma suposição sobre a lei.

A amostra usa **cláusulas fictícias expressas** de 15 dias corridos, exclui o dia do envio e desloca vencimento sem expediente para o próximo dia com expediente. O calendário é didático: fins de semana e um fechamento fictício. Ele não representa o calendário de Tapiratiba. A função também aceita dias úteis. Interrupções, suspensão, alterações de prazo, encerramento antecipado de expediente, indisponibilidade eletrônica e outros eventos exigem registro documental e ajuste validado; não são inferidos pelo algoritmo.

`regra_validada=0` ou tipo de dias não definido gera data limite nula e situação `regra_pendente`. No conjunto sintético `regra_validada=1` significa apenas que a **regra fictícia** está definida para a demonstração. Não significa validação jurídica de contrato real.

Atraso é medido em dias corridos depois do vencimento calculado, mesmo se o prazo de execução for em dias úteis. Entregas são consideradas quantitativamente aceitas **apenas na simulação**. Não há cálculo de sanção, juízo de culpa ou declaração de infração. Para aplicação real são necessários instrumento, comprovação da comunicação, calendário oficial, ocorrências e análise do responsável.
