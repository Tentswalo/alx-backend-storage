#!/usr/bin/env python3
from pymongo import MongoClient

def log_stats():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client.logs
    collection = db.nginx
    
    # Retrieve the total number of logs
    total_logs = collection.count_documents({})
    print(f'{total_logs} logs')
    
    # Retrieve the number of logs for each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')
    
    # Retrieve the number of logs with status "OK" (status=200) and method "GET"
    status_check = collection.count_documents({"method": "GET", "status": "200"})
    print(f'{status_check} status check')
    
    # Retrieve the top 10 most present IPs
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    
    top_ips = list(collection.aggregate(pipeline))
    
    print("Top 10 IPs:")
    for ip in top_ips:
        print(f'\t{ip["_id"]}: {ip["count"]}')

if __name__ == "__main__":
    log_stats()
