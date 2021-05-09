import torch, torchtext, numpy as np
import pandas as pd, csv
from torch import nn, optim
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import pdb
torch.manual_seed(291)
np.random.seed(291)
import pandas as pd

#Code adapted and inspired by movie recommender model in lecture 6
class Dataset(torch.utils.data.Dataset):
    def __init__(self, fn, books):
        self.dataframe = pd.read_csv(fn)
        self.books = pd.read_csv(books)
        u2n = { u: n for n, u in enumerate(self.dataframe['user_id'].unique()) } 
        df_book_conv = { m : m-1 for m in self.dataframe['book_id'] } 
        books_book_conv = {m : m-1 for m in self.books['book_id'] }
        self.dataframe['user_id'] = self.dataframe['user_id'].apply(lambda u: u2n[u])
        self.dataframe['book_id'] = self.dataframe['book_id'].apply(lambda m: df_book_conv[m]) #These book id conversion lambda functions may not be properly written
        self.books['book_id'] = self.books['book_id'].apply(lambda m: books_book_conv[m])
        self.coords = torch.LongTensor(self.dataframe[['user_id','book_id']].values) # (userId,bookId) <- coordinates
        self.ratings = torch.FloatTensor(self.dataframe['rating'].values)
        self.n_users = self.dataframe['user_id'].nunique()
        self.n_books = self.dataframe['book_id'].nunique()

    def __len__(self):
        return len(self.coords)
    
    def get_book_info(self, book_id): #This is wrong
      return (self.books[self.books["book_id"] == book_id]).loc[:,"original_title"].values[0], (self.books[self.books["book_id"] == book_id]).loc[:,"authors"].values[0], (self.books[self.books["book_id"] == book_id]).loc[:,"image_url"].values[0]

    def __getitem__(self, i):  
      return (self.coords[i], self.ratings[i]) 
#Dataset set up code
!wget https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/ratings.csv #Not sure this same formatting will work in a .py file
!wget https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/books.csv #Same as above
ds_full = Dataset('ratings.csv', 'books.csv')
n_train = int(0.8 * len(ds_full))
n_test = len(ds_full) - n_train
rng = torch.Generator().manual_seed(291)
ds_train, ds_test = torch.utils.data.random_split(ds_full, [n_train, n_test], rng)
len(ds_full)

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
  for i in range(ds_full.n_users): # 5 for now but should be ds_full.n_users
    diff = 0
    for rating in ratings:
      diff = diff + np.abs(matrix[i][rating[0]] - rating[1])#Matrix will be tensor - may need to accomadate if so adjust future uses
    if diff < bestDiff:
      bestDiff = diff
      bestUser = i
  return bestUser
NumBooks = 5 #Constant number of books to recommend per iteration
RecBatches = 300 #Constant number of books to add to the recommendation list for RL
BoostBatch = 100 #Constant number of books to add to the rec list when needed
BoostThreshold = RecBatches-BoostBatch

class User ():
  def __init__(self, ratings, matrix, id, emb_dim):
    self.id = id
    self.ratings = ratings
    self.pair_id = find_paired_user(ratings, matrix)
    emb_index = torch.LongTensor([self.pair_id])
    emb_index = emb_index.to(device) #May need to remove to call
    user_feature_vector = model.user_embedding(emb_index) # get feature vector for user 0
    row = matrix[self.pair_id].numpy()
    for i in range(10000):
      self.to_recommend[i]= [i, row[i]]
    self.to_recommend = np.sort(self.to_recommend)[::-1] #Make sure this is sorting to_recommend based on row[i]
    self.rl_model = RLModel(user_vector, emb_dim)#Need to change RLModel to initialize from a provided vector
    self.optimizer = optim.SGD(self.rl_model.parameters(),0.01,0.3)
    self.curr_rec_list = self.to_recommend[0:RecBatches]
    self.to_recommend = self.to_recommend[RecBatches:] #Double check for off by one errors
  def get_books(self):
    curr_recommendation = self.curr_rec_list[0:NumBooks]
    self.to_recommend = self.curr_rec_list[NumBooks:] #Double check for off by one errors
    update_rec_list(self)
    return curr_recommendation
  def update_rec_list(self):
    if len(self.curr_rec_list) < BoostThreshold:
      self.curr_rec_list.append(self.to_recommend[0:BoostBatch])
      self.to_recommend = self.to_recommend[BoostBatch:]
    for i in range(len(self.curr_rec_list)):
      self.curr_rec_list[i][1] = self.rl_model(self.curr_rec_list[i][0])
    self.curr_rec_list =  np.sort(self.curr_rec_list)[::-1]

def lossFunction(self, expected, rating): 
  return abs(expected - rating)

def create_matrix():
  index = torch.IntTensor([range(53424)])
  index = index.to(device)
  userMat = model.user_embedding(index)[0]
  index = torch.IntTensor([range(10000)])
  index = index.to(device)
  old = model.book_embedding(index)[0]
  bookMat = torch.zeros(24,10000)
  for i in range(24):
    bookMat[i] = torch.narrow(old,1,i,1).flatten()
  bookMat = bookMat.to(device)
  result = userMat@bookMat
  return torch.sigmoid(result)*5.5

def create_book_feature_matrix(model):
    index = torch.IntTensor([range(10000)])
    return model.book_embedding(index)[0]

class RLModel(nn.Module):
  def __init__(self,user_vector, emb_dim):
    super(RLModel, self).__init__()
    self.embedding = nn.Embedding(1,emb_dim)
    self.embedding.weight = user_vector #may need to mess around with some tensor dimensions
  def forward(self,input):
    book_vec = BookFeatureMatrix[input] #created using create_book_feature_matrix
    userNum = torch.LongTensor([0])
    result = torch.dot(self.embedding(userNum), book_vec)
    return torch.sigmoid(result)
def getRec(user, book_id):
  user.rl_model.train()
  with torch.enable_grad():
    pred = user.rl_model(book_id)
    return pred

def improve(swipe, pred, user):
  user.rl_model.train()
  user.optimizer.zero_grad()
  loss = lossFunction
  improve = loss(pred, swipe)
  improve.backward()
  user.rl_model.optimizer.step()


def get_recs(user_id):
  #Assuming right now users stored in user-array, may need to change this to accomadate grabbing it from the database
  currUser = users[user_id] #This array needs to be definied on initialization
  recs = currUser.get_books()
  recList = [],
  for book_id, _ in recs:
    title, author, url = ds_full.get_book_info(book_id)
    recList.append({"book id":book_id, "book title":title,"author name":author,"url":url})
  return recList

def update_model(user_id, init_flag, sentiments): #sentiments is (book_id,sentiment)
  if init_flag:
    ratings.append([sentiments[0].sentiments[1]) #this will need to be stored somewhere for user setup
    if len(ratings) == 20:
      users[user_id] = User(ratings, model_matrix, user_id, emb_dim)
  else:
    exp_rec = getRec(users[user_id],sentiments[0])
    result = sentiments[1]
    improve(result, exp_rec,users[user_id]) 

