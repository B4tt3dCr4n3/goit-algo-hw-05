"""Завдання 1. Додати метод delete для видалення пар ключ-значення таблиці 
HashTable , яка реалізована в конспекті."""

class HashTable:
    """Хеш-таблиця для зберігання пар ключ-значення."""
    def __init__(self, size):
        # Ініціалізація хеш-таблиці з заданим розміром
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        """Хеш-функція для обчислення індексу ключа."""
        return hash(key) % self.size

    def insert(self, key, value):
        """Вставка нового ключа та значення в хеш-таблицю."""
        key_hash = self.hash_function(key)
        key_value = [key, value]

        if self.table[key_hash] is None:
            # Якщо в цьому індексі ще немає списку, створюємо його
            self.table[key_hash] = list([key_value])
            return True
        else:
            # Перевіряємо, чи ключ вже існує
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    # Якщо ключ вже існує, оновлюємо значення
                    pair[1] = value
                    return True
            # Якщо ключ не існує, додаємо нову пару
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        """Пошук значення за ключем у хеш-таблиці."""
        key_hash = self.hash_function(key)
        if self.table[key_hash] is not None:
            # Перебираємо всі пари у відповідному списку
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    # Повертаємо значення, якщо ключ знайдено
                    return pair[1]
        # Повертаємо None, якщо ключ не знайдено
        return None

    def delete(self, key):
        """Видалення пари ключ-значення з хеш-таблиці."""
        key_hash = self.hash_function(key)
        if self.table[key_hash] is not None:
            # Перебираємо всі пари у відповідному списку
            for i in range(len(self.table[key_hash])):
                if self.table[key_hash][i][0] == key:
                    # Видаляємо пару, якщо ключ знайдено
                    self.table[key_hash].pop(i)
                    return True
        # Повертаємо False, якщо ключ не знайдено
        return False

# Тестуємо нашу хеш-таблицю:
H = HashTable(5)
H.insert("apple", 10)
H.insert("orange", 20)
H.insert("banana", 30)

# Перевірка значень за ключами
print(H.get("apple"))   # Виведе: 10
print(H.get("orange"))  # Виведе: 20
print(H.get("banana"))  # Виведе: 30

# Видаляємо "orange"
H.delete("orange")

# Перевірка значень після видалення
print(H.get("apple"))   # Виведе: 10
print(H.get("orange"))  # Виведе: None, бо "orange" видалено
print(H.get("banana"))  # Виведе: 30
