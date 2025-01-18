from pymongo import MongoClient

# Function to connect to MongoDB
def connect_to_mongo(uri, db_name):
    try:
        client = MongoClient(uri)  # Connect to MongoDB
        print("Connected to MongoDB successfully!")
        return client[db_name]  # Return the database instance
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

# Function to insert data into a collection
def insert_data(collection, data):
    try:
        if isinstance(data, list):
            # Insert multiple documents
            result = collection.insert_many(data)
            print(f"Inserted documents with IDs: {result.inserted_ids}")
        else:
            # Insert a single document
            result = collection.insert_one(data)
            print(f"Inserted document with ID: {result.inserted_id}")
    except Exception as e:
        print(f"Error inserting data: {e}")

# Main program
def update():
    # Replace with your MongoDB URI and database/collection names
    MONGO_URI = "mongodb+srv://Dhanush:2k22ca005@userdetails.mavp0oq.mongodb.net/?retryWrites=true&w=majority"
    DATABASE_NAME = "Users"
    COLLECTION_NAME = "User"

    # Connect to MongoDB
    db = connect_to_mongo(MONGO_URI, DATABASE_NAME)
    if db is not None:  # Explicitly check if db is not None
        # Select the collection
        collection = db[COLLECTION_NAME]

        # Example data to insert
        data_to_insert = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "age": 30,
            "skills": ["Python", "MongoDB", "JavaScript"]
        }

        # Insert data into the collection
        insert_data(collection, data_to_insert)

        # # Example: Insert multiple documents
        # data_list = [
        #     {"name": "Alice", "email": "alice@example.com", "age": 25},
        #     {"name": "Bob", "email": "bob@example.com", "age": 28}
        # ]
        # insert_data(collection, data_list)
    else:
        print("Failed to connect to the database. Exiting...")


update()
