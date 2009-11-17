#Our database is called 'review' so we must select it.
use review;
#If you change the format of the tables you need to drop them
#so that the create table will succeed.
#drop table user;
#drop table authorizations;

#create any tables that don't already exist.
create table if not exists authorization(
 authorization_id int not null auto_increment primary key,
 name varchar(40) not null,
 description varchar(255) not null);
 
create table if not exists user(
 user_id int not null auto_increment primary key,
 authorization_id int not null,
 username varchar(40) not null,
 password varchar(40) not null,
 first_name varchar(40) not null,
 last_name varchar(40) not null,
 email varchar(80) not null,
 credentials varchar(255), 
 foreign key (authorization_id) references authorization(auth_id) on delete cascade
);

create table if not exists submission(
 user_id int not null,
 performance_id int not null,
 submission_date date not null,
 primary key (user_id, performance_id),
 foreign key (user_id) references user(user_id) on delete cascade,
 foreign key (performance_id) references performance(performance_id) on delete cascade
);

create table if not exists reviewer_assignment(
 user_id int not null,
 performance_id int not null,
 assigner_id int not null,
 assignment_date date not null,
 primary key (user_id, performance_id),
 foreign key (user_id) references user(user_id) on delete cascade,
 foreign key (performance_id) references performance(performance_id) on delete cascade,
 foreign key (assigner_id) references user(user_id) on delete cascade
);

create table if not exists review(
 user_id int not null,
 performance_id int not null,
 inadmissible boolean not null,
 passed_review boolean not null,
 comments varchar(1024) not null,
 review_date date not null,
 primary key (user_id, performance_id),
 foreign key (user_id) references user(user_id) on delete cascade,
 foreign key (performance_id) references performance(performance_id) on delete cascade
);

create table if not exists performance(
 performance_id int not null auto_increment primary key,
 performers varchar(255) not null,
 composer varchar(128) not null,
 title varchar(128) not null,
 instruments varchar(128) not null,
 composition_year int,
 performance_year int not null,
 live_performance boolean not null,
 period_id int not null,
 century varchar(64),
 foreign key (period_id) references period(period_id) on delete cascade 
);

create table if not exists performance_files(
 performance_files_id int not null auto_increment primary key,
 performance_id int not null,
 url varchar(255) not null,
 foreign key (performance_id) references performance(performance_id) on delete cascade
);

create table if not exists period(
 period_id int not null auto_increment primary key,
 name varchar(80) not null,
 description varchar(255) not null
);

# Clear out the tables if they already had data in them.
truncate table authorization;
alter table authorization auto_increment = 1;
truncate table user;
alter table user auto_increment = 1;
truncate table submission;
alter table submission auto_increment = 1;
truncate table reviewer_assignment;
alter table reviewer_assignment auto_increment = 1;
truncate table review;
alter table review auto_increment = 1;
truncate table performance;
alter table performance auto_increment = 1;
truncate table performance_files;
alter table performance_files auto_increment = 1;
truncate table period;
alter table period auto_increment = 1;


#populate the tables with example data.
insert into authorization values (1, 'Administrator', 'Can assign reviewers, allow people to register as reviewers, ban unruly users, can also submit compositions.'),
                                 (2, 'Rater', 'Able to review submitted compositions as well as submitting compositions.'),
                                 (3, 'Submitter', 'Able to submit compositions and search for already-reviewed compositions.');

#just use 'pass' as the passwords for now.
insert into user values (1, 1, 'vp1021', SHA1('pass'), 'Luke', 'Paireepinart', 'vp1021@txstate.edu', ''),
                        (2, 1, 'nico',   SHA1('pass'), 'Nico', 'Schuler',      'nico.schuler@txstate.edu', '');

insert into period values (1, 'Baroque', 'Some random period');
insert into submission values (1, 1, CURDATE()), (2, 2, CURDATE());
insert into performance values (1, 'Joe Bob, Billy S. Stevens', 'Johann Sebastian Bach', 'Minuet in G', 'Violin, Flutes', 1670, 1999, 0, 1, '17th'),
(2, 'Russel Whittaker & the Royal Philharmonic', 'Johann Pachelbel', 'Canon in D major', 'Violin, Violin, Violin, Bass', 1680, 2008, 1, 1, '17th');