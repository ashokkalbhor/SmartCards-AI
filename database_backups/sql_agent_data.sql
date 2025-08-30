PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE chat_users (
	id INTEGER NOT NULL, 
	user_id VARCHAR NOT NULL, 
	username VARCHAR NOT NULL, 
	hashed_password VARCHAR NOT NULL, 
	client_id VARCHAR, 
	created_at DATETIME, 
	is_active BOOLEAN, 
	PRIMARY KEY (id)
);
CREATE TABLE conversations (
	id INTEGER NOT NULL, 
	user_id VARCHAR NOT NULL, 
	conversation_id VARCHAR NOT NULL, 
	title VARCHAR, 
	created_at DATETIME, 
	updated_at DATETIME, 
	message_count INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE chat_messages (
	id INTEGER NOT NULL, 
	user_id VARCHAR NOT NULL, 
	conversation_id VARCHAR NOT NULL, 
	message TEXT NOT NULL, 
	response TEXT NOT NULL, 
	timestamp DATETIME, 
	confidence FLOAT, 
	sql_query TEXT, 
	execution_time FLOAT, 
	error_message TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE user_sessions (
	id INTEGER NOT NULL, 
	user_id VARCHAR NOT NULL, 
	session_id VARCHAR NOT NULL, 
	session_start DATETIME, 
	last_activity DATETIME, 
	is_active BOOLEAN, 
	PRIMARY KEY (id)
);
CREATE TABLE documents (
	id VARCHAR NOT NULL, 
	filename VARCHAR NOT NULL, 
	original_filename VARCHAR NOT NULL, 
	file_path VARCHAR NOT NULL, 
	file_size INTEGER NOT NULL, 
	document_type VARCHAR NOT NULL, 
	status VARCHAR NOT NULL, 
	description TEXT, 
	tags TEXT, 
	user_id VARCHAR NOT NULL, 
	uploaded_at DATETIME, 
	processed_at DATETIME, 
	text_content TEXT, 
	vector_id VARCHAR, 
	error_message TEXT, 
	PRIMARY KEY (id)
);
COMMIT;
