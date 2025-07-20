from uuid import uuid4

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.runnables import RunnableConfig

from src import app_config
from src.database.pg import save_decision_log, save_question_log
from src.graph import generate_decision_graph, generate_question_graph
from src.modules.schemas.decision_generator_schema import DecisionRequest
from src.modules.schemas.question_generator_schema import QuestionRequest

app = FastAPI(title=app_config.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

def create_config(user_id: str) -> RunnableConfig:
    """Create RunnableConfig with user_id.
    """
    return {
        "configurable": {
            "user_id": user_id,
        },
        "recursion_limit": 200,
    }

@app.get("/")
async def root():
    """Root endpoint - API information.
    """
    return {
        "message": "Decision Helper API",
        "endpoints": [
            "/generate-questions - Generate questions.",
            "/generate-decision - Generate decision."
        ]
    }

@app.post("/generate-questions")
async def generate_questions(request: QuestionRequest):
    """Generate questions using the question graph.
    """
    try:
        # Check if user_id is provided in request, otherwise generate new one.
        if hasattr(request, "user_id") and request.user_id:
            user_id = request.user_id
        else:
            user_id = str(uuid4())  # Backend generates user_id.
        
        config = create_config(user_id)

        result = await generate_question_graph().ainvoke(
            input={
                "context": request.context,
                "options": request.options,
            },
            config=config,
        )

        web_search = result.get("web_search", []) if isinstance(result, dict) else ""

        questions = result.get("questions", []) if isinstance(result, dict) else []
        questions = [
            {
                "question": question.question,
                "answer_choices": question.answer_choices,
            } 
            for question in questions
        ]

        # Save to database
        save_question_log(
            user_id=user_id,
            context=request.context,
            options=request.options,
            questions=questions,
        )

        return {
            "questions": questions,
            "web_search": web_search,
            "user_id": user_id,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating question: {e!s}") from e

@app.post("/generate-decision")
async def generate_decision(request: DecisionRequest):
    """Generate decision using the decision graph.
    """
    try:
        # Ensure user_id is provided in request.
        if not hasattr(request, "user_id") or not request.user_id:
            raise HTTPException(
                status_code=400, 
                detail="Missing user_id in request. Please call generate-questions first and include the returned user_id."
            )
                
        # Ensure question_answer_pairs is provided
        if not hasattr(request, "question_answer_pairs") or not request.question_answer_pairs:
            raise HTTPException(
                status_code=400,
                detail="Missing question_answer_pairs in request. Please provide the answers from frontend."
            )
            
        config = create_config(request.user_id)

        result = await generate_decision_graph().ainvoke(
            input={
                "context": request.context,
                "options": request.options,
                "web_search": request.web_search,
                "question_answer_pairs": request.question_answer_pairs,
            },
            config=config,
        )

        chosen_option = result.get("chosen_option", "") if isinstance(result, dict) else ""
        reason = result.get("reason", "") if isinstance(result, dict) else ""
        # Save to database
        save_decision_log(
            user_id=request.user_id,
            chosen_option=chosen_option,
            reason=reason,
            question_answer_pairs=request.question_answer_pairs,
        )

        return {
            "chosen_option": chosen_option,
            "reason": reason,
            "user_id": request.user_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating decision: {e!s}") from e

@app.get("/health")
async def health_check():
    """Health check endpoint.
    """
    return {"status": "healthy", "service": f"{app_config.app_name}-api"}

if __name__ == "__main__":
    uvicorn.run("main:app", host=app_config.app_host, port=app_config.app_port, reload=True, log_level="debug")