from backend.utils import getDBInfo

# Test MongoDB URI and database name
mongo_uri, db_name = getDBInfo()

print(f"MongoDB URI: {mongo_uri}")
print(f"Database Name: {db_name}")
