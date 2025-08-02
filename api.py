from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from database import registrar, historico, deletar


app = FastAPI()

class agendas(BaseModel):
    local: str
    data_hora: str
    descricao: str

@app.post("/agendamentos/", status_code=status.HTTP_201_CREATED)
async def criar_agendamento(agenda: agendas):
    registrar(reg_local=agenda.local,
              reg_horario=agenda.data_hora,
              reg_descricao=agenda.descricao)
    return {"status": "agendamento concluido com sucesso", "registros": agenda}

@app.get("/historico")
async def listar_agendamentos():
    dados = historico()
    return {"agendamentos": dados}

@app.get("/apagar/{id_agendamento}")
async def apagar_agendamento(id_agendamento: int):
    deletar(id_agendamento)
    return {"status": f"comando para apagar o id {id_agendamento} foi executado"}

