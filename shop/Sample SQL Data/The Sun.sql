-- Get ID of existing The Sun
set @ID = (select `ID` from `product` where `name` = "The Sun");

-- Delete any old data for The Sun
delete from `review` where `productID` = @ID;
delete from `picture` where `productID` = @ID;
delete from `product_category` where `productID` = @ID;
delete from `product` where `ID` = @ID;

-- The Sun creation statement:
insert into `product` (`name`, `_price`, `description`, `_mass`, `_surface_gravity`, `_orbital_period`)
values ("The Sun", 1000000000000000000, "It's The Sun. VERY HOT" , 1989000000000000000000000000000, 274, 225000000);

-- Get new ID:
set @ID = (select `ID` from `product` where `name` = "The Sun");

-- Some sample images for earth:
insert into picture (productID, URL)
values (@ID, "https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fsunorbit.net%2Fpicts%2FSun_gr.jpg&f=1&nofb=1");

-- Some sample reviews for earth:
insert into review (`productID`, `rating`, `content`)
values (@ID, 1, "MY EYES");

insert into review (`productID`, `rating`, `content`)
values (@ID, 1, "It's too hot");

-- Setup categories for earth (this requires setup of categories first):
insert into `product_category` (`productID`, `categoryID`)
values (@ID, (select `ID` from `category` where `name` = "Star"));
