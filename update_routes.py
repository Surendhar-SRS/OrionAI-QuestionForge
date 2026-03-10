with open("backend/app/api/routes.py", "r") as f:
    content = f.read()

content = content.replace(
    'context = rag_service.retrieve_context(f"{request.topic}", db_question.course_id)',
    'context = await asyncio.to_thread(rag_service.retrieve_context, f"{request.topic}", db_question.course_id)'
)

with open("backend/app/api/routes.py", "w") as f:
    f.write(content)
