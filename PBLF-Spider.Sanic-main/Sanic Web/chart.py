import csv
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud
import zipfile


jieba.setLogLevel(jieba.logging.INFO)

# 自行修改路径修改路径
movie_path = 'csv/20230613161308_movie.csv'
comment_path = 'csv/20230613161308_movie_comment.csv'
emotion_path = 'csv/20230613161354_comment_emotion.csv'

with open(movie_path, 'r', encoding="UTF-8") as movie_file,\
        open(comment_path, 'r', encoding="UTF-8") as comment_file,\
        open(emotion_path, 'r', encoding="UTF-8") as emotion_file:
    movie_csv = list(csv.reader(movie_file))
    comment_csv = list(csv.reader(comment_file))
    emotion_csv = list(csv.reader(emotion_file))

    # index
    movie_name_index = 0
    movie_id_index = 0
    comment_content_index = 0
    comment_movie_id_index = 0
    positive_index = 0
    negative_index = 0

    for i in range(0, len(comment_csv[0])):
        if movie_csv[0][i] == "movie_name":
            movie_name_index = i
        if movie_csv[0][i] == "movie_id":
            movie_id_index = i

    for i in range(0, len(comment_csv[0])):
        if comment_csv[0][i] == "comment_content":
            comment_content_index = i
        if comment_csv[0][i] == "movie_id":
            comment_movie_id_index = i

    for i in range(0, len(emotion_csv[0])):
        if emotion_csv[0][i] == "positive_probs":
            positive_index = i
        if emotion_csv[0][i] == "negative_probs":
            negative_index = i

    movie_file.close()
    comment_file.close()
    emotion_file.close()

# 饼图绘制
def plot_movie_comment_pie():

    movie_name = []
    positives = []
    negatives = []

    with open(movie_path, 'r', encoding="UTF-8") as movie_file, \
            open(comment_path, 'r', encoding="UTF-8") as comment_file, \
            open(emotion_path, 'r', encoding="UTF-8") as emotion_file:
        movie_csv = list(csv.reader(movie_file))
        comment_csv = list(csv.reader(comment_file))
        emotion_csv = list(csv.reader(emotion_file))

        # get comments
        for i in range(1, len(movie_csv)):
            movie_name.append(movie_csv[i][movie_name_index])
            positive_num = 0
            negative_num = 0
            for j in range(1, len(comment_csv)):
                if movie_csv[i][movie_id_index] == comment_csv[j][comment_movie_id_index]:
                    positive_num += float(emotion_csv[j][positive_index])
                    negative_num += float(emotion_csv[j][negative_index])
            positives.append(positive_num)
            negatives.append(negative_num)
                # 调用函数绘制词云
            plot_movie_comment_wordcloud(movie_csv[i][movie_id_index],movie_csv[i][movie_name_index])
            print(i)
        # close
        movie_file.close()
        comment_file.close()
        emotion_file.close()


    for item in range(0,len(movie_name)):
        print(movie_name[item])
        plt.title(movie_name[item], fontsize=30)
        plt.axis('equal')
        plt.rcParams['font.sans-serif'] = "AR PL UMing CN"
        sizes = [positives[item], negatives[item]]
        labels = 'positive', 'negative'
        colors = ["#d5695d", "#5d8ca8"]
        plt.pie(sizes, labels=labels, startangle=45, colors=colors, radius=1.2, autopct='%.2f%%',
                textprops={'fontsize': 30, 'color': 'black'})
        plt.savefig('package/' + movie_name[item] + '情感分析图.png')
        plt.close()


        # close
        movie_file.close()
        comment_file.close()
        emotion_file.close()



# 绘制词云
def plot_movie_comment_wordcloud(movie_id,movie_name):
    comment = ""
    with open(movie_path, 'r', encoding="UTF-8") as movie_file, \
            open(comment_path, 'r', encoding="UTF-8") as comment_file:

        movie_csv = list(csv.reader(movie_file))
        comment_csv = list(csv.reader(comment_file))
        for i in range(1, len(movie_csv)):
            if movie_csv[i][movie_id_index] != movie_id:
                continue
            for j in range(1, len(comment_csv)):
                if comment_csv[j][comment_movie_id_index] == movie_id:
                    comment += comment_csv[j][comment_content_index]
        movie_file.close()
        comment_file.close()
    if comment == "":
        print({"code": -1, "message": "No comment."})
        return

    # cut
    cut_text = " ".join(jieba.lcut(comment))
    with open('stopword.txt', 'r', encoding="UTF-8") as f:
        stopwords = f.read()
    stopwords = ['\n', '', ' '] + stopwords.split()
    cloudfoundry = WordCloud(width=400, height=300, scale=1, margin=2,font_path='/usr/share/fonts/truetype/arphic/uming.ttc',
                            background_color='white', max_words=200,
                            random_state=100,stopwords=stopwords).generate(cut_text)

    plt.imshow(cloudfoundry)
    plt.axis("off")
    plt.savefig('package/' + movie_name + 'wordcloud.png')
    plt.close()

# 打包为zip文件
def file2zip(zip_file_name):
    with zipfile.ZipFile(zip_file_name, mode='w') as zf:
        zf.write('package', compress_type=zipfile.ZIP_DEFLATED)

if __name__ == '__main__':
    plt.rcParams["font.sans-serif"] = ["SimHei"] # setting word
    plt.rcParams["axes.unicode_minus"] = False
    # setting fiigsize
    plt.figure(figsize=(18, 6))
    plot_movie_comment_pie()
    file2zip('./package')
