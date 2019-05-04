--Databases Project Phase 3


CREATE TABLE Player
(
    Username   varchar(32),
    Password   varchar(32),
	Firstname   varchar(32),
    Lastname   varchar(32),
    PRIMARY KEY (Username)
);

CREATE TABLE Card
(
    Cardname   varchar(100),
    DBID     int,
    OracleID     int,
    foil int,
    LLocation   varchar(100),
	Sname   varchar(100),
	Pname   varchar(100),
	ColorID varchar(128),
	ColorIDtwo varchar(128),
	ColorIDthree varchar(128),
	ColorIDfour varchar(128),
	ColorIDfive varchar(128),
	Banlist varchar(128),
	Banlisttwo varchar(128),
	Banlistthree varchar(128),
	Banlistfour varchar(128),
	Banlistfive varchar(128),
    PRIMARY KEY (DBID)
);

CREATE TABLE Cardset
(
    Setname   varchar(32),
    Datereleased   date,
    PRIMARY KEY (Setname)
);


CREATE TABLE Location
(
    Locationname   varchar(100),
    PRIMARY KEY (Locationname)
);


ALTER TABLE Card ADD CONSTRAINT Card_Sname FOREIGN KEY (Sname) REFERENCES Cardset(Setname);
ALTER TABLE Card ADD CONSTRAINT Card_Pname FOREIGN KEY (Username) REFERENCES Player(Username);
ALTER TABLE Card ADD CONSTRAINT Card_LLocation FOREIGN KEY (LLocation) REFERENCES Location(Locationname);



--Get all of the cards owned by a certain player.
SELECT C.*
FROM Card C, Player P
WHERE C.Pname=P.Username;

--Get the information of the owner of the card (optional, may not be needed).
SELECT P.*
FROM Card C, Player P
WHERE C.Pname=P.Username;

--Get all of the information of cards stored in a given location.
SELECT C.*
FROM Card C, Location L
WHERE C.LLocation=L.Locationname;

--Get the information of a location that a card is in.
SELECT L.*
FROM Card C, Location L
WHERE C.LLocation=L.Locationname;

--Get the information of all cards belonging to a certain set.
SELECT C.*
FROM Card C, Cardset S
WHERE C.Sname=S.Setname;

--Get the information of the set that a card belongs to.
SELECT S.*
FROM Card C, Cardset S
WHERE C.Sname=S.Setname;








