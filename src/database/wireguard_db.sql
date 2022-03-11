create table Users (
   user_id  varchar(9),
   email   varchar(32),
   username     varchar(32),
   password  varchar(64),
   admin      bool,
   banned   bool,
   primary key (user_id)
)
