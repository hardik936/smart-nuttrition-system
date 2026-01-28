from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from models.user import User
from core.deps import get_current_user

router = APIRouter(prefix="/social", tags=["Social"])

@router.post("/follow/{user_id}")
def follow_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if target_user.id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")
        
    if target_user in current_user.following:
         raise HTTPException(status_code=400, detail="You are already following this user")

    current_user.following.append(target_user)
    db.commit()
    return {"message": f"You are now following {target_user.email}"}

@router.delete("/unfollow/{user_id}")
def unfollow_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if target_user not in current_user.following:
         raise HTTPException(status_code=400, detail="You are not following this user")

    current_user.following.remove(target_user)
    db.commit()
    return {"message": f"You have unfollowed {target_user.email}"}

@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Get top 50 users by streak count who have public profiles
    top_users = db.query(User).filter(User.is_public == True).order_by(User.streak_count.desc()).limit(50).all()
    
    leaderboard = []
    for user in top_users:
        leaderboard.append({
            "id": user.id,
            "email": user.email, # In a real app, we might mask this or use a username
            "streak_count": user.streak_count,
            "is_me": user.id == current_user.id
        })
    return leaderboard

@router.get("/friends")
def get_friends(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    friends = []
    for user in current_user.following:
        friends.append({
            "id": user.id,
            "email": user.email,
            "streak_count": user.streak_count
        })
    return friends

@router.get("/users/search")
def search_users(query: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not query:
        return []
    # Simple search by email
    users = db.query(User).filter(User.email.contains(query), User.is_public == True, User.id != current_user.id).limit(10).all()
    results = []
    for user in users:
        is_following = user in current_user.following
        results.append({
            "id": user.id,
            "email": user.email,
            "is_following": is_following
        })
    return results
