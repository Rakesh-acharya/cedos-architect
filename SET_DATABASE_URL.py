#!/usr/bin/env python3
"""
Set DATABASE_URL in Railway with proper URL encoding
Handles passwords with special characters automatically
"""

import urllib.parse
import subprocess
import sys
import getpass
import os

def main():
    print("\n" + "=" * 60)
    print("  Set Railway DATABASE_URL (URL-Encoded)")
    print("=" * 60 + "\n")
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    if os.path.exists(backend_dir):
        os.chdir(backend_dir)
    
    # Get Supabase password
    print("Enter your Supabase password:")
    print("(Special characters will be automatically URL-encoded)\n")
    password = getpass.getpass("Supabase Password: ")
    
    if not password:
        print("\n[ERROR] Password required!")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # URL encode the password
    password_encoded = urllib.parse.quote(password, safe='')
    
    print("\nPassword URL-encoded successfully\n")
    
    # Construct DATABASE_URL
    database_url = f"postgresql://postgres:{password_encoded}@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"
    
    print("Setting DATABASE_URL in Railway...\n")
    
    # Set the variable in Railway
    try:
        result = subprocess.run(
            ['railway', 'variables', 'set', f'DATABASE_URL={database_url}'],
            capture_output=True,
            text=True,
            check=True
        )
        
        print("[OK] DATABASE_URL set successfully!\n")
        
        print("Verifying variables...")
        subprocess.run(['railway', 'variables'], check=False)
        print()
        
        print("Redeploying...")
        subprocess.run(['railway', 'up'], check=False)
        print()
        
        print("=" * 60)
        print("  Done! Railway will auto-redeploy")
        print("=" * 60)
        print("\nThe DATABASE_URL has been set with proper URL encoding.")
        print("Special characters in password are now properly encoded.\n")
        
    except subprocess.CalledProcessError as e:
        print("\n[ERROR] Failed to set DATABASE_URL")
        print(f"Error: {e.stderr}\n")
        print("Try manually in Railway dashboard:")
        print("1. Go to Railway dashboard")
        print("2. Your service - Variables tab")
        print("3. Add: DATABASE_URL")
        print(f"4. Value: {database_url}\n")
    except FileNotFoundError:
        print("\n[ERROR] Railway CLI not found!")
        print("Install it: npm install -g @railway/cli\n")
        print("Or set manually in Railway dashboard:")
        print(f"DATABASE_URL = {database_url}\n")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
