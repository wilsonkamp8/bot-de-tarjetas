import random
import datetime
from telegram.ext import Updater, CommandHandler

# 🚨 Reemplaza este token con el tuyo (entre comillas)
TOKEN = '7861245578:AAEaaZ5Gq_Hs0g20gmN0z7OftKu0LN-1qTQ'

def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)
    for d in even_digits:
        total += sum(digits_of(d * 2))
    return total % 10 == 0

def generar_tarjetas(bin_str, mes, anio):
    tarjetas = []
    longitud_total = 16
    if len(bin_str) >= longitud_total:
        return ["❌ El BIN debe tener menos de 16 dígitos."]
    while len(tarjetas) < 10:
        faltan = longitud_total - len(bin_str) - 1
        base = bin_str + ''.join(str(random.randint(0, 9)) for _ in range(faltan))
        for i in range(10):
            candidato = base + str(i)
            if luhn_checksum(candidato):
                cvv = random.randint(100, 999)
                tarjetas.append(f"{candidato}|{mes}|{anio}|{cvv}")
                break
    return tarjetas

def generar(update, context):
    try:
        args = context.args
        if len(args) != 2:
            update.message.reply_text("❌ Usa el formato:\n/gen <BIN> <MM/AAAA>")
            return

        bin_input = args[0]
        fecha = args[1].split('/')
        if len(fecha) != 2:
            update.message.reply_text("❌ Fecha inválida. Usa MM/AAAA")
            return

        mes = f"{int(fecha[0]):02d}"
        anio = fecha[1]
        tarjetas = generar_tarjetas(bin_input, mes, anio)
        reply = "\n".join(tarjetas)
        update.message.reply_text(f"✅ Generadas:\n{reply}")
    except Exception as e:
        update.message.reply_text(f"⚠️ Error: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("gen", generar))
    updater.start_polling()
    print("🤖 Bot iniciado. Envíale /gen <BIN> <MM/AAAA> en Telegram.")
    updater.idle()

if __name__ == "__main__":
    main()

