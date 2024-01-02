import pandas as pd
import numpy as np
import string

def cut_csv(doc_name):
 with open(doc_name, 'r', encoding='utf-8') as file:
# нарез строки на списки по делителю 'Баланс', 
# сам список режем до подстроки 'Просрочено' и вычетаем 1 cписок по счету с помощью среза [1:]                                                                              
  data = [el.split('Просрочено:')[0] for el in file.read().split('Баланс')[1:]] 

# избавляемся от пробелов и делим строку на элементы по разделителю ','
  new_data = list(map(lambda x: x.split(',') ,data)) 
                # print(new_data[0],new_data[1],sep='\n')
                # print(new_data[0],new_data[3])
#  удаляем символьные элементы и оставляем значения после ':'
  transf = [[el[el.find(':',1)+1:].strip() for el in line if el not in string.punctuation ] for line in new_data]
# print(transf[0],transf[1],transf[3],sep='\n')
 return transf

def get_arr(transf):
 len_list = [len(line) for line in transf] # можно заметить что у нас списки разной длины 9, 10 и 12.
 #print(len_list)
# создаем списки разной длинны
 list_09_len, list_10_len, list_12_len = [], [], []
               

# transf разделяем по длине списков для дальнейшей обработки
 for el in transf:                                       
  if len(el) == 9:
   list_09_len.append(el)
  elif len(el) == 10:
   list_10_len.append(el)
  elif len(el) == 12:
   list_12_len.append(el)

# извлекаем по срезам сумму задолженности и название кредитной организации
 for line in list_09_len:                                
  line[3]=line[3][:line[3].find('\n',1)]
  line[7]=line[6][line[6].find(':',1)+2:]
  line[6]=line[6][:line[6].find('\n',1)]
                
 for line in list_10_len:                                
  line[3]=line[3][:line[3].find('\n',1)]
  line[8]=line[7][line[7].find(':',1)+2:]
  line[7]=line[7][:line[7].find('\n',1)]

# раставляем в удобном порядке значения и удаляем не используемые колонки )                                           (PEP8SORRY:)
 for line in list_09_len:
  line[1], line[2], line[3], line[4], line[5], line[6], line[7] = line[7], line[2], line[1], line[3], line[6], line[5], line[8]  
  del line [8]                                                                                                                     

 for line in list_10_len:
  line[1], line[2], line[3], line[4], line[5], line[6], line[7] = line[8], line[2], line[1], line[3], line[7], line[6], line[9] 
  del line [8]
  del line [8]

 for line in list_12_len:
  line[1], line[2], line[3], line[4], line[5], line[6], line[7] = line[9], line[2], line[1], line[3], line[8], line[7], line[11] 
  del line [8]
  del line [8]
  del line [8]
  del line [8]

# схлапываем списки в массив 
 full_arr = np.vstack([list_12_len, list_10_len, list_09_len])
 return full_arr

def get_csv(full_arr):
# создаем датафрейм
 df = pd.DataFrame(full_arr, columns=['type of credit institution', 'сredit institution name', 
                                      'date of loan issue', 'loan amount(RUB)','loan repayment amount(RUB)',
                                      'loan amount owed(RUB)', 'loan status', 'status date'])
# записываем в credit_history.csv
 df.to_csv(r"E:\Users\X\Desktop\parsing_nbki1\transform\credit_history.csv", index=False) 
 return df

if __name__ == '__main__':
  data = cut_csv('report.csv')
  arr = get_arr(data)
  df = get_csv(arr)
  print(df.head(5))