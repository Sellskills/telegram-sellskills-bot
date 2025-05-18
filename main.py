import logging
from telegram import Update, ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

ASK_NAME, ASK_QUESTIONS = range(2)
user_data = {}

questions = [
    "1. Quelle est la différence entre persuasion et manipulation ?\na) Aucune\nb) La persuasion respecte le choix\nc) La manipulation est obligatoire",
    "2. À quel moment proposer le dépôt ?\na) À la fin\nb) Dès que le besoin est clair\nc) Jamais",
    "3. Que faire après une objection ?\na) Raccrocher\nb) Reformuler et guider\nc) L’ignorer",
    "4. Le simulateur est utilisé... ?\na) En intro\nb) Comme levier d’aide\nc) Jamais",
    "5. Une accroche efficace doit...\na) Être floue\nb) Créer un cadre\nc) Être agressive",
    "6. Un bon agent de conversion est...\na) Passif\nb) Structuré\nc) Silencieux",
    "7. L’objectif d’un appel est...\na) Informer\nb) Convertir\nc) Discuter",
    "8. Que faire après un dépôt ?\na) Laisser le client seul\nb) Valoriser, rassurer\nc) Le rappeler plus tard",
    "9. Quelle qualité mentale est essentielle ?\na) Patience\nb) Discipline\nc) Chance",
    "10. En cas de doute du client, tu...\na) Presses\nb) Reformules\nc) Attends",
    "11. Le rôle du CRM est...\na) De stocker des infos\nb) De suivre les étapes\nc) Les deux",
    "12. Comment réagir à un 'non' ?\na) L’ignorer\nb) S’énerver\nc) Questionner calmement",
    "13. Quand faut-il structurer l’appel ?\na) Toujours\nb) Jamais\nc) Quand on y pense",
    "14. Le closing est...\na) Optionnel\nb) Un objectif\nc) Un hasard",
    "15. L’écoute active permet de...\na) Gagner la confiance\nb) Parler plus\nc) Raccourcir l’appel"
]

answers = ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'c', 'c', 'a', 'b', 'a']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text("👋 Bienvenue dans l’examen final de SellSkills Academy.

Veuillez entrer votre nom et prénom pour commencer.")
    return ASK_NAME

async def ask_questions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    user_id = update.effective_user.id
    user_data[user_id] = {'name': name, 'score': 0, 'step': 0}
    await update.message.reply_text(f"Merci {name}. Allons-y.")
    await update.message.reply_text(questions[0])
    return ASK_QUESTIONS

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    response = update.message.text.strip().lower()
    step = user_data[user_id]['step']

    if response == answers[step]:
        user_data[user_id]['score'] += 1

    user_data[user_id]['step'] += 1
    if user_data[user_id]['step'] < len(questions):
        await update.message.reply_text(questions[user_data[user_id]['step']])
        return ASK_QUESTIONS
    else:
        score = user_data[user_id]['score']
        await update.message.reply_text(f"✅ Examen terminé.
Score : {score}/15.")
        return ConversationHandler.END

def main():
    app = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_questions)],
            ASK_QUESTIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response)],
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
