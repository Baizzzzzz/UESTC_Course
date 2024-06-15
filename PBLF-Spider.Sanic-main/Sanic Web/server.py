import csv
import os
import time
import json as ger_json
from sanic import Sanic
from sanic.response import json
import jieba
import paddlehub
import zipfile
jieba.setLogLevel(jieba.logging.INFO)

app = Sanic("mySanic")

#上传书评数据文件接口
@app.route("/v1/movie/crawled/upload", methods=['POST'])
async def upload(request):
    # 错误处理
    allow_type = ['.json']
    file = request.files.get('file')
    type = os.path.splitext(file.name)
    if len(type) == 1 or type[1] not in allow_type:
        return json({"code": 0, "msg": "file's format is error!"})

    # 上传文件处理
    path = './upload'
    now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
    filename = now_time+'_'+type[0]+".json"
    with open(path+'/'+filename, 'wb') as f:
        f.write(file.body)
    f.close()

    # 调用
    name = convert_movie('./upload/'+filename)
    return json({"code": 1, "msg": "convert successfully",
                 "data": {"movie_csv_name": name[0], "comment_csv_name": name[1]}})

# 同步函数，提取并储存信息
def convert_movie(filename):
    name=[]
    # 提取 movie 信息
    with open(filename, 'r', encoding='UTF-8') as file:
        body = ger_json.load(file)
        file.close()

    # 获取 body 中书籍的键，用于 csv 中的表头
    keys = []
    for key in body[0].keys():
        if not type(body[0][key]) == type({}):
            if key == "movie_author":
                keys.append('movie_author1')
                keys.append('movie_author2')
            elif key == "movie_actor":
                keys.append('movie_actor1')
                keys.append('movie_actor2')
            elif key == 'comment_list':
                continue
            else:
                keys.append(key.strip())

    # 输入csv
    now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
    csv_name = now_time + '_movie.csv'
    with open('csv/' + csv_name, 'w+', newline='', encoding='UTF-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for item in body:
            if len(item['movie_author']) == 2:
                item["movie_author1"] = item['movie_author'][0]
                item["movie_author2"] = item['movie_author'][1]
            else:
                item["movie_author1"] = item['movie_author'][0]
                item["movie_author2"] = ""
            if len(item['movie_actor']) == 2:
                item["movie_actor1"] = item['movie_actor'][0]
                item["movie_actor2"] = item['movie_actor'][1]
            else:
                item["movie_actor1"] = item['movie_actor'][0]
                item["movie_actor2"] = ""
            item.pop("comment_list", None)
            item.pop("movie_author", None)
            item.pop("movie_actor", None)
            writer.writerow(item)
        file.close()

    # comment_csv
    with open(filename, 'r', encoding='UTF-8') as file:
        body = ger_json.load(file)
        file.close()

    keys = []
    keys.append('movie_id')
    for key in body[0]['comment_list'][0].keys():
        if not type(body[0]['comment_list'][0][key]) == type({}) and not type(body[0]['comment_list'][0][key]) == type(
                []):
            keys.append(key.strip())

    now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
    comment_csv_name = now_time + '_movie_comment.csv'
    with open('csv/' + comment_csv_name, 'w+', newline='', encoding="UTF-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for movie in body:
            for item in movie['comment_list']:
                item['movie_id'] = movie['movie_id']
                writer.writerow(item)
        file.close()

    name.append(csv_name)
    name.append(comment_csv_name)
    return name


# 查询云端文件信息
@app.route("/v1/movie/csv", methods=['GET'])
async def get_csv_info(request):
    # get filename
    filename = request.args.get("filename")
    path = os.getcwd() + '/csv'
    # is exists?
    if os.path.exists(path+ '/'+filename) == False:
        return json({"code": 0, 'msg': "file not exist.", "path": path})
    # get data
    data = []
    with open(path+'/'+filename, 'r', encoding="UTF-") as file:
        n_csv = list(csv.reader(file))
        header = n_csv[0]
        for i in range(1, len(n_csv)):
            n_row = n_csv[i]
            item = {}
            for j in range(0, len(header)):
                item[header[j]] = n_row[j]
            data.append(item)
        file.close()
    return json({"code": 1, "msg": "success", "data": data}, ensure_ascii=False)

# 查询电影信息
@app.route("/v1/movie/info", methods=['GET'])
async def get_movie_info(request):
    # is exists?
    filename = request.args.get("filename")
    movie_id = request.args.get("movie_id")
    path = "./csv"
    if filename != None and not os.path.exists(path+"/"+filename):
        return json({"code": 0, "msg": "the filename is none"})
    if not filename.endswith("movie.csv"):
        return json({"code": 0, "msg": "the file is not about movie!"})
    # get movies data
    movies = []
    with open(path+'/'+filename, 'r', encoding="UTF-8") as file:
        n_csv = list(csv.reader(file))
        header = n_csv[0]
        for i in range(1, len(n_csv)):
            n_row = n_csv[i]
            movie = {}
            movie_author = []
            movie_actor = []
            if movie_id != None and movie_id != n_row[0]:
                continue
            for j in range(0, len(header)):
                if header[j] == "movie_author1" and n_row[j] != None:
                    movie_author.append(n_row[j])
                elif header[j] == "movie_author2" and n_row[j] != None:
                    movie_author.append(n_row[j])
                elif header[j] == "movie_actor1" and n_row[j] != None:
                    movie_actor.append(n_row[j])
                elif header[j] == "movie_actor2" and n_row[j] != None:
                    movie_actor.append(n_row[j])
                if(header[j] != "movie_author1" and header[j] != "movie_author2" and header[j] != "movie_actor1" and header[j] != "movie_actor2" ):
                    movie[header[j]] = n_row[j]
            movie["movie_author"] = movie_author
            movie["movie_actor"] = movie_actor
            movies.append(movie)
        file.close()
    return json({"code": 1, "msg": "query successfully!", "data": movies}, ensure_ascii=False)

# 查询影评信息
@app.route("/v1/movie/comment", methods=['GET'])
async def get_comment_info(request):
    # is exists?
    filename = request.args.get("filename")
    movie_id = request.args.get("movie_id")
    path = os.getcwd()+"/csv"
    # get comments
    res = {}
    with open(path+'/'+filename, 'r', encoding="UTF-8") as file:
        n_csv = list(csv.reader(file))
        header = n_csv[0]
        comments = []
        for i in range(1, len(n_csv)):
            n_row = n_csv[i]
            if n_row[0] != movie_id:
                continue
            comment = {}
            for j in range(0, len(header)):
                if header[j] != "movie_id":
                    comment[header[j]] = n_row[j]
            comments.append(comment)
        res["movie_id"] = movie_id
        res["comment_list"] = comments
        file.close()
    return json({"code": 1, "msg": "query successfully!", "data": res}, ensure_ascii=False)

# sante情感分析
@app.route("/v1/movie/comment/sentiment-analysis/package", methods=['GET'])
async def get_data_analysis(request):
    comment_filename = os.getcwd()+'/csv/'+ request.args.get("comment_filename")
    now_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
    analysis_name = os.getcwd() + '/csv/' + now_time + '_comment_emotion.csv'

    analysis_movie(comment_filename, analysis_name)

def analysis_movie(path, analysis_path):
    if not os.path.exists(path):
        return json({"code": 0, "msg": "file is not exists"})

    # 评论内容列表
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
    input_dict = {"text": res}
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

    return json({"code": 1, "msg": "query successfully!", "data": None})




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
