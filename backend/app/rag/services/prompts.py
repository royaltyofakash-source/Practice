SYSTEM_PROMPT = (
    "You are a helpful assistant. Answer the user's question based on the provided context. "
    "If the answer is in the context, provide a detailed response. "
    "If the information is not in the context, say 'I don't have enough information to answer this question.'\n\n"
    "Context:\n{context}"
)

def build_system_prompt(context: str) -> str:
    return SYSTEM_PROMPT.format(context=context)
