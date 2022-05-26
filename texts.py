from main import _


async def start_text(locale):
    text = _("""Assalomu alaykum! 
    
    🌐 <b>IT Park Tashkent</b>`ning rasmiy Telegram-botiga xush kelibsiz!
    📚Iltimos, ta’lim tilini tanlang.
    
    ➖➖➖➖➖➖➖➖➖➖
    
    Здраствуйте!
    
    🌐 Добро пожаловать на официальный Telegram-бот <b>IT Park Tashkent</b>!
    📚Пожалуйста, выберите язык обучения.""", locale)
    return text


async def menu_text(locale):
    text = _("""Iltimos, menyu orqali keyingi qadamni tanlang!""", locale)
    return text


async def about_text(locale):
    text = _("""🏢 IT Park Tashkent 2021-yilda tashkil topgan bo‘lib, uning asosiy maqsadi - O‘zbekistonda IT sohasini rivojlantirish, IT-tadbirkorlik uchun zarur infratuzilmalarni yaratish, IT mutaxassislarni va IT kompaniyalarni qo‘llab-quvvatlash, istiqbolli startup loyihalarni ishga tushirish, shuningdek, dasturchilarni O‘zbekiston va jahon bozoriga tayyorlashdan iboratdir.
    
    Yuqori talabli IT-mutaxassis bo‘lishni xohlaysimi?
    
    ⚡️ Unda bizning kurslarimizdan birini tanlang va «Kursga yozilish» tugmasi orqali ro‘yxatdan o‘ting.""", locale)
    return text


async def courses_text(locale):
    courses_text = _("""🚀 Yuqori malakali IT-mutaxassis bo‘lishni, dasturlash tillarini o‘rganishni yoki IT-sohasida o‘z malakangizni oshirishni xohlaysizmi? Bunday holda, IT Center PRO`ning o‘quv kurslari, siz uchun eng yaxshi va optimal yechim bo‘la oladi!
    
    💥 Bizning tajribali o‘qituvchilarimiz sizga IT-industriyasining barcha yo‘nalishlari bo‘yicha kerakli bo‘lgan bilim va ko‘nikmalarni berishadi va zamonaviy IT-kompaniyalarda munosib ish topishingizga ko‘maklashishadi.
    
    ⚡️ O‘zingizni qiziqtirgan yo‘nalish bo‘yicha kurslarni tanlang va ro‘yxatdan o‘ting.👇👇👇""", locale)

    return courses_text


async def contact_text(locale):
    text = _("""❗️Hurmatli do‘stlar, agarda sizda bizning faoliyatimiz bo‘yicha shikoyat, savol yoki takliflaringiz bo‘lsa, iltimos, ularni shu yerda yozib qoldiring.
    
    ☎️ Qo‘shimcha ma`lumot uchun +998 90 178-00-03 yoki @mrsher8 ga murojaat qilishingiz mumkin.""", locale)
    return text


async def register_list_text(locale):
    text = _("""📍 Iltimos, o‘zingizga qulay bo‘lgan IT-Markazni tanlang 👇""", locale)
    return text


async def robots_text(locale):
    text = _("""📌 Мобильная робототехника
    
    🤖 Курсы робототехники нацелены на получение практических знаний. Мы не играем в Lego, мы учим программировать и собирать сложные электронные устройства (термостат, автополив, системы Умного дома), а также строить роботов на базе Arduino.
    
    📆 Продолжительность курса: 6 месяцев.
    
    💰 Стоимость курса: 500 000 сум/месяц.""")
    return text


async def scratch_text(locale):
    text = _("""📌 Scratch + IT-English
    
    🧩 Scratch — это программа, которая начинает путь детей к программированию. Дети используют эту программу, чтобы проверить себя в среде визуального программирования.
    
    🖇 Кроме того, курс «Scratch + IT English» разделен на две части, где студенты изучают английский язык в первой части урока и Scratch во второй. Программа построена на полноценной практике: после каждого занятия есть практические занятия, насыщенные интересными идеями.
    
    📆 Продолжительность курса: 4 месяца.
    
    💰 Стоимость курса: 1 000 000 сум/месяц""", locale)
    return text


async def smm_text(locale):
    text = _("""📌 SMM-менеджер
    
    👨‍💻 На протяжении всего курса вы получите знания и навыки во многих областях, таких как продвижение бренда в социальных сетях, создание контента и таргетинг. Кроме того, у Вас будет возможность повысить квалификацию, работая с реальными проектами.
    📆 Продолжительность курса: 3 месяца.
    
    💰 Стоимость курса: 1 000 000 сум/месяц""", locale)
    return text


async def english_text(locale):
    text = _("""📌 IT-English
    
    🇺🇸 Курсы IT-English проходят инновационным образом в соответствии с международно-признанными стандартами. Вы получите инновационную подготовку для успешной сдачи экзаменов CEFR и IELTS.
    
    👩‍🏫 Более того, многие наши педагоги - высококвалифицированные специалисты с огромным опытом работы за рубежом.
    
    📆 Продолжительность каждого уровня: 3 месяца.
    
    💰 Стоимость курса: 460 000 сум/месяц.""", locale)
    return text


async def graphics_text(locale):
    text = _("""📌 Графический и веб-дизайн
    
    🎨 Целью курса является создание сложных изображений и контента с помощью графических программ, повышение творческих способностей учащихся, профессиональное освоение таких программ, как Adobe Photoshop, Adobe Illustrator и Corel Draw.
    
    📆 Продолжительность курса: 4 месяца.
    
    💰 Стоимость курса: 800 000 сум/месяц.""", locale)
    return text


async def android_text(locale):
    text = _("""📌 Создание Android приложений
    
    📲 Android — самая популярная мобильная платформа в мире.
    
    Android-разработчики нужны в разных сферах: разработать онлайн-банкинг со сложной степенью защиты или приложение для интернет-магазина, приложения для изучения английского языка или мобильный сервис по доставке еды и продуктов.
    
    На курсе «Разработка Android приложений» Вы:
    
    - Научитесь с нуля создавать мобильные приложения под Android и программировать на Java и Kotlin.
    
    - Получите знания и навыки, необходимые для создания проектов уровня middle-специалиста.
    
    - Сможете самостоятельно проектировать логику работы мобильных приложений, настраивать среду приложений и другие ключевые события.
    
    📆 Продолжительность курса: 6 месяцев.
    
    💰 Стоимость курса: 1 000 000 сум/месяц.""", locale)
    return text


async def backend_text(locale):
    text = _("""📌 Backend программирование
    
    💻 Backend-разработчик - это специалист, который занимается программно-административной частью веб-приложений, внутренним содержанием системы, серверными технологиями, базой данных, архитектурой и логикой программных продуктов.
    
    ⚡️ На курсе Вы изучите язык программирования Python, один из самых популярных высокоуровневых языков программирования, а также освоите самые важные Backend-инструменты: Django, базы данных SQL, Git и другое.
    
    📆 Продолжительность курса: 6 месяцев.
    
    💰 Стоимость курса: 1 000 000 сум/месяц.""", locale)
    return text


async def web_text(locale):
    text = _("""📌 Веб программирование
    
    📲 Android — самая популярная мобильная платформа в мире.
    
    Android-разработчики нужны в разных сферах. К примеру, разработка онлайн-банкинга со сложной степенью защиты или приложений для интернет-магазинов, изучения английского языка или мобильного сервиса по доставке еды и продуктов.
    
    На курсе «Разработка Android приложений» Вы:
    
    - Научитесь с нуля создавать мобильные приложения под Android и программировать на Java и Kotlin.
    
    - Получите знания и навыки, необходимые для создания проектов уровня middle-специалиста.
    
    - Сможете самостоятельно проектировать логику работы мобильных приложений, настраивать среду приложений и другие ключевые события.
    
    📆 Продолжительность курса: 6 месяцев.
    
    💰 Стоимость курса: 1 000 000 сум/месяц.""", locale)
    return text


async def phone_add_text(locale):
    text = _("Iltimos, telefon raqamingizni kiriting yoki «Raqamni yuborish» tugmasini bosing. \n\n"
             "Misol uchun: +998 90 123-45-67", locale)
    return text


async def phone_error_answer(locale):
    text = _("Telefon raqam noto‘g‘ri formatda kiritildi❗️ \n\nIltimos, telefon raqamni qayta kiriting.", locale)
    return text


async def phone_add_button(locale):
    text = _("📞 Raqamni yuborish", locale)
    return text


async def back_reply_button(locale):
    text = _("⬅️ Ortga", locale)
    return text


async def fio_answer_text(locale):
    text = _("Iltimos, to‘liq ismingizni kiriting", locale)
    return text


async def age_answer_text(locale):
    text = _("Iltimos, yoshingizni kiriting", locale)
    return text


async def sex_answer_text(locale):
    text = _("Iltimos, jinsingizni tanlang", locale)
    return text


async def error_answer_text(locale):
    text = _("Kiritgan ma'lumotingiz mos kelmadi", locale)
    return text


async def error_age_answer(locale):
    text = _("Yosh chegarasi xato kiritildi", locale)
    return text


result_answer_text = _("""📃 F. I. SH.: {fio} 
👫 Jins: {sex} 
📅 Yosh: {age}
🏢 IT Center: {center}
🖥 Kurs: {course}
📞 Tel: {phone}

Qo‘shimcha savollaringiz mavjudmi? Unday holda bizning Call-markazimiga murojaat qiling.
 Tel: +998 99 309-11-99""")

new_request_text = _("""Yangi so'rov
📃 F. I. SH.: {fio} 
👫 Jins: {sex} 
📅 Yosh: {age}
🏢 IT Center: {center}
🖥 Kurs: {course}
📞 Tel: {phone}
""")


async def success_message_text(locale):
    text = _("Muvaffaqiyatli ro'yxatdan o'tdingiz", locale)
    return text


async def filial_tashkent(locale):
    text = _("""🏢 <b>IT Park Tashkent</b>
    
    📍 Manzil: Maxtumquli ko‘chasi, 1A, IT Park Tashkent binosi.
    
    📌 Mo‘ljal: Muhammad al-Xorazmiy nomidagi ixtisoslashtirilgan IT-maktab.
    
    📞 Tel: +998 99 309-11-99
    
    🔗 <a href="https://yandex.uz/maps/-/CCU5nFuESB">IT-Markaz xaritada</a>""", locale)
    return text


async def filial_mirzo(locale):
    text = _("""🏢 <b>IT Center - IT Center Mirzo-Ulug‘bek</b>
    
    📍 Manzil:  Qorasu-4, 6A, 121-maktab.
    
    📞 Tel: +998 99 180-11-99
    
    🔗 <a href="https://yandex.uz/maps/-/CCU5nFqgwD">IT-Markaz xaritada</a>""", locale)
    return text


async def filial_chilonzor(locale):
    text = _("""🏢 <b>IT Center - IT Center Chilonzor</b>
    
    📍 Manzil: Chilonzor hokimiyati, Jamoatchilik markazi binosi.
    
    📌 Mo‘ljal: Chilonzor metro.
    
    📞 Tel: +998 99 177-11-99
    
    🔗 <a href="https://yandex.uz/maps/-/CCU5nFdO0C">IT-Markaz xaritada</a>""", locale)

    return text


async def filial_sergeli(locale):
    text = _("""🏢 IT Center - IT Center Sergeli
    
    📍 Manzil: Sergeli 4, 34.
    
    📞 Tel: +998 99 137-11-99
    
    🔗 <a href="https://yandex.uz/maps/-/CCU5nFhIXD">IT-Markaz xaritada</a>""", locale)
    return text


async def filial_yakkasaroy(locale):
    text = _("""🏢 <b>IT Center - IT Center Yakkasaroy</b>
    
    📍 Manzil: Sho‘ta Rustaveli ko‘chasi, 17, Barkamol avlod binosi.
    
    📌 Mo‘ljal: Grand Mir mehmonxonasi.
    
    📞 Tel: +998 99 107-11-99
    
    🔗 <a href="https://yandex.uz/maps/-/CCU5nFh6SB">IT-Markaz xaritada </a>""", locale)
    return text


async def filial_bektemir(locale):
    text = _("""🏢 <b>IT Center - IT Center Bektemir</b>
    
    📍 Manzil: Yuqori Chirchiq koʻchasi, 43.
    
    📞 Tel: +998 99 127-11-99
    
    🔗 <a href="https://yandex.uz/maps/-/CCU5nFhs-B">IT-Markaz xaritada</a>""", locale)
    return text
