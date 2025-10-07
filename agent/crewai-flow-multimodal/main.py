import logging
import tempfile

import sounddevice as sd
import soundfile as sf

import config
from client import LLMClient, EmbeddingClient, MilvusClient, AssemblyAIClient
from crewai_workflows import CrewAIClient
from command import CommandHandler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize client instances
llm_client = LLMClient()
embedding_client = EmbeddingClient()
assemblyai_client = AssemblyAIClient()
crewai_client = CrewAIClient()
milvus_client = MilvusClient()

def record_audio(duration: int = 10, sample_rate: int = 16000) -> str:
    """Record audio from microphone and save to temporary file"""
    print(f"🎤 Recording for {duration} seconds... Speak now!")
    print("Press Ctrl+C to stop early")
    
    try:
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
        sd.wait()
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        sf.write(temp_file.name, audio_data, sample_rate)
        
        print("✅ Recording completed!")
        return temp_file.name
        
    except KeyboardInterrupt:
        print("\n⏹️ Recording stopped by user")
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        sf.write(temp_file.name, audio_data, sample_rate)
        return temp_file.name
    except Exception as e:
        print(f"❌ Recording failed: {e}")
        raise


def main():
    """Main application entry point"""
    print("\n🤖 Welcome to Multimodal Agentic RAG System!")
    print("=" * 50)
    
    # Validate API keys
    if not config.ASSEMBLYAI_API_KEY:
        print("\n❌ Missing API keys!")
        print("Please create a .env file with:")
        print("ASSEMBLYAI_API_KEY=your_key_here")
        return
    
    # Check system status and setup if needed
    print("🔍 Checking system status...")
    try:
        if milvus_client.check_system_status():
            print("✅ System ready!")
        else:
            print("\n⚠️ System not set up yet. Let's set it up first!")
            print("📡 Connecting to Milvus...")
            
            # Use Command pattern for system setup
            from command.command_pattern import SystemSetupCommand
            setup_command = SystemSetupCommand()
            setup_result = setup_command.execute()
            print(setup_result)
                
    except Exception as e:
        print(f"\n⚠️ Error checking system status: {e}")
        print("Make sure Milvus is running: docker-compose up -d")
        return
    
    # Main interaction loop using Command pattern
    command_handler = CommandHandler(record_audio_func=record_audio)
    
    while True:
        command_handler.show_menu()
        choice = input("\nEnter your choice (1-3): ").strip()
        
        # Get command based on user choice
        command = command_handler.get_command(choice)
        
        if command is not None:
            print("\n🤔 Processing...")
            result = command_handler.execute_command(command)
            
            # Check if user wants to exit
            if result == "EXIT":
                print("\n👋 Goodbye!")
                break
            
            # Display result if not empty
            if result:
                print(f"\n🤖 Response:\n{result}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc() 