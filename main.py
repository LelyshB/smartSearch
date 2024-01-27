import os
import re
from nltk.tokenize import word_tokenize
from collections import Counter
import nltk
from nltk.stem.snowball import RussianStemmer

nltk.download('punkt')

# Инициализация стеммера
stemmer = RussianStemmer()

# Функция для стемминга ключевых слов
def stem_keywords(keywords):
    return [stemmer.stem(word) for word in keywords]

# Функция для стемминга текста
def stem_text(text):
    return ' '.join([stemmer.stem(word) for word in word_tokenize(text.lower())])

# Функция для извлечения ключевых слов из запроса пользователя
def extract_keywords(query):
    return query.split()

# Функция для ранжирования документов
def rank_docs(docs, keywords, pod_dict):
    stemmed_keywords = stem_keywords(keywords)
    ranked_docs = {}
    for name, text in docs.items():
        stemmed_text = stem_text(text)
        
        # Сначала подсчитываем совпадения с ключевыми словами из запроса в под
        pod_score = sum([keyword_search(k, ' '.join(pod_dict.get(name, []))) for k in stemmed_keywords])
        
        # Затем подсчитываем совпадения в самом тексте
        keyword_score = sum([keyword_search(k, stemmed_text) for k in stemmed_keywords])
        
        # Итоговый счет — это сумма подсчетов
        total_score = pod_score * 2 + keyword_score  # умножение pod_score на 2 для приоритета
        
        if total_score > 0:
            ranked_docs[name] = total_score
            
    return dict(sorted(ranked_docs.items(), key=lambda item: item[1], reverse=True))

    stemmed_keywords = stem_keywords(keywords)
    ranked_docs = {}
    for name, text in docs.items():
        stemmed_text = stem_text(text)
        pod_score = sum([keyword_search(k, stemmed_text) for k in pod_dict.get(name, []) if k in stemmed_keywords])
        keyword_score = sum([keyword_search(k, stemmed_text) for k in stemmed_keywords])
        total_score = pod_score + keyword_score
        if total_score > 0:
            ranked_docs[name] = total_score
    return dict(sorted(ranked_docs.items(), key=lambda item: item[1], reverse=True))

# Функция для поиска ключевого слова в тексте
def keyword_search(keyword, text):
    return len(re.findall(f'\\b{keyword}\\b', text, re.IGNORECASE))

pod_dict = {
    'doc1.txt': ['книга', 'изобретение', 'вопросы'],
    'doc2.txt': ['современные дети', 'чтение', 'книги', 'родители', 'мотивация', 'интересы', 'возраст', 'семейные', 'выбор'],
    'doc3.txt': ['книга', 'изобретение', 'вопросы', 'ответы', 'компьютеры', 'чтение', 'развитие', 'любовь'],
    'doc4.txt': ['книга', 'литература', 'чтение',  'картина мира личности', 'язык'],
    'doc5.txt': ['книга', 'текст', 'виртуальная',  'воображение', 'интернет', 'мышление'],
    'doc6.txt': ['чтение', 'книга', 'автор', 'текст', 'способы чтения'],
    'doc7.txt': ['прочитанное','информация','впечатления','ассоциации','повторение'],
    'doc8.txt': ['художественная литература','книга','чтение','эмпатия','словарный','запас','образное', 'воображение'],
    'doc9.txt': ['старые', 'продажа', 'магазин' , 'покупатель', 'цена','книги'],
    'doc10.txt': ['книга','фольклор', 'писатель', 'клоун', 'сказка','Стивен','Кинг'],    
}

# Основной код
docs = {}
for i in range(1, 11):
    filename = f'doc{i}.txt'
    with open(filename, 'r', encoding='utf-8') as file:
        docs[filename] = file.read()

# Пример запрещенных слов
forbidden_words = ["запрещенный", "запретный"]

# Фильтрация
filtered_docs = {name: text for name, text in docs.items() if all(word.lower() not in text.lower() for word in forbidden_words)}

# Получение запроса пользователя
user_query = input("Введите ваш запрос: ")
keywords = extract_keywords(user_query)

# Ранжирование документов
ranked_docs = rank_docs(filtered_docs, keywords, pod_dict)

# Вывод результатов
for doc_name, score in ranked_docs.items():
    print(f"Документ: {doc_name}, Общий счет: {score}")