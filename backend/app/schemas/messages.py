from pydantic import BaseModel

# Esta clase representa la respuesta de un mensaje que se envía desde el servidor al cliente.
class MessageResponse(BaseModel):
    id: int
    role: str
    content: str

    class Config:
        from_attributes = True