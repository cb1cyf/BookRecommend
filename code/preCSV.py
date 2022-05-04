sql_path = './proj/SQL/book.sql'
csv_path = './proj/CSV/Ratings.csv'
ori_path = './BX-CSV-Dump/BX-Book-Ratings.csv'
isbn2id = {}
with open(sql_path, 'r', encoding='ISO-8859-1') as f:
    while True:
        sql = f.readline()
        if not len(sql):
            break
        if not sql.startswith('insert'):
            continue
        idx0 = sql.index('(')
        idx1 = sql.index(',', idx0)
        idx2 = sql.index("',", idx1)
        bookId = int(sql[idx0+1:idx1])
        isbn = sql[idx1+3:idx2]
        isbn2id[isbn] = bookId

with open(csv_path, 'a', encoding='UTF-8') as f:
    ori_f = open(ori_path, 'r', encoding='ISO-8859-1')
    header = ori_f.readline()
    while True:
        record = ori_f.readline()
        if not len(record):
            break
        data = record.strip().split(';')
        if len(data) != 3:
            print(record)
            break
        if int(data[-1].strip('"')) == 0:
            continue
        try:
            bookId = isbn2id[data[1].strip('"')]
            bookId = f'"{bookId}"'
            new_record = ';'.join([data[0], bookId, data[-1]]) + '\n'
            f.write(new_record)
            #f.flush()
            #print(new_record)
        except:
            continue
    ori_f.close()