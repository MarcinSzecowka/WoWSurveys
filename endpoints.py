from fastapi import FastAPI

app = FastAPI()


@app.post("/surveys")
async def create_survey(instance_name):
    return {
        "message": "created",
        "instance_name": instance_name
    }


@app.get("/surveys/{survey_id}/results")
async def get_survey_results(survey_id):
    """Retrieve the survey and its results"""
    return {"id": survey_id}


@app.get("/surveys/{survey_id}")
async def get_survey(survey_id):
    return {"id": survey_id}


@app.post("/surveys/{survey_id}/answers")
async def complete_the_survey(survey_id):
    score = 0.55
    return {
        "id": survey_id,
        "score": score
    }