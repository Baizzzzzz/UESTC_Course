import time
import csv
import paddlehub
import os

if __name__ == '__main__':
    # 自行替换文件名
    path = "csv/20230612210443_movie_comment.csv"
    analysis_path = "csv/20230612210443_movie_comment_analysis.csv"
    if not os.path.exists(path):
        print({"code": 0, "msg": "file is not exists"})

    # 读取评论内容
    res = []
    with open(path, encoding='UTF-8') as file:
        c_csv = list(csv.reader(file))
        c_header = c_csv[0]
        content_index = 0
        #获取评论字段索引值
        for i in range(0, len(c_header)):
            if c_header[i] == 'comment_content':
                content_index = i
                break
        # 获取评论内容
        for i in range(1, len(c_csv)):
            res.append(c_csv[i][content_index])
        file.close()

    # senta初始化
    senta = paddlehub.Module(name="senta_bilstm")
    # 情感分析
    input_dict = {"text":res}
    results = senta.sentiment_classify(data = input_dict)
    key_list = {"is_positive", "positive_probs", "negative_probs"}
    # 新建文件存储情感数据
    with open(analysis_path, "w+", newline='', encoding='UTF-8') as file:
        writer = csv.DictWriter(file, fieldnames=key_list)
        writer.writeheader()
        for item in results:
            is_positive = 0
            if item['sentiment_key'] == "positive":
                is_positive = 1
            value = {"positive_probs": format(item["positive_probs"], '.4f'),
                     "negative_probs": format(item["negative_probs"], '.4f'),
                     "is_positive": is_positive}
            writer.writerow(value)
        file.close()
    print({"code": 1,"msg":"success"})
