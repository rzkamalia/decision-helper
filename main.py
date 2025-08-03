from uuid import uuid4

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src import app_config
from src.database.pg import save_decision_log, save_question_log
from src.main_agents import Agents
from src.modules.schemas.decision_generator_schema import DecisionRequest
from src.modules.schemas.question_generator_schema import QuestionRequest

app = FastAPI(title=app_config.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

main_agents = Agents()


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "message": "Decision Helper API",
        "endpoints": ["/generate-questions - Generate questions.", "/generate-decision - Generate decision."],
    }


@app.post("/generate-questions")
async def generate_questions(request: QuestionRequest):
    """Generate questions based on context and options."""
    try:
        user_id = request.user_id if hasattr(request, "user_id") and request.user_id else str(uuid4())

        web_search_content, questions = await main_agents.generate_question_agents(
            context=request.context,
            options=request.options,
        )

        # Save to database
        save_question_log(
            user_id=user_id,
            context=request.context,
            options=request.options,
            questions=questions,
            web_search_content=web_search_content,
        )

        return {
            "user_id": user_id,
            "questions": questions,
            "web_search_content": web_search_content,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating question: {e!s}") from e


@app.post("/generate-decision")
async def generate_decision(request: DecisionRequest):
    """Generate decision."""
    try:
        if not hasattr(request, "user_id") or not request.user_id:
            raise HTTPException(
                status_code=400,
                detail="Missing user_id in request. Please call generate-questions first and include the returned user_id.",  # noqa: E501
            )

        if not hasattr(request, "question_answer_pairs") or not request.question_answer_pairs:
            raise HTTPException(
                status_code=400,
                detail="Missing question_answer_pairs in request. Please provide the answers from frontend.",
            )

        result = await main_agents.generate_decision_agents(
            context=request.context,
            options=request.options,
            question_answer_pairs=request.question_answer_pairs,
            web_search_content=request.web_search_content,
        )

        chosen_option = result["chosen_option"]
        reason = result["reason"]

        # Save to database
        save_decision_log(
            user_id=request.user_id,
            chosen_option=chosen_option,
            question_answer_pairs=request.question_answer_pairs,
            reason=reason,
        )

        return {
            "user_id": request.user_id,
            "chosen_option": chosen_option,
            "reason": reason,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating decision: {e!s}") from e


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": f"{app_config.app_name}-api"}


if __name__ == "__main__":
    uvicorn.run("main:app", host=app_config.app_host, port=app_config.app_port, reload=True, log_level="debug")
