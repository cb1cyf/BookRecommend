import re
# ISO-8859-1 = latin1
ori_path = './BX-SQL-Dump/BX-Books.sql'
path = './proj/SQL/book.sql'
id = 1
with open(path, 'a', encoding='ISO-8859-1') as f:
    ori_f = open(ori_path, 'r', encoding='ISO-8859-1')
    #header = ori_f.readline()
    while True:
        ori_csv = ori_f.readline()
        if not len(ori_csv):
            break
        if not ori_csv.startswith('INSERT'):
            continue
        idx = re.search(r"',[0-9]+,'", ori_csv).span()
        data1 = ori_csv[31:idx[0]].split("','")
        data2 = ori_csv[idx[1]-1:-2].split("','")
        #ori_csv = ori_csv[31:-2].split(",")
        if len(data1) != 3 or len(data2)!=4:
            print(data1, data2)
            print(id)
            break
        isbn = data1[0]+"'"
        title = data1[1]
        author = data1[2]
        url = data2[-2]
        sql = f"insert into book values ({id}, {isbn}, '{title}', '{author}', '{url}');\n"
        f.write(sql)
        #f.flush()
        #print(sql)
        id += 1
    ori_f.close()
