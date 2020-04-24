-- Get ID of existing Earth
set @ID = (select `ID` from `product` where `name` = "Earth");

-- Delete any old data for Earth
delete from `review` where `productID` = @ID;
delete from `picture` where `productID` = @ID;
delete from `product_category` where `productID` = @ID;
delete from `product` where `ID` = @ID;

-- Earth creation statement:
insert into `product` (`name`, `_price`, `description`, `_mass`, `_surface_gravity`, `_orbital_period`)
values ("Earth", 500000000000000000, "It's Earth, definetly not flat." , 5972000000000000000000000, 9.8, 1);

-- Get new ID:
set @ID = (select `ID` from `product` where `name` = "Earth");

-- Some sample images for earth:
insert into picture (productID, URL)
values (@ID, "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fplanetary.s3.amazonaws.com%2Fassets%2Fimages%2F3-earth%2F2017%2F20171005_epic_1b_20171003072042.jpg&f=1&nofb=1");

insert into picture (productID, URL)
values (@ID, "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.tvovermind.com%2Fwp-content%2Fuploads%2F2017%2F09%2FPlanet-Earth.jpg&f=1&nofb=1");

insert into picture (productID, URL)
values (@ID, "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimages.newscientist.com%2Fwp-content%2Fuploads%2F2019%2F09%2F09162708%2Fiss048-e-2035_lrg.jpg&f=1&nofb=1");

insert into picture (productID, URL)
values (@ID, "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.thisiscolossal.com%2Fwp-content%2Fuploads%2F2019%2F01%2FTheWorldFacebook1.jpg&f=1&nofb=1");

insert into picture (productID, URL)
values (@ID, "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2F2%2F2c%2FRotating_earth_%2528large%2529.gif&f=1&nofb=1");

-- Some sample reviews for earth:
insert into review (`productID`, `rating`, `content`)
values (@ID, 5, "I can see my house from here!");

insert into review (`productID`, `rating`, `content`)
values (@ID, 4, "The view is fantastic.");

insert into review (`productID`, `rating`, `content`)
values (@ID, 2, "The place may be nice, but some of the people are terrible.");

-- Setup categories for earth (this requires setup of categories first):
insert into `product_category` (`productID`, `categoryID`)
values (@ID, (select `ID` from `category` where `name` = "Planet"));

insert into `product_category` (`productID`, `categoryID`)
values (@ID, (select `ID` from `category` where `name` = "Rocky Body"));

insert into `product_category` (`productID`, `categoryID`)
values (@ID, (select `ID` from `category` where `name` = "Habitable"));