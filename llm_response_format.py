from pydantic import BaseModel

class LLMResponseFormat(BaseModel):
    response: str
    answer_correct: bool