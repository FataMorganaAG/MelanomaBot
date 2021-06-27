import telebot
from PIL import Image

bot = telebot.TeleBot('TOKEN')


@bot.message_handler(commands=['start'])  # стартовое сообщение
def start_command(message):
    bot.send_message(message.chat.id,
                     "Привет! \n" +
                     "Для просмотра всех моих команд нажмите /help.")


@bot.message_handler(commands=['help'])  # все команды и сообщить о проблеме (оно же видимо главное меню)
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Сообщить разработчику о проблеме', url='telegram.me/reeen_a'
  )
    )
    bot.send_message(
        message.chat.id,
        'Доступные команды: \n' +
        '1) Для того, чтобы изучить общую информацию о заболевании, нажмите /melanoma.\n' +
        '2) Для того, чтобы узнать о факторах риска заболевания, нажмите /risk. \n' +
        '3) Для того, чтобы узнать о мерах предосторожности, нажмите /precautions. \n' +
        '4) Для того, чтобы проверить ваше родимое пятно по фотографии, нажмите /check. \n' +
        '5) Для того, чтобы пройти тест-диагностику на выявление тревожных симптомов заболевания, нажмите /test. \n' +
        '6) Для того, чтобы получить персонализированный совет, нажмите /advice',
        reply_markup=keyboard
    )


@bot.message_handler(commands=['melanoma'])  # о заболевании
def melanoma(message):
    bot.send_message(
        message.chat.id,
        "Меланома - это злокачественное образование, происходящее из пигментных клеток, "
        "находящихся в эпидермисе. Меланома может проявлять себя разнообразно, но "
        "чаще всего она появляется из приобретенных в течение жизни родимых пятен, "
        "которые претерпевают изменения. Меланома всегда считалась одним из самых "
        "агрессивных видов опухолей, и чуть более 10 лет назад прогноз пациентов "
        "был крайне неблагоприятным. К счастью, на данный момент, "
        "при своевременном обращении к специалисту, "
        "достаточно высокий процент пациентов вылечивается. "
        "Именно поэтому важно вовремя обращать внимание на изменения, "
        "происходящие с родимыми пятнами "
        "и проходить медицинские обследования в случае "
        "подозрения на возникновение меланомы.")


@bot.message_handler(commands=['risk'])  # факторы риска
def risk(message):
    bot.send_message(
        message.chat.id,
        "Никто не застрахован от появления меланомы, однако есть факторы риска, "
        "благоприятствующие возникновению и развитию болезни. "
        "К таким факторам относятся: \n" +
        "1. Воздействие солнечных лучей (особенно приводящее к повторяющимся солнечным ожогам) \n" +
        "2. Повторное загорание с воздействием ультрафиолетовых лучей или лечение "
        "с применением псоралена и ультрафиолетовых лучей \n" +
        "3. Наличие немеланомных опухолей кожи \n" +
        "4. Наследственный фактор \n" +
        "5. Светлая кожа, веснушки \n" +
        "6. Иммуносупрессия (угнетение иммунитета) \n" +
        "7. Контакт (особенно систематический) с канцерогенами")


@bot.message_handler(commands=['precautions'])  # меры предосторожности
def precautions(message):
    bot.send_message(
        message.chat.id,
        "Снизить риск возникновения меланомы могут помочь следующие меры предосторожности: \n" +
        "1. Избегайте длительного нахождения на солнце и в солярии, по возможности находитесь в тени и "
        "минимизируйте активность на открытом воздухе ч 10 часов утра до 4 часов дня "
        "(в часы, когда солнечные лучи наиболее активны) \n" +
        "2. По возможности закрывайте спину и плечи одеждой \n" +
        "3. Защитите от солнца глаза, уши, лицо и шею с помощью шляпы \n" +
        "4. Используйте солнцезащитные очки \n" +
        "5. Используйте качественный солнцезащитный крем с SPF не менее 30 "
        "с водостойкой формулой. Защитные средства должны использоваться, даже если вы выходите "
        "на улицу на короткое время. Они наносятся как минимум за 30 минут до выхода на солнце и часто добавляются "
        "на тело (каждые два часа), особенно после купания, потоотделения и протирания тканью")

@bot.message_handler(commands=['check']) # загружаем картинку для проверки
def check(message):
    image_file = bot.get_file(message.photo[-1].file_id)
    image_file.download("image.jpg")
    # здесь нужно доделать добавление картинки от пользователя
    
    im_new = mpimg.imread("image.jpg")
    im_new = image_to_batch(im_new, 224)
    model = keras.models.load_model('mymodel.h5')
    clf = model.predict(im_new, batch_size=224)
    clf = clf.flatten()
    clf = clf.tolist()
   
    if clf[0] > clf[1]:
        bot.send_message(
            message.chat.id, "Скорее всего поводов для беспокойства нет. \n" +
                             "Хотите обсудить тревожные симптомы в формате теста? Нажмите  /test ")
    elif clf[0] <= clf[1]:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            telebot.types.InlineKeyboardButton(
                'Да', url='https://www.google.com/search?q=%D0%9A%D0%BB%D0%B8%D0%BD%D0%B8%D0%BA%D0%B0+%D1%80%D1%8F%D0%B4%D0%BE%D0%BC+%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0+%D0%BD%D0%B0+%D0%BC%D0%B5%D0%BB%D0%B0%D0%BD%D0%BE%D0%BC%D1%83&sxsrf=ALeKk032W6pfrQv03_hyPu5mzw6kMS7JJw%3A1622477440635&ei=gAq1YKGOJs-GrwSYuJ-gBQ&oq=%D0%9A%D0%BB%D0%B8%D0%BD%D0%B8%D0%BA%D0%B0+%D1%80%D1%8F%D0%B4%D0%BE%D0%BC+%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0+%D0%BD%D0%B0+%D0%BC%D0%B5%D0%BB%D0%B0%D0%BD%D0%BE%D0%BC%D1%83&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECc6BwgAEEcQsAM6BQgAEM0CUKVCWPFGYNdJaAJwA3gAgAGCAogBkQiSAQUwLjUuMZgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=gws-wiz&ved=0ahUKEwihzoS8p_TwAhVPw4sKHRjcB1QQ4dUDCA4&uact=5'
            )
        )
        bot.send_message(
            message.chat.id,
            "Возможно Вам действительно следует обратиться к специалисту. Хотите найти клинику?",
            reply_markup=keyboard
        )
    else:
        bot.send_message(
            message.chat.id,
            "Кажется, что-то пошло не так. Попробуйте загрузить другое изображение.")
            
def image_to_batch(img, size):
    img_resized = cv2.resize(img, (size, size)).reshape(1, size, size, img.shape[2])
    return img_resized


@bot.message_handler(commands=['test'])  # тест по симптомам вопрос 1
def test(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Да', callback_data='Да'),
        telebot.types.InlineKeyboardButton('Нет', callback_data='Нет_1')
    )
    bot.send_message(
        message.chat.id,
        "1. Родимое пятно новое и сильно изменяется в размерах?",
        reply_markup=keyboard
        )


@bot.message_handler(commands=['advice'])  # персонализированный совет вопрос 1
def advice(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Да', callback_data='Совет1'),
        telebot.types.InlineKeyboardButton('Нет', callback_data='Вопрос2')
    )
    bot.send_message(
        message.chat.id,
        "У Вас светлая кожа, которая краснеет при длительном нахождении на солнце или аллергия на солнце?",
        reply_markup=keyboard
        )


@bot.callback_query_handler(func=lambda call: True)  # обработчик кнопок
def callback_query(call):
    # тест
    if call.data == "Да":
        bot.send_message(call.message.chat.id, "Возможно, вам стоит пройти осмотр у специалиста. Найти клинику?")
    elif call.data == "Нет_1":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Да', callback_data='Да'),
            telebot.types.InlineKeyboardButton('Нет', callback_data='Нет_2')
        )
        bot.send_message(call.message.chat.id, "2. Изменилась ли величина/цвет/форма имеющегося родимого пятна?",
                         reply_markup=keyboard
                         )
    elif call.data == "Нет_2":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Да', callback_data='Да'),
            telebot.types.InlineKeyboardButton('Нет', callback_data='Нет_3')
        )
        bot.send_message(call.message.chat.id, "3. Есть ли изменения интенсивности окраски родимого пятна - "
                                               "увеличилась до чёрного цвета, или наоборот, уменьшилась?",
                         reply_markup=keyboard
                         )
    elif call.data == "Нет_3":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Да', callback_data='Да'),
            telebot.types.InlineKeyboardButton('Нет', callback_data='Нет_4')
        )
        bot.send_message(call.message.chat.id, "4. Пигментация родимого пятна неравномерна?",
                         reply_markup=keyboard
                         )
    elif call.data == "Нет_4":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Да', callback_data='Да'),
            telebot.types.InlineKeyboardButton('Нет', callback_data='Нет_5')
        )
        bot.send_message(call.message.chat.id, "5. Родимое пятно воспаляется/шелушится/зудит/кровоточит?",
                         reply_markup=keyboard
                         )
    elif call.data == "Нет_5":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Да', callback_data='Да'),
            telebot.types.InlineKeyboardButton('Нет', callback_data='Нет_6')
        )
        bot.send_message(call.message.chat.id, "6. Присуствует ли асимметрия "
                                               "(если мысленно сложить пятно пополам, его контуры не совпадут)?",
                         reply_markup=keyboard
                         )
    elif call.data == "Нет_6":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Да', callback_data='Да'),
            telebot.types.InlineKeyboardButton('Нет', callback_data='Нет_7')
        )
        bot.send_message(call.message.chat.id, "7. Края пятна неровные, нечёткие?",
                         reply_markup=keyboard
                         )
    elif call.data == "Нет_7":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Да', callback_data='Да'),
            telebot.types.InlineKeyboardButton('Нет', callback_data='Нет_8')
        )
        bot.send_message(call.message.chat.id, "8. Диаметр более 6 мм (примерно как ластик у карандаша)?",
                         reply_markup=keyboard
                         )
    elif call.data == "Нет_8": #будет готова нейронка - можно добавить кнопку для перехода к проверке по фото
        bot.send_message(call.message.chat.id, "Скорее всего поводов для беспокойства нет. \n" +
                                               "Для большей уверенности предлагаем вам проверить родимое пятно по фотографии. \n" +
                                               "Если вам это интересно, нажмите /check.")
    # советы
    elif call.data == "Совет1":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Да', callback_data='Вопрос2'),
            telebot.types.InlineKeyboardButton('Нет', callback_data='ОбщийСовет')
        )
        bot.send_message(call.message.chat.id, "Используйте качественный солнцезащитный крем с SPF не менее 30 (по возможности 50) "
                         "с водостойкой формулой за полчаса до выхода и обновляйте его каждые 2 часа. \n" +
                         "Перейти к следующему вопросу?",
                         reply_markup=keyboard
                         )
    elif call.data == "Вопрос2":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Да', callback_data='Совет2'),
            telebot.types.InlineKeyboardButton('Нет', callback_data='Вопрос3')
        )
        bot.send_message(call.message.chat.id, "Есть ли среди ваших родственников лица, страдающие онкологическими заболеваниями "
                                               "(особенно тем или иным видом рака кожи)?",
                         reply_markup=keyboard
                         )
    elif call.data == "Совет2":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Да', callback_data='Вопрос3'),
            telebot.types.InlineKeyboardButton('Нет', callback_data='ОбщийСовет')
        )
        bot.send_message(call.message.chat.id, "Тщательно следите за своими родимыми пятнами, их изменениями и своим общим самочувствием, "
                                               "не затягивайте с обращением к специалисту в случае подозрений на ухудшение состояния. Вам также лучше не посещать солярий. \n" +
                         "Перейти к следующему вопросу?",
                         reply_markup=keyboard
                         )
    elif call.data == "Вопрос3":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Да', callback_data='Совет3'),
            telebot.types.InlineKeyboardButton('Нет', callback_data='ОбщийСовет')
        )
        bot.send_message(call.message.chat.id, "Посещаете ли вы солярий?",
                         reply_markup=keyboard
                         )
    elif call.data == "Совет3":
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            telebot.types.InlineKeyboardButton('Прочитать общий совет', callback_data='ОбщийСовет')
        )
        bot.send_message(call.message.chat.id, "Не забывайте использовать солнцезащитный крем при продолжительности сеанса более 4 минут. "
                                               "Тщательно следите за таймингом, воздержитесь от длительных сеансов.",
                         reply_markup=keyboard
                         )
    elif call.data == "ОбщийСовет":
        bot.send_message(call.message.chat.id, "Общий совет: \n" +
                         "По возможности сократите время пребывания на солнце в промежутке от 10 часов утра до 4 часов дня, старайтесь находиться в тени и защищать спину, плечи, лицо, уши, шею и глаза с помощью одежды, головных уборов и солнцезащитных очков. "
                         "Используйте качественный солнцезащитный крем с водостойкой формулой за полчаса до выхода и обновляйте его каждые 2 часа. \n" +
                         "Чтобы посмотреть другие команды бота, нажмите /help")


if __name__ == '__main__':  # бесконечный цикл получения новых записей со стороны Telegram
    bot.infinity_polling()
