-- This file is for setting up some sample categories
-- Delete all existing categories
delete from `product_category` where `ID` > 0;
delete from `category` where `ID` > 0;

insert into `category` (`name`)
values ("Planet");

insert into `category` (`name`)
values ("Rocky Body");

insert into `category` (`name`)
values ("Gas Giant");

insert into `category` (`name`)
values ("Moon");

insert into `category` (`name`)
values ("Star");

insert into `category` (`name`)
values("Habitable");
