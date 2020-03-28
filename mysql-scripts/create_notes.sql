CREATE TABLE notes(
    id int unsigned primary key auto_increment,
    title varchar(255),
    creation_date datetime,
    user_id int unsigned,
    content text
);

