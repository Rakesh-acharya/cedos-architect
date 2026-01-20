"""
Create Default Users for All Roles
Run this script to create default users for testing and development
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash

def create_default_users():
    """Create default users for all roles"""
    db = SessionLocal()
    
    # Default users for each role
    default_users = [
        {
            'email': 'admin@cedos.com',
            'username': 'admin',
            'full_name': 'System Administrator',
            'role': UserRole.ADMIN,
            'password': 'admin123',
            'is_active': True,
            'is_verified': True
        },
        {
            'email': 'engineer@cedos.com',
            'username': 'engineer',
            'full_name': 'Civil Engineer',
            'role': UserRole.ENGINEER,
            'password': 'engineer123',
            'is_active': True,
            'is_verified': True
        },
        {
            'email': 'senior@cedos.com',
            'username': 'senior',
            'full_name': 'Senior Engineer',
            'role': UserRole.SENIOR_ENGINEER,
            'password': 'senior123',
            'is_active': True,
            'is_verified': True
        },
        {
            'email': 'manager@cedos.com',
            'username': 'manager',
            'full_name': 'Project Manager',
            'role': UserRole.PROJECT_MANAGER,
            'password': 'manager123',
            'is_active': True,
            'is_verified': True
        },
        {
            'email': 'qs@cedos.com',
            'username': 'qs',
            'full_name': 'Quantity Surveyor',
            'role': UserRole.QUANTITY_SURVEYOR,
            'password': 'qs123',
            'is_active': True,
            'is_verified': True
        },
        {
            'email': 'auditor@cedos.com',
            'username': 'auditor',
            'full_name': 'Auditor',
            'role': UserRole.AUDITOR,
            'password': 'auditor123',
            'is_active': True,
            'is_verified': True
        },
        {
            'email': 'govt@cedos.com',
            'username': 'govt',
            'full_name': 'Government Officer',
            'role': UserRole.GOVERNMENT_OFFICER,
            'password': 'govt123',
            'is_active': True,
            'is_verified': True
        }
    ]
    
    created_count = 0
    skipped_count = 0
    
    print("\nCreating default users...\n")
    
    for user_data in default_users:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == user_data['email']) | 
            (User.username == user_data['username'])
        ).first()
        
        if existing_user:
            print(f"  [SKIP] User already exists: {user_data['username']} ({user_data['role'].value})")
            skipped_count += 1
            continue
        
        # Create user
        user = User(
            email=user_data['email'],
            username=user_data['username'],
            full_name=user_data['full_name'],
            role=user_data['role'],
            hashed_password=get_password_hash(user_data['password']),
            is_active=user_data['is_active'],
            is_verified=user_data['is_verified']
        )
        
        db.add(user)
        created_count += 1
        print(f"  [OK] Created user: {user_data['username']} ({user_data['role'].value})")
    
    db.commit()
    db.close()
    
    print(f"\n")
    print(f"  Summary: Created {created_count} users, Skipped {skipped_count} users")
    print(f"  [OK] Default users setup complete!\n")

if __name__ == '__main__':
    try:
        create_default_users()
    except Exception as e:
        print(f"\n  [ERROR] Failed to create users: {e}")
        print(f"  Make sure database is running and migrations are applied.\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
