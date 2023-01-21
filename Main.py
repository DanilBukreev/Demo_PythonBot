!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import Update
import logging
from telegram.ext import CommandHandler, CallbackQueryHandler,ContextTypes, ApplicationBuilder
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import sqlite3
import ssl
import pandas as pd
import certifi
import math



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



logging.info("Bot has been started successfully")



async def InitNullValues(context):
    ############################### Init category1_tag_name ############################################
    listOfkeyCat1 = ['CheckLabelShow','CheckLabelSport','..............']
    for i in listOfkeyCat1:
        context.user_data[i] = " "
    ############################### Init Tables########################################################
    listOfkeydt=['AnswersArray','split_dataframes','................']
    for dt in listOfkeydt:
        context.user_data[dt] = []
    ############################### Init category2_tag_name ############################################
    listOfkeyCat2 = ['CheckLabelSW','CheckLabelCity','CheckLabelAnime','CheckLabelGoT','CheckLabelLotR','CheckLabelCrazy','CheckLabelMemes','CheckLabelBrawlStars','CheckLabelOutCity','CheckLabelDriving','CheckLabelBeer','CheckLabelStringAlc','CheckLabelVine','CheckLabelGuitar','CheckLabelMusic20','CheckLabelBusiness']
    for j in listOfkeyCat2:
        context.user_data[j] = " "
    ############################### Prices #############################################################




def DataNormalizer(context):
    AnswersArray = context.user_data.get('AnswersArray', 'Not found')
    for i in range(len(AnswersArray)):
        if AnswersArray[i]=='Male':
            AnswersArray[i]='Одному человеку (М)'
        elif AnswersArray[i]=='Female':






async def telegram_bot_sendtext(bot_message,update: Update, context: ContextTypes.DEFAULT_TYPE,phototext):
    url="https://docs.python-telegram-bot.org/en/v20.0a6/telegram.bot.html"
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_message,parse_mode="HTML", disable_web_page_preview=True)
    await context.bot.send_photo(chat_id=update.effective_chat.id,photo=phototext,caption=bot_message,parse_mode="HTML")



async def db_SelectGenMenu (update: Update, context: ContextTypes.DEFAULT_TYPE):
    DataNormalizer(context)
    AnswersArraytemp = context.user_data.get('AnswersArray', 'db_SelectMenu_Not found')
    context.user_data["df_SelectGenMenu"] =[]
    df_SelectGenMenu=context.user_data.get('df_SelectGenMenu', 'db_SelectGenMenu_Not found')
    logging.info("После нормализации вектор выгляжит так")
    logging.info(AnswersArraytemp)
    conn = sqlite3.connect('DataBase/GiftPickerdb.db', check_same_thread=False)
    df_SelectGenMenu = pd.read_sql_query("Select category1_tag_name,category2_tag_name, price_tag_name From Gifts WHERE gift_recipients_tag_name LIKE '%{0}%' AND age_tag_name LIKE '%{1}%'".format(AnswersArraytemp[0], AnswersArraytemp[1]),conn)
    conn.close()
    #del AnswersArraytemp[0:2]
    df_SelectGenMenu["Flag"] = 0
    for items in AnswersArraytemp:
        for index, row in df_SelectGenMenu.iterrows():
            if items in str(row["price_tag_name"]):
                FlagValue = df_SelectGenMenu.iloc[index, 3]
                df_SelectGenMenu.at[index, "Flag"] = int(FlagValue) + 1


    MaxValue=df_SelectGenMenu["Flag"].max()
    selecteddf = df_SelectGenMenu.loc[df_SelectGenMenu['Flag'] >= int(MaxValue)]
    #del selecteddf[0]
    uniquelist=selecteddf['category1_tag_name'].unique()
    uniquelistCat2=selecteddf['category2_tag_name'].unique()
    context.user_data["uniquelist"] = uniquelist
    context.user_data["uniquelistCat2"] = uniquelistCat2

    if len(uniquelist)==1 and uniquelist[0]=='Universal':
        logging.info("Нет категорий первого уровня")
        await db_GiftQueury(update,context)
    else:
        await GenerateBottonsSubCategoryOne(update, context)


async def db_GiftQueury (update: Update, context: ContextTypes.DEFAULT_TYPE):
    DataNormalizer(context)
    AnswersArray = context.user_data.get('AnswersArray', 'Not found')

    logging.info("После нормализации вектор выгляжит так")
    logging.info(AnswersArray)
    conn = sqlite3.connect('*.db', check_same_thread=False)
    df = pd.read_sql_query("Select * From ********** LIKE '%{0}%' AND ***************** LIKE '%{1}%'".format(AnswersArray[0], AnswersArray[1]), conn)
    df2 = pd.read_sql_query(
        "Select * From *********** LIKE '%Universal%' OR  LIKE '%Universal%'  ",
        conn)
    lenArray = len(AnswersArray)
    logging.info("длинна массива выборки из БД - {0}".format(lenArray))
    logging.info(AnswersArray)
    df["Flag"] = 0
    df2["Flag"] = 0
    join_dfs = pd.DataFrame
    for items in AnswersArray:
        for index, row in df.iterrows():
            if items in str(row["category1_tag_name"]):
                FlagValue = df.iloc[index, 10]
                df.at[index, "Flag"] = int(FlagValue) + 1
            if items in str(row["category2_tag_name"]):
                FlagValue = df.iloc[index, 10]
                df.at[index, "Flag"] = int(FlagValue) + 1
            if items in str(row["gift_recipients_tag_name"]):
                FlagValue = df.iloc[index, 10]
                df.at[index, "Flag"] = int(FlagValue) + 1
            if items in str(row["age_tag_name"]):
                FlagValue = df.iloc[index, 10]
                df.at[index, "Flag"] = int(FlagValue) + 1
            if items in str(row["price_tag_name"]):
                FlagValue = df.iloc[index, 10]
                df.at[index, "Flag"] = int(FlagValue) + 1

    for items in AnswersArray:
        for index2, row2 in df2.iterrows():
            if items in str(row2["gift_recipients_tag_name"]):
                FlagValue2 = df2.iloc[index2, 10]
                df2.at[index2, "Flag"] = int(FlagValue2) + 1
            if items in str(row2["age_tag_name"]):
                FlagValue2 = df2.iloc[index2, 10]
                df2.at[index2, "Flag"] = int(FlagValue2) + 1
            if items in str(row2["price_tag_name"]):
                FlagValue2 = df2.iloc[index2, 10]
                df2.at[index2, "Flag"] = int(FlagValue2) + 1

    selecteddf = df.loc[df['Flag'] >= 5]
    selecteddf=selecteddf.sample(frac=1,random_state=1).reset_index()
    try:
        selecteddf.iloc[-1, selecteddf.columns.get_loc('Flag')] = 403
    except IndexError:
        logging.info("Таблица с подарками второй категории пуста")
    # print(selecteddf)
    selectedUni = df2.loc[df2['Flag'] >= 3]
    selectedUni=selectedUni.sample(frac=1,random_state=1).reset_index()
    # print(selectedUni)
    join_dfs = pd.concat([selecteddf, selectedUni])

    #join_dfs.sample(frac=1)
    logging.info("кол-во строк таблицы по категориям: {0}".format(len(join_dfs)))
    if len(join_dfs)<=3:
        split_dataframes=join_dfs
        context.user_data['split_dataframes'] = split_dataframes
        await PartitionAnswer(split_dataframes, update, context)
    else:
        split_dataframes = await split_dataframe_by_position(join_dfs, 3)
        context.user_data['split_dataframes'] = split_dataframes
        await PartitionAnswer(split_dataframes[0],update,context)



async def split_dataframe_by_position(df,splits):
    dataframes = []
    index_to_split = 3
    splits = math.ceil(len(df) / 3)
    start = 0
    end = index_to_split
    for split in range(splits):
        temporary_df = df.iloc[start:end, :]
        if temporary_df.empty:
            continue
        dataframes.append(temporary_df)
        start += index_to_split
        end += index_to_split
    return dataframes


async def PartitionAnswer(df,update: Update, context):
    split_dataframes = context.user_data.get('split_dataframes', 'Not found')
    for index,row in df.iterrows():
        gift_name = row["gift_name"]
        Flag=row["Flag"]
        gift_price = row["gift_price"]
        gift_comment = row["gift_comment"]
        gift_link = row["gift_link"]
        gift_id=str(row["gift_id"])
        phototext="Photo/" + gift_id + ".PNG"
        text = f'<a href="{gift_link}">▶️ Ссылка ◀️</a>'
        bot_message = '<b>'+gift_name+'</b>'+ '\n' + '\n' + gift_comment+ '\n' + '\n' +  '💰Цена: <b>'+str(gift_price)+'</b>'+ '\n' +  '\n' + text
        #bot_message = 'Фотка: {здесь будет фотка}' + '\n' + '*'+gift_name+'*'+ '\n' +gift_comment+ '\n' + 'Цена: *'+str(gift_price)+'*'+ '\n' + 'Ссылка: ' + gift_link
        #bot_message = 'Заголовок:'+gift_name
        #print(bot_message)
        await telegram_bot_sendtext(bot_message,update,context,phototext)
        if Flag==403:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=SelectedCatVariants(), parse_mode="HTML")

        logging.info("Отправили первую рассылку ")
    #if len(split_dataframes) <= 3:
    #    await context.bot.send_message(chat_id=update.effective_chat.id, text=EndVariants_message(),reply_markup=main_menu_keyboard(),parse_mode="HTML")
    #else:
    try:
        del split_dataframes[0]
        context.user_data['split_dataframes'] = split_dataframes
        if not split_dataframes:
            logging.info("Таблица пуста")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=EndVariants_message(), reply_markup=main_menu_keyboard(), parse_mode="HTML")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Показать еще варианты? ",reply_markup=partition_keyboard(),parse_mode="HTML")
    except KeyError:
        logging.info("Ошибка при удалении элемента таблицы")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=EndVariants_message(),
                                       reply_markup=main_menu_keyboard(), parse_mode="HTML")

    

async def PartitionAnswer2(update: Update, context):
    split_dataframes = context.user_data.get('split_dataframes', 'Not found')
    if not split_dataframes:
        logging.info("Таблица пуста")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=EndVariants_message(), reply_markup=main_menu_keyboard(), parse_mode="HTML")
    else:
        await PartitionAnswer(split_dataframes[0],update,context)
    #await context.bot.send_message(chat_id=update.effective_chat.id, text="Показать еще варианты? ",reply_markup=partition_keyboard(),parse_mode="HTML")
   # if len(split_dataframes)==0:
   #     print("последний вариант был отправлен. Вызов меню")
   #     await context.bot.send_message(chat_id=update.effective_chat.id, text=EndVariants_message() ,reply_markup=partition_keyboard(),parse_mode="HTML")
       #await context.bot.send_message(chat_id=update.effective_chat.id, text="Показать еще варианты? ",reply_markup=partition_keyboard(),parse_mode="HTML")




def GlobalVarUpdate(update,context, NeedAdd: bool):
    GlobeChosenFunc =str(update.callback_query.data)
    context.user_data['GlobeChosenFunc'] = GlobeChosenFunc
    if NeedAdd:
        AnswersArray = context.user_data.get('AnswersArray', 'GVU_Not found')
        AnswersArray.append(GlobeChosenFunc)
        context.user_data['AnswersArray'] = AnswersArray
    logging.info(GlobeChosenFunc)


def GlobalVarUpdateAge(update,context):  # Мега костыль
    GlobeChosenFunc =str(update.callback_query.data)
    context.user_data['GlobeChosenFunc'] = GlobeChosenFunc
    AnswersArray = context.user_data.get('AnswersArray', 'GVU_Not found')
    listAge=['0 - 10 лет', '11-17 лет', '18-29 лет', '30-45 лет', '45-59 лет', '60 лет']
    if any(ext in GlobeChosenFunc for ext in listAge):
        AnswersArray.append(GlobeChosenFunc)
        context.user_data['AnswersArray'] = AnswersArray
    if  '10 лет' in GlobeChosenFunc :
        AnswersArray.append(GlobeChosenFunc)
        context.user_data['AnswersArray'] = AnswersArray




def SwitchCase(in_argument,context):

    CheckLabelShow = context.user_data.get('CheckLabelShow', 'Not found')
    CheckLabelGames = context.user_data.get('CheckLabelGames', 'Not found')
    AnswersArray = context.user_data.get('AnswersArray', 'Not found')
    CheckLabelSport = context.user_data.get('CheckLabelSport', 'Not found')
    CheckLabelTeam = context.user_data.get('CheckLabelTeam', 'Not found')
    CheckLabelHumour = context.user_data.get('CheckLabelHumour', 'Not found')
    CheckLabelMaster = context.user_data.get('CheckLabelMaster', 'Not found')
    CheckLabelDrink = context.user_data.get('CheckLabelDrink', 'Not found')
    CheckLabelCars = context.user_data.get('CheckLabelCars', 'Not found')
    CheckLabelMusic = context.user_data.get('CheckLabelMusic', 'Not found')
    CheckLabelFazenda = context.user_data.get('CheckLabelFazenda', 'Not found')
    CheckLabelNew = context.user_data.get('CheckLabelNew', 'Not found')
    CheckLabelGym = context.user_data.get('CheckLabelGym', 'Not found')
    match in_argument:
        case "Залипнуть в сериал"|"Movie"|"Залипнуть в сериал✅"|"Movie✅":
            if CheckLabelShow in "✅":
                context.user_data['CheckLabelShow'] = " "
                try:
                    AnswersArray.remove("Залипнуть в сериал")
                    context.user_data['AnswersArray'] = AnswersArray
                except ValueError:
                    AnswersArray.remove("Movie")
                    context.user_data['AnswersArray'] = AnswersArray
                logging.info("state of check - "+ CheckLabelShow)
            else:
                CheckLabelShow = "✅"
                context.user_data['CheckLabelShow'] = CheckLabelShow
                AnswersArray.append(in_argument)
                context.user_data['AnswersArray'] = AnswersArray
        case "Рубиться в онлайн игры"|"Games"|"Рубиться в онлайн игры✅"|"Games✅":
            if CheckLabelGames in "✅":
               context.user_data['CheckLabelGames'] = " "
               try:
                   AnswersArray.remove("Рубиться в онлайн игры")
                   context.user_data['AnswersArray'] = AnswersArray
               except ValueError:
                   AnswersArray.remove("Games")
                   context.user_data['AnswersArray'] = AnswersArray
               logging.info("state of check - " + CheckLabelGames)
            else:
               CheckLabelGames = "✅"
               context.user_data['CheckLabelGames'] = CheckLabelGames
               AnswersArray.append(in_argument)
               context.user_data['AnswersArray'] = AnswersArray
 

############################### Bot ############################################
async def start(update, context):
  await update.message.reply_text(main_menu_message(),
                            reply_markup=main_menu_keyboard())
  global User_ID
  User_ID = str(update.message.from_user['id'])
  ############################### Init args ############################################
  await InitNullValues(context)
  ############################### Init Labels  ############################################

  connUsers = sqlite3.connect('*.db', check_same_thread=False)
  cursorUsers = connUsers.cursor()
  User_ID = str(update.message.from_user['id'])
  User=update.message.from_user['username']
  cursorUsers.execute('INSERT INTO Users (UserID,Username) VALUES (?,?)',(User_ID,User))
  connUsers.commit()
  connUsers .close()



async def main_menu(update,context):  # Главное меню
  await InitNullValues(context)
  query = update.callback_query
  await query.answer()
  await query.edit_message_text(
                        text=main_menu_message(),
                        reply_markup=main_menu_keyboard())

async def F11_submenu(update,context):  # Меню выбора М или Ж...
  context.user_data['AnswersArray'] = []
  await InitNullValues(context)
  query = update.callback_query
  await query.answer()
  await query.edit_message_text(
                        text=F11_menu_message(),
                        reply_markup=F11_submenu_keyboard())

async def F12_submenu(update, context):   #меню возраста
    GlobalVarUpdate(update,context, NeedAdd=True)
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
          text=F12_menu_message(),
          reply_markup=F12_submenu_keyboard())



async def GenerateBottons(update,context):
    GlobalVarUpdate(update,context, NeedAdd=False)
    GlobeChosenFunc = context.user_data.get('GlobeChosenFunc', 'Not found')
    SwitchCaseDinamicMenu(GlobeChosenFunc.strip(),context)
    AnswersArray = context.user_data.get('AnswersArray', 'Not found')
    uniquelistCat2 = context.user_data.get('uniquelistCat2', 'cat2_Not Found')
    logging.info("array is " + str(AnswersArray))
    query = update.callback_query
    await query.answer()


    list_of_Categories = []
    if "Залипнуть в сериал" in AnswersArray or  "Movie" in AnswersArray:
        if 'Аниме' in uniquelistCat2:
            list_of_Categories.append('Аниме'+CheckLabelAnime)
        if 'Игра престолов' in uniquelistCat2:
            list_of_Categories.append('Игра престолов'+CheckLabelGoT)
        if 'Властелин колец' in uniquelistCat2:
            list_of_Categories.append('Властелин колец'+CheckLabelLotR)
        if 'Звёздные войны' in uniquelistCat2:
            list_of_Categories.append('Звёздные войны' + CheckLabelSW)


    list_of_Categories.append('Подтвердить выбор')
    list_of_Categories.append('В главное меню')
    button_list = []
    for each in list_of_Categories:
        if "Подтвердить выбор" in each:
            button_list.append(InlineKeyboardButton("➡️Подтвердить выбор", callback_data="access"))
        elif "В главное меню" in each:
            button_list.append(InlineKeyboardButton("🏠В главное меню", callback_data="main"))
        else:
            button_list.append(InlineKeyboardButton(each, callback_data=each))
    reply_markup = InlineKeyboardMarkup(
        build_menu(button_list, n_cols=1))  # n_cols = 1 is for single column and mutliple rows
    if "Провести отдых активно" in AnswersArray or "Sport"  in AnswersArray or "Рубиться в онлайн игры" in AnswersArray or "Games" in AnswersArray or "Узнавать новое" in AnswersArray or  "New" in AnswersArray or "Разбираться в музыке" in AnswersArray or  "Music" in AnswersArray or "Разбираться в машинах" in AnswersArray or  "Cars" in AnswersArray or "Пропустить бокальчик" in AnswersArray or  "Drink" in AnswersArray or "Залипнуть в сериал" in AnswersArray or  "Movie" in AnswersArray or "Всё ОК с чувством юмора" in AnswersArray or  "Humour" in AnswersArray:
        context.user_data['AnotherMenuFlag'] = False
    else:
        context.user_data['AnotherMenuFlag'] = True
    AnotherMenuFlag = context.user_data.get('AnotherMenuFlag', 'GB_AMF_Not found')
    if AnotherMenuFlag:
        logging.info("нет подкатегорий")
        await db_GiftQueury(update,context)
    else:
        await query.edit_message_text(text=F14_menu_message(), reply_markup=reply_markup)




############################ Keyboards #########################################
def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton('➡️ Выбрать подарок', callback_data='m1')]]
  return InlineKeyboardMarkup(keyboard)
def F11_submenu_keyboard():

  keyboard = [[InlineKeyboardButton('Одному человеку (М 🙋‍♂️)', callback_data='Male')],
              [InlineKeyboardButton('Одному человеку (Ж 🙋‍♀️)', callback_data='Female')],
              [InlineKeyboardButton('Паре', callback_data='Паре')],
              [InlineKeyboardButton('Всей семье', callback_data='Всей семье')],
              [InlineKeyboardButton('🏠 В главное меню', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
  menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu
