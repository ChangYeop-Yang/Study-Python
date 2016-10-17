# A dictionary of movie critics and their ratings of a small
# set of movies
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}

from math import sqrt

# 유클리디안 거리점수(Euclidean distance score)
# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs, person1, person2):  # 구현하기 쉬운 장점이 있으나 분포 상관관계를 고려하지 않는다.
    # Get the list of shared_items
    # 비교하는 두 사람의 공통적인 항목을 저장하는 Dictionary
    si = {}

    # Person1와 Person2가 같은 값을 가지고 있는 경우 Dictionary 생성
    for item in prefs[person1]:
        if item in prefs[person2]: si[item] = 1

    # if they have no ratings in common, return 0
    # 비교하는 두 사람의 비교 항목들을 공통적으로 가지지 않은 경우 함수 종료
    if len(si) == 0: return 0

    # Add up the squares of all the differences
    # 각 축을 기준으로 차이를 구하고 제곱을 구한 후, 구한 값의 총합의 제곱근이 거리 점수이다.
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])

    # 유사할 수록 더 높은 값을 가지는 계산식 사용하여 결과 값이 항상 0과 1사이의 값을 반환한다.
    return 1 / (1 + sqrt(sum_of_squares)) # 반환 값이 1과 가까울 수록 유사도는 높으며 1인 경우에는 비교하는 두 사람의 유사도가 같다.

# 피어슨 상관점수(Pearson correlation score)
# Returns the Pearson correlation coefficient for p1 and p2
# 상관계수 ⓐ : 두 개의 데이터 집합이 한 직선으로 얼마나 잘 표현되는가를 나타내는 측정값
# 상관계수 ⓑ : 잘 정규화되지 않은 데이터의 경우에 보다 나은 결과 제공
def sim_pearson(prefs, p1, p2):
    # Get the list of mutually rated items
    # 비교하는 두 사람의 공통적인 항목을 저장하는 Dictionary
    si = {}

    # Person1와 Person2가 같은 값을 가지고 있는 경우 Dictionary 생성
    for item in prefs[p1]:
        if item in prefs[p2]: si[item] = 1

    # if they are no ratings in common, return 0
    # 비교하는 두 사람이 공통적인 항목을 가지지 않은 경우 함수 종료
    if len(si) == 0: return 0

    # Sum calculations
    n = len(si) # Dictionary si의 길이 값을 저장

    # Sums of all the preferences
    sum1 = sum([prefs[p1][it] for it in si]) # Person1의 항목 중 si에 자료가 있는 경우 점수를 합하여 sum1에 저장한다.
    sum2 = sum([prefs[p2][it] for it in si]) # Person2의 항목 중 si에 자료가 있는 경우 점수를 합하여 sum2에 저장한다.

    # Sums of the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si]) # Person1의 항목 중 si에 자료가 있는 경우 점수를 제곱한 뒤 합하여 sum1Sq에 저장한다.
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si]) # Person2의 항목 중 si에 자료가 있는 경우 점수를 제곱한 뒤 합하여 sum2Sq에 저장한다.

    # Sum of the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si]) # si에 있는 항목들을 Person1와 Person2에서 공통적인 제품들의 점수를 곱한 뒤 총합을 구한다.

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / n) # ∑XY - ∑X∑Y / N
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n)) # (∑X^2 - (∑X)^2 / N) * (∑Y^2 - (∑Y)^2 / N)
    if den == 0: return 0 # 연관이 전혀 없으므로 함수 종료

    # 1: 완전연관 / 0 : 연관이 전혀 없음 / -1 : 완전히 반대로 연관
    return num / den


# 특정인과 유사한 취향을 가진 사람을 구하는 함수
# 매개변수 similarity = 유사도 함수 (sim_distance, sim_pearson), n = 동일한 사람 수 설정, prefs = 리스트 변수, person = 찾을 사람
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]

    scores.sort()  # 정렬
    scores.reverse()  # 순서 역순
    return scores[0:n]


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
# 매개변수 similarity = 유사도 함수 (sim_distance, sim_pearson), prefs = 리스트 변수, person = 찾을 사람
def getRecommendations(prefs, person, similarity=sim_pearson):  # 사용자 기반 협력 필터링은 추천할 때에도 유사성 계산을 함으로써 시간이 소비가 많다.

    # Dictionary
    totals = {}
    simSums = {}

    for other in prefs:
        if other == person: continue  # don't compare me to myself
        sim = similarity(prefs, person, other)

        # ignore scores of zero or lower
        if sim <= 0: continue
        for item in prefs[other]:

            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # 아직 영화를 보지 않은 경우 또는 점수를 주지 않은 경우

                # item을 Key값으로 자료구조 생성
                totals.setdefault(item, 0)
                # Similarity(유사성) * Score(점수)
                totals[item] += prefs[other][item] * sim

                # Sum of similarities (유사성에 합을 더함)
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # Create the normalized list
    rankings = [(total / simSums[item], item) for item, total in totals.items()]

    # Return the sorted list
    rankings.sort()  # 정렬
    rankings.reverse()  # 순서 역순
    return rankings


# Invert the preference matrix to be item-centric
# 자료사전의 Key와 Value를 바꾸는 함수
def transformPrefs(prefs):
    # Dictionary
    result = {}

    for person in prefs:
        for item in prefs[person]:  # Value 값을 Key 값으로 변경
            result.setdefault(item, {})

        result[item][person] = prefs[person][item]

    return result


# 항목기반 필터링(Item-Based Filtering)
# 항목 기반 협력 필터링은 사전에 유사성 계산을 한 뒤 저장함으로써 추천 시에는 빠른 속도를 가진다.

def calculateSimilarItems(prefs, n=10):
    # Create a dictionary of items showing which other items they
    # are most similar to.
    result = {}

    # Invert the preference matrix to be item-centric
    itemPrefs = transformPrefs(prefs)

    c = 0
    for item in itemPrefs:
        # Status updates for large datasets
        c += 1

        if c % 100 == 0: print
        "%d / %d" % (c, len(itemPrefs))
        # Find the most similar items to this one

        scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item] = scores

    return result


def getRecommendedItems(prefs, itemMatch, user):
    # Dictionary
    userRatings = prefs[user]
    scores = {}
    totalSim = {}

    # Loop over items rated by this user
    for (item, rating) in userRatings.items():

        # Loop over items similar to this one
        for (similarity, item2) in itemMatch[item]:

            # Ignore if this user has already rated this item
            if item2 in userRatings: continue

            # Weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating

            # Sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    # Divide each total score by total weighting to get an average
    rankings = [(score / totalSim[item], item) for item, score in scores.items()]

    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings

def loadMovieLens(path='C:\Users\user\Desktop\data'):
  # Get movie titles
  movies={}
  for line in open(path+'\u.item'):
    (id,title)=line.split('|')[0:2]
    movies[id]=title

# Load data
  prefs={}
  for line in open(path+'\u.data'):
    (user,movieid,rating,ts)=line.split('\t')
    prefs.setdefault(user,{})
    prefs[user][movies[movieid]]=float(rating)
  return prefs
