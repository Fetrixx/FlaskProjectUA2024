-- comment definition

CREATE TABLE comment (
	id INTEGER NOT NULL, 
	data VARCHAR(1000), 
	date DATETIME, 
	user_id INTEGER, 
	publication_id INTEGER, 
	parent_id INTEGER, 
	likes_count INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(publication_id) REFERENCES publication (id), 
	FOREIGN KEY(parent_id) REFERENCES comment (id)
);



-- follow definition

CREATE TABLE follow (
	id INTEGER NOT NULL, 
	follower_id INTEGER, 
	followed_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(follower_id) REFERENCES user (id), 
	FOREIGN KEY(followed_id) REFERENCES user (id)
);



-- "like" definition

CREATE TABLE "like" (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	publication_id INTEGER, 
	comment_id INTEGER, 
	date DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(publication_id) REFERENCES publication (id), 
	FOREIGN KEY(comment_id) REFERENCES comment (id)
);


-- message definition

CREATE TABLE message (
	id INTEGER NOT NULL, 
	sender_id INTEGER, 
	receiver_id INTEGER, 
	content TEXT, 
	timestamp DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(sender_id) REFERENCES user (id), 
	FOREIGN KEY(receiver_id) REFERENCES user (id)
);


-- profile definition

CREATE TABLE profile (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	bio TEXT, 
	background_picture VARCHAR(200), 
	PRIMARY KEY (id), 
	UNIQUE (user_id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);

-- publication definition

CREATE TABLE publication (
	id INTEGER NOT NULL, 
	data VARCHAR(10000), 
	content_type VARCHAR(50), 
	image_url VARCHAR(200), 
	video_url VARCHAR(200), 
	date DATETIME, 
	user_id INTEGER, 
	likes_count INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);

-- "user" definition

CREATE TABLE user (
	id INTEGER NOT NULL, 
	email VARCHAR(150), 
	password VARCHAR(150), 
	first_name VARCHAR(150), 
	username VARCHAR(150), 
	profile_picture VARCHAR(200), 
	date_joined DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (email), 
	UNIQUE (username)
);

