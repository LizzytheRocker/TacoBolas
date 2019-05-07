# this file interacts with the SQL code/database
import mysql.connector
import requests
import json

class Mdb:
  def __init__(self):
    self.currentPlayer =''
    try: 
      self.mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "Taco",
        database = "magiclocation"
      )
      self.cur = mydb.cursor()
    except:
      self.mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "Taco"
      )
      self.cur = self.mydb.cursor()
      self.cur.execute("CREATE DATABASE magiclocation")
      
      self.cur.execute("SHOW TABLES")

      if not self.cur:
        self.cur.execute("CREATE TABLE Player (Username varchar(32), Password varchar(32) NOT NULL, Firstname varchar(32), Lastname varchar(32), PRIMARY KEY (Username))")
        self.cur.execute("CREATE TABLE Card (Cardname varchar(100), DBID int AUTO_INCREMENT, OracleID int, foil int, LLocation varchar(100), Sname varchar(100), Uname varchar(100), ColorW bool, ColorU bool, ColorB bool, ColorR bool, ColorG bool, BanStandard bool, BanPauper bool, BanModern bool, BanPenny bool, BanCommander bool, PRIMARY KEY (DBID))")
        self.cur.execute("CREATE TABLE Cardset (Setname varchar(32), Datereleased date, PRIMARY KEY (Setname))")
        self.cur.execute("CREATE TABLE Location (Locationname varchar(100), PRIMARY KEY (Locationname))")

        self.cur.execute("ALTER TABLE Card ADD CONSTRAINT Card_Sname FOREIGN KEY (Sname) REFERENCES Cardset(Setname)")
        self.cur.execute("ALTER TABLE Card ADD CONSTRAINT Card_Uname FOREIGN KEY (Uname) REFERENCES Player(Username)")
        self.cur.execute("ALTER TABLE Card ADD CONSTRAINT Card_LLocation FOREIGN KEY (LLocation) REFERENCES Location(Locationname)")
  
  # insert card
  def insertWholeCard(self, Cardname, OracleID, foil, LLocation, Sname, ColorW=0, ColorU=0, ColorB=0, ColorR=0, ColorG=0, BanStandard=0, BanPauper=0, BanModern=0, BanPenny=0, BanCommander=0):
    #if set not in set table
    ST = "SELECT S.Setname FROM Cardset"
    self.cur.execute(ST)
    S  =self.cur.fetchall()
    missing = True
    for t in S:
      if Sname == t[0]:
        missing = False
        break
    if missing:
      self.insertCardset(Sname)
    #if location not in table
    LN = "SELECT L.Locationname FROM Location L"
    self.cur.execute(LN)
    L =self.cur.fetchall()
    missing=True
    for t in L:
      if LLocation == t[0]:
        missing = False
        break
    if missing:
      self.insertLocation(LLocation)

    param = "INSERT INTO Card VALUES('{}', {}, {}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(Cardname, OracleID, foil, LLocation, Sname, self.currentPlayer, ColorW, ColorU, ColorB, ColorR, ColorG, BanStandard, BanPauper, BanModern, BanPenny, BanCommander)
    self.cur.execute(param)
    self.mydb.commit()

  # log in?
  def logIn(self, username, password):
    #check if username/password combo match entry in db
    param ="SELECT P.Username, P.Password FROM Player P WHERE P.Username = '{}'".format(username)
    self.cur.execute(param)
    pw=self.cur.fetchall()
    Accept = False
    for x in pw:
      if x[1]==password:
        Accept=True
    #select the password
    if Accept:
      self.currentPlayer = username
      return True
    #if true, change self.currentPlayer to Uname
    return False

  # insert player
  def signUp(self, Username, Password, Firstname, Lastname):
    check = "SELECT P.Username FROM Player P"
    self.cur.execute(check)
    User=self.cur.fetchall()
    for x in User:
      if Username == x:
        return False
    param = "INSERT INTO Player VALUES('{}','{}','{}','{}')".format(Username, Password, Firstname, Lastname)
    self.cur.execute(param)
    self.mydb.commit()
    return True
    # login

  # insert location
  def insertLocation(self, locationname):
    LN = "SELECT L.Locationname FROM Location L"
    self.cur.execute(LN)
    L =self.cur.fetchall()
    missing=True
    for t in L:
      if locationname == t[0]:
        missing = False
        break
    if missing:
      param = "INSERT INTO Location VALUES ('{}')".format(locationname) 
      self.cur.execute(param)
      self.mydb.commit()

  def deletePlayer(self,username):
    par="DELETE FROM Player WHERE username = '{}'".format(username)
    self.cur.execute(par)
    self.mydb.commit()

  #insert cardset
  def insertCardset(self, Setname, Datereleased="NULL"):
    ST = "SELECT S.Setname FROM Cardset"
    self.cur.execute(ST)
    S  =self.cur.fetchall()
    missing = True
    for t in S:
      if Setname == t[0]:
        missing = False
        break
    if missing:
      par = "INSERT INTO Cardset VALUES ('{}','{}')".format(Setname,Datereleased)
      self.cur.execute(par)
      self.mydb.commit()
  
  # find card functions- By name, by color id, by banned or not, by foil, by set, -alot need to return dbid.. nvm lol.

  def CardsOwned(self):
    search = "SELECT * FROM Card AS C WHERE C.Pname='{}'".format(self.currentPlayer)
    self.cur.execute(search)
    res = self.cur.fetchall()
    #don't worry about printing it here, just return the res. I think its a tuple of tuples
    #for x in res:
    #  print(x)
    return res
    
  def CardbyName(self, name):
    if self.isLoggedIn():
      search = "SELECT * FROM Card AS C WHERE C.Pname = '{}' AND C.Cardname = '{}'".format(self.currentPlayer, name)
      self.cur.execute(search)
      res = self.cur.fetchall()
      return res
  
  def CardbyCI(self, ci): #i think ci will be a list but i'm unsure
    if self.isLoggedIn():
      return
  
  def banList(self, format): 
    if self.isLoggedIn():
      search = "SELECT * FROM Card AS C WHERE C.Pname = {} AND C.Ban{} = 1".format(self.currentPlayer, format)
      self.cur.execute(search)
      res = self.cur.fetchall()
      return res

  def notBanned(self, format):
    if self.isLoggedIn():
      search = "SELECT * FROM Card AS C WHERE C.Pname = {} AND C.Ban{} = 0".format(self.currentPlayer, format)
      self.cur.execute(search)
      res = self.cur.fetchall()
      return res

  def CardinFoil(self, name):
    if self.isLoggedIn():
      search = "SELECT * FROM Card AS C WHERE C.Pname = {} AND C.Cardname = '{}' AND C.foil = 1".format(self.currentPlayer, name)
      self.cur.execute(search)
      res = self.cur.fetchall()
      return res

  def CardsinSet(self, set):
    if self.isLoggedIn():
      search = "SELECT * FROM Card AS C WHERE C.Pname = {} AND C.Sname = '{}'".format(self.currentPlayer, set)
      self.cur.execute(search)
      res = self.cur.fetchall()
      return res

  def CardsinLoc(self, loc):
    if self.isLoggedIn():
      search = "SELECT * FROM Card AS C WHERE C.Pname = {} AND C.LLocation = '{}'".format(self.currentPlayer, loc)
      self.cur.execute(search)
      res = self.cur.fetchall()
      return res
  
  def doesLocExist(self, loc):
    search = "SELECT Locationname FROM Location AS L WHERE L.Locationname = '{}'"
    self.cur.execute(search)
    res = self.cur.fetchall()
    return (False, True)[res]
  
  # edit card location
  def editCardL(self, DBID, location):
    if self.isLoggedIn():
      if not self.doesLocExist(location):
        self.insertLocation(location)
      edit = "UPDATE Card AS C SET C.LLocation = '{}' WHERE C.Pname = '{}' AND C.DBID = {}".format(location, self.currentPlayer, DBID)
      self.cur.execute(edit)

  # delete card
  def deleteCard(self, DBID):
    if self.isLoggedIn():
      remove = "DELETE FROM Card WHERE Card.DBID = '{}'".format(DBID)
      self.cur.execute(remove)

  def isLoggedIn(self):
    return not self.currentPlayer == ''
  
  def logOut(self):
    self.currentPlayer = ''
  
  #Check requested Card is available
  def requestCheck(self, name, loc, foil):
    name.replace(" ", "+")
    G = 'https://api.scryfall.com/cards/search?unique=prints&q={}'.format(name)
    r = requests.get(G)
    if r.status_code == 200:
      cards = requestCard(G)
      if cards[totalcards] >1:
        ### retrieve 3 digit code ###
        code =
        card = retrieveCardList( cards, code)
        while card == None:
          ###try again, rerun code function
          code= 
          card = retrieveCardList( cards, code)
      elif cards[totalcards] ==1:
        card = card["data"][0]  
      ci = card["color_identity"]
      w,u,b,r,g = 0,0,0,0,0
      for c in ci:
        if c=='W':
          w= 1
        if c=='U':
          u =1
        if c=='B':
          b =1
        if c=='R':
          r = 1
        if c=='G':
          g = 1
      stan, paup,mod,pen,com = 0,0,0,0,0
      if card["legalities"]["standard"]=="legal":
        stan = 1
      if card["legalities"]["pauper"]=="legal":
        paup = 1
      if card["legalities"]["modern"]=="legal":
        mod = 1
      if card["legalities"]["penny"]=="legal":
        pen = 1
      if card["legalities"]["commander"]=="legal":
        com = 1
      self.insertinsertWholeCard(card["name"],card["oracle_id"],foil, loc, self.currentPlayer, w,u,b,r,g,stan, paup,mod,pen,com)
      return True
    else:
      return False

  #Request Card by name, return a dictonary
  def requestCard(url):
    r= requests.get(url)
    data = json.loads(r.text)
    return data

  #select card from dictionary using set 3 digit code (if nessicary)
  def retrieveCardList( cardL, dset):
    for x in cardL["data"]
      if x["set"]== dset:
        return x


  #Parse dictionary entry apart and enter it into the data base
  
# note to gabby: ternary statements are like (false, true)[condition]
  
if __name__ == "__main__":
  Taco = Mdb()
  
