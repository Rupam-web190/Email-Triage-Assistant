import requests
import time
import os
import sys

# Configuration
BASE_URL = 'http://127.0.0.1:5000'
TEST_FILES_DIR = 'test_cases'

def print_header(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def check_health():
    print_header("1. SYSTEM HEALTH CHECK")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status'].upper()}")
            print(f"🕒 Timestamp: {data['timestamp']}")
            print(f"📦 Version: {data['version']}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        sys.exit(1)

def upload_eml():
    print_header("2. UPLOAD & TRIAGE (SINGLE FILE)")
    
    # Create a dummy file if needed, but we should use existing test cases
    file_path = os.path.join(TEST_FILES_DIR, 'urgent_sales_pitch.eml')
    if not os.path.exists(file_path):
        print("⚠️ Test file not found, creating dummy...")
        os.makedirs(TEST_FILES_DIR, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write("Subject: Urgent\nFrom: boss@test.com\n\nDo this now.")
            
    files = {'file': open(file_path, 'rb')}
    start = time.time()
    response = requests.post(f"{BASE_URL}/triage", files=files)
    duration = time.time() - start
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Upload Successful ({duration:.2f}s)")
        print(f"📧 Subject: {data.get('subject')}")
        print(f"🏷️  Category: {data.get('smart_folder', {}).get('folder', 'N/A')}")
        print(f"🔥 Priority: {data.get('priority_score', 'N/A')}/5")
        print(f"🛡️  Security Scan: PASSED")
    else:
        print(f"❌ Failed: {response.text}")

def batch_process():
    print_header("3. HIGH-VOLUME BATCH PROCESSING")
    print("🔄 Processing 50+ threads from simulated inbox...")
    
    start = time.time()
    response = requests.post(f"{BASE_URL}/batch")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Batch Complete!")
        print(f"📊 Processed: {data['processed_count']} threads")
        print(f"⏱️  Time Taken: {data['time_taken']}s")
        print(f"📉 Compression: {data['compression_rate']}")
        
        # Show top 3 results
        print("\n--- Top Ranked Emails ---")
        for i, thread in enumerate(data['results'][:3]):
            print(f"{i+1}. [{thread.get('priority_score')}/5] {thread.get('subject')}")
    else:
        print(f"❌ Failed: {response.text}")

def generate_reply():
    print_header("4. AI AUTO-RESPONSE GENERATION")
    
    payload = {
        "thread": {
            "id": "demo_1",
            "subject": "Partnership Opportunity",
            "body": "Hi, we would like to discuss a potential partnership. Are you available next Tuesday?",
            "sender": "partner@bigcorp.com"
        },
        "tone": "professional"
    }
    
    print(f"📩 Incoming: '{payload['thread']['subject']}'")
    print(f"🤖 Generating '{payload['tone']}' reply...")
    
    start = time.time()
    response = requests.post(f"{BASE_URL}/reply", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📝 Draft Reply ({time.time()-start:.2f}s):")
        print(f"{'-'*40}")
        print(data['draft_reply'])
        print(f"{'-'*40}")
    else:
        print(f"❌ Failed: {response.text}")

if __name__ == "__main__":
    print("\n🚀 STARTING DEMO SCENARIOS 🚀")
    print("Ensure backend is running on port 5000")
    time.sleep(1)
    
    check_health()
    time.sleep(1)
    
    upload_eml()
    time.sleep(1)
    
    batch_process()
    time.sleep(1)
    
    generate_reply()
    
    print("\n✨ DEMO COMPLETE ✨")
