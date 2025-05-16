import asyncio
import uuid
from fastapi import APIRouter, File, Body
from fastapi.responses import StreamingResponse
from typing import Annotated


router = APIRouter(prefix="/notification", tags=["Notification"])
clients_lock = asyncio.Lock()
clients: dict[str, asyncio.Queue] = {}


@router.post("/robot")
async def read_robot_notification(file: Annotated[bytes, File()]):
    """
    Receive information about a robot
    """
    content = file.decode()
    async with clients_lock:
        queues = list(clients.values())
    for queue in queues:
        await queue.put(content)
    return {"message": "Robot notification received"}


@router.post("/all")
async def send_clients_notification(message: Annotated[str, Body(embed=True)]):
    """
    Send message to all the clients
    """
    async with clients_lock:
        queues = list(clients.values())
    for queue in queues:
        await queue.put(message)
    return {"message": "Message sent to all clients"}


@router.get("/sse")
async def send_data():
    """
    Send queued data to the client using Server-Sent Events (SSE)
    """
    client_id = str(uuid.uuid4())
    queue = asyncio.Queue()
    async with clients_lock:
        clients[client_id] = queue

    async def event_generator():
        try:
            while True:
                data = await queue.get()
                lines = data.splitlines()
                sse_data = "".join(f"data: {line}\n" for line in lines)
                yield f"{sse_data}\n"
                queue.task_done()
        finally:
            async with clients_lock:
                clients.pop(client_id, None)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
