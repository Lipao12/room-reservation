CREATE TABLE users(
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE rooms(
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    capacity INT NOT NULL CHECK (capacity > 0)
);

CREATE TABLE reservation(
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL, 
    room_id UUID NOT NULL,
    date DATE NOT NULL, 
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(50) CHECK (status IN ('pending', 'confirmed', 'cancelled')) NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
    );