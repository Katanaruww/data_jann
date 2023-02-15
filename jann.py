import sqlite3

from aiogram import Dispatcher, Bot
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

storage = MemoryStorage()


class FSM(StatesGroup):
    message = State()


bot = Bot("5693287180:AAHs_0p-6D3R7bVSa9ArYbuoWdEzoW6GaSY")
dp = Dispatcher(bot, storage=storage)
admins = [1140638587, 41520535]
supp = "https://t.me/katana_tm"
conn = sqlite3.connect('jannet.db', check_same_thread=False)
cursor = conn.cursor()
mark = InlineKeyboardMarkup()
mark.add(InlineKeyboardButton("Услуги", callback_data="services"),
         InlineKeyboardButton("О мне", callback_data="about_me"))
mark.add(InlineKeyboardButton("Связаться со мной", url=supp))


@dp.message_handler(commands=["start"])
async def start(message):
    tg_id = message.chat.id
    tg_user = message.chat.username
    tg_fio = f"{message.chat.first_name} {message.chat.last_name}"
    cursor.execute("INSERT INTO users (tg_id, tg_tag, tg_fio) VALUES (?, ?, ?)", (tg_id, tg_user, tg_fio,))
    conn.commit()
    await bot.send_message(message.chat.id, "<b>Привет, я бот-помощник персонального коучера - Жанны Панчишиной!</b>",
                           parse_mode="HTML", reply_markup=mark)


@dp.message_handler(commands=["adm"])
async def start(message):
    id_tg = message.chat.id
    if id_tg in admins:
        adm = InlineKeyboardMarkup()
        adm.add(InlineKeyboardButton("Списки юзеров", callback_data="users_list"))
        adm.add(InlineKeyboardButton("Рассылка", callback_data="send_mess"))
        await bot.send_message(message.chat.id, "<b>Одобрено✅</b>", parse_mode="HTML", reply_markup=adm)
    else:
        await bot.send_message(message.chat.id, "<b>Отказано🫡</b>")

@dp.callback_query_handler(lambda call: call.data and call.data.startswith("give_"))
async def delete(call: types.CallbackQuery):
    cursor.execute("UPDATE users SET opl_why = 'opl' WHERE tg_id = ?", (call.data.replace("give_", ""),))
    conn.commit()
    row = cursor.execute("SELECT * FROM users WHERE opl_why = 'no_opl'").fetchall()
    opl = InlineKeyboardMarkup()
    for i in range(len(row)):
        opl.add(InlineKeyboardButton(f"{row[i][2]}", callback_data=f"{row[i][1]}"),
                InlineKeyboardButton("🚫", callback_data=f"give_{row[i][1]}"))
    opl.add(InlineKeyboardButton("Назад👈", callback_data="users_list"))
    await call.message.edit_text("<b>Выберите пользователя</b>\n\n"
                                 "P.S. чтобы обозначить что пользователь не оплатил просто нажмите на '🚫'",
                                 parse_mode="HTML", reply_markup=opl)
@dp.callback_query_handler(lambda call: call.data and call.data.startswith("no_give_"))
async def delete(call: types.CallbackQuery):
    cursor.execute("UPDATE users SET opl_why = 'no_opl' WHERE tg_id = ?", (call.data.replace("no_give_", ""),))
    conn.commit()
    row = cursor.execute("SELECT * FROM users WHERE opl_why = 'opl'").fetchall()
    opl = InlineKeyboardMarkup()
    for i in range(len(row)):
        opl.add(InlineKeyboardButton(f"{row[i][2]}", callback_data=f"{row[i][1]}"),
                InlineKeyboardButton("🚫", callback_data=f"give_{row[i][1]}"))
    opl.add(InlineKeyboardButton("Назад👈", callback_data="users_list"))
    await call.message.edit_text("<b>Выберите пользователя</b>\n\n"
                                 "P.S. чтобы обозначить что пользователь не оплатил просто нажмите на '🚫'",
                                 parse_mode="HTML", reply_markup=opl)
@dp.callback_query_handler(lambda call: True)
async def call(call):
    if call.data == "services":
        serv = InlineKeyboardMarkup()
        serv.add(InlineKeyboardButton("Соматипология", callback_data="somatipologia"))
        serv.add(InlineKeyboardButton("Тренинги личностного роста", callback_data="tren_lich_rost"))
        serv.add(InlineKeyboardButton('Игра "Секрет денег"', callback_data="secret_money"))
        serv.add(InlineKeyboardButton('Книга "Финансовая азбука для детей и взрослых"', callback_data="fin_azb"))
        serv.add(InlineKeyboardButton("На главную⬅", callback_data="callback"))
        await call.message.edit_text("<b>Я предоставляю 4 типа услуг\n\n"
                                     "Подробнее узнайте ниже⬇</b>", parse_mode="HTML", reply_markup=serv)
    elif call.data == "fin_azb":
        back = InlineKeyboardMarkup()
        back.add(InlineKeyboardButton("Написать менеджеру💻", url=supp))
        back.add(InlineKeyboardButton("Назад⬅", callback_data="services"))
        await call.message.edit_text("<b>Книга Финансовая азбука для детей и взрослых\n\n"
                                     "<i>Личная консультация</i>\n\n"
                                     "Стоимость от 5.000 рублей.</b>", parse_mode="HTML", reply_markup=back)
    elif call.data == "tren_lich_rost":
        back = InlineKeyboardMarkup()
        back.add(InlineKeyboardButton("Написать менеджеру💻", url=supp))
        back.add(InlineKeyboardButton("Назад⬅", callback_data="services"))
        await call.message.edit_text("<b>Тренинги личностного роста\n\n"
                                     "<i>Личная консультация</i>\n\n"
                                     "<i>Анализ</i>\n\n"
                                     "Стоимость от 5.000 рублей.</b>", parse_mode="HTML", reply_markup=back)
    elif call.data == "somatipologia":
        som = InlineKeyboardMarkup()
        som.add(InlineKeyboardButton("Определить СомаТип - выбор дела по душе", callback_data="search_soma_choice_work"))
        som.add(InlineKeyboardButton("Определить СомаТип", callback_data="search_soma"))
        som.add(InlineKeyboardButton("Совместимость пары", callback_data="sovm_pari"))
        som.add(InlineKeyboardButton("Подбор идеального партнёра", callback_data="podbor_ideal_parner"))
        som.add(InlineKeyboardButton("Аудит персонала", callback_data="audit_personal"))
        som.add(InlineKeyboardButton("Аудит персонала на предприятии", callback_data="audit_personal_on_predpr"))
        som.add(InlineKeyboardButton("Определить СомаТип ребёнка", callback_data="search_soma_chindler"))
        som.add(InlineKeyboardButton("Индивидуальный коучинг по развитию Соматипа",
                                     callback_data="ind_coach_razv_som"))
        som.add(InlineKeyboardButton("Назад⬅", callback_data="services"))
        await call.message.edit_text("СомаТип", reply_markup=som)
    elif call.data == "search_soma_choice_work":
        back = InlineKeyboardMarkup()
        back.add(InlineKeyboardButton("Написать менеджеру💻", url=supp))
        back.add(InlineKeyboardButton("Назад⬅", callback_data="somatipologia"))
        await call.message.edit_text("<b>Определить СомаТип - выбор дела по душе\n\n"
                                     "Стоимость 5.000 рублей.</b>", parse_mode="HTML", reply_markup=back)
    elif call.data == "search_soma":
        back = InlineKeyboardMarkup()
        back.add(InlineKeyboardButton("Написать менеджеру💻", url=supp))
        back.add(InlineKeyboardButton("Назад⬅", callback_data="somatipologia"))
        await call.message.edit_text("<b>Определить СомаТип</b>\n\n"
                                     "<i>Подсознательные ценности (ПЦ)\n\n</i>"
                                     "<i>Миссия вашего СомаТипа\n\n</i>"
                                     "<i>Уровень вашего развития (УР)\n\n</i>"
                                     "<i>Основная сила (ОС)\n\n</i>"
                                     "<i>Консультация 1,5 часа\n\n</i>"
                                     "<i>Письменные выводы и рекомендации</i>\n\n"
                                     "<b>Стоимость 9.900 рублей.</b>", parse_mode="HTML", reply_markup=back)
    elif call.data == "sovm_pari":
        back = InlineKeyboardMarkup()
        back.add(InlineKeyboardButton("Написать менеджеру💻", url=supp))
        back.add(InlineKeyboardButton("Назад⬅", callback_data="somatipologia"))
        await call.message.edit_text("<b>Совместимость пары</b>\n\n"
                                     "<i>Определение СомаТипов (ПЦ, ОС, УР, предназначение)\n\n</i>"
                                     "<i>Выдача письменных заключений и рекомендаций\n\n</i>"
                                     "<i>Консультация 3-4 часа\n\n</i>"
                                     "<i>Письменные выводы и рекомендации</i>\n\n"
                                     "<b>Стоимость 18.900 рублей.</b>", parse_mode="HTML", reply_markup=back)
    elif call.data == "podbor_ideal_parner":
        back = InlineKeyboardMarkup()
        back.add(InlineKeyboardButton("Написать менеджеру💻", url=supp))
        back.add(InlineKeyboardButton("Назад⬅", callback_data="somatipologia"))
        await call.message.edit_text("<b>Подбор идеального партнёра</b>\n\n"
                                     "<i>Определение СомаТипов (ПЦ, ОС, УР, предназначение)\n\n</i>"
                                     "<i>Выдача письменных заключений и рекомендаций\n\n</i>"
                                     "<i>Описание идеального партнера по всем параметрам и рекомендации, где его найти\n\n</i>"
                                     "<b>Стоимость 9.900 рублей.</b>", parse_mode="HTML", reply_markup=back)
    elif call.data == "audit_personal":
        back = InlineKeyboardMarkup()
        back.add(InlineKeyboardButton("Написать менеджеру💻", url=supp))
        back.add(InlineKeyboardButton("Назад⬅", callback_data="somatipologia"))
        await call.message.edit_text("<b>Аудит персонала</b>\n\n"
                                     "<i>Определение СомаТипа (ПЦ, ОС, УР, СУРК (соответствие сотрудника уровню развития компании)\n\n</i>"
                                     "<i>Ваша эффективность в бизнесе, на каком этапе, заключение по 10 параметрам\n\n</i>"
                                     "<i>Консультация одного сотрудника 1,5 - 2 часа\n\n</i>"
                                     "<i>Письменные выводы и рекомендации</i>\n\n"
                                     "<b>Стоимость на одного человека 15.900 рублей.</b>", parse_mode="HTML", reply_markup=back)
    elif call.data == "audit_personal_on_predpr":
        back = InlineKeyboardMarkup()
        back.add(InlineKeyboardButton("Написать менеджеру💻", url=supp))
        back.add(InlineKeyboardButton("Назад⬅", callback_data="somatipologia"))
        await call.message.edit_text("<b>Аудит персонала на предприятии</b>\n\n"
                                     "<i>Определение СомаТипа (ПЦ, ОС, УР, СУРК (соответствие сотрудника уровню развития компании)\n\n</i>"
                                     "<i>+ тренинг «Совместимость в команде»\n\n</i>"
                                     "<i>Консультация одного сотрудника 1,5 - 2 часа\n\n</i>"
                                     "<i>Письменные выводы и рекомендации</i>\n\n"
                                     "<b>Стоимость 370.000 рублей.</b>", parse_mode="HTML",
                                     reply_markup=back)
    elif call.data == "search_soma_chindler":
        back = InlineKeyboardMarkup()
        back.add(InlineKeyboardButton("Написать менеджеру💻", url=supp))
        back.add(InlineKeyboardButton("Назад⬅", callback_data="somatipologia"))
        await call.message.edit_text("<b>Определить СомаТип ребёнка и ПЦ</b>\n\n"
                                     "<i>Консультация 1,5 - 2 часа\n\n</i>"
                                     "<i>Выдача письменного заключения и рекомендаций по воспитанию и развитию</i>\n\n"
                                     "<b>Стоимость 9.900 рублей.</b>", parse_mode="HTML",
                                     reply_markup=back)
    elif call.data == "ind_coach_razv_som":
        back = InlineKeyboardMarkup()
        back.add(InlineKeyboardButton("Написать менеджеру💻", url=supp))
        back.add(InlineKeyboardButton("Назад⬅", callback_data="somatipologia"))
        await call.message.edit_text("<b>Индивидуальный коучинг по развитию СомаТипа</b>\n\n"
                                     "<i>Повышение Уровня Развития\n\n</i>"
                                     "<i>6 недель работы\n\n</i>"
                                     "<i>1 – 2 видео встречи в неделю</i>\n\n"
                                     "<b>Стоимость 70.000 - 250.000 рублей.</b>", parse_mode="HTML",
                                     reply_markup=back)
    elif call.data == "secret_money":
        back = InlineKeyboardMarkup()
        back.add(InlineKeyboardButton("Написать менеджеру💻", url=supp))
        back.add(InlineKeyboardButton("Назад⬅", callback_data="services"))
        await call.message.edit_text("<b>Игра Секрет Денег</b>\n\n"
                                     "<b>Бизнес-игра «Секрет денег»</b> — настоящий тренажер, который поможет расширить границы Вашей финансовой грамотности и привлечь в Вашу жизнь гораздо больше денег, чем Вы имеете сейчас.\n\n"
                                     "<i>Игра воспроизводит события из реальности и позволяет путем проб и ошибок идти к своей цели.</i>\n\n"
                                     "<i>Систематически играя в эту увлекательную игру, Вы наработаете навыки, которые пригодятся в современном мире.</i>\n\n"
                                     "<i>Огромная польза и приятное времяпрепровождение — несомненные плюсы, которые несет игра «Секрет Денег».</i>\n\n"
                                     "<i>Вы можете приобрести у нас Бизнес-игру «Секрет денег» и тренироваться самостоятельно.</i>\n\n"
                                     "<b>Стоимость от 10.000 рублей.</b>", parse_mode="HTML", reply_markup=back)
    elif call.data == "fin_azb":
        pass
    elif call.data == "about_me":
        back = InlineKeyboardMarkup()
        back.add(InlineKeyboardButton("На главную⬅", callback_data="callback"))
        await call.message.edit_text("<b>Что вам нужно знать обо мне?\n\n</b>"
                                     "<b>Я</b> - эксперт в области развития личной и командной эффективности, Тренер и Коуч по развитию навыков и компетенций в различных областях жизни!\n\n "
                                     "<b>Соматиполог</b>, член ассоциации соматипологов\n\n"
                                     "<b>Веду тренинги и провожу консультации</b> по развитию личности:\n"
                                     "¤ <i>Трансформационные программы\n</i>"
                                     "¤ <i>Тренинги деньги/финансы\n</i>"
                                     "¤ <i>Отношения мужчин и женщин\n</i>"
                                     "¤ <i>Секреты семейного счастья\n</i>"
                                     "¤ <i>Женские тренинги\n\n</i>"
                                     "Есть ещё различные проекты, эти самые яркие! \n\n"
                                     "<i>Бизнес тренинги проводила в 2гис, Альфа-Банк, компания Пролайн!</i>",
                                     parse_mode="HTML", reply_markup=back)
    elif call.data == "callback":
        await call.message.edit_text("<b>Привет, я бот-помощник персонального коучера - Жанны Панчишиной!</b>",
                                     parse_mode="HTML", reply_markup=mark)
    elif call.data == "users_list":
        users = InlineKeyboardMarkup()
        users.add(InlineKeyboardButton("Оплатили🙂", callback_data="opl_users"), InlineKeyboardButton("Не оплатили☹", callback_data="noopl_users"))
        users.add(InlineKeyboardButton("Назад👈", callback_data="adm_inline"))
        await call.message.edit_text("<b>Выберите тип пользователей:</b>", parse_mode="HTML", reply_markup=users)
    elif call.data == "opl_users":
        row = cursor.execute("SELECT * FROM users WHERE opl_why = 'opl'").fetchall()
        opl = InlineKeyboardMarkup()
        for i in range(len(row)):
            opl.add(InlineKeyboardButton(f"{row[i][2]}", callback_data=f"{row[i][1]}"), InlineKeyboardButton("✅", callback_data=f"no_give_{row[i][1]}"))
        opl.add(InlineKeyboardButton("Назад👈", callback_data="users_list"))
        await call.message.edit_text("<b>Выберите пользователя</b>\n\n"
                                     "P.S. чтобы обозначить что пользователь не оплатил просто нажмите на '✅'", parse_mode="HTML", reply_markup=opl)
    elif call.data == "noopl_users":
        row = cursor.execute("SELECT * FROM users WHERE opl_why = 'no_opl'").fetchall()
        opl = InlineKeyboardMarkup()
        for i in range(len(row)):
            opl.add(InlineKeyboardButton(f"{row[i][2]}", callback_data=f"{row[i][1]}"), InlineKeyboardButton("🚫", callback_data=f"give_{row[i][1]}"))
        opl.add(InlineKeyboardButton("Назад👈", callback_data="users_list"))
        await call.message.edit_text("<b>Выберите пользователя</b>\n\n"
                                     "P.S. чтобы обозначить что пользователь оплатил просто нажмите на '🚫'",
                                     parse_mode="HTML", reply_markup=opl)
    elif call.data == "adm_inline":
        adm = InlineKeyboardMarkup()
        adm.add(InlineKeyboardButton("Списки юзеров", callback_data="users_list"))
        adm.add(InlineKeyboardButton("Рассылка", callback_data="send_mess"))
        await bot.send_message(call.message.chat.id, "<b>Одобрено✅</b>", parse_mode="HTML", reply_markup=adm)
    elif call.data == "send_mess":
        await call.message.edit_text("Введите текст отправки:")
        await FSM.message.set()
@dp.message_handler(state=FSM.message)
async def message(message, state: FSMContext):
    message = message.text
    await state.update_data(message=message)
    data = await state.get_data()
    message = data.get('message')
    row = cursor.execute("SELECT * FROM users").fetchall()
    for i in range(len(row)):
        await bot.send_message(row[i][1], message, parse_mode="HTML")
    print("рассылка готова!")
    await state.finish()
executor.start_polling(dp)
