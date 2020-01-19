from telegram import InlineKeyboardButton,InlineKeyboardMarkup,Bot
from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.utils.helpers import escape_markdown
from telegram.ext import Updater,CommandHandler,CallbackQueryHandler,ConversationHandler,\
    Filters,MessageHandler,InlineQueryHandler
import logging
from uuid import uuid4
import json
from telegram import ParseMode
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


with open('token.json') as j:
    token = json.load(j)

BOT = Bot(token['token'])

A, B, C, D, E, F, X,Z = range(8)
prev = None
NEXT = 10

def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    print(query)
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Caps",
            input_message_content=InputTextMessageContent(
                query.upper())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN))]

    update.inline_query.answer(results)

def start(update, context):
    user = update.message.from_user
    USER = 'Hi 🖐🏼 '
    logger.info('User %s started conversation', USER)
    keyboard = [
        [
            InlineKeyboardButton('Search Course',callback_data='search'),
            InlineKeyboardButton('Choose By year',callback_data='choose_by_year')
        ],
        [InlineKeyboardButton('List All Available Course',callback_data='ListAll')],
    ]
    keyboard.append([InlineKeyboardButton('Exit ❌', callback_data='exit')])
    reply_markup=InlineKeyboardMarkup(keyboard,one_time_keyboard=True)
    update.message.reply_text(
        USER,
        reply_markup=reply_markup
    )
    context.user_data['message_id'] = update.message.message_id
    if 'next' in context.user_data:
        del context.user_data['next']
    context.user_data['User'] = user
    return A
def startover(update,context):
    print(context.user_data)
    keyboard = [
        [
            InlineKeyboardButton('Search Course',callback_data='search'),
            InlineKeyboardButton('Choose By year',callback_data='choose_by_year')
        ],
        [InlineKeyboardButton('List All Available Course',callback_data='ListAll')],
    ]
    keyboard.append([InlineKeyboardButton('Exit ❌', callback_data='exit')])
    reply_markup=InlineKeyboardMarkup(keyboard,one_time_keyboard=True)
    chatid = None
    try:
        chatid = update.message.chat.id
        context.user_data['message_id'] = update.message.message_id
    except Exception:
    	try:
    		chatid = update.callback_query.message.chat.id
    		context.user_data['message_id'] = update.callback_query.message.message_id
    		print(update.callback_query.message.message_id)
    	except Exception as e:
    		import traceback; traceback.print_exc();
    		pass
    	import traceback; traceback.print_exc();
    	pass
    bot = context.bot
    # BOT.edit_message_text(
    #     chat_id=chatid,
    #     message_id=context.user_data['message_id'],
    #     text="Please Choose Where your collage!",
    # )
    try:
    	BOT.delete_message(
            chat_id=chatid,
            message_id=context.user_data['message_id']
        )
    except Exception as e:
    	pass
    BOT.send_message(
        chat_id=chatid,
        text="Hi Again",
        reply_markup=reply_markup
    )
    
    #print('start over',context.user_data)
    return A
def collage(update, context):
    bot = context.bot
    query = update.callback_query
    keyboard=[
        [
            InlineKeyboardButton('Applied', callback_data='Applied'),
            InlineKeyboardButton('Engineering', callback_data='Engineering')
        ]
        ,[InlineKeyboardButton('⬅️ Back', callback_data='back')]
    ]
    keyboard.append([InlineKeyboardButton('Exit ❌', callback_data='exit')])
    reply_markup=InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Please Choose Where your collage!",
        reply_markup=reply_markup
    )
    if query.data == 'back' or query.data == 'backcol':
        return B
    if query.data != 'back' or query.data != 'backcol':
        context.user_data['choice'] = query.data
    #print('college ',context.user_data)
    context.user_data['message_id'] = query.message.message_id
    return B

def school(update, context):
    global prev
    prev = school
    bot = context.bot
    query = update.callback_query
    keyboard = []
    data = query.data
    context.user_data['message_id'] = query.message.message_id
    if query.data == 'back' or query.data == 'backcol' or query.data == 'backap':
        if 'college' in context.user_data :
            data = context.user_data['college']
    #print('school ',context.user_data)
    #print('data in college =',data)
    if data == 'Engineering' :
        keyboard = [
            [InlineKeyboardButton('Freshman Division', callback_data='fresh')],
            [InlineKeyboardButton('School of Civil Engineering and Architecture (SOCEA)', callback_data='SOCEA')],
            [InlineKeyboardButton('School of Mechanical, Chemical & Materials Engineering (SoMCME)', callback_data='SoMCME')],
            [InlineKeyboardButton('School of Electrical Engineering & Computing (SoEEC)', callback_data='SoEEC')],
        ] 
    elif data == 'Applied':
           keyboard = [
               [InlineKeyboardButton('Freshman Division', callback_data='fresh')],
               [InlineKeyboardButton('Applied Physics', callback_data='AP')],
               [InlineKeyboardButton('Applied Biology', callback_data='AB')],
               [InlineKeyboardButton('Applied Chemistry', callback_data='AC')],
               [InlineKeyboardButton('Applied Geology', callback_data='AG')],
               [InlineKeyboardButton('Applied Mathematics', callback_data='AM')],
           ]
           context.user_data['school'] = 'Applied'
    keyboard.append([InlineKeyboardButton('⬅️ Back', callback_data='back')])
    keyboard.append([InlineKeyboardButton('Exit ❌', callback_data='exit')])
    reply_markup=InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Please Choose Your School!",
        reply_markup=reply_markup
    )
    if query.data == 'back' or query.data == 'backcol' or query.data == 'backap':
        return C
    if query.data != 'back' or query.data != 'backcol' or query.data != 'backap':
        context.user_data['college'] = query.data
    return C
def dep(update,context):
    bot = context.bot
    query = update.callback_query
    keyboard = list()
    data = query.data
    # if query.data == 'backdep':
    #     #print(context.user_data)
    if query.data == 'back' or query.data == 'backdep' :
        data = context.user_data['school']
    #print('data =', data)
    #print('dep ',context.user_data)
    context.user_data['message_id'] = query.message.message_id
    if data == 'SoEEC':
        keyboard = [ 
            [InlineKeyboardButton('2nd Year 1st Semetser', callback_data='2nd')],
            [InlineKeyboardButton('Computer Science and Engineering (CSE)', callback_data='CSE')],
            [InlineKeyboardButton('Electronics and Communication Engineering (ECE)', callback_data='ECE')],
            [InlineKeyboardButton('Electrical Power and Control Engineering (EPCE)', callback_data='EPCE')]
        ]
    elif data == 'SoMCME' :
        keyboard=[
            [InlineKeyboardButton('2nd Year 1st Semetser', callback_data='2nd')],
            [InlineKeyboardButton('Thermal and Aerospace Engineering', callback_data='TAE')],
            [InlineKeyboardButton('Chemical Engineering', callback_data='CE')],
            [InlineKeyboardButton('Mechanical Design and Manufacturing Engineering', callback_data='MDME')],
            [InlineKeyboardButton('Materials Science and Engineering', callback_data='MSE')],
            [InlineKeyboardButton('Mechanical Systems and Vehicle Engineering', callback_data='MSVE')]
        ]
    elif data == 'SOCEA':
        keyboard=[
            [InlineKeyboardButton('2nd Year 1st Semetser', callback_data='2nd')],
            [InlineKeyboardButton('Architecture', callback_data='Arch')],
            [InlineKeyboardButton('Water Resource Engineering', callback_data='WRE')],
            [InlineKeyboardButton('Civil Engineering', callback_data='CE')]
        ]
    else:
        keyboard=[[InlineKeyboardButton('None',callback_data='None')]]
    keyboard.append([InlineKeyboardButton('⬅️ Back', callback_data='back')])
    keyboard.append([InlineKeyboardButton('Exit ❌', callback_data='exit')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Please Choose Your Department',
        reply_markup=reply_markup
    )
    if query.data == 'back' or query.data == 'backdep':
        return D
    if query.data != 'back' or query.data != 'backdep':
        context.user_data['school'] = query.data
    # #print(context.user_data)
    return D
def year(update, context):
    bot = context.bot
    query = update.callback_query
    context.user_data['message_id'] = query.message.message_id
    keyboard = []
    temp = list()
    for i in range(2,6):
        temp.append(InlineKeyboardButton(str(i), callback_data=str(i)))
    keyboard.append(temp)
    if context.user_data['college'] == 'Applied':
        keyboard.append([InlineKeyboardButton('⬅️ Back', callback_data='backap')])
    else:
        keyboard.append([InlineKeyboardButton('⬅️ Back', callback_data='back')])
    keyboard.append([InlineKeyboardButton('Exit ❌', callback_data='exit')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Please Choose Your Year",
        reply_markup=reply_markup
    )
    

    if query.data != 'back':
        context.user_data['dep'] = query.data
    #print('data =', query.data)
    #print('year ',context.user_data)
    return E
def sem(update, context):
    bot = context.bot
    query = update.callback_query
    context.user_data['message_id'] = query.message.message_id
    keyboard = []
    temp = list()
    if query.data != '2nd' or str(query.data).isdigit():
        context.user_data['year'] = query.data
    if query.data == 'fresh':
        context.user_data['school'] = query.data
    
    for i in range(1,3):
        temp.append(InlineKeyboardButton('Semester ' + str(i), callback_data='sem' + str(i)))
    keyboard.append(temp)
    if context.user_data['year'] == '2' and context.user_data['college'] == 'Engineering':
        keyboard = [[InlineKeyboardButton('Semester ' + str(2), callback_data='sem' + str(2))]]
    if context.user_data['school'] == 'fresh' :
        keyboard.append([InlineKeyboardButton('⬅️ Back', callback_data='backcol')])
    else:
        keyboard.append([InlineKeyboardButton('⬅️ Back', callback_data='back')])
    keyboard.append([InlineKeyboardButton('Exit ❌', callback_data='exit')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Please Choose what Semester you are in",
        reply_markup=reply_markup
    )
    
    # #print(context.user_data)
    #print('data =', query.data)
    #print('sem ',context.user_data)
    return F
def course(update, context):
    with open("course_set.json") as course_set:
        course_set = json.load(course_set)
    print(context.user_data)
    bot = context.bot
    query = update.callback_query
    context.user_data['message_id'] = query.message.message_id
    keyboard = []
    if query.data == '2nd':
        k = course_set["Engineering"]["SoEEC"]["2nd_1st"]
        context.user_data['dep'] = query.data
    elif query.data != 'back':
        context.user_data['sem'] = query.data
    for i in range(1, 6):
        keyboard.append([InlineKeyboardButton('Course ' + str(i), callback_data=str(i))])
    if query.data == '2nd':
        k = course_set["Engineering"]["SoEEC"]["2nd_1st"]
        a = []
        for i in k:
            a.append([InlineKeyboardButton(i[0],callback_data=i[1])])
        keyboard = a
    if 'dep' in context.user_data and context.user_data['dep'] == '2nd':
        keyboard.append([InlineKeyboardButton('⬅️ Back', callback_data='backdep')])
    else:
        keyboard.append([InlineKeyboardButton('⬅️ Back', callback_data='back')])
    if query.data == '2nd':
        k = course_set["Engineering"]["SoEEC"]["2nd_1st"]
        a = []
        for i in k:
            a.append([InlineKeyboardButton(i[0],callback_data=i[1])])
        keyboard = a
    keyboard.append([InlineKeyboardButton('Exit ❌', callback_data='exit')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    if not str(query.data).isdigit():
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="Select a Course",
            reply_markup=reply_markup
        )
    else:
        BOT.send_message(
            chat_id=query.message.chat_id,
            text="You will Recieve Course number " + str(query.data))
        BOT.send_document(
            chat_id=query.message.chat_id,
            document="BQADBAADgggAAiwEGFDt4lwjlYFDvBYE"
        )
        BOT.delete_message(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
        )
        BOT.send_message(
            chat_id=query.message.chat_id,
            text='select Course',
            reply_markup=reply_markup
        )
    return Z
def search(update, context):
    bot = context.bot
    query = update.callback_query
    context.user_data['message_id'] = query.message.message_id
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='''Send me the course You want
<strong>Please Be carefull with spelling</strong>''',
        parse_mode=ParseMode.HTML
    )
    return Z

def ListAll(update,context):
    next = 1
    if 'next' in context.user_data:
        next = int(context.user_data['next'])
    bot = context.bot
    query = update.callback_query
    context.user_data['message_id'] = query.message.message_id
    keyboard = []
    if query.data == 'back':
        next -= 10
    else:
        next += 10
    for i in range(next-10, next):
        keyboard.append([InlineKeyboardButton('Course ' + str(i), callback_data=str(i))])
    keyboard.append([InlineKeyboardButton('Next ➡️', callback_data='next')])
    if next > 11 :
        keyboard.append([InlineKeyboardButton('Back ⬅️', callback_data='back')])
    keyboard.append([InlineKeyboardButton('Exit ❌', callback_data='5')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Select a Course",
        reply_markup=reply_markup
    )
    context.user_data['next'] = next
    return X
def end(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    context.user_data['message_id'] = query.message.message_id
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="See you next time!"
    )
    return ConversationHandler.END
def endtext(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""

    try:
        BOT.delete_message(
            chat_id=update.message.chat.id,
            message_id=context.user_data['message_id']
        )
    except:
        pass
    update.message.reply_text('See you ')
    return ConversationHandler.END
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
def main():
    updater = Updater(token=token['token'], use_context=True)
    dis = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start',start)],
        states=
        {
            A : [  CallbackQueryHandler(collage, pattern='^choose_by_year$'),
                   CallbackQueryHandler(search, pattern='^search$'),
                   CallbackQueryHandler(ListAll, pattern='^ListAll$'),
                   CallbackQueryHandler(end, pattern='^(exit)$')],

            B : [ CallbackQueryHandler(school, pattern='^Engineering|Applied$'),
                  CallbackQueryHandler(startover, pattern='^back$'),
                  CallbackQueryHandler(end, pattern='^(exit)$')],

            C : [ CallbackQueryHandler(dep, pattern='^(SoEEC|SoMCME|SOCEA)$'),
                  CallbackQueryHandler(year, pattern='^(AP|AB|AC|AG|AM)$'),  
                  CallbackQueryHandler(sem,pattern='fresh'),
                  CallbackQueryHandler(collage, pattern='^back$'),
                  CallbackQueryHandler(end, pattern='^(exit)$'),
                ],

            D : [ CallbackQueryHandler(school, pattern='^(back)$'),
                  CallbackQueryHandler(course, pattern='^(2nd)$'),
                  CallbackQueryHandler(end, pattern='^(exit)$'),
                  CallbackQueryHandler(year, pattern=r'[A-Za-z0-9]')],

            E : [ CallbackQueryHandler(dep, pattern='^(back)$'),
                  CallbackQueryHandler(school, pattern='^(backap)$'),
                  CallbackQueryHandler(end, pattern='^(exit)$'),
                  CallbackQueryHandler(sem, pattern=r'[A-Za-z0-9]')],

            F : [ CallbackQueryHandler(year, pattern='^(back)$'),
                  CallbackQueryHandler(school, pattern='^(backcol)$'),
                  CallbackQueryHandler(end, pattern='^(exit)$'),
                  CallbackQueryHandler(course, pattern=r'[A-Za-z0-9]')],

            X : [ CallbackQueryHandler(end, pattern='^(exit)$'),
                  CallbackQueryHandler(ListAll, pattern=r'[A-Za-z]'),
                  CallbackQueryHandler(end, pattern=r'[A-Za-z0-9]'),],

            Z : [ CallbackQueryHandler(dep, pattern='^(backdep)$'),
                  CallbackQueryHandler(sem, pattern='^(back)$'),
                  CallbackQueryHandler(end, pattern='^(exit)$'),
                  CallbackQueryHandler(course, pattern=r'[A-Za-z0-9]'),
                  MessageHandler(Filters.text,endtext)
            ]
        },
        fallbacks=[CommandHandler('cancel',endtext),CommandHandler('start',startover)]
    )
    dis.add_handler(InlineQueryHandler(inlinequery))
    dis.add_handler(conv_handler)
    dis.add_error_handler(error)
    updater.start_polling()
    updater.idle()

    return 0
    
if __name__ == '__main__':
    main()