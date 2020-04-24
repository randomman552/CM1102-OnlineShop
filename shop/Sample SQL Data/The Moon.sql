-- Get ID of existing The Moon:
set @ID = (select `ID` from `product` where `name` = "The Moon");

-- Delete any old data for The Moon:
delete from `review` where `productID` = @ID;
delete from `picture` where `productID` = @ID;
delete from `product_category` where `productID` = @ID;
delete from `product` where `ID` = @ID;

-- The Moon creation statement:
insert into `product` (`name`, `_price`, `description`, `_mass`, `_surface_gravity`, `_orbital_period`)
values ("The Moon", 5000000000000000, "The Moon, very original name." , 73480000000000000000000, 1.624, 0.0747);

-- Get new ID:
set @ID = (select `ID` from `product` where `name` = "The Moon");

-- Some sample images for earth:
insert into picture (productID, URL)
values (@ID, "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2F4.bp.blogspot.com%2F-GOHT016yZNQ%2FVNwOoj0G_3I%2FAAAAAAAACUQ%2Fbh5W9SrBTXA%2Fs1600%2Ffull-moon.jpg&f=1&nofb=1");

insert into picture (productID, URL)
values (@ID, "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.K1rTO9kxxlFiSvhaKqI9ygHaHa%26pid%3DApi&f=1");

-- Some sample reviews for earth:
insert into review (`productID`, `rating`, `content`)
values (@ID, 1, "I can't breathe here.");

insert into review (`productID`, `rating`, `content`)
values (@ID, 5, "");

insert into review (`productID`, `rating`, `content`)
values (@ID, 5, "Wonderful!");

-- Setup categories for earth (this requires setup of categories first):
insert into `product_category` (`productID`, `categoryID`)
values (@ID, (select `ID` from `category` where `name` = "Moon"));

insert into `product_category` (`productID`, `categoryID`)
values (@ID, (select `ID` from `category` where `name` = "Rocky Body"));