from typing import List


def montar_prompt(pergunta: str, chunks: List[str]) -> str:
    """
    Recebe a pergunta do usuário e os chunks recuperados
    e monta o prompt completo para enviar ao LLM.
    """

    contexto = "\n\n".join(chunks)

    prompt = f"""
Você é um assistente da NovaTech.

Regras:
- Responda apenas com base nas informações fornecidas no contexto.
- Não invente informações.
- Se a resposta não estiver presente no contexto, responda:
  "Não encontrei informação suficiente nos documentos fornecidos."
- Sempre que possível, indique de qual documento a informação foi obtida.

Contexto:
{contexto}

Pergunta:
{pergunta}

Resposta:
"""

    return prompt


if __name__ == "__main__":
    pergunta = "Qual o prazo de devolução?"

    chunks = [
        "O cliente pode solicitar a devolução de mercadorias em até 7 dias úteis após o recebimento.",
        "Cargas perigosas não são elegíveis para devolução pelo processo padrão."
    ]

    prompt = montar_prompt(pergunta, chunks)

    print(prompt)