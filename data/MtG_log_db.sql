DROP DATABASE IF EXISTS MtG_log;
CREATE DATABASE MtG_log;
USE MtG_log;

CREATE TABLE `Players` (
  `id` varchar(64) NOT NULL,
  `name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `Decks` (
  `id` varchar(64) NOT NULL,
  `commander` varchar(128) NOT NULL,
  `player_id` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `KO_categories` (
  `id` varchar(64) NOT NULL,
  `KO_category` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `KO_methods` (
  `id` varchar(64) NOT NULL,
  `KO_method` varchar(128) NOT NULL,
  `KO_category_id` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `Die_roll_methods` (
  `id` varchar(64) NOT NULL,
  `method` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `Games` (
  `id` varchar(64) NOT NULL,
  `date` datetime NOT NULL,
  `seat_1_deck_id` varchar(64) NOT NULL,
  `seat_1_KO_turn` integer,
  `seat_1_KO_method_id` varchar(64),
  `seat_2_deck_id` varchar(64) NOT NULL,
  `seat_2_KO_turn` integer,
  `seat_2_KO_method_id` varchar(64),
  `seat_3_deck_id` varchar(64),
  `seat_3_KO_turn` integer,
  `seat_3_KO_method_id` varchar(64),
  `seat_4_deck_id` varchar(64),
  `seat_4_KO_turn` integer,
  `seat_4_KO_method_id` varchar(64),
  `seat_5_deck_id` varchar(64),
  `seat_5_KO_turn` integer,
  `seat_5_KO_method_id` varchar(64),
  `Die_roll_method_id` varchar(64),
  PRIMARY KEY (`id`)
);
