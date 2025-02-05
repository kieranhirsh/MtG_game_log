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

/*LOCK TABLES `Colour_Identities` WRITE;*/
INSERT INTO `Colour_Identities` VALUES ('018240aa-1533-4c89-9a7e-8f7d57d849a4','Gruul','rg'),('04f42ef3-d4be-45ea-a289-031b7261ab38','Dune-Brood','brgw'),('1447712e-0fb2-4a08-a23e-9345923f3be1','Bant','gwu'),('218a0838-cbe1-4308-aabb-8de17cc5873b','Orzhov','wb'),('26842c69-c93d-4ad2-8627-cbe100b600f7','Mono-blue','u'),('302f8628-53b7-44e1-8d77-2aaf65538ba8','Rainbow','wubrg'),('3256d58c-f465-46ff-94f7-435625da0a3a','Yore-Tiller','wubr'),('3b391a97-4c58-4132-8200-68bc2898aef9','Mono-red','r'),('3de61941-7ac0-4230-aa3b-a8f079e64472','Boros','rw'),('532de6fb-59c1-487b-8931-47e70d5cefb2','Mardu','rwb'),('59cb4e07-0520-4b9e-b59c-96088df32978','Ink-Treader','rgwu'),('5d5f6800-e325-4507-a1d5-d8689cd714b9','Sultai','bgu'),('62eb1f23-0289-46f6-8d3e-ed016a341945','Golgari','bg'),('702360b8-7181-41a6-b8ac-662eeace3cf2','Dimir','ub'),('71f2e91c-12aa-4358-ae0b-affd4f823cb2','Temur','gur'),('7aa24b49-5e15-4fef-8e2a-8f8ee2984cc9','Esper','wub'),('7c705ad4-f0c3-467e-b480-63a9a809871c','Colourless',''),('7eda5111-5c65-493c-bc32-92a6261ce547','Selesnya','gw'),('880393b9-3191-4a6b-a4c5-42f97a659e2c','Witch-Maw','gwub'),('8a0eed82-6019-46e7-9683-21b622c859b4','Jeskai','urw'),('9aa54b57-e5f0-44b6-9c26-09b357a4d54f','Abzan','wbg'),('9fb8539e-2258-4239-bc87-de29d55565e0','Mono-green','g'),('a3dec342-cc95-49ec-8dae-4f966da95624','Grixis','ubr'),('ad5cec7a-e866-493a-a39c-a0bff8d46eef','Mono-white','w'),('b2f7fcf3-ce9f-4898-8d6b-d667de484db2','Jund','brg'),('b5fa6356-25a5-48d5-b2dc-c08a7df6ebe9','Izzet','ur'),('b6092dea-04b5-4c40-a089-6d297fb86cfb','Azorius','wu'),('c3daee5a-4ce2-4ccd-bec1-43953ee105c5','Rakdos','br'),('cf77b2f2-70ea-432b-8af0-46bfae139e50','Glint-Eye','ubrg'),('d37e8574-23c4-4dd1-a017-d0b9209bac69','Naya','rgw'),('ee1465f8-e828-4a00-baf7-adf39653c678','Simic','gu'),('ff8bc843-3aa7-4cd4-9db6-c378a69f57b7','Mono-black','b');
/*REVOKE WRITE on `Colour_Identities` FROM *;*/

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
