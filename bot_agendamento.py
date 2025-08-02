import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import requests
from cliente import criar_dados, historicos, apagar
from api import criar_agendamento, listar_agendamentos, apagar_agendamento
LOCAL, DATA_HORA, DESCRICAO = range(3)

load_dotenv()
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("ERRO, token não encontrado")

async def pegar_local(update: Update, context:ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text("qual local: ")
    return LOCAL

async def local(update: Update, context:ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data['local'] = update.message.text
    await update.message.reply_text(f"local: {context.user_data['local']}\nagora digite a data e hora")
    return DATA_HORA

async def data_hora(update: Update, context:ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['data_hora'] = update.message.text
    await update.message.reply_text(f"data-hora: {context.user_data['data_hora']}\nagora digite uma breve descrição do compromisso")
    return DESCRICAO

async def salvar(update: Update, context:ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data['descricao'] = update.message.text

    dados_agenda = context.user_data
    
    await update.message.reply_text("agendado com sucesso\n" \
    f"local: {dados_agenda['local']}\n"
    f"data-hora: {dados_agenda['data_hora']}\n"
    f"descricao: {dados_agenda['descricao']}")

    resultado_api = criar_dados(
        local=dados_agenda['local'],
        data_hora=dados_agenda['data_hora'],
        descricao=dados_agenda['descricao']
    )
    
async def comando_historico(update: Update, context:ContextTypes.DEFAULT_TYPE):
    historico = historicos()
    
    if historico is None:
        await update.message.reply_text(
            "Desculpe, não consegui acessar o serviço de agendamentos no momento. "
            "A API pode estar desligada ou com problemas.")
        return
    
    if 'agendamentos' not in historico or not historico['agendamentos']:
        await update.message.reply_text("Não há agendamentos para mostrar.")
        return

    mensagem = "Histórico de Agendamentos:\n\n"
    
    for agendamento in historico['agendamentos']:
        # O agendamento é uma lista, por isso acessamos os itens pelo índice [0], [1], etc.
        # Adicionei a verificação para garantir que o item é uma lista com o tamanho correto
        if isinstance(agendamento, list) and len(agendamento) >= 4:
            # Índice 0 = ID
            # Índice 1 = Local
            # Índice 2 = Data e Hora
            # Índice 3 = Descrição
            mensagem += f"ID: {agendamento[0]}\n"
            mensagem += f"Local: {agendamento[1]}\n"
            mensagem += f"Data e Hora: {agendamento[2]}\n"
            mensagem += f"Descrição: {agendamento[3]}\n"
            mensagem += "----------------\n"
        else:
            # Se o item não for uma lista válida, avisa o usuário.
            mensagem += f"Item com formato inválido: {agendamento}\n"
            mensagem += "----------------\n"
    
    await update.message.reply_text(mensagem)


async def delete(update: Update, context:ContextTypes.DEFAULT_TYPE):
    try:
        #pega o primeiro argumento depois do comando
        id_str = context.args[0]
        id_int = int(id_str)

        apagar(id_int)
        
        await update.message.reply_text(f"agendamento com o id {id_int} foi apagado com sucesso")
    except IndexError:
        await update.message.reply_text("uso correto: /apagar <id>")
    except ValueError:
        await update.message.reply_text("id invalido, digite um numero")
    except Exception as e:
        await update.message.reply_text(f"erro ao apagar {e}")

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela a operação."""
    context.user_data.clear()
    await update.message.reply_text("Operação cancelada. Digite /start para começar de novo.")
    return ConversationHandler.END



def main():
    print("criando aplicação[+]...")
    application = Application.builder().token(TOKEN).build()
    print("aplicação rodando[+]...")

    conv_hundler = ConversationHandler(
        entry_points=[CommandHandler("start", pegar_local)],
        states={
            LOCAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, local)],
            DATA_HORA: [MessageHandler(filters.TEXT & ~filters.COMMAND,data_hora)],
            DESCRICAO: [MessageHandler(filters.TEXT & ~filters.COMMAND,salvar)]
            },
        fallbacks=[CommandHandler("cancelar", cancelar)]
    )

    application.add_handler(conv_hundler)

    hist = CommandHandler("historico", comando_historico)
    application.add_handler(hist)
    apag = CommandHandler("apagar", delete)
    application.add_handler(apag)

    application.run_polling()


if __name__ == "__main__":
    main()