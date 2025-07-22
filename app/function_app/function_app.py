"""
Azure Function App for PII Detection.

"""

import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from typing import Dict, Any

import azure.functions as func
import azurefunctions.extensions.bindings.blob as blob
# from azure.storage.blob import BlobServiceClient
# from presidio_analyzer import AnalyzerEngine
# from azure.storage.queue import QueueServiceClient

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize spaCy model on startup
# def ensure_spacy_model():
#     """Ensure spaCy English model is available."""
#     try:
#         import spacy
#         try:
#             spacy.load('en_core_web_sm')
#             logger.info("✅ spaCy English model already available")
#         except OSError:
#             logger.info("📦 Downloading spaCy English model...")
#             subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
#             logger.info("✅ spaCy English model downloaded successfully")
#     except Exception as e:
#         logger.warning(f"⚠️ Could not ensure spaCy model: {str(e)}")

# # Ensure spaCy model is available on startup
# try:
#     ensure_spacy_model()
# except Exception as e:
#     logger.warning(f"⚠️ spaCy model initialization failed: {str(e)}")



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

@app.blob_trigger(
    arg_name="client", path="data/{name}", connection="AzureWebJobsStorage"
)
def blob_trigger(client: blob.BlobClient):
    logging.info(
        f"Python blob trigger function processed blob \n"
        f"Properties: {client.get_blob_properties()}\n"
        f"Blob content head: {client.download_blob().read(size=1)}"
    )

# @app.function_name("http_trigger_pii_analysis_simple")
# @app.route(route="pii/analysis/{container_name}/{blob_name}", 
#                   auth_level=func.AuthLevel.ANONYMOUS)
# def http_trigger_pii_analysis(req: func.HttpRequest) -> func.HttpResponse:
#     """HTTP trigger for manual PII analysis using simple detection."""
#     try:
#         container_name = req.route_params.get('container_name')
#         blob_name = req.route_params.get('blob_name')
        
#         if not container_name or not blob_name:
#             return func.HttpResponse(
#                 json.dumps({"error": "Missing container_name or blob_name"}),
#                 status_code=400,
#                 mimetype="application/json"
#             )
        
#         logger.info(f"HTTP trigger fired for simple analysis: {blob_name}")
        
#         # Analyze the blob for PII using simple detection
#         analysis_result = analyze_blob_for_pii_presidio(blob_name, container_name)
        
#         return func.HttpResponse(
#             json.dumps(analysis_result, indent=2),
#             status_code=200 if analysis_result.get("status") == "completed" else 400,
#             mimetype="application/json"
#         )
#     except Exception as e:
#         logger.error(f"Error in HTTP trigger function: {str(e)}")
#         return func.HttpResponse(
#             json.dumps({"error": str(e)}),
#             status_code=500,
#             mimetype="application/json"
#         )
    

# @app.blob_trigger(arg_name="myblob", path="data/{name}", connection="AzureWebJobsStorage")
# def blob_trigger(myblob: blob.BlobClient):
#     """Azure Function triggered when a blob is created or updated."""
#     trigger_start_time = datetime()
#     try:
#         # Enhanced logging for troubleshooting
#         logger.info(f"🔥 BLOB TRIGGER FIRED at {trigger_start_time.isoformat()}")
#         logger.info(f"📁 Raw blob path: {myblob.name}")
#         logger.info(f"📏 Blob length: {myblob.length} bytes")
#         logger.info(f"🔗 Connection string configured: {'Yes' if get_storage_connection_string() else 'No'}")
        
#         blob_name = myblob.name.split('/')[-1]
#         container_name = "data"
        
#         logger.info(f"📋 Extracted blob name: '{blob_name}'")
#         logger.info(f"📦 Container name: '{container_name}'")
        
#         # Check if blob name is valid
#         if not blob_name or blob_name.strip() == '':
#             logger.error("❌ Invalid blob name extracted from path")
#             return
        
#         # Check blob size
#         if myblob.length == 0:
#             logger.warning(f"⚠️ Empty blob detected: {blob_name}")
        
#         # Test storage connection before processing
#         try:
#             connection_string = get_storage_connection_string()
#             if connection_string:
#                 logger.info("✅ Storage connection string found")
#                 # Test the connection
#                 blob_service_client = BlobServiceClient.from_connection_string(connection_string)
#                 # Try to get account info to verify connection
#                 account_info = blob_service_client.get_account_information()
#                 logger.info(f"✅ Storage connection verified. Account type: {account_info.get('account_kind', 'unknown')}")
#             else:
#                 logger.error("❌ No storage connection string found")
#                 return
#         except Exception as conn_e:
#             logger.error(f"❌ Storage connection test failed: {str(conn_e)}")
#             return
        
#         logger.info(f"🔍 Starting PII analysis for: {blob_name}")
        
#         # Analyze the blob for PII using simple detection
#         analysis_result = analyze_blob_for_pii_presidio(blob_name, container_name)
        
#         logger.info(f"📊 Analysis result status: {analysis_result.get('status')}")
        
#         # Send results to queue
#         logger.info(f"📤 Sending results to queue...")
#         send_to_results_queue(analysis_result)
#         logger.info(f"✅ Results sent to queue successfully")
        
#         # Log summary
#         if analysis_result.get("status") == "completed":
#             pii_count = analysis_result.get("pii_entities_found", 0)
#             processing_time = (datetime.utcnow() - trigger_start_time).total_seconds()
#             logger.info(f"✅ Simple PII analysis completed for {blob_name}: {pii_count} entities found in {processing_time:.2f}s")
#         elif analysis_result.get("status") == "skipped":
#             logger.info(f"⏭️ Analysis skipped for {blob_name}: {analysis_result.get('reason')}")
#         else:
#             logger.error(f"❌ Analysis failed for {blob_name}: {analysis_result.get('error')}")
        
    # except Exception as e:
    #     processing_time = (datetime.utcnow() - trigger_start_time).total_seconds()
    #     logger.error(f"💥 CRITICAL ERROR in blob trigger function after {processing_time:.2f}s: {str(e)}")
    #     logger.error(f"📍 Error type: {type(e).__name__}")
        
    #     # Try to send error to queue for monitoring
    #     try:
    #         error_result = {
    #             "blob_name": getattr(myblob, 'name', 'unknown').split('/')[-1],
    #             "status": "error",
    #             "error": str(e),
    #             "error_type": type(e).__name__,
    #             "analysis_timestamp": datetime.utcnow().isoformat(),
    #             "trigger_duration_seconds": processing_time
    #         }
    #         send_to_results_queue(error_result)
    #         logger.info("📤 Error details sent to results queue")
    #     except Exception as queue_error:
    #         logger.error(f"❌ Failed to send error to queue: {str(queue_error)}")
    
    # finally:
    #     total_time = (datetime.utcnow() - trigger_start_time).total_seconds()
    #     logger.info(f"🏁 Blob trigger completed in {total_time:.2f} seconds")

# @app.function_name("diagnostics")
# @app.route(route="diagnostics", auth_level=func.AuthLevel.ANONYMOUS)
# def diagnostics(req: func.HttpRequest) -> func.HttpResponse:
#     """Diagnostic endpoint to troubleshoot blob trigger issues."""
#     try:
#         diagnostics_info = {
#             "timestamp": datetime.utcnow().isoformat(),
#             "function_app_version": "1.0.0-simple",
#             "environment_variables": {},
#             "storage_connection": {},
#             "blob_container_info": {},
#             "queue_info": {}
#         }
        
#         # Check environment variables
#         env_vars_to_check = [
#             "AzureWebJobsStorage",
#             "STORAGE_ACCOUNT_NAME", 
#             "STORAGE_ACCOUNT_KEY",
#             "STORAGE_CONNECTION_STRING",
#             "PII_PROCESSING_QUEUE_NAME",
#             "PII_RESULTS_QUEUE_NAME",
#             "STORAGE_CONTAINER_NAME",
#             "FUNCTIONS_WORKER_RUNTIME",
#             "WEBSITE_RUN_FROM_PACKAGE"
#         ]
        
#         for var in env_vars_to_check:
#             value = os.environ.get(var)
#             diagnostics_info["environment_variables"][var] = {
#                 "configured": value is not None,
#                 "length": len(value) if value else 0,
#                 "starts_with": value[:20] + "..." if value and len(value) > 20 else value
#             }
        
#         # Test storage connection
#         try:
#             connection_string = get_storage_connection_string()
#             if connection_string:
#                 blob_service_client = BlobServiceClient.from_connection_string(connection_string)
#                 account_info = blob_service_client.get_account_information()
                
#                 diagnostics_info["storage_connection"] = {
#                     "status": "connected",
#                     "account_kind": account_info.get('account_kind'),
#                     "sku_name": account_info.get('sku_name')
#                 }
                
#                 # Check data container
#                 try:
#                     container_client = blob_service_client.get_container_client("data")
#                     container_properties = container_client.get_container_properties()
                    
#                     # List some blobs
#                     blobs = list(container_client.list_blobs(max_results=10))
                    
#                     diagnostics_info["blob_container_info"] = {
#                         "exists": True,
#                         "last_modified": container_properties.last_modified.isoformat() if container_properties.last_modified else None,
#                         "blob_count": len(blobs),
#                         "recent_blobs": [
#                             {
#                                 "name": blob.name,
#                                 "size": blob.size,
#                                 "last_modified": blob.last_modified.isoformat() if blob.last_modified else None
#                             } for blob in blobs[:5]
#                         ]
#                     }
#                 except Exception as container_error:
#                     diagnostics_info["blob_container_info"] = {
#                         "exists": False,
#                         "error": str(container_error)
#                     }
                
#                 # Check queues
#                 try:
#                     queue_service_client = QueueServiceClient.from_connection_string(connection_string)
                    
#                     # Check pii-results queue
#                     try:
#                         results_queue = queue_service_client.get_queue_client("pii-results")
#                         queue_properties = results_queue.get_queue_properties()
                        
#                         # Peek at messages
#                         messages = list(results_queue.peek_messages(max_messages=5))
                        
#                         diagnostics_info["queue_info"]["pii_results"] = {
#                             "exists": True,
#                             "approximate_message_count": queue_properties.approximate_message_count,
#                             "recent_messages": len(messages)
#                         }
#                     except Exception as queue_error:
#                         diagnostics_info["queue_info"]["pii_results"] = {
#                             "exists": False,
#                             "error": str(queue_error)
#                         }
                    
#                 except Exception as queue_error:
#                     diagnostics_info["queue_info"] = {
#                         "error": str(queue_error)
#                     }
                    
#             else:
#                 diagnostics_info["storage_connection"] = {
#                     "status": "no_connection_string"
#                 }
                
#         except Exception as storage_error:
#             diagnostics_info["storage_connection"] = {
#                 "status": "error",
#                 "error": str(storage_error)
#             }
        
#         return func.HttpResponse(
#             json.dumps(diagnostics_info, indent=2),
#             status_code=200,
#             mimetype="application/json"
#         )
        
#     except Exception as e:
#         return func.HttpResponse(
#             json.dumps({
#                 "error": str(e),
#                 "timestamp": datetime.utcnow().isoformat()
#             }),
#             status_code=500,
#             mimetype="application/json"
#         )

# @app.function_name("test_blob_trigger")
# @app.route(route="test/blob/trigger/{blob_name}", auth_level=func.AuthLevel.ANONYMOUS)
# def test_blob_trigger(req: func.HttpRequest) -> func.HttpResponse:
#     """Test endpoint to manually trigger blob analysis."""
#     try:
#         blob_name = req.route_params.get('blob_name')
        
#         if not blob_name:
#             return func.HttpResponse(
#                 json.dumps({"error": "blob_name parameter required"}),
#                 status_code=400,
#                 mimetype="application/json"
#             )
        
#         logger.info(f"🧪 Manual test trigger for blob: {blob_name}")
        
#         # Test if blob exists
#         try:
#             connection_string = get_storage_connection_string()
#             blob_service_client = BlobServiceClient.from_connection_string(connection_string)
#             blob_client = blob_service_client.get_blob_client(container="data", blob=blob_name)
#             blob_properties = blob_client.get_blob_properties()
            
#             logger.info(f"✅ Blob found: {blob_name}, size: {blob_properties.size} bytes")
            
#         except Exception as blob_error:
#             return func.HttpResponse(
#                 json.dumps({
#                     "error": f"Blob not found or inaccessible: {str(blob_error)}",
#                     "blob_name": blob_name
#                 }),
#                 status_code=404,
#                 mimetype="application/json"
#             )
        
#         # Manually run the analysis
#         analysis_result = analyze_blob_for_pii_presidio(blob_name, "data")
        
#         # Send to queue
#         send_to_results_queue(analysis_result)
        
#         return func.HttpResponse(
#             json.dumps({
#                 "message": f"Manual analysis completed for {blob_name}",
#                 "result": analysis_result
#             }, indent=2),
#             status_code=200,
#             mimetype="application/json"
#         )
        
#     except Exception as e:
#         logger.error(f"Error in test blob trigger: {str(e)}")
#         return func.HttpResponse(
#             json.dumps({"error": str(e)}),
#             status_code=500,
#             mimetype="application/json"
#         )

# def get_storage_connection_string():
#     """Get storage connection string from environment variables."""
#     return os.environ.get('AzureWebJobsStorage')


# def analyze_blob_for_pii_presidio(blob_name: str, container_name: str = "data") -> Dict[str, Any]:
#     """
#     Analyze a specific blob for PII content using Presidio.
    
#     Args:
#         blob_name: Name of the blob to analyze
#         container_name: Name of the container (default: "data")
        
#     Returns:
#         Dictionary with PII analysis results
#     """
#     try:
#         connection_string = get_storage_connection_string()
#         if not connection_string:
#             raise ValueError("Storage connection string not found")
        
#         # Initialize blob service client
#         blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
#         # Check if file type is supported
#         supported_extensions = ['.txt', '.csv', '.json', '.log', '.md']
#         file_extension = os.path.splitext(blob_name.lower())[1]
        
#         if file_extension not in supported_extensions:
#             logger.info(f"Skipping unsupported file type: {blob_name}")
#             return {
#                 "blob_name": blob_name,
#                 "status": "skipped",
#                 "reason": "unsupported_file_type",
#                 "supported_types": supported_extensions
#             }
        
#         # Download blob content
#         blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
#         blob_data = blob_client.download_blob()
#         content = blob_data.readall().decode('utf-8', errors='ignore')
        
#         if not content.strip():
#             logger.info(f"Empty file, skipping: {blob_name}")
#             return {
#                 "blob_name": blob_name,
#                 "status": "skipped",
#                 "reason": "empty_file"
#             }
        
#         # Use Presidio AnalyzerEngine
#         analyzer = AnalyzerEngine()
#         results = analyzer.analyze(text=content, entities=None, language="en")
#         pii_entities = [
#             {
#                 'entity_type': r.entity_type,
#                 'start': r.start,
#                 'end': r.end,
#                 'score': r.score,
#                 'text': content[r.start:r.end]
#             } for r in results
#         ]
        
#         # Get blob properties
#         blob_properties = blob_client.get_blob_properties()
        
#         analysis_result = {
#             "blob_name": blob_name,
#             "container_name": container_name,
#             "status": "completed",
#             "analysis_timestamp": datetime.utcnow().isoformat(),
#             "file_size": blob_properties.size,
#             "pii_entities_found": len(pii_entities),
#             "pii_entities": pii_entities,
#             "content_length": len(content),
#             "detection_method": "presidio"
#         }
        
#         logger.info(f"PII analysis completed for {blob_name}: found {len(pii_entities)} entities")
#         return analysis_result
        
#     except Exception as e:
#         logger.error(f"Error analyzing blob {blob_name}: {str(e)}")
#         return {
#             "blob_name": blob_name,
#             "status": "error",
#             "error": str(e),
#             "analysis_timestamp": datetime.utcnow().isoformat()
#         }


# def send_to_results_queue(analysis_result: Dict[str, Any]):
#     """Send analysis results to the results queue."""
#     try:
#         connection_string = get_storage_connection_string()
#         if not connection_string:
#             logger.error("Storage connection string not found for queue operations")
#             return
        
#         queue_service_client = QueueServiceClient.from_connection_string(connection_string)
#         queue_client = queue_service_client.get_queue_client("pii-results")
        
#         # Send message to queue
#         message = json.dumps(analysis_result)
#         queue_client.send_message(message)
        
#         logger.info(f"Analysis result sent to queue for {analysis_result.get('blob_name')}")
        
#     except Exception as e:
#         logger.error(f"Error sending to results queue: {str(e)}")
