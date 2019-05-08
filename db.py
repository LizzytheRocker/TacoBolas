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
        database = "magicloc"
      )
      self.cur = mydb.cursor()
    except:
      self.mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "Taco"
      )
      self.cur = self.mydb.cursor()
      self.cur.execute("CREATE DATABASE magicloc")
      
      self.cur.execute("SHOW TABLES")

      if not self.cur:
        self.cur.execute("CREATE TABLE Player (Username varchar(32), Password varchar(32) NOT NULL, Firstname varchar(32), Lastname varchar(32), PRIMARY KEY (Username))")
        self.cur.execute("CREATE TABLE Card (DBID int AUTO_INCREMENT, OracleID varchar(255), foil int, LLocation varchar(100), Sname varchar(100), Uname varchar(100), PRIMARY KEY (DBID, OracleID))")
        self.cur.execute("CREATE TABLE Carddata (OracleID varchar(255), Cardname varchar(100), ColorW boolean, ColorU boolean, ColorB boolean, ColorR boolean, ColorG boolean, BanStandard boolean, BanPauper boolean, BanModern boolean, BanPenny boolean, BanCommander boolean, PRIMARY KEY (OracleID))")

        self.cur.execute("ALTER TABLE Card ADD CONSTRAINT Card_Uname FOREIGN KEY (Uname) REFERENCES Player(Username)")
        self.cur.execute("ALTER TABLE Carddata ADD CONSTRAINT Card_OID FOREIGN KEY (OracleID) REFERENCES Card(OracleID)")
  
  def findOID(self, OID): ####Rember res is a tuple. so.... if its not none i think
    search = "SELECT D.OracleID FROM Carddata AS D WHERE D.OracleID = '{}'".format(OID)
    self.cur.execute(search)
    res = self.cur.fetchall()
    return res

  # insert card
  def insertWholeCard(self, Cardname, OracleID, foil, LLocation, Sname, ColorW=0, ColorU=0, ColorB=0, ColorR=0, ColorG=0, BanStandard=0, BanPauper=0, BanModern=0, BanPenny=0, BanCommander=0):
    param1 = "INSERT INTO Card VALUES('{}', {}, '{}', '{}', '{}')".format(OracleID, foil, LLocation, Sname, self.currentPlayer)
    self.cur.execute(param1)
    self.mydb.commit()
    if len(findOID(OracleID)) == 0: #thanks
      param2 = "INSERT INTO Carddata VALUES ('{}', '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(OracleID, Cardname, ColorW, ColorU, ColorB, ColorR, ColorG, BanStandard, BanPauper, BanModern, BanPenny, BanCommander)
      self.cur.execute(param2)
      self.mydb.commit()

  # log in
  def logIn(self, username, password):
    #check if username/password combo match entry in db
    param ="SELECT P.Username, P.Password FROM Player P WHERE P.Username = '{}'".format(username)
    self.cur.execute(param)
    pw=self.cur.fetchall()
    Accept = False
    for x in pw:
      if x[1]==password and x[0]==username:
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
    # redirect player to login

  def deletePlayer(self,username):
    par="DELETE FROM Player WHERE Username = '{}' CASCADE".format(username)
    self.cur.execute(par)
    self.mydb.commit()
  
  # find card functions- By name, by color id, by banned or not, by foil, by set, -alot need to return dbid.. nvm lol.

  def CardsOwned(self):
    search = "SELECT D.Cardname, C.foil, C.LLocation, C.Sname, D.ColorW, D.ColorU, D.ColorB, D.ColorR, D.ColorG, D.BanStandard, D.BanPauper, D.BanModern, D.BanPenny, D.BanCommander FROM Card as C, Carddata as D WHERE C.OracleID = D.OracleID AND C.Uname = '{}'".format(self.currentPlayer)
    self.cur.execute(search)
    res = self.cur.fetchall()
    return res
    
  def CardbyName(self, name):
    search = "SELECT D.Cardname, C.foil, C.LLocation, C.Sname, D.ColorW, D.ColorU, D.ColorB, D.ColorR, D.ColorG, D.BanStandard, D.BanPauper, D.BanModern, D.BanPenny, D.BanCommander FROM Card as C, Carddata as D WHERE C.OracleID = D.OracleID AND C.Uname = '{}' AND D.Cardname = '{}'".format(self.currentPlayer, name)
    self.cur.execute(search)
    res = self.cur.fetchall()
    return res
  
  def CardbyCI(self, ci): #i think ci will be a list but i'm unsure
    return
  
  def banList(self, format): 
    search = "SELECT D.Cardname, C.foil, C.LLocation, C.Sname, D.ColorW, D.ColorU, D.ColorB, D.ColorR, D.ColorG, D.BanStandard, D.BanPauper, D.BanModern, D.BanPenny, D.BanCommander FROM Card as C, Carddata as D WHERE C.OracleID = D.OracleID AND C.Uname = '{}' AND D.Ban{} = 1".format(self.currentPlayer, format)
    self.cur.execute(search)
    res = self.cur.fetchall()
    return res

  def notBanned(self, format):
    search = "SELECT D.Cardname, C.foil, C.LLocation, C.Sname, D.ColorW, D.ColorU, D.ColorB, D.ColorR, D.ColorG, D.BanStandard, D.BanPauper, D.BanModern, D.BanPenny, D.BanCommander FROM Card as C, Carddata as D WHERE C.OracleID = D.OracleID AND C.Uname = '{}' AND D.Ban{} = 0".format(self.currentPlayer, format)
    self.cur.execute(search)
    res = self.cur.fetchall()
    return res

  def CardinFoil(self, name):
    search = "SELECT D.Cardname, C.foil, C.LLocation, C.Sname, D.ColorW, D.ColorU, D.ColorB, D.ColorR, D.ColorG, D.BanStandard, D.BanPauper, D.BanModern, D.BanPenny, D.BanCommander FROM Card as C, Carddata as D WHERE C.OracleID = D.OracleID AND C.Uname = '{}' AND D.Cardname = '{}' AND C.foil = 1".format(self.currentPlayer)
    self.cur.execute(search)
    res = self.cur.fetchall()
    return res

  def CardsinSet(self, set):
    search = "SELECT D.Cardname, C.foil, C.LLocation, C.Sname, D.ColorW, D.ColorU, D.ColorB, D.ColorR, D.ColorG, D.BanStandard, D.BanPauper, D.BanModern, D.BanPenny, D.BanCommander FROM Card as C, Carddata as D WHERE C.OracleID = D.OracleID AND C.Uname = '{}' AND C.Sname = '{}'".format(self.currentPlayer, set)
    self.cur.execute(search)
    res = self.cur.fetchall()
    return res

  def CardsinLoc(self, loc):
    search = "SELECT D.Cardname, C.foil, C.LLocation, C.Sname, D.ColorW, D.ColorU, D.ColorB, D.ColorR, D.ColorG, D.BanStandard, D.BanPauper, D.BanModern, D.BanPenny, D.BanCommander FROM Card as C, Carddata as D WHERE C.OracleID = D.OracleID AND C.Uname = '{}' AND C.LLocation = '{}'".format(self.currentPlayer, loc)
    self.cur.execute(search)
    res = self.cur.fetchall()
    return res
  
  # thought this might be useful? -g
  def findDBID(self, Cardname, OracleID, foil, LLocation, Sname, ColorW, ColorU, ColorB, ColorR, ColorG, BanStandard, BanPauper, BanModern, BanPenny, BanCommander):
    search = "SELECT C.DBID FROM Card AS C, Carddata AS D WHERE C.OracleID = D.OracleID AND D.Cardname = '{}' AND D.OracleID = '{}' AND C.foil = {} AND C.LLocation = '{}' AND C.Sname = '{}' AND D.ColorW = {} AND D.ColorU = {} AND D.ColorB = {} AND D.ColorR = {} AND D.ColorG = {} AND D.BanStandard = {} AND D.BanPauper = {} AND D.BanModern = {} AND D.BanPenny = {} AND D.BanCommander = {}".format(Cardname, OracleID, foil, LLocation, Sname, ColorW, ColorU, ColorB, ColorR, ColorG, BanStandard, BanPauper, BanModern, BanPenny, BanCommander)
    self.cur.execute(search)
    res = self.cur.fetchall()
    return res

  def editCardL(self, DBID, location):
    edit = "UPDATE Card AS C SET C.LLocation = '{}' AND C.Pname = '{}' AND C.DBID = {}".format(location, self.currentPlayer, DBID)
    self.cur.execute(edit)
    self.mydb.commit()

  def deleteCard(self, DBID):
    remove = "DELETE FROM Card WHERE Card.DBID = '{}' CASCADE".format(DBID)
    self.cur.execute(remove)
    self.mydb.commit()

  def isLoggedIn(self):
    return not len(self.currentPlayer) == 0
  
  def logOut(self):
    self.currentPlayer = ''

  # api stuff below
  
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
  
if __name__ == "__main__":
  Taco = Mdb()
  
