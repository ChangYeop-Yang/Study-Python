# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
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
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

from math import sqrt

# 유클리디안 거리점수(Euclidean distance score)
# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs,person1,person2): # 구현하기 쉬운 장점이 있으나 분포 상관관계를 고려하지 않
  # Get the list of shared_items
  si={}

  for item in prefs[person1]: 
    if item in prefs[person2]: si[item]=1

  # if they have no ratings in common, return 0
  if len(si)==0: return 0 # 두 사람의 점수가 공통으로 가지지 않은 경우 Return 0

  # Add up the squares of all the differences
  sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) 
                      for item in prefs[person1] if item in prefs[person2]])


  return 1/(1+sqrt(sum_of_squares))
  # 항상 0과 1사이의 값을 리턴하며 동일한 선호도를 가지는 경우 Return 1
  # 결과값이 1과 가까울 수록 유사도가 높다


# 피어슨 상관점수(Pearson correlation score)
# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs,p1,p2):
  # Get the list of mutually rated items
  si={}
  for item in prefs[p1]: 
    if item in prefs[p2]: si[item]=1

  # if they are no ratings in common, return 0
  if len(si)==0: return 0 # 두 사람의 점수가 공통으로 가지지 않은 경우 Return 0

  # Sum calculations
  n=len(si)
  
  # Sums of all the preferences
  # 모든 선호도의 합을 계산
  sum1=sum([prefs[p1][it] for it in si])
  sum2=sum([prefs[p2][it] for it in si])
  
  # Sums of the squares
  sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
  sum2Sq=sum([pow(prefs[p2][it],2) for it in si]) 
  
  # Sum of the products
  pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
  
  # Calculate r (Pearson score)
  num=pSum-(sum1*sum2/n)
  den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
  if den==0: return 0

  r=num/den

  return r


# 특정인과 유사한 취향을 가진 사람을 구하는 함수
# 매개변수 similarity = 유사도 함수 (sim_distance, sim_pearson), n = 동일한 사람 수 설정, prefs = 리스트 변수, person = 찾을 사람
def topMatches(prefs, person, n=5, similarity=sim_pearson):

  scores = [(similarity(prefs, person, other), other)
            for other in prefs if other != person]

  scores.sort() # 정렬
  scores.reverse() # 순서 역순
  return scores[0:n]


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
# 매개변수 similarity = 유사도 함수 (sim_distance, sim_pearson), prefs = 리스트 변수, person = 찾을 사람
def getRecommendations(prefs, person, similarity=sim_pearson): # 사용자 기반 협력 필터링은 추천할 때에도 유사성 계산을 함으로써 시간이 소비가 많다.

  # Dictionary
  totals={}
  simSums={}
  
  for other in prefs:
    if other == person: continue # don't compare me to myself
    sim=similarity(prefs,person,other)

    # ignore scores of zero or lower
    if sim<=0: continue
    for item in prefs[other]:
     
      # only score movies I haven't seen yet
      if item not in prefs[person] or prefs[person][item] == 0:
      # 아직 영화를 보지 않은 경우 또는 점수를 주지 않은 경우
        
        # item을 Key값으로 자료구조 생성
        totals.setdefault(item,0)
        # Similarity(유사성) * Score(점수)
        totals[item] += prefs[other][item] * sim
        
        # Sum of similarities (유사성에 합을 더함)
        simSums.setdefault(item,0)
        simSums[item]+=sim

  # Create the normalized list
  rankings=[(total/simSums[item],item) for item, total in totals.items()]

  # Return the sorted list
  rankings.sort() # 정렬
  rankings.reverse() # 순서 역순
  return rankings  

# Invert the preference matrix to be item-centric
# 자료사전의 Key와 Value를 바꾸는 함수
def transformPrefs(prefs):

  # Dictionary
  result = {}
  
  for person in prefs:
    for item in prefs[person]: # Value 값을 Key 값으로 변경
      result.setdefault(item, {})

    result[item][person] = prefs[person][item]

  return result

# 항목기반 필터링(Item-Based Filtering)
# 항목 기반 협력 필터링은 사전에 유사성 계산을 한 뒤 저장함으로써 추천 시에는 빠른 속도를 가진다.

def calculateSimilarItems(prefs, n=10):
  # Create a dictionary of items showing which other items they
  # are most similar to.
  result={}

  # Invert the preference matrix to be item-centric
  itemPrefs=transformPrefs(prefs)
  
  c=0
  for item in itemPrefs:
    # Status updates for large datasets
    c+=1

    if c % 100==0 : print "%d / %d" % (c,len(itemPrefs))
    # Find the most similar items to this one

    scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
    result[item]=scores

  return result

def getRecommendedItems(prefs,itemMatch,user):

  # Dictionary
  userRatings=prefs[user]
  scores={}
  totalSim={}
  
  # Loop over items rated by this user
  for (item,rating) in userRatings.items():

    # Loop over items similar to this one
    for (similarity,item2) in itemMatch[item]:

      # Ignore if this user has already rated this item
      if item2 in userRatings: continue
      
      # Weighted sum of rating times similarity
      scores.setdefault(item2,0)
      scores[item2]+=similarity*rating
      
      # Sum of all the similarities
      totalSim.setdefault(item2,0)
      totalSim[item2]+=similarity

  # Divide each total score by total weighting to get an average
  rankings=[(score/totalSim[item],item) for item,score in scores.items( )]

  # Return the rankings from highest to lowest
  rankings.sort( )
  rankings.reverse( )
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
