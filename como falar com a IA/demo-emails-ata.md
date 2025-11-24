# DEMO — E-mails → Ata de reunião (como a LLM lê Markdown + XML)

Objetivo: demonstrar delimitadores, tags XML e um formato de saída fixo que produzem respostas assertivas e replicáveis.

---

## 1) Prompt Estruturado (cole acima dos e-mails quando for usar)
PAPEL: Analista de operações.
OBJETIVO: Gerar ATA de reunião com Sumário, Decisões, Ações (responsável, deadline, origem), Pendências, Riscos, Perguntas em aberto e Anexos.
REGRAS:
- Não inventar fora das tags.
- Datas em AAAA-MM-DD.
- Se faltar dado crítico, registrar em “Perguntas em aberto”.
- Em cada Ação, incluir origem no formato "YYYY-MM-DD | subject".
FORMATO DE SAÍDA (copiar literalmente na resposta):
## Sumário
- Contexto:
- Período dos e-mails: AAAA-MM-DD a AAAA-MM-DD
- Participantes citados (únicos):
- Principais tópicos (3–5 bullets):
## Decisões
- [D1] ...
## Ações
- [A1] título — responsável — deadline — origem("YYYY-MM-DD | subject")
## Pendências
- [P1] ...
## Riscos
- [R1] ...
## Perguntas em aberto
- [Q1] ...
## Anexos citados
- [F1] nome.ext — origem("YYYY-MM-DD | subject")

---

## 2) Entradas — E-mails (exemplo)
Cole seus e-mails entre os delimitadores abaixo.

<<<BEGIN_EMAILS

    <from>ana.lima@empresa.com</from>
    <to>projeto-pagamentos@empresa.com</to>
    <cc>financeiro@empresa.com</cc>
    <date>2025-11-20</date>
    <subject>Contrato PSP — versão final</subject>
Confirmamos a aprovação do PSP X. Precisamos atualizar o contrato até 01/12.
O jurídico pediu que a Ana Lima conduza a atualização. Em anexo: contrato_v12.pdf

    <from>marcos.silva@empresa.com</from>
    <to>projeto-pagamentos@empresa.com</to>
    <date>2025-11-21</date>
    <subject>Integração webhook — status</subject>
O endpoint /payments/webhook está em homologação. Se o PSP liberar hoje,
conseguimos ir para produção dia 28/11. Falta a chave de produção do PSP.

    <from>fernanda.rocha@empresa.com</from>
    <to>projeto-pagamentos@empresa.com</to>
    <date>2025-11-22</date>
    <subject>Prazo de go-live</subject>
Diretoria confirmou go-live em 2025-11-30. Sem a chave de produção,
o risco aumenta. Precisamos de responsável explícito por essa solicitação.
END_EMAILS>>>

---

## 3) Saída Esperada (exemplo de renderização pela LLM)
## Sumário
- Contexto: E-mails sobre “Lançamento Módulo Pagamentos”
- Período dos e-mails: 2025-11-20 a 2025-11-22
- Participantes citados (únicos): Ana Lima; Marcos Silva; Fernanda Rocha; Jurídico; Diretoria
- Principais tópicos:
  - Aprovação do PSP e atualização de contrato
  - Integração de webhook em homologação
  - Dependência da chave de produção do PSP
  - Go-live alvo em 2025-11-30

## Decisões
- [D1] Aprovação do PSP X confirmada (2025-11-20 | Contrato PSP — versão final)
- [D2] Go-live confirmado para 2025-11-30 (2025-11-22 | Prazo de go-live)

## Ações
- [A1] Atualizar contrato do PSP — Ana Lima — 2025-12-01 — origem("2025-11-20 | Contrato PSP — versão final")
- [A2] Solicitar chave de produção ao PSP — (responsável não informado) — (deadline não informado) — origem("2025-11-21 | Integração webhook — status")

## Pendências
- [P1] Definir responsável e prazo para solicitação da chave de produção

## Riscos
- [R1] Atraso do PSP na entrega da chave pode impactar o go-live de 2025-11-30

## Perguntas em aberto
- [Q1] Quem será o responsável por solicitar a chave de produção ao PSP?
- [Q2] O jurídico aprovou a versão final do contrato v12.pdf sem ressalvas?

## Anexos citados
- [F1] contrato_v12.pdf — origem("2025-11-20 | Contrato PSP — versão final")
