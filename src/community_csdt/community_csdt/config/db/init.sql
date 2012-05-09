-- Notes:
--  A user registered as public can be both a student and/or a teacher. A user registered as a student can only be a student.  
--   1) The column 'permissions' in the users table can be either p for public or s for student
--   2) The column 'active' indicates whether or not the table object is "deleted" - we still keep a copy of them in the database even if they did
--   3) The column 'visible' indicates whether or not the table object is viewable by the public. 1 indicates public. 0 indicates private
--   4) The column 'permissions' in the class_memberships table can be either 's' for student or 't' for teacher or 'a' for administrator
--   5) The column 'flag' indicates whether or not the entry in a table has been flagged. 1 indicates yes. 0 indicates no.


-- Contains information about a user
-- To delete set active = 0.
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  first_name varchar(50) NOT NULL,
  last_name varchar(50) NOT NULL,
  email varchar(50),
  permissions char(1) NOT NULL default 'p',
  reset_pass tinyint(1) NOT NULL default 0,
  reset_pass_counter INTEGER NOT NULL default 0,
  visible tinyint(1) NOT NULL default 1,
  active tinyint(1) NOT NULL default 1
);

INSERT INTO users (first_name, last_name, email, permissions) VALUES ('CSDT', 'Administrator', 'csdt.community@gmail.com', 'a');
INSERT INTO users (first_name, last_name, email, permissions) VALUES ('Josh', 'Green', 'greenj7@rpi.edu', 'p');
INSERT INTO users (first_name, last_name, email, permissions, active) VALUES ('Babe', 'Ruth', 'ruthb5@rpi.edu', 'p', 0);
INSERT INTO users (first_name, last_name, email, permissions) VALUES ('Jason', 'Lane', 'lanej4@rpi.edu', 'p');
INSERT INTO users (first_name, last_name, email, permissions, active) VALUES ('Roger', 'Clemens', 'clemensr22@rpi.edu', 'p', 0);
INSERT INTO users (first_name, last_name, email, permissions) VALUES ('Bryce', 'Harper', 'harperb6@rpi.edu', 'p');
INSERT INTO users (first_name, last_name, permissions) VALUES ('Jose', 'Altuve', 's');


-- Contains information about a user's username and password
-- No need to delete entries
CREATE TABLE IF NOT EXISTS usernames (
  user_id INTEGER NOT NULL,
  username varchar(50) NOT NULL,
  pass varchar(50) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO usernames (user_id, username, pass) VALUES (1, 'csdt.administrator', '12345678');
INSERT INTO usernames (user_id, username, pass) VALUES (2, 'greenj7', '12345678');
INSERT INTO usernames (user_id, username, pass) VALUES (3, 'ruthb5', '12345678');
INSERT INTO usernames (user_id, username, pass) VALUES (4, 'lanej4', '12345678');
INSERT INTO usernames (user_id, username, pass) VALUES (5, 'clemensr22', '12345678');
INSERT INTO usernames (user_id, username, pass) VALUES (6, 'harperb6', '12345678');
INSERT INTO usernames (user_id, username, pass) VALUES (7, 'altuvej27', '12345678');


-- Contains information about a user's profile
-- No need to delete entries
CREATE TABLE IF NOT EXISTS user_profile (
  user_id INTEGER NOT NULL,
  about varchar(200) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO user_profile (user_id, about) VALUES (1, '');
INSERT INTO user_profile (user_id, about) VALUES (2, '');
INSERT INTO user_profile (user_id, about) VALUES (3, '');
INSERT INTO user_profile (user_id, about) VALUES (4, '');
INSERT INTO user_profile (user_id, about) VALUES (5, '');
INSERT INTO user_profile (user_id, about) VALUES (6, '');
INSERT INTO user_profile (user_id, about) VALUES (7, '');


CREATE TABLE IF NOT EXISTS use_log (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  time_in TIMESTAMP NOT NULL,
  time_out TIMESTAMP NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Contains information about all classrooms in system
-- To delete a classroom, just set active = 0
-- The column 'flag_comment_level' indicates the level for which a teacher wants to have flagged comments propogate through the system. 0 indicates that 
--   flagged comments will get mediated by site mediators. 1 indicates that a teacher will get all flagged comments proprogated to themselves first.
--   2 indicates that all posted comments get mediated by the teacher first before being displayed.
CREATE TABLE IF NOT EXISTS classrooms (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  owner INTEGER NOT NULL,
  description varchar(400),
  flag_comment_level INTEGER NOT NULL default 0,
  visible tinyint(1) NOT NULL default 1,
  active tinyint(1) NOT NULL default 1,
  time timestamp NOT NULL default CURRENT_TIMESTAMP,
  FOREIGN KEY (owner) REFERENCES users(id)
);

INSERT INTO classrooms (owner, description) VALUES (2, 'RPI - Math 101\n\nA Mathematics course offered at RPI.');
INSERT INTO classrooms (owner, description, active) VALUES (2, 'RPI - Math 99\n\nA Mathematics course offered at RPI.', 0);
INSERT INTO classrooms (owner, description, visible) VALUES (2, 'RPI - Math 102\n\nA Mathematics course offered at RPI.', 0);
INSERT INTO classrooms (owner, description) VALUES (4, 'RPI - Math 103\n\nA Mathematics course offered at RPI.');

-- Contains information about all classnames in system
-- No need to delete entries
CREATE TABLE IF NOT EXISTS classnames (
  class_id INTEGER NOT NULL,
  classname varchar(50) NOT NULL,
  pass varchar(50) NOT NULL,
  FOREIGN KEY (class_id) REFERENCES classrooms(id)
);

INSERT INTO classnames (class_id, classname, pass) VALUES (1, 'RPI - Math 101', '12345678');
INSERT INTO classnames (class_id, classname, pass) VALUES (2, 'RPI - Math 99', '12345678');
INSERT INTO classnames (class_id, classname, pass) VALUES (3, 'RPI - Math 102', '12345678');
INSERT INTO classnames (class_id, classname, pass) VALUES (4, 'RPI - Math 103', '12345678');

-- Contains information about all users and their permissions in all classrooms
-- Delete the entries
CREATE TABLE IF NOT EXISTS class_memberships (
  user_id INTEGER NOT NULL,
  class_id INTEGER NOT NULL,
  permissions char(1) NOT NULL default 's',
  FOREIGN KEY (user_id) REFERENCES users(id),  
  FOREIGN KEY (class_id) REFERENCES classrooms(id)
);

INSERT INTO class_memberships (user_id, class_id, permissions) VALUES ('2', '1', 't');
INSERT INTO class_memberships (user_id, class_id, permissions) VALUES ('2', '3', 't');
INSERT INTO class_memberships (user_id, class_id, permissions) VALUES ('2', '4', 's');
INSERT INTO class_memberships (user_id, class_id, permissions) VALUES ('4', '1', 's');
INSERT INTO class_memberships (user_id, class_id, permissions) VALUES ('4', '4', 't');
INSERT INTO class_memberships (user_id, class_id, permissions) VALUES ('4', '3', 's');
INSERT INTO class_memberships (user_id, class_id, permissions) VALUES ('5', '1', 's');
INSERT INTO class_memberships (user_id, class_id, permissions) VALUES ('7', '1', 's');

-- Contains information about all projects uploaded
-- To delete a project, just set active = 0
CREATE TABLE IF NOT EXISTS projects (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  proj_name varchar(100) NOT NULL,
  stored_proj_name varchar(100),
  proj_type varchar(50) NOT NULL,
  description varchar(200) NOT NULL,
  num_views int NOT NULL default 0,
  downloads int NOT NULL default 0,
  visible tinyint(1) NOT NULL default 1,
  active tinyint(1) NOT NULL default 1,
  time timestamp NOT NULL default CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO projects (user_id, proj_name, stored_proj_name, proj_type, description, visible, time) VALUES 
(2, 'Proj A', '1.Proj A', 'SB', 'A demo of a SB application', 1, '2011-06-16 15:01:46');
INSERT INTO projects (user_id, proj_name, stored_proj_name, proj_type, description, visible, time) VALUES 
(2, 'Proj B', '2.Proj B', 'CC', 'A demo of a CC application', 1, '2011-06-16 15:03:32');
INSERT INTO projects (user_id, proj_name, stored_proj_name, proj_type, description, visible, active, time) VALUES 
(2, 'Proj C', '3.Proj C', 'SB', 'A demo of a SB application', 1, 0, '2011-06-16 15:08:14');
INSERT INTO projects (user_id, proj_name, stored_proj_name, proj_type, description, visible, active, time) VALUES 
(3, 'Proj D', '4.Proj D', 'SB', 'A demo of a SB application', 1, 0, '2011-06-16 15:12:16');

-- Contains information about what projects reside in what classes
-- Delete the entries
CREATE TABLE IF NOT EXISTS project_memberships (
  project_id INTEGER NOT NULL,
  class_id INTEGER NOT NULL,
  FOREIGN KEY (project_id) REFERENCES projects(id),  
  FOREIGN KEY (class_id) REFERENCES classrooms(id)
);

INSERT INTO project_memberships (project_id, class_id) VALUES (2, 1);

-- Contains information about the ratings of all projects uploaded
-- Delete the entries
CREATE TABLE IF NOT EXISTS project_ratings (
  project_id INTEGER NOT NULL,
  user_id int NOT NULL,
  rating tinyint(1) NOT NULL default 0,
  flag tinyint(1) NOT NULL default 0,
  FOREIGN KEY (project_id) REFERENCES projects(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO project_ratings (project_id, user_id, rating) VALUES (1, 3, 1);
INSERT INTO project_ratings (project_id, user_id, rating) VALUES (1, 4, 1);

-- Contains information of all comments for all projects
-- To delete a project comment set active = 0
CREATE TABLE IF NOT EXISTS project_comments (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  project_id INTEGER NOT NULL,
  text varchar(200) NOT NULL,
  flag tinyint(1) NOT NULL default 0,
  active tinyint(1) NOT NULL default 1,
  time timestamp NOT NULL default CURRENT_TIMESTAMP,
  FOREIGN KEY (project_id) REFERENCES projects(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO project_comments (user_id, project_id, text, active) VALUES (6, 1, 'nice project', 1); 
INSERT INTO project_comments (user_id, project_id, text, active) VALUES (4, 1, 'This is a very cool project. I thoroughly enjoyed it.', 0); 
INSERT INTO project_comments (user_id, project_id, text, active) VALUES (4, 2, 'Sweet!', 0);
INSERT INTO project_comments (user_id, project_id, text, active) VALUES (6, 1, 'Awesome.', 1); 

-- Contains information of which users submited what rating, and flagged which comment
-- Delete the entries
CREATE TABLE IF NOT EXISTS project_comments_ratings (
  proj_comment_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  rating tinyint(1) NOT NULL default 0,
  flag tinyint(1) NOT NULL default 0,
  FOREIGN KEY (proj_comment_id) REFERENCES project_comments(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO project_comments_ratings (proj_comment_id, user_id, rating) VALUES (1, 2, 1);
INSERT INTO project_comments_ratings (proj_comment_id, user_id, rating) VALUES (1, 6, 1);
INSERT INTO project_comments_ratings (proj_comment_id, user_id, rating) VALUES (2, 6, 1);
INSERT INTO project_comments_ratings (proj_comment_id, user_id, rating) VALUES (4, 2, 1);


