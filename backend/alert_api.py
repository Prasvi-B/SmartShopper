from fastapi import APIRouter, Request

router = APIRouter()

@router.post('/alerts')
async def create_alert(request: Request):
    data = await request.json()
    # Save alert to DB (omitted for brevity)
    return {'status': 'success'}

@router.delete('/alerts/{alert_id}')
async def delete_alert(alert_id: int):
    # Delete alert from DB (omitted for brevity)
    return {'status': 'deleted'}
