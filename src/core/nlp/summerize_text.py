from sumy.parsers.html import HtmlParser
# from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "english"
SENTENCES_COUNT = 1


def summerize_text(text):
    text = text.replace("#", " ").replace("\n", " ")
    parser = HtmlParser.from_string(text, "https://www.topsocial.com", Tokenizer(LANGUAGE))
    # or for plain text files
    # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    sentences = summarizer(parser.document, SENTENCES_COUNT)
    return sentences[0] if len(sentences) > 0 else None
    # for sentence in summarizer(parser.document, SENTENCES_COUNT):
    #     print(sentence)
# summerize_text("""با این حال در روزهاى پایانى فصل و با انتشار دوباره شایعه مذاکره اش با پرسپولیس، منصوریان رویه تازه اى براى این هافبک دفاعى در نظر گرفت و در اولین گام نامش را از لیست جدال با الاهلى خط زد. مساله اى که باعث شد تا او به حالت قهر در دو تمرین بعد از این بازى غایب باشد. منصوریان در سفر به مشهد و براى دیدار با پدیده هم بار دیگر نام این بازیکن را از لیست تیمش خط زد تا باقرى و جدایى از پیراهن استقلال به اپیزود پایانى خود نزدیک شود.
#
# از آنجایی که برانکو هم در پایان فصل پیش و هم در نقل و انتقالات نیم فصل علاقه خود به جذب این بازیکن را نشان داده بود و در نهایت ناکام مانده بود، حالا مرد کروات امیدوار شده تا سومین تیرش در جذب باقری به هدف بخورد و پیراهن پرسپولیس را به هافبک استقلال هدیه بدهد. اتفاقی که به زودی رخ خواهد داد.
#  """)