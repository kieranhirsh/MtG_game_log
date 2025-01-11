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
  `winner` varchar(128),
  `game_length_turns` integer,
  `die_roll_method_id` varchar(64),
  `start_time` time,
  `end_time` time,
  `game_length_time` time,
  PRIMARY KEY (`id`)
);

CREATE TABLE `Seat_1` (
  `id` varchar(64) NOT NULL,
  `game_id` varchar(64) NOT NULL,
  `deck_id` varchar(64) NOT NULL,
  `KO_turn` integer,
  `KO_method_id` varchar(64)
  PRIMARY KEY (`id`)
);

CREATE TABLE `Seat_2` (
  `id` varchar(64) NOT NULL,
  `game_id` varchar(64) NOT NULL,
  `deck_id` varchar(64) NOT NULL,
  `KO_turn` integer,
  `KO_method_id` varchar(64)
  PRIMARY KEY (`id`)
);

CREATE TABLE `Seat_3` (
  `id` varchar(64) NOT NULL,
  `game_id` varchar(64) NOT NULL,
  `deck_id` varchar(64) NOT NULL,
  `KO_turn` integer,
  `KO_method_id` varchar(64)
  PRIMARY KEY (`id`)
);

CREATE TABLE `Seat_4` (
  `id` varchar(64) NOT NULL,
  `game_id` varchar(64) NOT NULL,
  `deck_id` varchar(64) NOT NULL,
  `KO_turn` integer,
  `KO_method_id` varchar(64)
  PRIMARY KEY (`id`)
);

CREATE TABLE `Seat_5` (
  `id` varchar(64) NOT NULL,
  `game_id` varchar(64) NOT NULL,
  `deck_id` varchar(64) NOT NULL,
  `KO_turn` integer,
  `KO_method_id` varchar(64)
  PRIMARY KEY (`id`)
);

CREATE TABLE `Cards` (
  `id` varchar(64) NOT NULL,
  `name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `Decklists` (
  `id` varchar(64) NOT NULL,
  `deck_id` varchar(64) NOT NULL,
  `card_1_id` varchar(64) NOT NULL,
  `card_2_id` varchar(64) NOT NULL,
  `card_3_id` varchar(64) NOT NULL,
  `card_4_id` varchar(64) NOT NULL,
  `card_5_id` varchar(64) NOT NULL,
  `card_6_id` varchar(64) NOT NULL,
  `card_7_id` varchar(64) NOT NULL,
  `card_8_id` varchar(64) NOT NULL,
  `card_9_id` varchar(64) NOT NULL,
  `card_10_id` varchar(64) NOT NULL,
  `card_11_id` varchar(64) NOT NULL,
  `card_12_id` varchar(64) NOT NULL,
  `card_13_id` varchar(64) NOT NULL,
  `card_14_id` varchar(64) NOT NULL,
  `card_15_id` varchar(64) NOT NULL,
  `card_16_id` varchar(64) NOT NULL,
  `card_17_id` varchar(64) NOT NULL,
  `card_18_id` varchar(64) NOT NULL,
  `card_19_id` varchar(64) NOT NULL,
  `card_20_id` varchar(64) NOT NULL,
  `card_21_id` varchar(64) NOT NULL,
  `card_22_id` varchar(64) NOT NULL,
  `card_23_id` varchar(64) NOT NULL,
  `card_24_id` varchar(64) NOT NULL,
  `card_25_id` varchar(64) NOT NULL,
  `card_26_id` varchar(64) NOT NULL,
  `card_27_id` varchar(64) NOT NULL,
  `card_28_id` varchar(64) NOT NULL,
  `card_29_id` varchar(64) NOT NULL,
  `card_30_id` varchar(64) NOT NULL,
  `card_31_id` varchar(64) NOT NULL,
  `card_32_id` varchar(64) NOT NULL,
  `card_33_id` varchar(64) NOT NULL,
  `card_34_id` varchar(64) NOT NULL,
  `card_35_id` varchar(64) NOT NULL,
  `card_36_id` varchar(64) NOT NULL,
  `card_37_id` varchar(64) NOT NULL,
  `card_38_id` varchar(64) NOT NULL,
  `card_39_id` varchar(64) NOT NULL,
  `card_40_id` varchar(64) NOT NULL,
  `card_41_id` varchar(64) NOT NULL,
  `card_42_id` varchar(64) NOT NULL,
  `card_43_id` varchar(64) NOT NULL,
  `card_44_id` varchar(64) NOT NULL,
  `card_45_id` varchar(64) NOT NULL,
  `card_46_id` varchar(64) NOT NULL,
  `card_47_id` varchar(64) NOT NULL,
  `card_48_id` varchar(64) NOT NULL,
  `card_49_id` varchar(64) NOT NULL,
  `card_50_id` varchar(64) NOT NULL,
  `card_51_id` varchar(64) NOT NULL,
  `card_52_id` varchar(64) NOT NULL,
  `card_53_id` varchar(64) NOT NULL,
  `card_54_id` varchar(64) NOT NULL,
  `card_55_id` varchar(64) NOT NULL,
  `card_56_id` varchar(64) NOT NULL,
  `card_57_id` varchar(64) NOT NULL,
  `card_58_id` varchar(64) NOT NULL,
  `card_59_id` varchar(64) NOT NULL,
  `card_60_id` varchar(64) NOT NULL,
  `card_61_id` varchar(64) NOT NULL,
  `card_62_id` varchar(64) NOT NULL,
  `card_63_id` varchar(64) NOT NULL,
  `card_64_id` varchar(64) NOT NULL,
  `card_65_id` varchar(64) NOT NULL,
  `card_66_id` varchar(64) NOT NULL,
  `card_67_id` varchar(64) NOT NULL,
  `card_68_id` varchar(64) NOT NULL,
  `card_69_id` varchar(64) NOT NULL,
  `card_70_id` varchar(64) NOT NULL,
  `card_71_id` varchar(64) NOT NULL,
  `card_72_id` varchar(64) NOT NULL,
  `card_73_id` varchar(64) NOT NULL,
  `card_74_id` varchar(64) NOT NULL,
  `card_75_id` varchar(64) NOT NULL,
  `card_76_id` varchar(64) NOT NULL,
  `card_77_id` varchar(64) NOT NULL,
  `card_78_id` varchar(64) NOT NULL,
  `card_79_id` varchar(64) NOT NULL,
  `card_80_id` varchar(64) NOT NULL,
  `card_81_id` varchar(64) NOT NULL,
  `card_82_id` varchar(64) NOT NULL,
  `card_83_id` varchar(64) NOT NULL,
  `card_84_id` varchar(64) NOT NULL,
  `card_85_id` varchar(64) NOT NULL,
  `card_86_id` varchar(64) NOT NULL,
  `card_87_id` varchar(64) NOT NULL,
  `card_88_id` varchar(64) NOT NULL,
  `card_89_id` varchar(64) NOT NULL,
  `card_90_id` varchar(64) NOT NULL,
  `card_91_id` varchar(64) NOT NULL,
  `card_92_id` varchar(64) NOT NULL,
  `card_93_id` varchar(64) NOT NULL,
  `card_94_id` varchar(64) NOT NULL,
  `card_95_id` varchar(64) NOT NULL,
  `card_96_id` varchar(64) NOT NULL,
  `card_97_id` varchar(64) NOT NULL,
  `card_98_id` varchar(64) NOT NULL,
  `card_99_id` varchar(64) NOT NULL,
  `card_100_id` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
);
