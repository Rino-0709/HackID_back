from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_stacks():
    tech_stacks = [
        {"id": 1, "name": "JavaScript"},
        {"id": 2, "name": "Python"},
        {"id": 3, "name": "TypeScript"},
        {"id": 4, "name": "Java"},
        {"id": 5, "name": "C#"},
        {"id": 6, "name": "Ruby"},
        {"id": 7, "name": "PHP"},
        {"id": 8, "name": "Go"},
        {"id": 9, "name": "Rust"},
        {"id": 10, "name": "C++"},
        {"id": 11, "name": "Kotlin"},
        {"id": 12, "name": "Swift"},
        {"id": 13, "name": "Dart"},
        {"id": 14, "name": "Scala"},
        {"id": 15, "name": "Perl"},
        {"id": 16, "name": "Shell"},
        {"id": 17, "name": "SQL"},
        {"id": 18, "name": "R"},
        {"id": 19, "name": "MATLAB"},
        {"id": 20, "name": "HTML"},
        {"id": 21, "name": "CSS"},
        {"id": 22, "name": "NoSQL"},
    ]
    return tech_stacks
