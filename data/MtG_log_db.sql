DROP DATABASE IF EXISTS MtG_log;
CREATE DATABASE MtG_log;
USE MtG_log;

CREATE TABLE Players (
  id varchar(64) NOT NULL,
  name varchar(128) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE Colour_Identities (
  id varchar(64) NOT NULL,
  colour_identity varchar(128) NOT NULL,
  colours varchar(128) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE Decks (
  id varchar(64) NOT NULL,
  commander varchar(128) NOT NULL,
  player_id varchar(64) NOT NULL,
  colour_identity_id varchar(64) NOT NULL,
  PRIMARY KEY (id),
  KEY player_id (player_id),
  KEY colour_identity_id (colour_identity_id),
  CONSTRAINT decks_ibfk_1 FOREIGN KEY (player_id) REFERENCES Players (id),
  CONSTRAINT decks_ibfk_2 FOREIGN KEY (colour_identity_id) REFERENCES Colour_Identities (id)
);
