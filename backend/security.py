from fastapi import Request, HTTPException
import re

def validate_input(data: dict):
    for k, v in data.items():
        if isinstance(v, str) and re.search(r'[<>"\'%;]', v):
            raise HTTPException(status_code=400, detail=f"Invalid input: {k}")
