import pandas as pd
import numpy
from pandas.io.excel import ExcelWriter



pd.set_option('display.max_colwidth', None, 'display.max_rows', None,
'display.max_columns', None, 'display.expand_frame_repr', False)
df = pd.read_csv('dataset.csv', encoding='utf8')
df = df.drop(df.columns[[4, 6, 8, 10, 12, 14]], axis=1)
df = df.rename(columns={'Остаток': 'ВсегоТовара', 'Количество': 'НаВитрине'})
res=pd.DataFrame
#Почистить данные с NaN. Вывести среднюю цену.
#Вывести разницу между начальной ценой и средней для всех товаров.
def Task_1(df):
    #чистка столбцов
    df1 = df.dropna(axis='index', how='any', subset=['Цена'])

    #среднее значение цены
    res=df1.groupby("КодКатегории", sort=False).mean().reset_index()
    res=res[['КодКатегории','Цена']]
    res=res.rename(columns = {'Цена' : 'СредняяЦена'})

    #Объединение таблиц и добавление Разницы
    res1 = df1.merge(res, on = 'КодКатегории')
    res1 = res1.assign(Разница = res1.СредняяЦена - res1.Цена)
    print(res1[['КодКатегории', 'Цена', 'СредняяЦена', 'Разница']])

#Task_1(df)
print()

# Посчитать площадь и объём товаров.
# У товаров у которых нету данных по высоте, ширине, длине считать среднее в категории.
# Также отсортировать список по частоте продаж товаров.
# Исключить товары у которых частота продаж меньше 0.012 и у которых нет остатков и транзита
def Task_2(df):
    global res
    #группировка столбцов
    df2 = df[['КодКатегории', 'ДлинаЕд', 'ШиринаЕд', 'ВысотаЕд']].groupby(['КодКатегории']).mean('ДлинаЕд', 'ШиринаЕд','ВысотаЕд')
    res = df.merge(df2.rename(columns={'ДлинаЕд': 'Д', 'ШиринаЕд': 'Ш', 'ВысотаЕд': 'В'}), on='КодКатегории')

    # Если 0 по высоте, ширине, длине - выводить среднее в категории
    res['ДлинаЕд'] = res['ДлинаЕд'].fillna(0)
    res['ШиринаЕд'] = res['ШиринаЕд'].fillna(0)
    res['ВысотаЕд'] = res['ВысотаЕд'].fillna(0)
    res['ДлинаЕд'] = numpy.where((res.ДлинаЕд == 0), res['Д'], res.ДлинаЕд)
    res['ШиринаЕд'] = numpy.where((res.ШиринаЕд == 0), res['Ш'], res.ШиринаЕд)
    res['ВысотаЕд'] = numpy.where((res.ВысотаЕд == 0), res['В'], res.ВысотаЕд)
    res = res.drop(['Д', 'Ш', 'В'], axis=1)

    # Добавить столбцы с площадью и объёмом
    res = res.assign(Площадь=2 * ( res.ДлинаЕд * res.ШиринаЕд + res.ДлинаЕд * res.ВысотаЕд + res.ШиринаЕд * res.ВысотаЕд))
    res = res.assign(Объем=res.ДлинаЕд * res.ШиринаЕд * res.ВысотаЕд)
    #сортировка
    res = res.sort_values('ЧастотаПродаж', ascending=True).reset_index(drop=True)
    #фильтр
    res=res.loc[(res["ЧастотаПродаж"]>=0.012) & ((res["ВсегоТовара"]>0.0) | (res["Транзит"]>0.0))]
    #print(res)
Task_2(df)

# Каждый товар имеет свою занимаемую площадь.
# Нужно рассчитать сколько товаров данных категорий влезет по площади.
# На выходе получить эксель файл с товарами из задания 5 с доп столбцом "Остаток площади"
def Task_3(df,res):
    def Conclusion(res, b):
        #Читаем файл
        a = pd.read_excel(io='moduls.xlsx', engine='openpyxl', sheet_name=b)
        a = a.rename(columns={'Площадь': 'Остаток_площади'})
        a['Остаток_площади'] = a['Остаток_площади'].fillna(0)
        a['Остаток_площади'] = numpy.where((a.Остаток_площади == 0.0), a['Остаток_площади'].iloc[0], a.Остаток_площади)
        #Фильтруем по модулям
        a = res.merge(a, on='КодКатегории')
        # Посчиать остаток в цикле для модуля
        a.loc[0, 'Остаток_площади'] = float(a.loc[[0]].Остаток_площади) - float(a.loc[[0]].Площадь)
        for i in range(1, a.shape[0]):
            a.loc[i, 'Остаток_площади'] = float(a.loc[[i - 1]].Остаток_площади) - float(a.loc[[i]].Площадь)
        return a

    #Выполняем для каждого модуля
    tv = Conclusion(res, 'ТВ')
    cmp = Conclusion(res, 'Компы')
    cml = Conclusion(res, 'Комплектующие')
    ph = Conclusion(res, 'Телефоны')

    #Запись результата в файл
    writer = pd.ExcelWriter('result.xlsx')
    tv.to_excel(writer, 'ТВ')
    cmp.to_excel(writer, 'Компы')
    cml.to_excel(writer, 'Комплектующие')
    ph.to_excel(writer, 'Телефоны')
    writer.save()

Task_3(df,res)









