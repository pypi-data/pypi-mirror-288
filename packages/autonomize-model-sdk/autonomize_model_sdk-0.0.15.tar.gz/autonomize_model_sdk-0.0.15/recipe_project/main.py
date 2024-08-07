import os
import logging
from modelhub.clients import PipelineManager
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Initialize the ModelHub client
pipeline_manager = PipelineManager(base_url=os.getenv("MODELHUB_BASE_URL"))

pipeline = pipeline_manager.start_pipeline("pipeline_config.yaml")

logger.info("Pipeline started: %s", pipeline)