import logging
import random
import asyncio
import time
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.types import FSInputFile
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = '8632161784:AAF-uGCqIx1TsDI_IxGS9kRxbAW8pXCtP-o'
ADMIN_ID = 8557740388
MIN_PLAYERS = 2

Base = declarative_base()

class PlayerStats(Base):
    __tablename__ = 'player_stats'
    user_id = Column(Integer, primary_key=True)
    games = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    points = Column(Integer, default=0)


class Registration(Base):
    __tablename__ = 'registrations'
    chat_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, primary_key=True)

engine = create_engine('sqlite:///game.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

TARGET_CHAT_NAME = "𝕃𝕖𝕥𝕒𝕝 𝕄𝕒𝕗𝕚𝕒"
TARGET_CHAT_LINK = "https://t.me/+CCYQqyga20JmMWE6"

@dp.message(lambda m: getattr(m.chat, 'type', None) == 'private' and m.text and m.text.startswith('/start'))
async def private_start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=TARGET_CHAT_NAME, url=TARGET_CHAT_LINK)]
    ])
    await message.answer(f"Բոտի պաշտոնական չատը 👇👇👇", reply_markup=kb)


@dp.message(lambda m: getattr(m.chat, 'type', None) == 'private' and m.text and m.text.startswith('/'))
async def private_ignore(message: types.Message):
    return

rebus = {
    "Պինգվինաշեն": {"image": "images/pingvinashen.jpg", "answers": ["Պինգվինաշեն"]},
    "Արիել": {"image": "images/ariel.jpg", "answers": ["Արիել", "Արյել"]},
    "Սառցե սիրտ": {"image": "images/sarcesirty.jpg", "answers": ["Սառցե սիրտը", "Sartce Sirty", "Սառցե սիրտ", "Sartce Sirt"]},
    "Գեղեցկուհին ու հրեշը": {"image": "images/gexeckuhinuhreshy.jpg", "answers": ["Գեղեցկուհին ու հրեշը", "Գեղեցկուհին և հրեշը"]},
    "Գտնված երազ": {"image": "images/gtnvaceraz.jpg", "answers": ["Գտնված երազ"]},
    "Սպիտակաձյունիկը և յոթ թզուկները": {"image": "images/spitakadzyunik.jpg", "answers": ["Սպիտակաձյունիկը և յոթ թզուկները", "Սպիտակաձյունիկ և յոթ թզուկներ","Սպիտակաձյունիկը ևշու յոթ թզուկները", "Սպիտակաձյունիկ ու յոթ թզուկներ"]},
    "Փոքրիկ Իշխանը": {"image": "images/poqrikishxan.jpg", "answers": ["Փոքրիկ Իշխանը"]},
    "Զվերոպոլիս": {"image": "images/zverapolis.jpg", "answers": ["Զվերոպոլիս", "Զվերապոլիս"]},
    "Կարմիր գլխարկը": {"image": "images/karmirglxark.jpg", "answers": ["Կարմիր գլխարկը"]},
    "Բրեմենյան երաժիշտներ": {"image": "images/bremenyanerajishtner.jpg", "answers": ["Բրեմենյան երաժիշտներ","Բրեմենյան երաժիշտները"]},
    "Վալլի": {"image": "images/valli.jpg", "answers": ["Վալլի", "Վալի"]},
    "Դեպի վեր": {"image": "images/depiver.jpg", "answers": ["Դեպի վեր", "Վեր"]},
    "Կոշկավոր կատուն": {"image": "images/koshkavorkatun.jpg", "answers": ["Կոշկավոր կատու", "Կոշկավոր կատուն"]},
    "Մադագասկար": {"image": "images/madagaskar.jpg", "answers": ["Մադագասկար"]},
    "Խաղալիքների պատմություն": {"image": "images/xaxaliqneripatmutyun.jpg", "answers": ["Խաղալիքների պատմություն", "Խաղալիքների պատմությունը"]},
    "Վինի թուխ": {"image": "images/vinitux.jpg", "answers": ["Վիննի թուխ", "Վինի թուխ", "Վինի պուխ", "Վիննի պուխ"]},
    "Առյուծ արքան": {"image": "images/simba.jpg", "answers": ["Սիմբա", "Առյուծ արքա", "Առյուծ արքան"]},
    "Շռեկ": {"image": "images/shrek.jpg", "answers": ["Շրեկ", "Շռեկ"]},
    "Ռիո": {"image": "images/rio.jpg", "answers": ["Ռիո", "Րիո"]},
    "Սառցե դարաշրջան": {"image": "images/sarcejamanakashrjan.jpg", "answers": ["Սառցե ժամանակաշրջան", "Սառցե դարաշրջան"]},
    "Ռատատույ": {"image": "images/ratatuy.jpg", "answers": ["Ռատատույ", "Րատատույ"]},
    "Ռապունցել": {"image": "images/rapuncel.jpg", "answers": ["Ռապունցել", "Րապունցել"]},
    "Ռալֆ": {"image": "images/ralf.jpg", "answers": ["Ռալֆ", "Րալֆ"]},
    "Մոանա": {"image": "images/moana.jpg", "answers": ["Մոանա", "Մուանա", "Մուաննա", "Մոաննա"]},
    "Մեծ հերոս": {"image": "images/mecheros.jpg", "answers": ["Մեծ հերոս"]},
}

game_started = False
registration_started = False
players = []
pinned_message_id = None
scores = {}
correct_rebus = None
rebus_guessed = False
admin_chat_id = None
guess_attempts = {}
remaining_rebus = list(rebus.items())
current_round_task = None
current_game_chat_id = None

def get_player_stats(user_id: int) -> dict:
    session = Session()
    try:
        player = session.query(PlayerStats).filter_by(user_id=user_id).first()
        if player:
            return {"games": player.games, "wins": player.wins, "points": player.points}
        return {"games": 0, "wins": 0, "points": 0}
    finally:
        session.close()


def _strip_trailing_yoch(s: str) -> str:
    if not s:
        return s
    s = s.strip()

    if s.endswith('ը'):
        return s[:-1].strip()
    return s


def normalize_for_compare(s: str) -> str:
    if s is None:
        return ''
    return _strip_trailing_yoch(s).lower()


def ensure_trailing_yoch_display(s: str) -> str:
    if not s:
        return s
    s = s.strip()
    if not s.endswith('ը'):
        return s + 'ը'
    return s


def load_players(chat_id: int) -> list[int]:
    """Return list of user_ids that are registered in the given chat."""
    session = Session()
    try:
        regs = session.query(Registration).filter_by(chat_id=chat_id).all()
        return [r.user_id for r in regs]
    finally:
        session.close()


def add_registration(chat_id: int, user_id: int):
    session = Session()
    try:
        if not session.query(Registration).filter_by(chat_id=chat_id, user_id=user_id).first():
            session.add(Registration(chat_id=chat_id, user_id=user_id))
            session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


def remove_registration(chat_id: int, user_id: int):
    session = Session()
    try:
        session.query(Registration).filter_by(chat_id=chat_id, user_id=user_id).delete()
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


def clear_registrations(chat_id: int):
    session = Session()
    try:
        session.query(Registration).filter_by(chat_id=chat_id).delete()
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()

def update_player_stats(user_id: int, is_win: bool = False, points: int = 1):
    session = Session()
    try:
        player = session.query(PlayerStats).filter_by(user_id=user_id).first()
        if not player:
            player = PlayerStats(user_id=user_id)
            session.add(player)
            player.games = 0
            player.wins = 0
            player.points = 0
        player.games = (player.games or 0) + 1
        player.points = (player.points or 0) + points
        if is_win:
            player.wins = (player.wins or 0) + 1
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"DB update error {user_id}: {e}")
    finally:
        session.close()

async def safe_delete(message: types.Message | None):
    if not message:
        return
    try:
        await message.delete()
    except Exception as e:
        err = str(e).lower()
        if "can't be deleted" in err or "bad request" in err or "not found" in err:
            pass
        else:
            logger.warning(f"Delete failed {getattr(message, 'message_id', 'unknown')}: {e}")

def get_registration_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Միանալ", callback_data="join_game")],
        [InlineKeyboardButton(text="🚶 Լքել խաղը", callback_data="leave_game")]
    ])

async def get_user_name(user_id: int) -> str:
    try:
        user = await bot.get_chat(user_id)
        return f"<a href='tg://user?id={user_id}'>{user.first_name}</a>"
    except:
        return "✖️"


user_name_cache: dict[int, tuple[str, float]] = {}
USER_NAME_TTL = 300


async def get_user_name(user_id: int) -> str:
    now = time.time()
    entry = user_name_cache.get(user_id)
    if entry and entry[1] > now:
        return entry[0]
    try:
        user = await bot.get_chat(user_id)
        name = f"<a href='tg://user?id={user_id}'>{user.first_name}</a>"
    except:
        name = "✖️"
    user_name_cache[user_id] = (name, now + USER_NAME_TTL)
    return name


def invalidate_user_name(user_id: int):
    user_name_cache.pop(user_id, None)

callback_cooldowns: dict[tuple[int, int, str], float] = {}
CALLBACK_COOLDOWN = 1.0

async def is_user_admin(chat_id: int, user_id: int) -> bool:
    try:
        admins = await bot.get_chat_administrators(chat_id)
        return any(admin.user.id == user_id for admin in admins)
    except:
        return False

async def update_registration_message(chat_id: int):
    global pinned_message_id, registration_started
    if not registration_started:
        return

    if players:
        name_coros = [get_user_name(pid) for pid in players]
        results = await asyncio.gather(*name_coros, return_exceptions=True)
        registered_lines = []
        for i, res in enumerate(results):
            if isinstance(res, Exception):
                registered_lines.append(f"{i+1}.✖️")
            else:
                registered_lines.append(f"{i+1}. {res}")
        registered = '\n'.join(registered_lines)
    else:
        registered = ''
    text = f"<b>🧩 Սմայլ խաղի գրանցում</b>\n\n👤 Մասնակիցներ՝\n{registered or '︎︎ㅤ'}"
    try:
        if pinned_message_id:
            await bot.edit_message_text(text, chat_id=chat_id, message_id=pinned_message_id,
                                       reply_markup=get_registration_keyboard(), parse_mode="HTML")
        else:
            msg = await bot.send_message(chat_id, text, reply_markup=get_registration_keyboard(), parse_mode="HTML")
            pinned_message_id = msg.message_id
            await bot.pin_chat_message(chat_id, msg.message_id)
    except Exception as e:
        logger.error(f"Reg message error: {e}")

def reset_game_state():
    global game_started, registration_started, pinned_message_id, correct_rebus, rebus_guessed, current_round_task, current_game_chat_id
    game_started = False
    registration_started = False
    players.clear()
    pinned_message_id = None
    correct_rebus = None
    rebus_guessed = False
    scores.clear()
    guess_attempts.clear()
    remaining_rebus[:] = list(rebus.items())
    if current_round_task and not current_round_task.done():
        current_round_task.cancel()
    current_round_task = None
    current_game_chat_id = None

@dp.message(Command(commands=['game']))
async def start_registration(message: types.Message):
    global registration_started, pinned_message_id, players
    await safe_delete(message)
    if game_started:
        await message.answer("Խաղն արդեն ընթացքի մեջ է։")
        return
    if not await is_user_admin(message.chat.id, message.from_user.id):
        return

    if registration_started:

        if pinned_message_id:
            try:
                await bot.unpin_chat_message(message.chat.id)
            except Exception:
                pass
            try:
                await bot.delete_message(message.chat.id, pinned_message_id)
            except Exception:
                pass
            pinned_message_id = None

        players = load_players(message.chat.id)
        await update_registration_message(message.chat.id)
    else:

        registration_started = True

        players.clear()
        clear_registrations(message.chat.id)
        pinned_message_id = None
        await update_registration_message(message.chat.id)

@dp.callback_query(lambda c: c.data == "join_game")
async def join_game(callback: types.CallbackQuery):
    global players
    chat_id = callback.message.chat.id
    now = time.time()
    key = (chat_id, callback.from_user.id, 'join')
    last = callback_cooldowns.get(key, 0)
    if now - last < CALLBACK_COOLDOWN:
        await callback.answer("Խնդրում եմ սպասել։")
        return
    if callback.from_user.id in players:
        callback_cooldowns[key] = now
        await callback.answer("Դուք արդեն գրանցված եք։")
        return
    players.append(callback.from_user.id)

    await callback.answer("Դուք միացել եք խաղին!")

    callback_cooldowns[key] = now
    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, add_registration, chat_id, callback.from_user.id)
    asyncio.create_task(update_registration_message(chat_id))

@dp.callback_query(lambda c: c.data == "leave_game")
async def leave_game(callback: types.CallbackQuery):
    global players
    chat_id = callback.message.chat.id
    now = time.time()
    key = (chat_id, callback.from_user.id, 'leave')
    last = callback_cooldowns.get(key, 0)
    if now - last < CALLBACK_COOLDOWN:
        await callback.answer("Խնդրում եմ սպասել։")
        return
    if callback.from_user.id not in players:
        callback_cooldowns[key] = now
        await callback.answer("Դուք գրանցված չեք։")
        return
    players.remove(callback.from_user.id)

    await callback.answer("Դուք լքել եք գրանցումը։")

    callback_cooldowns[key] = now
    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, remove_registration, chat_id, callback.from_user.id)
    asyncio.create_task(update_registration_message(chat_id))

@dp.message(Command(commands=['start']))
async def cmd_start_game(message: types.Message):
    global game_started, registration_started, pinned_message_id
    await safe_delete(message)
    if not await is_user_admin(message.chat.id, message.from_user.id):
        return

    if not registration_started:
        return
    if game_started:
        await message.answer("Խաղն արդեն ընթացքի մեջ է։")
        return
    if len(players) < MIN_PLAYERS:
        return
    registration_started = False
    game_started = True
    global current_game_chat_id
    current_game_chat_id = message.chat.id

    if pinned_message_id:
        try:
            await bot.unpin_chat_message(message.chat.id)
        except:
            pass
        try:
            await bot.delete_message(message.chat.id, pinned_message_id)
        except Exception:
            pass
        pinned_message_id = None

    clear_registrations(message.chat.id)
    await message.answer("<b>Խաղը սկսված է! 🎮</b>\nՄաղթում եմ ձեզ հաճելի մրցութային ժամանց 🫶")
    await send_next_round(message)

async def send_next_round(origin):
    global correct_rebus, rebus_guessed, current_round_task, remaining_rebus
    if not remaining_rebus:
        await finish_game(origin)
        return
    rebus_item = random.choice(remaining_rebus)
    correct_rebus = rebus_item[0]
    remaining_rebus.remove(rebus_item)
    rebus_guessed = False
    player_list = '\n'.join([f"{i+1}. {await get_user_name(pid)} - {scores.get(pid, 0)}" for i, pid in enumerate(players)])
    chat_id = origin.chat.id if hasattr(origin, 'chat') else origin
    await bot.send_message(chat_id, f"👥 Մասնակիցներ:\n{player_list}\n\n👁‍🗨 Ուշադրություն…", parse_mode="HTML")
    await asyncio.sleep(1)
    photo = FSInputFile(rebus_item[1]["image"])
    await bot.send_photo(chat_id, photo, caption=" 📺 Գուշակե՛ք մուլտֆիլմը 📺")
    if current_round_task and not current_round_task.done():
        current_round_task.cancel()
    current_round_task = asyncio.create_task(round_timer(chat_id))

async def round_timer(chat_id):
    global rebus_guessed, correct_rebus
    try:
        await asyncio.sleep(30)
        if not rebus_guessed and correct_rebus:
            display_answer = _strip_trailing_yoch(correct_rebus)
            await bot.send_message(
                chat_id,
                f"⌛ Ժամանակն ավարտվեց!\nՃիշտ պատասխանն է՝ <b>{display_answer}</b>",
                parse_mode="HTML",
            )
            await send_next_round(chat_id)
    except asyncio.CancelledError:
        pass

@dp.message(Command(commands=['stop']))
async def stop_game(message: types.Message):
    global game_started, registration_started
    await safe_delete(message)
    if not await is_user_admin(message.chat.id, message.from_user.id):
        return

    if not registration_started and not game_started:
        return

    if pinned_message_id:
        try:
            await bot.unpin_chat_message(message.chat.id)
        except:
            pass
        try:
            await bot.delete_message(message.chat.id, pinned_message_id)
        except Exception:
            pass
    reset_game_state()
    clear_registrations(message.chat.id)
    await message.answer("Խաղը / գրանցումը դադարեցվեց։")



@dp.message(lambda m: game_started and m.chat.id == current_game_chat_id and m.from_user.id in players and not m.text.startswith("/") and not m.text.startswith("!"))
async def handle_guess(message: types.Message):
    global rebus_guessed
    last = guess_attempts.get(message.from_user.id, 0)
    now = message.date.timestamp()
    if now - last < 2:
        await message.reply("ㅤ")
        return
    guess_attempts[message.from_user.id] = now
    guess = message.text.strip()
    normalized_guess = normalize_for_compare(guess)
    answers = rebus.get(correct_rebus, {}).get("answers", [])
    normalized_answers = [normalize_for_compare(a) for a in answers]
    if normalized_guess in normalized_answers and not rebus_guessed:
        rebus_guessed = True
        update_player_stats(message.from_user.id, is_win=True, points=1)
        scores[message.from_user.id] = scores.get(message.from_user.id, 0) + 1
        await message.reply(f"✅ Ճիշտ է! +1 միավոր - {message.from_user.first_name}")
        if current_round_task:
            current_round_task.cancel()
        await send_next_round(message)

@dp.message(lambda m: game_started and m.chat.id == current_game_chat_id and m.from_user.id not in players and not m.text.startswith("/"))
async def delete_non_player_messages(message: types.Message):
    """Delete messages from users who are not in the game (only in the active game chat)"""
    await safe_delete(message)

@dp.message(lambda m: m.text and m.text.startswith("!"))
async def handle_admin_commands(message: types.Message):
    """Allow admins to use ! commands without restriction, delete non-admin ! commands"""
    if not await is_user_admin(message.chat.id, message.from_user.id):
        await safe_delete(message)

async def finish_game(origin):
    global scores, game_started
    game_started = False
    chat_id = origin.chat.id if hasattr(origin, 'chat') else origin
    for pid in players:
        update_player_stats(pid, is_win=False, points=0)
        if players:
            player_list = '\n'.join([f"{await get_user_name(pid)} - {scores.get(pid, 0)}" for pid in players])
            await bot.send_message(chat_id, f"Խաղն ավարտվեց - ոչ ոք միավոր չհավաքեց։\n\n👥 Մասնակիցներ՝\n{player_list}", parse_mode="HTML")
        else:
            await bot.send_message(chat_id, "Խաղն ավարտվեց - ոչ ոք միավոր չհավաքեց։")
        reset_game_state()
        return
    max_score = max(scores.values())
    winners = [uid for uid, sc in scores.items() if sc == max_score]
    if len(winners) > 1:
        names = ", ".join([await get_user_name(uid) for uid in winners])
        text = f"🤝 Ոչ-ոքի! Հաղթողներ՝ {names} - {max_score} միավոր"
    else:
        name = await get_user_name(winners[0])
        text = f"🏆 Հաղթող՝ {name} - {max_score} միավոր"
    player_list = '\n'.join([f"{await get_user_name(pid)} - {scores.get(pid, 0)}" for pid in players])
    full_text = f"{text}\n\n👥 Բոլոր խաղացողները՝\n{player_list}"
    await bot.send_message(chat_id, full_text, parse_mode="HTML")

    clear_registrations(chat_id)
    reset_game_state()

async def main():

    default_commands = [
        types.BotCommand(command="game", description="🧩 Բացել գրանցում"),
        types.BotCommand(command="start", description="👋 Սկսել խաղը"),
        types.BotCommand(command="stop", description="⛔ Կանգնեցնել խաղը/գրանցումը"),
    ]
    private_commands = [
        types.BotCommand(command="start", description="👋 Մեկնարկել բոտը")
    ]
    try:
        await bot.set_my_commands(default_commands, scope=types.BotCommandScopeDefault())
        await bot.set_my_commands(private_commands, scope=types.BotCommandScopeAllPrivateChats())
    except Exception as e:
        logger.warning(f"Setting commands failed: {e}")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
