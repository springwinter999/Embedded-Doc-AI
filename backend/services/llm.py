import httpx
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, CHAT_MODEL


def build_prompt(question: str, context: list[dict]) -> list[dict]:
    """Build the message list for RAG: system prompt with context + user question."""
    if context:
        context_text = "\n\n---\n\n".join([
            f"[来源: {c['metadata'].get('filename', '')} 第{c['metadata'].get('page', '?')}页]\n{c['text']}"
            for c in context
        ])
        system_content = (
            "你是一个嵌入式开发助手，专门回答关于STM32单片机 HAL库和寄存器配置的问题。\n"
            "请严格基于以下文档片段回答用户问题。如果文档中没有相关信息，请明确说明。\n"
            "回答时应包含：代码示例（如果有）、相关寄存器/函数说明、以及来源章节标注。\n\n"
            "### 参考文档片段 ###\n"
            f"{context_text}"
        )
    else:
        system_content = (
            "你是一个嵌入式开发助手。注意：当前知识库中没有找到与问题相关的文档片段，"
            "请告知用户这一情况，并建议检查文档是否已索引。"
        )

    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": question},
    ]


def ask(messages: list[dict]) -> str:
    """Send messages to DeepSeek Chat and return the response text."""
    with httpx.Client(timeout=120) as client:
        response = client.post(
            f"{DEEPSEEK_BASE_URL}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": CHAT_MODEL,
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 2048,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
