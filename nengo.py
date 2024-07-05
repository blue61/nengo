# Nengo calculation from a western date
# does only work in the known reigns
import datetime

def japdigit(n: int) -> str:
    """ get a japanese kanji digit as a unicode character.
    may be called for arguments 0..9 
    """
    # check for invalid values
    assert(n >= 0)
    assert(n < 10)
    jdigits= "零一二三四五六七八九十"
    s = jdigits[n]
    return s

def japnum(n : int) -> str:
    """ get a japanese kanji number as a unicode character sequence.
    may be called for arguments 0..99 
    """
    # check for invalid values
    assert(n >= 0)
    assert(n < 100)
    if n > 10:
        einer = n % 10
        n = (n - einer) // 10
    else:
        einer = n
        n = 0
    if n > 0:
        zs = japdigit(n)
        zs += '十'
    else:
        zs = ""
    if einer > 0:
        es = japdigit(einer)
    else:
        es = ""
    return zs + es

# ---------------------------------------------------------------------

# startdate of Nengos
meiji_start = datetime.date( 1868, 1, 8 )
taisho_start = datetime.date( 1912, 7, 30)
showa_start = datetime.date( 1926, 12, 25)
heisei_start = datetime.date( 1989, 1, 8 )
reiwa_start = datetime.date( 2019, 5, 1 )

#meiji_s = "meiji (明治)"
#taisho_s = "taisho (大正)"
#showa_s = "showa (正和)"
#heisei_s = "heisei (平成)"
#reiwa_s = "reiwa (令和)"

# Names of Nengos in Kanji
meiji_s = "明治"
taisho_s = "大正"
showa_s = "正和"
heisei_s = "平成"
reiwa_s = "令和"

# aus wikipedia.de:
# Das erste Jahr einer Periode – das sich ja nicht mit dem westlichen Kalender deckt – 
# wird als gannen (元年) bezeichnet. Das heißt z. B. 1989 ist bis zum 7. Januar = Shōwa 64, 
# danach dann Heisei gannen. 
gannen_s = "元年"

blank_s = " "

# ---------------------------------------------------------------------
def nengo_jahr(dd : datetime) -> (str, str):
    """ return the Nengo Year as Nengo Name and Year-Name. 
    the Year-Name is either gannen for the very first year, 
    or the number of years converted to kanji. 
    the return value is a tuple (Nengo-Name, Jahr-Name)
    """
    if dd > reiwa_start:
        diff = dd - reiwa_start
        nengo_name = reiwa_s
    elif dd > heisei_start:
        diff = dd - heisei_start
        nengo_name = heisei_s
    elif dd > showa_start:
        diff = dd - showa_start
        nengo_name = showa_s
    elif dd > taisho_start:
        diff = dd - taisho_start
        nengo_name = taisho_s
    elif dd > meiji_start:
        diff = dd - meiji_start
        nengo_name = meiji_s
    else:
        raise ValueError
    
    nengo_jahr = 1 + diff.days // 365
    if nengo_jahr > 1:
        jahr_name = japnum(nengo_jahr)
    else:
        jahr_name = gannen_s
    return (nengo_name, jahr_name)
    

# ------------------------------------------------------------

# siehe https://www.japanwelt.de/blog/monatsnamen-wochentagsbezeichnung-japan
# traditional month names
# "Mutsuki (睦月)",                            # Jan
# "Kisaragi (如月) or Kinusaragi (衣更着)",    # Feb
# "Yayoi (弥生)",                               # März
# "Uzuki (卯月)",                               # April
# "Satsuki (皐月/早月)",                         # Mai
# "Minatsuki  Minazuki (水無月)",            # Juni
# "Fumizuki (文月)",                            # Juli 
# "Hazuki (葉月)",                              # August
# "Nagatsuki (長月)",                           # September
# "Kaminazuki oder Kannazuki (神無月)",         # Oktober
# "Kamiarizuki (神在月)",                       # November
# "Shiwasu (師走)",                             # Dezember


def nengo(datumstr: str) -> str:
    """ errechne einen String für das japanische nengo datum.
    
    Nengo-Name Jahres-Kanjizahl 年 Monats-Kanjizahl 月 (trad. Monat) Tagesdatum-Kanjizahl 日 (Wochentag)
    
    Beispiele:
    13.5.1961 ->
    正和三十五年五月(皐月)三十一日(水曜日)

    7.2.1966 ->
    正和四十年二月(如月)七日(月曜日)

    29.12.1961 ->
    正和三十六年一十二月(師走)二十九日(金曜日)

    19.3.1997 ->
    平成九年三月(弥生)一十九日(水曜日)

    """
    # split the given date
    ts, ms, js = datumstr.split(".")

    # convert to integer numbers
    jj = int(js)
    mm = int(ms)
    tt = int(ts)

    # convert to a datetime
    dd = datetime.date(jj,mm,tt)

    # some kanji's used later
    year_k = "年"
    month_k = "月" 
    day_k = "日" 

    # names in Kanji only, and only the first if there are more than one
    trad_mon_ks= [ "(睦月)",   # Jan
                "(如月)",    # Feb
                "(弥生)",    # März
                "(卯月)",    # April
                "(皐月)",    # Mai
                "(水無月)",  # Juni
                "(文月)",    # Juli 
                "(葉月)",    # August
                "(長月)",    # September
                "(神無月)",  # Oktober
                "(神在月)",  # November
                "(師走)",    # Dezember
              ]

    # weekday names
    weekday_st = [
        "(月曜日)",   # Montag
        "(火曜日)",   # Dienstag
        "(水曜日)",   # Mittwoch 
        "(木曜日)",   # Donnerstag 
        "(金曜日)",   # Freitag 
        "(土曜日)",	  # Samstag
        "(日曜日)",   # Sonntag
    ]

    # main calculation
    nengo_tupel = nengo_jahr(dd)
    trad_mon = trad_mon_ks[ mm-1 ]  # the index starts with 0, the months with 1
    weekday = weekday_st[dd.weekday()]
    retval = nengo_tupel[0] + blank_s + \
        nengo_tupel[1] + year_k + blank_s + \
        japnum(mm) + month_k + blank_s + \
        trad_mon + blank_s + \
        japnum(tt) + day_k + blank_s + \
        weekday
    return retval



if __name__ == "__main__":
    # request the western date. seperated by .   Format: DD.MM.YYY
    # Hint: this would need to be localized
    datumstr = input("Westliches Datum: ")

    try:
        print( nengo( datumstr ) )
    except ValueError:
        print("Error, date is out of range")

