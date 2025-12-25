import sys
import os
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Add src and project root to sys.path
CURRENT_FILE = Path(__file__).resolve()
SRC_DIR = CURRENT_FILE.parent.parent
PROJECT_ROOT = SRC_DIR.parent

if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Now these imports should work
from sales_data_analysis.data.db_manager import DBManager
from sales_data_analysis.agents.orchestrator import OrchestratorAgent
from sales_data_analysis.logger import setup_logger
from config.settings import RESULTS_DIR

# Setup logger
logger = setup_logger()

def save_result(query, response):
    """Save query and response to a timestamped file in the results directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = RESULTS_DIR / f"result_{timestamp}.txt"
    try:
        with open(filename, "w") as f:
            f.write(f"Query: {query}\n\n")
            f.write(f"Response:\n{response}\n")
        logger.info(f"Result saved to {filename}")
        print(f"Result saved to {filename}")
    except Exception as e:
        logger.error(f"Failed to save result: {e}")

def main():
    parser = argparse.ArgumentParser(description="Retail Insights Assistant")
    # Default to relative path for portability
    default_data_path = os.path.join(os.getcwd(), "Sales_Dataset", "Amazon Sale Report.csv")
    
    parser.add_argument("--data", type=str, help="Path to sales CSV file", 
                       default=default_data_path)
    parser.add_argument("--query", type=str, help="Single query to run non-interactively")
    args = parser.parse_args()

    logger.info("Initializing System...")
    print("Initializing System...")
    
    # Initialize DB and Agents
    db = DBManager("sales_data.db") # Use a persistent file for performance
    
    if os.path.exists(args.data):
        logger.info(f"Loading data from {args.data}...")
        print(f"Loading data from {args.data}...")
        success, msg = db.ingest_csv(args.data)
        if not success:
            logger.error(f"Error loading data: {msg}")
            print(f"Error loading data: {msg}")
            return
        logger.info("Data loaded successfully.")
        print("Data loaded successfully.")
    else:
        logger.warning(f"Data file not found at {args.data}. Assuming DB is already populated.")
        print(f"Warning: Data file not found at {args.data}. Assuming DB is already populated.")

    orchestrator = OrchestratorAgent(db)
    
    if args.query:
        logger.info(f"Processing Query: {args.query}")
        print(f"\nProcessing Query: {args.query}")
        response = orchestrator.process(args.query)
        print(f"\nAssistant: {response}\n")
        save_result(args.query, response)
        return

    print("\n" + "="*50)
    print("Retail Insights Assistant Ready! (Type 'exit' to quit)")
    print("="*50 + "\n")
    logger.info("Retail Insights Assistant Ready")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit', 'q']:
                logger.info("User requested exit.")
                break
            
            if not user_input.strip():
                continue

            print("\nAssistant is thinking...")
            logger.info(f"Processing user input: {user_input}")
            response = orchestrator.process(user_input)
            print(f"\nAssistant: {response}\n")
            save_result(user_input, response)
            print("-" * 30)
            
        except EOFError:
            print("\nExiting...")
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            print(f"\nError: {e}\n")

if __name__ == "__main__":
    main()
