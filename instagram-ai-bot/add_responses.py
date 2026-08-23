"""
📝 RESPONSE MANAGER — Supabase Database Mein Responses Add/Update Karo
========================================================================
Yeh script se tum naye responses add kar sakte ho bina bot band kiye!
Bot automatically 5 min mein naye responses pick kar lega.

Usage:
  python add_responses.py

Ya directly Supabase Dashboard se bhi add kar sakte ho:
  https://supabase.com/dashboard/project/ijkxadnmeqfflfuwvmfz/editor
"""

import requests, json

SUPABASE_URL = "https://ijkxadnmeqfflfuwvmfz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlqa3hhZG5tZXFmZmxmdXd2bWZ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODcyMTg0MTUsImV4cCI6MjEwMjc5NDQxNX0.i-fNXpFmLTGC635QUD33n7neNUarentevjyUxp4I4FA"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def add_response(keyword, response, category="general"):
    """Ek response add karo."""
    data = {"keyword": keyword, "response": response, "category": category}
    r = requests.post(f"{SUPABASE_URL}/rest/v1/bot_responses", json=data, headers=headers)
    if r.status_code == 201:
        print(f"  ✅ Added: '{keyword}' → '{response}'")
        return True
    else:
        print(f"  ❌ Failed: {r.status_code} {r.text}")
        return False

def add_bulk(responses_list):
    """Multiple responses ek saath add karo."""
    r = requests.post(f"{SUPABASE_URL}/rest/v1/bot_responses", json=responses_list, headers=headers)
    if r.status_code == 201:
        print(f"  ✅ Added {len(responses_list)} responses!")
        return True
    else:
        print(f"  ❌ Failed: {r.status_code}")
        return False

def view_all():
    """Saari responses dekho."""
    r = requests.get(f"{SUPABASE_URL}/rest/v1/bot_responses?select=keyword,response,category&order=keyword", headers=headers)
    if r.status_code == 200:
        data = r.json()
        print(f"\n📦 Total responses: {len(data)}\n")
        current_kw = ""
        for item in data:
            if item["keyword"] != current_kw:
                current_kw = item["keyword"]
                print(f"\n  🔑 {current_kw} [{item['category']}]:")
            print(f"     → {item['response']}")
        return data
    return []

def delete_response(keyword):
    """Ek keyword ke saare responses delete karo."""
    r = requests.delete(f"{SUPABASE_URL}/rest/v1/bot_responses?keyword=eq.{keyword}", headers=headers)
    if r.status_code == 200 or r.status_code == 204:
        print(f"  🗑️ Deleted all responses for: '{keyword}'")
    else:
        print(f"  ❌ Failed: {r.status_code}")

def search(keyword):
    """Keyword search karo."""
    r = requests.get(f"{SUPABASE_URL}/rest/v1/bot_responses?keyword=ilike.%25{keyword}%25&select=keyword,response", headers=headers)
    if r.status_code == 200:
        data = r.json()
        print(f"\n🔍 Found {len(data)} results for '{keyword}':")
        for item in data:
            print(f"  {item['keyword']} → {item['response']}")
        return data
    return []

# ===== INTERACTIVE MODE =====
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════╗
║  📝 Bot Response Manager                     ║
╠══════════════════════════════════════════════╣
║  1. Add single response                      ║
║  2. Add multiple responses                   ║
║  3. View all responses                       ║
║  4. Search responses                         ║
║  5. Delete keyword                           ║
║  6. Exit                                     ║
╚══════════════════════════════════════════════╝
""")

    while True:
        choice = input("\nChoice (1-6): ").strip()

        if choice == "1":
            kw = input("  Keyword: ").strip().lower()
            resp = input("  Response: ").strip()
            cat = input("  Category (enter for 'general'): ").strip() or "general"
            add_response(kw, resp, cat)

        elif choice == "2":
            print("  Enter responses (empty keyword to stop):")
            bulk = []
            while True:
                kw = input("  Keyword: ").strip().lower()
                if not kw:
                    break
                resp = input("  Response: ").strip()
                cat = input("  Category: ").strip() or "general"
                bulk.append({"keyword": kw, "response": resp, "category": cat})
            if bulk:
                add_bulk(bulk)

        elif choice == "3":
            view_all()

        elif choice == "4":
            kw = input("  Search keyword: ").strip()
            search(kw)

        elif choice == "5":
            kw = input("  Keyword to delete: ").strip().lower()
            confirm = input(f"  Delete all '{kw}' responses? (y/n): ")
            if confirm.lower() == "y":
                delete_response(kw)

        elif choice == "6":
            print("👋 Bye!")
            break
