import torch
import numpy as np
import pandas as pd, csv
from torch import nn, optim
from tqdm.auto import tqdm
torch.manual_seed(291)
np.random.seed(291)

NumBooks = 5 #Constant number of books to recommend per iteration
RecBatches = 300 #Constant number of books to add to the recommendation list for RL
BoostBatch = 100 #Constant number of books to add to the rec list when needed
BoostThreshold = RecBatches-BoostBatch
NumBooks = 9810
NumUsers = 53424
hardcoded = [3,15,18,815,96,4,9,127,14,2458,2738,316,60,5,2992,259,617,237]

#Code adapted and inspired by movie recommender model in lecture 6
#class Dataset(torch.utils.data.Dataset):
 #   def __init__(self, fn, books):
 #       self.dataframe = pd.read_csv(fn)
 #       self.books = pd.read_csv(books)
 #       u2n = { u: n for n, u in enumerate(self.dataframe['user_id'].unique()) } 
 #       df_book_conv = { m : m-1 for m in self.dataframe['book_id'] } 
  #      books_book_conv = {m : m-1 for m in self.books['book_id'] }
 #       self.dataframe['user_id'] = self.dataframe['user_id'].apply(lambda u: u2n[u])
  #      self.dataframe['book_id'] = self.dataframe['book_id'].apply(lambda m: df_book_conv[m]) #These book id conversion lambda functions may not be properly written
 #       self.books['book_id'] = self.books['book_id'].apply(lambda m: books_book_conv[m])
 #       self.coords = torch.LongTensor(self.dataframe[['user_id','book_id']].values) # (userId,bookId) <- coordinates
     #   self.ratings = torch.FloatTensor(self.dataframe['rating'].values)
 #       self.n_users = self.dataframe['user_id'].nunique()
   #     self.n_books = self.dataframe['book_id'].nunique()

  #  def __len__(self):
 #       return len(self.coords)
    
 #   def get_book_info(self, book_id): #This is wrong
   #   title = (self.books[self.books["book_id"] == book_id]).loc[:,"title"].values[0]
  #    author = (self.books[self.books["book_id"] == book_id]).loc[:,"authors"].values[0]
   #   url = (self.books[self.books["book_id"] == book_id]).loc[:,"image_url"].values[0]
   #   return title, author, url

  #  def __getitem__(self, i):  
  #    return (self.coords[i], self.ratings[i])  
#New Dataset Class Below
#class Dataset(torch.utils.data.Dataset):
    #def __init__(self, fn):
   #     self.dataframe = pd.read_csv(fn)
  #      u2n = { u: n for n, u in enumerate(self.dataframe['user_id'].unique()) } 
  #      apply_conv = { m: conv_arr[m] for m in self.dataframe["book_id"] }
  #      self.dataframe['user_id'] = self.dataframe['user_id'].apply(lambda u: u2n[u])
  #      self.dataframe["book_id"] = self.dataframe["book_id"].apply(lambda m: apply_conv[m])
  #      self.dataframe = self.dataframe[self.dataframe["book_id"] != -1]
  #      self.coords = torch.LongTensor(self.dataframe[['user_id', 'book_id']].values)
  #      self.ratings = torch.FloatTensor(self.dataframe['rating'].values)
     #   self.n_users = self.dataframe['user_id'].nunique()
   #     self.n_boooks = self.dataframe['book_id'].nunique()
    
 #   def __len__(self):
   #     return len(self.coords)

 #   def __getitem__(self, i):
 #       return (self.coords[i], self.ratings[i])


#Dataset set up code
#ds_full = Dataset('goodbooks-ratings.csv', 'goodbooks.csv')
#n_train = int(0.8 * len(ds_full))
#n_test = len(ds_full) - n_train
#rng = torch.Generator().manual_seed(291)
#ds_train, ds_test = torch.utils.data.random_split(ds_full, [n_train, n_test], rng)
#len(ds_full)

#Code adapted and inspired by movie recommender model in lecture 6
#Code adapted and inspired by movie recommender model in lecture 6
class BookRecommenderEmbeddingML(nn.Module):
  def __init__(self, n_users, n_books, emb_dim):
    super(BookRecommenderEmbeddingML, self).__init__()
    self.user_embedding = nn.Embedding(n_users, emb_dim)
    #self.user_bias = nn.Embedding(n_users, 1) #I question if this is helpful for our use of this model, due to our plan to use users in this dataset to represent multiple users - Declan
    self.book_embedding = nn.Embedding(n_books, emb_dim)
    #self.book_bias = nn.Embedding(n_books, 1)
    nn.init.xavier_uniform_(self.user_embedding.weight)
    nn.init.xavier_uniform_(self.book_embedding.weight)
    #nn.init.zeros_(self.user_bias.weight)
    #nn.init.zeros_(self.book_bias.weight)
    self.dropout = nn.Dropout(0.25)
  
  def forward(self, samples):
    users = self.user_embedding(samples[:,0]) # gets embedding of users
    users = self.dropout(users)
    books = self.book_embedding(samples[:,1])
    books = self.dropout(books)
    dot = (users * books).sum(1)
    #user_b = self.user_bias(samples[:,0]).squeeze()
    #book_b = self.book_bias(samples[:,1]).squeeze()
    return torch.sigmoid(dot) * 5.5
#Training code
device = torch.device('cuda:0')
def run_test(model, ldr, crit):
    total_loss, total_count = 0, 0
    model.eval()
    tq_iters = tqdm(ldr, leave=False, desc='test iter')
    with torch.no_grad():
        for coords, labels in tq_iters:
            coords, labels = coords.to(device), labels.to(device)
            preds = model(coords)
            loss = crit(preds, labels)
            total_loss += loss.item() * labels.size(0)
            total_count += labels.size(0)
            tq_iters.set_postfix({'loss': total_loss/total_count}, refresh=True)
    return total_loss / total_count

def run_train(model, ldr, crit, opt, sched):
    model.train()
    total_loss, total_count = 0, 0
    tq_iters = tqdm(ldr, leave=False, desc='train iter')
    for (coords, labels) in tq_iters:
        opt.zero_grad()
        coords, labels = coords.to(device), labels.to(device)
        preds = model(coords)
        pdb.set_trace()
        loss = crit(preds, labels)
        loss.backward()
        opt.step()
        sched.step()
        total_loss += loss.item() * labels.size(0)
        total_count += labels.size(0)
        tq_iters.set_postfix({'loss': total_loss/total_count}, refresh=True)
    return total_loss / total_count
##
def run_all(model, ldr_train, ldr_test, crit, opt, sched, n_epochs=10):
    best_loss = np.inf
    tq_epochs = tqdm(range(n_epochs), desc='epochs', unit='ep')
    for epoch in tq_epochs:
        train_loss = run_train(model, ldr_train, crit, opt, sched)
        test_loss = run_test(model, ldr_test, crit)
        tqdm.write(f'epoch {epoch}   train loss {train_loss:.6f}    test loss {test_loss:.6f}')
        if test_loss < best_loss:
            best_loss = test_loss
            tq_epochs.set_postfix({'bE': epoch, 'bL': best_loss}, refresh=True)
#Actual code of training the model omitted
def find_paired_user(ratings, matrix):
  bestDiff = np.inf
  bestUser = 0
  for i in range(NumUsers): # 5 for now but should be ds_full.n_users
    diff = 0
    for rating in ratings:
      diff = diff + abs(matrix[i][rating[0]] - rating[1])#Matrix will be tensor - may need to accomadate if so adjust future uses
    if diff < bestDiff:
      bestDiff = diff
      bestUser = i
  return bestUser

class User ():
  def __init__(self, ratings, matrix, id, emb_dim, model):
    self.id = id
    self.ratings = ratings
    self.pair_id = find_paired_user(ratings, matrix)
    emb_index = torch.LongTensor([self.pair_id])
    #emb_index = emb_index.to(device)
    user_feature_vector = model.user_embedding(emb_index) # get feature vector for user 0
    row = matrix[self.pair_id].detach().numpy()
    self.to_recommend = []
    for i in range(NumBooks):
      self.to_recommend.append([i, row[i]])
    self.to_recommend = sorted(self.to_recommend, key=lambda x : x[1]) #From https://stackoverflow.com/a/4174956
    self.to_recommend.reverse()
    self.rl_model = RLModel(user_feature_vector, emb_dim)
    self.optimizer = optim.SGD(self.rl_model.parameters(),1,0.3)
    self.curr_rec_list = self.to_recommend[0:RecBatches]
    self.to_recommend = self.to_recommend[RecBatches:]
  def update_rec_list(self, matrix):
    if len(self.curr_rec_list) < BoostThreshold:
      self.curr_rec_list = self.curr_rec_list + (self.to_recommend[0:BoostBatch])
      self.to_recommend = self.to_recommend[BoostBatch:]
    for i in range(len(self.curr_rec_list)):
      self.curr_rec_list[i][1] = getRec(self, self.curr_rec_list[i][0], matrix)
    self.curr_rec_list =  sorted(self.curr_rec_list, key=lambda x : x[1]) #From https://stackoverflow.com/a/4174956
    self.curr_rec_list.reverse()
  def get_books(self, matrix):
    #pdb.set_trace()
    curr_recommendation = self.curr_rec_list[0:NumBooks]
    self.curr_rec_list = self.curr_rec_list[NumBooks:]
    #This code checks against hardcoded intialization books
    #stay = True
    #while stay and len(hardcoded): #as long as there are still entries in hardcoded we need to check
     # toCheck = curr_recommendation #toCheck used to avoid modifying curr_recommendation as we loop through it
     # goodToGo = True #This get set to false, when we bring in a new book, meaning we need to loop through the books again
     # for entry in toCheck:
     #   if entry[0] in hardcoded:
     #     goodToGo = False
    #      curr_recommendation.remove(entry)#
    #      hardcoded.remove(entry[0]) #we no longer what to check this value
    #      curr_recommendation.append(self.curr_rec_list[0])
   #       self.curr_rec_list = self.curr_rec_list[1:]
   #       self.update_rec_list(matrix)
   #   if goodToGo:
  #      stay = False
    self.update_rec_list(matrix)
    return curr_recommendation

def lossFunction(self, expected, rating): 
  return abs(expected - rating)

def create_matrix(model):
  index = torch.IntTensor([range(53424)])
  #index = index.to(device)
  userMat = model.user_embedding(index)[0]
  index = torch.IntTensor([range(NumBooks)])
  #index = index.to(device)
  old = model.book_embedding(index)[0]
  bookMat = torch.zeros(24,NumBooks)
  for i in range(24):
    bookMat[i] = torch.narrow(old,1,i,1).flatten()
  #bookMat = bookMat.to(device)
  result = userMat@bookMat
  return torch.sigmoid(result)*5.5

def create_book_feature_matrix(model):
    index = torch.IntTensor([range(NumBooks)])
    return model.book_embedding(index)[0]

class RLModel(nn.Module):
  def __init__(self,user_vector, emb_dim):
    super(RLModel, self).__init__()
    self.embedding = nn.Embedding(1,emb_dim)
    self.embedding.weight = torch.nn.Parameter(user_vector) 
  def forward(self,input, matrix):
    book_vec = matrix[int(input)] #created using create_book_feature_matrix
    userNum = torch.LongTensor([0])

    result = (self.embedding(torch.LongTensor([[0]]))[0] * book_vec.view(1,24)).sum(1)
    return torch.sigmoid(result)
def getRec(user, book_id, b_matrix):
  user.rl_model.eval()
  with torch.no_grad():
   pred = user.rl_model(book_id, b_matrix)
  return pred[0].item()

def improve(swipe, book_id, user, b_matrix):
  user.rl_model.train()
  with torch.enable_grad():
    user.optimizer.zero_grad()
    pred = user.rl_model(book_id, b_matrix)
    loss = nn.MSELoss()
    improve = loss(pred, torch.FloatTensor([swipe]))
    improve.backward(retain_graph=True)
    user.optimizer.step()#

def get_book_data(book_id, collection):
    #print(collection.find_one({"book_id" :book_id})["title"])
    #print(type(book_id))
    return collection.find_one({"book_id":book_id})["title"], collection.find_one({"book_id":book_id})["authors"], collection.find_one({"book_id":book_id})["image_url"]

def get_recs(users, user_id, b_matrix, collection):
  #Assuming right now users stored in user-array, may need to change this to accomadate grabbing it from the database
  currUser = users[int(user_id)]
  recs = currUser.get_books(b_matrix)
  #print(recs)
  recList = []
  for book_id, _ in recs:
    #print(book_id)
    title, author, url = get_book_data(book_id, collection)
    #print(title)
    #print(author)
    #print(url)
    if title != title:
      #print("uh-oh")
      recList.append({"id":book_id, "name":"","author":author,"url":url})
    else:
      #print("we good")
      recList.append({"id":book_id, "name":title,"author":author,"url":url})
  #print(recList[0])
  return recList

def update_model(users, user_id, init_flag, sentiments, ratings, model_matrix, b_matrix): #sentiments is (book_id,sentiment)
  if init_flag:
    ratings.append([sentiments[0],5*sentiments[1]]) 
    if len(ratings) == 20:
      users[user_id] = User(ratings, model_matrix, user_id, emb_dim)
      users.append(0)
      ratings = []
  else:
    improve(sentiments[1], sentiments[0], users[int(user_id)], b_matrix) 

#