import math # Подкючаем библиотеку для log()

def poscitat(tekst): # Функция, которая принимает числа на ввод и обрабатывает их

    tekst = tekst.replace(" ", "")
    if tekst == "":
        return "Вы забыли ввести выражение, повторите попытку"

    # Обработка log()
    while "log" in tekst:
        start = tekst.find("log") # Находим индексы логарифма
        otkr = tekst.find("(", start) # Находим индекс открывающейся скобки

        if otkr == -1: # Если не нашел скобку
            return "Вы забыли открыть скобку, повторите попытку"

        balans = 1 # Счетчик вложенности скобок
        zakr = -1 # Переменная для сохранения индекса закрывающейся скобки
        for i in range(otkr + 1, len(tekst)): # Идем от откр скобки до конца строки
            if tekst[i] == "(": # Если встретили откр скобку
                balans += 1 # Счетчик +1
            elif tekst[i] == ")":
                balans -= 1
                if balans == 0:
                    zakr = i # Запоминаем позицию
                    break # Выходим из цикла

        if zakr == -1: # Если не нашли закр скобку
            return "Проверьте правильность написания выражения"

        vnutri = tekst[otkr+1:zakr] # Делаем срез то что находится в log()
        chislo = poscitat(vnutri)
        if type(chislo) == str: # Если внутри была ошибка, функция вернула текст
            return chislo

        if chislo <= 0: # Логарифм может быть только положительным и больше нуля
            return "Проверьте правильность написания log()"

        log_chislo = str(math.log(chislo)) # Считаем логарифм и превращаем результат в строку
        tekst = tekst[:start] + log_chislo + tekst[zakr+1:] # Меняем логарифм на результат

     # Обработка скобок
    while "(" in tekst:
        otkr = tekst.find("(") # Находим откр скобку
        balans = 1
        zakr = -1
        for i in range(otkr+1, len(tekst)):
            if tekst[i] == "(": 
                balans += 1
            elif tekst[i] == ")":
                balans -= 1
                if balans == 0:
                    zakr = i
                    break

        if zakr == -1:
            return "Проверьте правильность расположения скобок"

        vnutri = tekst[otkr+1:zakr]
        if vnutri == "":
            return "Вы забыли ввести выражение, повторите попытку"

        chislo = poscitat(vnutri)
        if type(chislo) == str:
            return chislo

        tekst = tekst[:otkr] + str(chislo) + tekst[zakr+1:]

    # Обработка приоритетов действий
    for i in range(len(tekst) - 1, 0, -1):
        znak = tekst[i]
        if znak in "+-":
            if tekst[i-1] in "+-*/^": # Защита от двойных знаков
                continue
            levoe_str = tekst[:i] # Левая часть
            pravoe_str = tekst[i+1:] # Правая часть
            if levoe_str == "" or pravoe_str == "":
                return "Убедитесь в правильности написания примера"
            levoe = poscitat(levoe_str)
            pravoe = poscitat(pravoe_str)
            if type(levoe) == "str":
                return levoe
            if type(pravoe) == "str":
                return pravoe
            if znak == "+":
                return levoe + pravoe
            if znak == "-":
                return levoe - pravoe

    # Обработка XOR
    for i in range(len(tekst) -1, 0, -1):
        znak = tekst[i]
        if znak == "^":
            if tekst[i-1] in "+-*/^":
                continue
            levoe_str = tekst[:i]
            pravoe_str = tekst[i+1:]
            if levoe_str == "" or pravoe_str == "":
                return "Убедитесь в правильности написания примера"
            levoe = poscitat(levoe_str)
            pravoe = poscitat(pravoe_str)
            if type(levoe) == "str":
                return levoe
            if type(pravoe) == "str":
                return pravoe
            return int(levoe) ^ int(pravoe)

    # Обработка умножения и деления
    for i in range(len(tekst) -1, 0, -1):
        znak = tekst[i]
        if znak in "*/":
            if tekst[i-1] in "+-*/":
                continue
            levoe_str = tekst[:i]
            pravoe_str = tekst[i+1:]
            if levoe_str == "" or pravoe_str == "":
                return "Убедитесь в правильности написания примера"
            levoe = poscitat(levoe_str)
            pravoe = poscitat(pravoe_str)
            if type(levoe) == "str":
                return levoe
            if type(pravoe) == "str":
                return pravoe
            if znak == "*":
                return levoe * pravoe
            if znak == "/":
                if pravoe == 0:
                    return "Деление на ноль невозможно"
                return levoe / pravoe

    # Проверка знаков
    proverka = tekst
    if proverka[0] == "-": # Если число отрицательное
        proverka = proverka[1:] # Отрезаем минус для проверки остатка

    tochek = 0 # Счетчик точек
    for bukva in proverka: # Перебираем символы
        if bukva == ".":
            tochek += 1
        if bukva.isdigit() == False and bukva != ".": # Если не цифра и не точка
            return "Убедитесь в правильности написания примера"

        if tochek > 1:
            return "Убедитесь в правильности написания примера"

        try:
            return float(tekst)
        except:
            return "Убедитесь в правильности написания примера"

# Запуск и меню
print("\n\nКалькулятор")
print("Действия которые может выполнить программа:\n")
print("+ сложение")
print("- разность")
print("* умножение")
print("/ деление")
print("log() натуральный логарифм")
print("^ побитовое исключающее\n")
print("Для выхода напишите: Выход")

while True:
    vvod = input("Введите выражение: ")
    if vvod == "Выход":
        print("\nДо свидания!")
        break

    vvod = vvod.replace(",", ".")  # Заменяем запятые на точки
    
    otvet = poscitat(vvod)  # Считаем
    
    if type(otvet) == str:  # Если вернулась ошибка
        print(otvet)  # Печатаем ошибку
    else:  # Если вернулось число
        print("Ответ:", otvet)  # Печатаем ответ
    print()  # Пустая строка
