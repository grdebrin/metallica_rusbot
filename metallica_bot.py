import logging
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

# Настройка логгирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

# Состояния разговора
ALBUM, SONG = range(2)

# Загрузка переводов песен
def load_song_translations():
    with open('song_translations.txt', 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()
    song_translations = {}
    i = 0
    while i < len(lines):
        song_name = lines[i]
        translation_lines = []
        i += 1
        while i < len(lines) and lines[i] != '':
            translation_lines.append(lines[i])
            i += 1
        song_translations[song_name] = '\n'.join(translation_lines)
        i += 1
    return song_translations

song_translations = load_song_translations()

# Чтение токена из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ Не найден токен! Установите переменную окружения BOT_TOKEN.")

# Инициализация бота
updater = Updater(token=TOKEN, use_context=True)

# Обработчик команды /start
def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    try:
        update.message.reply_photo(photo=open('metallica.jpeg', 'rb'))
    except FileNotFoundError:
        update.message.reply_text("⚠️ Файл metallica.jpeg не найден в папке с ботом.")
    update.message.reply_text(
        f'Привет, {user.first_name}! Здесь ты сможешь посмотреть перевод песен группы Metallica.\n'
        'Выбери альбом, а затем песню:',
        reply_markup=get_album_keyboard()
    )
    return ALBUM

# Клавиатура для выбора альбома
def get_album_keyboard() -> ReplyKeyboardMarkup:
    albums = [
        ['Альбом - Kill Em All'], ['Альбом - Ride the Lightning'],
        ['Альбом - Master of Puppets'], ['Альбом - And Justice for All'],
        ['Альбом - Metallica'], ['Альбом - Load'], ['Альбом - ReLoad'],
        ['Альбом - S&M'], ['Альбом - St Anger'], ['Альбом - Death Magnetic'],
        ['Альбом - Beyond Magnetic'], ['Альбом - Hardwired To Self-Destruct'],
        ['Альбом - 72 Seasons'], ['Singles'], ['Exit']
    ]
    return ReplyKeyboardMarkup(albums, one_time_keyboard=True, resize_keyboard=True)

# Обработчик выбора альбома
def select_album(update: Update, context: CallbackContext) -> int:
    album = update.message.text
    if album == 'Exit':
        user = update.message.from_user
        update.message.reply_text(f'До свидания, {user.first_name}!', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        album = album.replace('Альбом - ', '')
        context.user_data['album'] = album
        update.message.reply_text(
            f'Выбран альбом: {album}\nТеперь выбери песню:',
            reply_markup=get_song_keyboard(album)
        )
        return SONG

# Клавиатура для выбора песни
def get_song_keyboard(album: str) -> ReplyKeyboardMarkup:
    songs = []
    if album == 'Kill Em All':
        songs = [['Hit the Lights'], ['The Four Horsemen'], ['Motorbreath'], ['Jump in the Fire'],
                 ['Anesthesia'], ['Whiplash'], ['Phantom Lord'], ['No Remorse'],
                 ['Seek and Destroy'], ['Metal Militia']]
    elif album == 'Ride the Lightning':
        songs = [['Fight Fire with Fire'], ['Ride the Lightning'], ['For Whom the Bell Tolls'],
                 ['Fade to Black'], ['Trapped Under Ice'], ['Escape'],
                 ['Creeping Death'], ['The Call of Ktulu']]
    elif album == 'Master of Puppets':
        songs = [['Battery'], ['Master of Puppets'], ['The Thing That Should Not Be'],
                 ['Welcome Home (Sanitarium)'], ['Disposable Heroes'], ['Leper Messiah'],
                 ['Orion'], ['Damage, Inc']]
    elif album == 'And Justice for All':
        songs = [['Blackened'], ['And Justice for All'], ['Eye of the Beholder'],
                 ['One'], ['The Shortest Straw'], ['Harvester of Sorrow'],
                 ['The Frayed Ends of Sanity'], ['To Live Is to Die'], ['Dyers Eve']]
    elif album == 'Metallica':
        songs = [['Enter Sandman'], ['Sad but True'], ['Holier Than Thou'], ['The Unforgiven'],
                 ['Wherever I May Roam'], ['Dont Tread on Me'], ['Through the Never'],
                 ['Nothing Else Matters'], ['Of Wolf and Man'], ['The God That Failed'],
                 ['My Friend of Misery'], ['The Struggle Within']]
    elif album == 'Load':
        songs = [['Aint My Bitch'], ['2 X 4'], ['The House Jack Built'], ['Until It Sleeps'],
                 ['King Nothing'], ['Hero of the Day'], ['Bleeding Me'], ['Cure'],
                 ['Poor Twisted Me'], ['Wasting My Hate'], ['Mama Said'], ['Thorn Within'],
                 ['Ronnie'], ['The Outlaw Torn']]
    elif album == 'ReLoad':
        songs = [['Fuel'], ['The Memory Remains'], ['Devils Dance'], ['The Unforgiven II'],
                 ['Better than You'], ['Slither'], ['Carpe Diem Baby'], ['Bad Seed'],
                 ['Where the Wild Things Are'], ['Prince Charming'], ['Low Mans Lyric'],
                 ['Attitude'], ['Fixxxer']]
    elif album == 'S&M':
        songs = [['Human'], ['No Leaf Clover']]
    elif album == 'St Anger':
        songs = [['Frantic'], ['St Anger'], ['Some Kind of Monster'], ['Dirty Window'],
                 ['Invisible Kid'], ['My World'], ['Shoot Me Again'], ['Sweet Amber'],
                 ['The Unnamed Feeling'], ['Purify'], ['All Within My Hands']]
    elif album == 'Death Magnetic':
        songs = [['That Was Just Your Life'], ['The End of the Line'], ['Broken, Beat and Scarred'],
                 ['The Day That Never Comes'], ['All Nightmare Long'], ['Cyanide'],
                 ['The Unforgiven III'], ['The Judas Kiss'], ['Suicide and Redemption'], ['My Apocalypse']]
    elif album == 'Beyond Magnetic':
        songs = [['Hate Train'], ['Just A Bullet Away'], ['Hell and Back'], ['Rebel of Babylon']]
    elif album == 'Hardwired To Self-Destruct':
        songs = [['Hardwired'], ['Atlas, Rise!'], ['Now That Were Dead'], ['Moth into Flame'],
                 ['Dream No More'], ['Halo on Fire'], ['Confusion'], ['ManUNkind'],
                 ['Here Comes Revenge'], ['Am I Savage?'], ['Murder One'], ['Spit Out the Bone']]
    elif album == '72 Seasons':
        songs = [['72 Seasons'], ['Shadows Follow'], ['Screaming Suicide'], ['Sleepwalk My Life Away'],
                 ['You Must Burn!'], ['Lux Eterna'], ['Crown of Barbed Wire'], ['Chasing Light'],
                 ['If Darkness Had a Son'], ['Too Far Gone?'], ['Room of Mirrors'], ['Inamorata']]
    elif album == 'Singles':
        songs = [['I Disappear']]
    songs.append(['Back'])
    return ReplyKeyboardMarkup(songs, one_time_keyboard=True, resize_keyboard=True)

# Обработчик выбора песни
def select_song(update: Update, context: CallbackContext) -> None:
    song = update.message.text
    if song == 'Back':
        update.message.reply_text('Выбери альбом:', reply_markup=get_album_keyboard())
        return ALBUM
    else:
        album = context.user_data['album']
        song_key = f"{song} by Metallica"
        translation = song_translations.get(song_key, "Перевод отсутствует.")
        update.message.reply_text(
            f"Перевод песни '{song}' из альбома '{album}' на русский язык:\n{translation}",
            reply_markup=get_album_keyboard()
        )
        return ALBUM

# Создание и регистрация ConversationHandler
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        ALBUM: [MessageHandler(Filters.text & ~Filters.command, select_album)],
        SONG: [MessageHandler(Filters.text & ~Filters.command, select_song)],
    },
    fallbacks=[CommandHandler('start', start)]
)

# Добавление ConversationHandler
updater.dispatcher.add_handler(conversation_handler)

# Запуск бота
if __name__ == "__main__":
    updater.start_polling()
    updater.idle()
