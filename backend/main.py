"from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef root():\n    return {\"message\": \"Smart Farming Backend Running\"}" 
