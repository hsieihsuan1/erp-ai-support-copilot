"""Local-only portfolio demo. Demo identities are public aliases, not credentials."""
import threading
from pathlib import Path
from typing import Literal
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

from app.integrations import create_mock_ticket
from app.retrieval import SyntheticRetriever

ROOT = Path(__file__).parents[1]
IDENTITIES = {"alpha-agent": ("alpha", "agent"), "alpha-reviewer": ("alpha", "reviewer"), "beta-agent": ("beta", "agent")}
MODULES = Literal["Payables", "Procurement", "Other"]


def identity(x_demo_identity: str = Header(default="")) -> tuple[str, str]:
    principal = IDENTITIES.get(x_demo_identity)
    if not principal:
        raise HTTPException(401, "Choose a documented demo identity. Never use this as production authentication.")
    return principal


class ChatInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(min_length=1, max_length=2000)
    module: MODULES = "Payables"
    session_id: str | None = Field(default=None, max_length=36)


class TicketInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    session_id: str = Field(min_length=1, max_length=36)
    provider: Literal["servicenow", "jira"] = "servicenow"
    confirmed: bool = False


def create_app() -> FastAPI:
    app = FastAPI(title="ERP Support Copilot - local synthetic demo")
    retriever = SyntheticRetriever()
    sessions: dict = {}
    tickets: dict = {}
    lock = threading.RLock()

    def owned_session(sid, who):
        session = sessions.get(sid)
        # Deliberately return the same status for missing and unowned sessions.
        if not session or session["owner"] != who:
            raise HTTPException(404, "Session not found")
        return session

    @app.get("/health")
    def health():
        return {"status": "ok", "mode": "synthetic", "remote_calls": False}

    @app.post("/api/chat")
    def chat(data: ChatInput, who=Depends(identity)):
        if not data.message.strip():
            raise HTTPException(422, "Message cannot be blank")
        with lock:
            if data.session_id:
                sid = data.session_id
                session = owned_session(sid, who)
            else:
                if len(sessions) >= 100:
                    raise HTTPException(503, "Demo session limit reached. Restart to reset.")
                sid = str(uuid4())
                session = sessions[sid] = {"owner": who, "messages": [], "attempts": 0}
            if len(session["messages"]) >= 40:
                raise HTTPException(409, "Demo turn limit reached. Start a new session.")
            docs = retriever.search(data.message, who[0], data.module)
            session["attempts"] += 1
            if docs:
                answer = "Synthetic runbook guidance (not a confirmed fix):\n" + docs[0]["text"]
                reason = "Review the cited runbook and verify the result with a human."
            else:
                answer = "No matching synthetic runbook in this tenant and module. Ask human support; do not change ERP permissions or configuration based on a guess."
                reason = "No supporting source found."
            needs_ticket = not docs or session["attempts"] >= 3
            if session["attempts"] >= 3:
                reason = "Three turns without user-verified resolution. Human review suggested."
            session["messages"].extend([{"role": "user", "content": data.message}, {"role": "assistant", "content": answer}])
            return {"session_id": sid, "message": answer, "mode": "synthetic",
                    "resolved": False, "needs_ticket": needs_ticket, "reason": reason,
                    "sources": [{"id": d["id"], "title": d["title"], "tenant": d["tenant"]} for d in docs],
                    "turn_count": session["attempts"]}

    @app.get("/api/session/{sid}")
    def session(sid: str, who=Depends(identity)):
        with lock:
            current = owned_session(sid, who)
            return {"session_id": sid, "messages": [dict(m) for m in current["messages"]], "turn_count": current["attempts"]}

    @app.post("/api/tickets")
    def ticket(data: TicketInput, who=Depends(identity)):
        if not data.confirmed:
            raise HTTPException(409, "Confirm the transcript before creating a mock ticket")
        with lock:
            current = owned_session(data.session_id, who)
            key = (who, data.session_id, data.provider)
            if key not in tickets:
                tickets[key] = create_mock_ticket(data.provider, data.session_id, current["messages"], len(tickets) + 1)
            return tickets[key]

    @app.get("/")
    def home():
        return FileResponse(ROOT / "demo/index.html")

    @app.get("/demo/erp")
    def erp():
        return FileResponse(ROOT / "demo/erp.html")

    app.mount("/widget", StaticFiles(directory=ROOT / "extension/widget"), name="widget")
    app.mount("/demo-assets", StaticFiles(directory=ROOT / "demo"), name="demo-assets")
    return app


app = create_app()
