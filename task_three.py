"""Завдання 3. Порівняти ефективність алгоритмів пошуку підрядка: Боєра-Мура, 
Кнута-Морріса-Пратта та Рабіна-Карпа на основі двох текстових 
файлів (стаття 1, стаття 2). Використовуючи timeit, треба виміряти час 
виконання кожного алгоритму для двох видів підрядків: одного, що дійсно 
існує в тексті, та іншого — вигаданого (вибір підрядків за вашим бажанням). 
На основі отриманих даних визначити найшвидший алгоритм для кожного тексту 
окремо та в цілому."""

import timeit
import pandas as pd

# Функція для алгоритму Боєра-Мура
def boyer_moore(text, pattern):
    """Функція для пошуку підрядка в тексті за алгоритмом Боєра-Мура."""
    m = len(pattern)
    n = len(text)
    if m > n:
        return -1  # Повертає -1, якщо шаблон довший за текст
    skip = [m] * 65536  # Створює таблицю пропусків для всіх можливих символів Unicode
    for k in range(m - 1):
        skip[ord(pattern[k])] = m - k - 1  # Заповнює таблицю пропусків значеннями
    k = m - 1
    while k < n:
        j = m - 1
        i = k
        while j >= 0 and text[i] == pattern[j]:
            j -= 1
            i -= 1
        if j == -1:
            return i + 1  # Повертає індекс знайденого підрядка
        k += skip[ord(text[k])]
    return -1  # Повертає -1, якщо підрядок не знайдено

# Функція для алгоритму Кнута-Морріса-Пратта
def knuth_morris_pratt(text, pattern):
    """Функція для пошуку підрядка в тексті за алгоритмом Кнута-Морріса-Пратта."""
    # Внутрішня функція для обчислення префіксної функції
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)  # Обчислення префіксної функції
    i = 0
    j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j  # Повертає індекс знайденого підрядка
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1  # Повертає -1, якщо підрядок не знайдено

# Функція для алгоритму Рабіна-Карпа
def rabin_karp(text, pattern):
    """Функція для пошуку підрядка в тексті за алгоритмом Рабіна-Карпа."""
    d = 256  # Кількість можливих символів
    q = 101  # Просте число для хешування
    m = len(pattern)
    n = len(text)
    p = 0  # Хеш значення для шаблону
    t = 0  # Хеш значення для тексту
    h = 1  # Значення h буде використане для обчислення хешу
    for i in range(m - 1):
        h = (h * d) % q  # Обчислення значення h
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q  # Початкове значення хешу для шаблону
        t = (d * t + ord(text[i])) % q  # Початкове значення хешу для тексту
    for i in range(n - m + 1):
        if p == t:  # Якщо хеші збігаються, перевірка символів
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                return i  # Повертає індекс знайденого підрядка
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q  # Обчислення хешу для наступного вікна
            if t < 0:
                t = t + q  # Якщо хеш негативний, приводимо його до позитивного
    return -1  # Повертає -1, якщо підрядок не знайдено

# Читання файлів
with open('article1.txt', 'r', encoding='utf-8') as file:
    article1 = file.read()

with open('article2.txt', 'r', encoding='utf-8') as file:
    article2 = file.read()

# Підрядки для пошуку
patterns_article1 = ["алгоритми", "неіснуючийпідрядок"]
patterns_article2 = ["даних", "вигаданийпідрядок"]

# Функція для вимірювання часу виконання алгоритму
def measure_time(article, pattern, search_function):
    """Функція для вимірювання часу виконання алгоритму пошуку підрядка."""
    # Виконує функцію пошуку 1000 разів і повертає середній час виконання
    return timeit.timeit(lambda: search_function(article, pattern), number=1000)

# Результати вимірювань для article1
results_article1 = {
    "Boyer-Moore": [measure_time(article1, pattern, boyer_moore) for pattern in patterns_article1],
    "Knuth-Morris-Pratt": [measure_time(article1, pattern, knuth_morris_pratt) for pattern in patterns_article1],
    "Rabin-Karp": [measure_time(article1, pattern, rabin_karp) for pattern in patterns_article1]
}

# Результати вимірювань для article2
results_article2 = {
    "Boyer-Moore": [measure_time(article2, pattern, boyer_moore) for pattern in patterns_article2],
    "Knuth-Morris-Pratt": [measure_time(article2, pattern, knuth_morris_pratt) for pattern in patterns_article2],
    "Rabin-Karp": [measure_time(article2, pattern, rabin_karp) for pattern in patterns_article2]
}

# Створення таблиць результатів
df_article1 = pd.DataFrame(results_article1, index=["існуючий", "вигаданий"])
df_article2 = pd.DataFrame(results_article2, index=["існуючий", "вигаданий"])

# Виведення результатів
print("Article 1 Results:\n", df_article1)
print("\nArticle 2 Results:\n", df_article2)
