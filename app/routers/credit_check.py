from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
import asyncio
import httpx
import random
import uuid
from datetime import datetime
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/credit-check", tags=["Credit Check"])

async def perform_credit_check(customer_id: str, callback_url: str, wait_seconds: int):
    """
    Background task that simulates a credit check process.
    Waits for the specified time, then sends a callback.
    """
    await asyncio.sleep(wait_seconds)

    # Generate mock credit data
    credit_score = random.randint(300, 850)

    # Determine risk level based on score
    if credit_score >= 750:
        risk_level = "low"
    elif credit_score >= 650:
        risk_level = "medium"
    else:
        risk_level = "high"

    # Prepare callback data
    callback_data = {
        "customer_id": customer_id,
        "credit_score": credit_score,
        "risk_level": risk_level,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Send callback
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                callback_url,
                json=callback_data,
                timeout=10.0
            )
            print(f"Callback sent to {callback_url}: Status {response.status_code}")
        except Exception as e:
            print(f"Failed to send callback to {callback_url}: {str(e)}")

@router.post("/", response_model=schemas.CreditCheckResponse)
async def initiate_credit_check(
    request: schemas.CreditCheckRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Initiate a credit check for a customer.
    Returns immediately and processes the check in the background.
    """
    # Verify customer exists and belongs to user
    customer = db.query(models.Customer).filter(
        models.Customer.id == request.customer_id,
        models.Customer.user_id == current_user.id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    # Generate a task ID
    task_id = str(uuid.uuid4())

    # Queue the background task
    background_tasks.add_task(
        perform_credit_check,
        request.customer_id,
        request.callback_url,
        request.wait_seconds
    )

    return schemas.CreditCheckResponse(
        message=f"Credit check initiated for customer {request.customer_id}",
        task_id=task_id
    )