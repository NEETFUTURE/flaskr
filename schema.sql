drop table if exists entry;
create table entries (
	id integer primary key autoincrement,
	username string not null,
	text string not null
	);

create table users (
	id integer primary key autoincrement,
	username string not null,
	pass string not null
	);
	 
