# this file interacts with the SQL code/database
import mysql.connector



class Mdb:
  def __init__(self):
    self.currentPlayer =''
    #try: 
    self.mydb = mysql.connector.connect(
      host = "localhost",
      user = "root",
      passwd = "Taco",
      database = "magicloc"
      )
    self.cur = self.mydb.cursor(buffered=True)

    # except:
    #   self.mydb = mysql.connector.connect(
    #     host = "localhost",
    #     user = "root",
    #     passwd = "Taco"
    #   )
    #   self.cur = self.mydb.cursor()
    #   self.cur.execute("CREATE DATABASE magicloc")
      
    self.cur.execute("SHOW TABLES")
    r=self.cur.fetchall()

    if r == []:
      self.cur.execute("CREATE TABLE Player (Username varchar(32), Password varchar(32) NOT NULL, Firstname varchar(32), Lastname varchar(32), PRIMARY KEY (Username))")
      self.mydb.commit()
      self.cur.execute("CREATE TABLE Card (DBID int NOT NULL IDENTITY(1,1), OracleID varchar(255), foil int, LLocation varchar(100), Sname varchar(100), Uname varchar(100), PRIMARY KEY (DBID, OracleID))")
      self.mydb.commit()      
      self.cur.execute("CREATE TABLE Carddata (OracleID varchar(255), Cardname varchar(100), ColorW boolean, ColorU boolean, ColorB boolean, ColorR boolean, ColorG boolean, BanStandard boolean, BanPauper boolean, BanModern boolean, BanPenny boolean, BanCommander boolean, PRIMARY KEY (OracleID))")
      self.mydb.commit()
      self.cur.execute("ALTER TABLE Card ADD CONSTRAINT Card_Uname FOREIGN KEY (Uname) REFERENCES Player(Username)")
      self.mydb.commit()
      self.cur.execute("ALTER TABLE Card ADD CONSTRAINT Card_OID FOREIGN KEY (OracleID) REFERENCES Carddata(OracleID)")
      self.mydb.commit()  

  def findOID(self, OID): ####Rember res is a tuple. so.... if its not none i think
    search = "SELECT D.OracleID FROM Carddata AS D WHERE D.OracleID = '{}'".format(OID)
    self.cur.execute(search)
    res = self.cur.fetchall()
    return res

  def findOIDinCard(self, OID): ####Rember res is a tuple. so.... if its not none i think
    search = "SELECT D.OracleID FROM Card AS D WHERE D.OracleID = '{}'".format(OID)
    self.cur.execute(search)
    res = self.cur.fetchall()
    return res

  # insert card
  def insertWholeCard(self, Cardname, OracleID, foil, LLocation, Sname, ColorW=0, ColorU=0, ColorB=0, ColorR=0, ColorG=0, BanStandard=0, BanPauper=0, BanModern=0, BanPenny=0, BanCommander=0):
    if len(self.findOID(OracleID)) == 0: #thanks
      param2 = "INSERT INTO Carddata VALUES ('{}', '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(OracleID, Cardname, ColorW, ColorU, ColorB, ColorR, ColorG, BanStandard, BanPauper, BanModern, BanPenny, BanCommander)
      self.cur.execute(param2)
      self.mydb.commit()
    param1 = "INSERT INTO Card (OracleID, foil, LLocation, Sname, Uname) VALUES('{}', {}, '{}', '{}', '{}')".format(OracleID, foil, LLocation, Sname, self.currentPlayer)
    self.cur.execute(param1)
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
      if Username == x[0]:
        return False
    param = "INSERT INTO Player VALUES('{}','{}','{}','{}')".format(Username, Password, Firstname, Lastname)
    self.cur.execute(param)
    self.mydb.commit()
    return True
    # redirect player to login

  def deletePlayer(self,username):
    cards = self.CardsOwnedInternal()
    for x in cards:
      self.deleteCard(x[1],x[0])

    par="DELETE FROM Player WHERE Username = '{}'".format(username)
    self.cur.execute(par)
    self.mydb.commit()
  
  # find card functions- By name, by color id, by banned or not, by foil, by set, -alot need to return dbid.. nvm lol.

  #new
  def CardsOwnedInternal(self):
    search = "SELECT * FROM Card as C, Carddata as D WHERE C.OracleID = D.OracleID AND C.Uname = '{}'".format(self.currentPlayer)
    self.cur.execute(search)
    res = self.cur.fetchall()
    return res

  def CardsOwned(self):
    search = "SELECT D.Cardname, C.foil, C.LLocation, C.Sname, D.ColorW, D.ColorU, D.ColorB, D.ColorR, D.ColorG, D.BanStandard, D.BanPauper, D.BanModern, D.BanPenny, D.BanCommander FROM Card as C, Carddata as D WHERE C.OracleID = D.OracleID AND C.Uname = '{}'".format(self.currentPlayer)
    self.cur.execute(search)
    res = self.cur.fetchall()
    return res
    
  #new
  def CardbyNameInternal(self, name):
    search = "SELECT * FROM Card as C, Carddata as D WHERE C.OracleID = D.OracleID AND C.Uname = '{}' AND D.Cardname = '{}'".format(self.currentPlayer, name)
    self.cur.execute(search)
    res = self.cur.fetchall()
    return res

  def CardbyName(self, name):
    search = "SELECT D.Cardname, C.foil, C.LLocation, C.Sname, D.ColorW, D.ColorU, D.ColorB, D.ColorR, D.ColorG, D.BanStandard, D.BanPauper, D.BanModern, D.BanPenny, D.BanCommander FROM Card as C, Carddata as D WHERE C.OracleID = D.OracleID AND C.Uname = '{}' AND D.Cardname = '{}'".format(self.currentPlayer, name)
    self.cur.execute(search)
    res = self.cur.fetchall()
    return res
  
  def CardbyCI(self, W, U, B, R, G):
    search = "SELECT D.Cardname, C.foil, C.LLocation, C.Sname, D.ColorW, D.ColorU, D.ColorB, D.ColorR, D.ColorG, D.BanStandard, D.BanPauper, D.BanModern, D.BanPenny, D.BanCommander FROM Card as C, Carddata as D WHERE C.OracleID = D.OracleID AND C.Uname = '{}' AND D.ColorW = {} AND D.ColorU = {} AND D.ColorB = {} AND D.ColorR = {} AND D.ColorG = {}".format(self.currentPlayer, W, U, B, R, G)
    self.cur.execute(search)
    res = self.cur.fetchall()
    return res
  
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

  def CardinFoil(self):
    search = "SELECT D.Cardname, C.foil, C.LLocation, C.Sname, D.ColorW, D.ColorU, D.ColorB, D.ColorR, D.ColorG, D.BanStandard, D.BanPauper, D.BanModern, D.BanPenny, D.BanCommander FROM Card as C, Carddata as D WHERE C.OracleID = D.OracleID AND C.Uname = '{}' AND C.foil = 1".format(self.currentPlayer)
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
    edit = "UPDATE Card AS C SET C.LLocation = '{}' WHERE C.Uname = '{}' AND C.DBID = {}".format(location, self.currentPlayer, DBID)
    self.cur.execute(edit)
    self.mydb.commit()

  def deleteCard(self, OID, DBID):
    remove = "DELETE FROM Card WHERE Card.DBID = '{}'".format(DBID)
    self.cur.execute(remove)
    self.mydb.commit()
    if len(self.findOIDinCard(OID))+1 == 1:
      remove = "DELETE FROM Carddata WHERE Carddata.OracleID = '{}'".format(OID)
      self.cur.execute(remove)
      self.mydb.commit()

  def isLoggedIn(self):
    return not len(self.currentPlayer) == 0
  
  def logOut(self):
    self.currentPlayer = ''

  # api stuff below
  
  # def requestCheck(self, name, loc, foil):
  #   name.replace(" ", "+")
  #   G = 'https://api.scryfall.com/cards/search?unique=prints&q={}'.format(name)
  #   r = requests.get(G)
  #   if r.status_code == 200:
  #     cards = requestCard(G)
  #     if cards[totalcards] >1:
  #       ### retrieve 3 digit code ###
  #       code =
  #       card = retrieveCardList( cards, code)
  #       while card == None:
  #         ###try again, rerun code function
  #         code= 
  #         card = retrieveCardList( cards, code)
  #     elif cards[totalcards] ==1:
  #       card = card["data"][0]  
  #     ci = card["color_identity"]
  #     w,u,b,r,g = 0,0,0,0,0
  #     for c in ci:
  #       if c=='W':
  #         w= 1
  #       if c=='U':
  #         u =1
  #       if c=='B':
  #         b =1
  #       if c=='R':
  #         r = 1
  #       if c=='G':
  #         g = 1
  #     stan, paup,mod,pen,com = 0,0,0,0,0
  #     if card["legalities"]["standard"]=="legal":
  #       stan = 1
  #     if card["legalities"]["pauper"]=="legal":
  #       paup = 1
  #     if card["legalities"]["modern"]=="legal":
  #       mod = 1
  #     if card["legalities"]["penny"]=="legal":
  #       pen = 1
  #     if card["legalities"]["commander"]=="legal":
  #       com = 1
  #     self.insertinsertWholeCard(card["name"],card["oracle_id"],foil, loc, self.currentPlayer, w,u,b,r,g,stan, paup,mod,pen,com)
  #     return True
  #   else:
  #     return False

  # #Request Card by name, return a dictonary
  # def requestCard(url):
  #   r= requests.get(url)
  #   data = json.loads(r.text)
  #   return data

  # #select card from dictionary using set 3 digit code (if nessicary)
  # def retrieveCardList( cardL, dset):
  #   for x in cardL["data"]
  #     if x["set"]== dset:
  #       return x


  # #Parse dictionary entry apart and enter it into the data base
  
if __name__ == "__main__":
  Taco = Mdb()
  Taco.signUp("gabrielle", "Hunter2", "Gabrielle", "Watson")
  Taco.logIn("gabrielle", "Hunter2")

  Taco.insertWholeCard("Name", "584-gjdl-583290", 0, "in my butt", "cool set 1", 1, 0, 0, 0, 0, 0, 1, 1, 0, 0)

  print(Taco.CardbyNameInternal("Name"))
  
  # print("1", Taco.CardsOwned())
  # print("2", Taco.CardbyName("Name"))
  # print("3", Taco.CardbyName("Nameo"))
  # print("4", Taco.banList("Modern"))
  # print("5", Taco.banList("Commander"))
  # print("6", Taco.notBanned("Commander"))
  # print("7", Taco.notBanned("Modern"))
  # print("8", Taco.CardinFoil("Name"))
  # print("9", Taco.CardsinSet("cool set 1"))
  # print("10", Taco.CardsinSet("cool set 2"))
  # print("11", Taco.CardsinLoc("in my butt"))
  # print("12", Taco.CardsinLoc("not in my butt"))

  Taco.deletePlayer("gabrielle")

  Taco.logOut()
  
