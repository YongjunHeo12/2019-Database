# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 15:53:24 2019

"""
#카테고리 예측?

###############################
# category 정보 읽기...
import json
CATEGORY = dict()
with open('KR_category_id.json') as f:
    data = json.load(f)
for x in data['items']:
    CATEGORY[x['id']] = x['snippet']['title']    
    


HEAD = (
'video_id',   # 0
'trending_date',  # 1
'title', # 2
'channel_title', # 3
'category_id', # 4
'publish_time', # 5
'tags', # 6
'views', # 7
'likes', # 8
'dislikes', # 9
'comment_count', # 10
'thumbnail_link', # 11
'comments_disabled', # 12
'ratings_disabled', # 13
'video_error_or_removed', # 14
'description' # 15
)

def make_word_list(s):#태그전체를 각 단어로 쪼개는 함수 
    
    w_lst = list()
    for x in s.split('|'):  #태그 받아왔으니구분자인 |로 나눈다     
        x = x.replace('"', '')
        x = x.replace("'", '')
        for z in x.split(' '):
            if z != '' and z != ' ':
                w_lst.append(z)
    return w_lst            




########### (1) FEATURE 추출해 보기 ###############
cnt = 0
Tags = dict()

with open('KRvideos.csv', encoding='UTF-8') as f:
    for line in f:
        items = line.strip().split(',')
        if len(items) != 16: continue
        cnt += 1
        if items[6] == '[none]': continue  # tags
        w_lst = make_word_list(items[6])   
        for w in w_lst: #w를 각 행의 태그 개수만큼 반복할 때
            if w in Tags:  #만약 w라는 단어가 Tags라는 dict안에 있으면 Tags[단어]에 +1를 해주고
                Tags[w] += 1
            else:            #없으면 Tags[단어]를 1로 만든다
                Tags[w] = 1        

tmp = [(x, y) for x, y in Tags.items()]
tmp_s = sorted(tmp, reverse=True, key=lambda x:x[1])
print('TOP 30 tags ===>', tmp_s[:30])

########### (2) FEATURE 저장 : 학습데이터 구성해보기 ###############
def make_feature(items):
    
    FEATURES = ('먹방', '뉴스', '문재인', '영화', '한국', '리뷰', '게임', '김정은', '고양이', '영상', '북한', '트럼프', '밴쯔', '미국', '아프리카TV')
    feature = [0 for _ in range(len(FEATURES))] # feature는 위에 FEATURES에 있는 개수만큼 for뤂
    w_lst = make_word_list(items[6])    #태그를 쪼개서 각 단어로 된것을 받아온다
    for w in w_lst:
        if w in FEATURES: #태그에 있는 단어가 위에 FEATURES에 있으면                
            feature[FEATURES.index(w)] = 1 #feature 0~ FEATURES 총 길이 사이에 단어가 있는 위치에 1의 값을 넣어줌, 예를들어 feature에 먹방이란 단어가 있으면 feature[0] = 1이 되는 것임
    feature.append(int(items[7]))   # view
    feature.append(int(items[8]))   # like
    feature.append(int(items[9]))   # dislike
    
    return feature

#--------------------------
Video = dict()

cnt = 0
with open('KRvideos.csv', encoding='UTF-8') as f:
    all_lines = f.readlines()

all_lines.pop(0)  # title line  
for line in all_lines:
    items = line.strip().split(',') #한 row에 ,로 구분된 각 데이터들
    if len(items) != 16: continue  #attribute가 16개 넘어가면 다시 위로
    cnt += 1
    if items[6] == '[none]': continue #태그에 아무것도 없으면 다시 위로
    v_key = items[0]   #video_id를 key로
    target = items[4]    # category_id --> TARGET, 카테고리를 타켓으로
    Video[v_key] = make_feature(items) + [target]  #배열 새로 정의 각 v_id마다 위에서 만든 feature(여기엔 지정된 단어가 있는 태그가 있는지에 대한 정보랑 view, likes dislikes 정보가 있음) + 카테고리 정보가 들어있음

#print(Video.values()) #Video라는 dict은 현재 key값이 video_id이고 16번재 value가 조회수 17은 좋아요 18은 싫어요 19는 '카테고리번호'가 있다
    
######### (3) Decision Trees
import numpy as np

lst = list()
for key, val in Video.items(): 
    lst.append([x for x in val])
    
data = np.array(lst)    
print(data.shape)    

x_train, t_train = data[:5000, :-1], data[:5000, -1]
x_test, t_test = data[5000:, :-1], data[5000:, -1]

from sklearn.tree import DecisionTreeClassifier
                
tree = DecisionTreeClassifier(random_state=0, max_depth=5)
tree.fit(x_train, t_train)

print("훈련 세트 정확도: {:.3f}".format(tree.score(x_train, t_train)))
print("테스트 세트 정확도: {:.3f}".format(tree.score(x_test, t_test)))


####### (4) 실제로는 어떻게 사용하나?
real = '''
#xuOQq_fzEjk,18.14.06,2018년 6월 13일 아침 뉴스,News Express,25,2018-06-12T13:17:29.000Z,"한국|""북한""|""미국""|""중국""|""일본""|""러시아""|""한국뉴스""|""뉴스""|""국제뉴스""|""북한뉴스""|""문재인""|""트럼프""|""김정은""|""김일성""|""김정일""|""김여정""|""김영철""|""펜스""|""아베""|""시진핑""|""푸틴""",62555,319,71,105,https://i.ytimg.com/vi/xuOQq_fzEjk/default.jpg,FALSE,FALSE,FALSE,2018년 6월 13일 아침 뉴스등록되지 않은 구독자가 여기에서 내 새 채널을 지원합니다.https://goo.gl/jsu1A1
'''
items = real.strip().split(',')
one = make_feature(items)
target = items[4]  # 어떤것을 target으로 할지 위에서는 카테고리를 타겠으로 했음

predicted_cat = tree.predict([one])
print('예측한 카테고리 ==>', CATEGORY[predicted_cat[0]])
print('진짜 카테고리 ==>', CATEGORY[target])


 
