# Smart Nutrition System - Use Case Diagram

```mermaid
usecaseDiagram
    actor "User" as U
    actor "AI/ML Service" as AI
    actor "External OCR/Food API" as EXT

    package "User Management" {
        usecase "Register" as UC1
        usecase "Login" as UC2
        usecase "View/Update Profile" as UC3
    }

    package "Meal Management" {
        usecase "View Meal Plan" as UC4
        usecase "Generate Meal Plan" as UC5
        usecase "Log Meal" as UC6
    }

    package "Food Tracking & Analysis" {
        usecase "Scan Food Label" as UC7
        usecase "Search Food" as UC8
        usecase "View Food Details" as UC9
        usecase "Get Recommendations" as UC10
    }

    package "Gamification" {
        usecase "View Dashboard (Streaks/Badges)" as UC11
    }

    U --> UC1
    U --> UC2
    U --> UC3
    U --> UC4
    U --> UC5
    U --> UC6
    U --> UC7
    U --> UC8
    U --> UC9
    U --> UC10
    U --> UC11

    UC5 ..> AI : <<include>>
    UC10 ..> AI : <<include>>
    UC7 ..> EXT : <<include>>
    UC8 ..> EXT : <<include>>
```
