import re
import scraper
import nltk
import pandas as pd
from nltk.corpus import stopwords
from unidecode import unidecode


def limpeza_html(txt):
    txt_tratado = re.sub('&.*;| YjFXEf;_;\\$\\d{1,2}">|<span class="X43Kjb">(?=Shipp)', '', txt)

    txt_tratado = re.sub('<div jscontroller="H6eOGe" jsmodel="y8Aajc" jsdata="yf3HXc;_;\\$',
                         '\n-----------\nN_', txt_tratado)

    txt_tratado = re.sub('<div class="bAhLNe kx8XBd"><span class="X43Kjb">', '\nNome: ', txt_tratado)
    txt_tratado = re.sub('</span>.*<div aria-label="', '\nAvaliação: ', txt_tratado)
    txt_tratado = re.sub('<div>Shipp do Brasil Tecnologia', '\nResposta: ', txt_tratado)
    txt_tratado = re.sub('" role="img">.*"p2TkOb">', '\nData: ', txt_tratado)

    txt_tratado = re.sub('</span>.*<span jsname="fbQN7e" style="">', '\nComentario: ', txt_tratado)
    txt_tratado = re.sub('</span>.*<span jsname="bN97Pc">', '\nComentario: ', txt_tratado)

    txt_tratado = re.sub('</span>.*<div class="bAhLNe kx8XBd">|<.*>', '', txt_tratado)
    txt_tratado = re.sub(' {2,}|[<>]|^"},', '', txt_tratado)
    txt_tratado = re.sub('\n{2,}', ' ', txt_tratado)

    txt_tratado = re.sub('Avaliado com 5 de 5 estrelas', '5', txt_tratado)
    txt_tratado = re.sub('Avaliado com 4 de 5 estrelas', '4', txt_tratado)
    txt_tratado = re.sub('Avaliado com 3 de 5 estrelas', '3', txt_tratado)
    txt_tratado = re.sub('Avaliado com 2 de 5 estrelas', '2', txt_tratado)
    txt_tratado = re.sub('Avaliado com 1 de 5 estrelas', '1', txt_tratado)

    txt_tratado = re.sub(' de janeiro de ', '/1/', txt_tratado)
    txt_tratado = re.sub(' de fevereiro de ', '/2/', txt_tratado)
    txt_tratado = re.sub(' de março de ', '/3/', txt_tratado)
    txt_tratado = re.sub(' de abril de ', '/4/', txt_tratado)
    txt_tratado = re.sub(' de maio de ', '/5/', txt_tratado)
    txt_tratado = re.sub(' de junho de ', '/6/', txt_tratado)
    txt_tratado = re.sub(' de julho de ', '/7/', txt_tratado)
    txt_tratado = re.sub(' de agosto de ', '/8/', txt_tratado)
    txt_tratado = re.sub(' de setembro de ', '/9/', txt_tratado)
    txt_tratado = re.sub(' de outubro de ', '/10/', txt_tratado)
    txt_tratado = re.sub(' de novembro de ', '/11/', txt_tratado)
    txt_tratado = re.sub(' de dezembro de ', '/12/', txt_tratado)

    txt_tratado = re.sub('a{2,}', 'a', txt_tratado)
    txt_tratado = re.sub('e{2,}', 'e', txt_tratado)
    txt_tratado = re.sub('i{2,}', 'i', txt_tratado)
    txt_tratado = re.sub('o{2,}', 'o', txt_tratado)
    txt_tratado = re.sub('u{2,}', 'u', txt_tratado)

    txt_tratado = re.sub('[Vv][Ii][Ll][Aa] [Vv][Ee][Ll][Hh][Aa]', 'vilavelha', txt_tratado)
    txt_tratado = re.sub('[Nn]ão', 'nao', txt_tratado)

    txt_tratado = re.sub('[꧁༺꧂ø,.!@;><$*"#%+=(){}?]|\\.\\.\\.| r\\$ |'
                         'você|diz|ainda| pra | ter |sms', '', txt_tratado)

    print(txt_tratado)
    return txt_tratado


def html_to_table(txt):
    comentario_tratado = limpeza_html(txt)

    numero = re.findall('N_\\d{1,5}', comentario_tratado)
    nome = re.findall('Nome: .*', comentario_tratado)
    aval = re.findall('Avaliação: .*', comentario_tratado)
    data = re.findall('Data: .*', comentario_tratado)
    coment = re.findall('Comentario: .*', comentario_tratado)

    dict_coment = {'num':numero,
                   'nome': nome,
                   'aval': aval,
                   'data': data,
                   'coment':coment}

    return dict_coment


def lemmatize_text(txt):
    stop_list = set(stopwords.words('portuguese'))
    return [lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(txt) if w not in stop_list and len(w) >= 3]


def export_data(raw_txt):
    comentarios = raw_txt.read()
    dict_coment = html_to_table(comentarios)

    df = pd.DataFrame().from_dict(dict_coment)
    df['num'] = df['num'].str.replace('N_', '')
    df['nome'] = df['nome'].str.replace('Nome: ', '')
    df['aval'] = df['aval'].str.replace('Avaliação: ', '')
    df['data'] = df['data'].str.replace('Data: ', '')
    df['coment'] = df['coment'].str.replace('Comentario: ', '')
    df['coment'] = df['coment'].str.replace('\\d{1,}', '')
    df['coment'] = df['coment'].str.lower()
    df['coment'] = df['coment'].str.replace('aapp|aplicativo', 'app')

    df['text_lemmatized'] = df.coment.apply(lemmatize_text).astype(str)
    df['lemma'] = df['text_lemmatized'].str.replace(']|\\[|\'| {2,}|,|/', '').apply(unidecode)

    print(df.to_string())

    df.to_csv('tabela_comentario.csv', encoding='utf-16', index=False)


w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()

raw_html = open('comentarios.txt', 'r', encoding='utf-8')


if __name__ == "__main__":
    export_data(raw_html)
