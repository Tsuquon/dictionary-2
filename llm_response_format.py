from pydantic import BaseModel

class LLMResponseFormat(BaseModel):
    response: str
    answer_correct: bool
    
    
class ConversationResponse(BaseModel):
    feedback_response: str
    next_response: str