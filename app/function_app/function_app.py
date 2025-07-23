"""
Azure Function App for PII Detection.

"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any

import azure.functions as func
from azure.storage.blob import BlobServiceClient
from presidio_analyzer import AnalyzerEngine
# from azure.storage.queue import QueueServiceClient

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Azure Functions app
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name("health")
@app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS)
def health(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint."""
    return func.HttpResponse(
        json.dumps({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
        }),
        status_code=200,
        mimetype="application/json"
    )

@app.function_name("http_trigger_pii_analysis_simple")
@app.route(route="pii/analysis/{container_name}/{blob_name}", 
                  auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger_pii_analysis(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP trigger for manual PII analysis using simple detection."""
    try:
        container_name = req.route_params.get('container_name')
        blob_name = req.route_params.get('blob_name')
        
        if not container_name or not blob_name:
            return func.HttpResponse(
                json.dumps({"error": "Missing container_name or blob_name"}),
                status_code=400,
                mimetype="application/json"
            )
        
        logger.info(f"HTTP trigger fired for simple analysis: {blob_name}")
        
        # Analyze the blob for PII using simple detection
        analysis_result = analyze_blob_for_pii_presidio(blob_name, container_name)
        
        return func.HttpResponse(
            json.dumps(analysis_result, indent=2),
            status_code=200 if analysis_result.get("status") == "completed" else 400,
            mimetype="application/json"
        )
    except Exception as e:
        logger.error(f"Error in HTTP trigger function: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
    
@app.function_name(name="BlobTrigger1")
@app.blob_trigger(arg_name="myblob", 
                  path="data/{name}",
                  connection="AzureWebJobsStorage")
def test_function(myblob: func.InputStream):
   logging.info(f"c \n"
                f"Name: {myblob.name}\n"
                f"Blob Size: {myblob.length} bytes")
   
   blob_name = myblob.name.split('/')[-1]
   container_name = myblob.name.split('/')[0]

   logger.info(f"🔍 Starting PII analysis for: {blob_name}")

   # Analyze the blob for PII using simple detection
   analysis_result = analyze_blob_for_pii_presidio(blob_name, container_name)

   logging.info(
       json.dumps({
           "message": f"Manual analysis completed for {blob_name}",
           "result": analysis_result
           }, indent=2) 
    )
   
def get_storage_connection_string():
    """Get storage connection string from environment variables."""
    return os.environ.get('AzureWebJobsStorage')


def analyze_blob_for_pii_presidio(blob_name: str, container_name: str = "data") -> Dict[str, Any]:
    """
    Analyze a specific blob for PII content using Presidio.
    
    Args:
        blob_name: Name of the blob to analyze
        container_name: Name of the container (default: "data")
        
    Returns:
        Dictionary with PII analysis results
    """
    try:
        connection_string = get_storage_connection_string()
        if not connection_string:
            raise ValueError("Storage connection string not found")
        
        # Initialize blob service client
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Check if file type is supported
        supported_extensions = ['.txt', '.csv', '.json', '.log', '.md']
        file_extension = os.path.splitext(blob_name.lower())[1]
        
        if file_extension not in supported_extensions:
            logger.info(f"Skipping unsupported file type: {blob_name}")
            return {
                "blob_name": blob_name,
                "status": "skipped",
                "reason": "unsupported_file_type",
                "supported_types": supported_extensions
            }
        
        # Download blob content
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_data = blob_client.download_blob()
        content = blob_data.readall().decode('utf-8', errors='ignore')
        
        if not content.strip():
            logger.info(f"Empty file, skipping: {blob_name}")
            return {
                "blob_name": blob_name,
                "status": "skipped",
                "reason": "empty_file"
            }
        
        # Use Presidio AnalyzerEngine
        analyzer = AnalyzerEngine()
        results = analyzer.analyze(text=content, entities=None, language="en")
        pii_entities = [
            {
                'entity_type': r.entity_type,
                'start': r.start,
                'end': r.end,
                'score': r.score,
                'text': content[r.start:r.end]
            } for r in results
        ]
        
        # Get blob properties
        blob_properties = blob_client.get_blob_properties()
        
        analysis_result = {
            "blob_name": blob_name,
            "container_name": container_name,
            "status": "completed",
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "file_size": blob_properties.size,
            "pii_entities_found": len(pii_entities),
            "pii_entities": pii_entities,
            "content_length": len(content),
            "detection_method": "presidio"
        }
        
        logger.info(f"PII analysis completed for {blob_name}: found {len(pii_entities)} entities")
        return analysis_result
        
    except Exception as e:
        logger.error(f"Error analyzing blob {blob_name}: {str(e)}")
        return {
            "blob_name": blob_name,
            "status": "error",
            "error": str(e),
            "analysis_timestamp": datetime.utcnow().isoformat()
        }
