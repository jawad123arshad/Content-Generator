# #!/usr/bin/env python3
# """
# MLOps Content Generator - Main Entry Point
# Complete production-ready application
# """

# import os
# import sys
# import argparse
# import logging
# from pathlib import Path

# # Add project root to path
# sys.path.insert(0, str(Path(__file__).parent))

# from src.models.content_generator import ContentGenerator
# from src.monitoring.logger import AppLogger
# from src.utils.config_manager import ConfigManager

# def setup_environment():
#     """Setup environment and directories"""
#     directories = ['models', 'logs', 'experiments', 'models/registry', 'data']
#     for directory in directories:
#         Path(directory).mkdir(parents=True, exist_ok=True)
    
#     # Create .env if not exists
#     if not Path('.env').exists():
#         with open('.env.example', 'r') as source:
#             with open('.env', 'w') as target:
#                 target.write(source.read())
#         print("✅ Created .env file from template")

# def interactive_mode(generator):
#     """Run in interactive mode"""
#     print("\n" + "="*60)
#     print("🤖 MLOPS CONTENT GENERATOR - INTERACTIVE MODE")
#     print("="*60)
#     print(f"Model: {generator.get_model_info()['model_name']}")
#     print(f"Device: {generator.get_model_info()['device']}")
#     print("="*60)
#     print("Commands:")
#     print("  /help     - Show this help")
#     print("  /model    - Show current model info")
#     print("  /switch   - Switch to different model")
#     print("  /metrics  - Show generation metrics")
#     print("  /quit     - Exit")
#     print("="*60)
    
#     while True:
#         print("\n" + "-"*40)
#         prompt = input("📝 Enter your prompt: ").strip()
        
#         if prompt.lower() == '/quit':
#             break
#         elif prompt.lower() == '/help':
#             print("\nCommands:", "  /help - Show help", "  /model - Show model info", 
#                   "  /switch - Switch model", "  /metrics - Show metrics", "  /quit - Exit", sep="\n")
#             continue
#         elif prompt.lower() == '/model':
#             info = generator.get_model_info()
#             print(f"\n📊 Current Model: {info['model_name']}")
#             print(f"   Device: {info['device']}")
#             print(f"   Status: {'Loaded' if info['is_loaded'] else 'Not Loaded'}")
#             continue
#         elif prompt.lower() == '/switch':
#             print("\nAvailable models: gpt2, gpt2-medium, microsoft/DialoGPT-medium, EleutherAI/gpt-neo-125M")
#             model_name = input("Enter model name: ").strip()
#             try:
#                 generator.model_loader.unload_model()
#                 generator.initialize(model_name)
#                 print(f"✅ Switched to {model_name}")
#             except Exception as e:
#                 print(f"❌ Error: {e}")
#             continue
#         elif prompt.lower() == '/metrics':
#             print("\n📈 Generation Metrics:")
#             print("   Check logs/metrics.jsonl for detailed metrics")
#             continue
        
#         if not prompt:
#             continue
            
#         try:
#             max_words = int(input("Max words per line (default 50): ") or "50")
#             num_lines = int(input("Number of lines (default 1): ") or "1")
#             temperature = float(input("Temperature 0.1-1.0 (default 0.7): ") or "0.7")
            
#             print("\n⏳ Generating...")
#             result = generator.generate(
#                 prompt=prompt,
#                 max_words=max_words,
#                 num_lines=num_lines,
#                 temperature=temperature
#             )
            
#             if result['status'] == 'success':
#                 print("\n" + "="*60)
#                 print("✨ GENERATED CONTENT:")
#                 print("="*60)
#                 print(result['generated_content'])
#                 print("="*60)
#                 print(f"⏱️  Time: {result['metadata']['generation_time']}s")
#                 print(f"📊 Generation ID: {result['generation_id']}")
#             else:
#                 print(f"❌ Error: {result.get('error', 'Unknown error')}")
                
#         except KeyboardInterrupt:
#             print("\n\n👋 Goodbye!")
#             break
#         except Exception as e:
#             print(f"❌ Error: {e}")

# def batch_mode(generator, input_file):
#     """Run in batch mode from file"""
#     print(f"📂 Processing batch from {input_file}")
    
#     with open(input_file, 'r') as f:
#         prompts = [line.strip() for line in f if line.strip()]
    
#     print(f"📝 Found {len(prompts)} prompts")
#     results = generator.batch_generate(prompts)
    
#     output_file = f"batch_output_{Path(input_file).stem}.json"
#     import json
#     with open(output_file, 'w') as f:
#         json.dump(results, f, indent=2)
    
#     print(f"✅ Results saved to {output_file}")

# def main():
#     """Main entry point"""
#     parser = argparse.ArgumentParser(description='MLOps Content Generator')
#     parser.add_argument('--model', type=str, default='gpt2',
#                        help='Model name (default: gpt2)')
#     parser.add_argument('--config', type=str, default='config/config.yaml',
#                        help='Config file path')
#     parser.add_argument('--batch', type=str, help='Batch input file')
#     parser.add_argument('--interactive', action='store_true', 
#                        help='Run in interactive mode')
#     parser.add_argument('--setup', action='store_true',
#                        help='Setup environment and exit')
    
#     args = parser.parse_args()
    
#     # Setup environment
#     setup_environment()
    
#     if args.setup:
#         print("✅ Environment setup complete")
#         return
    
#     # Initialize generator
#     print(f"🚀 Initializing Content Generator with model: {args.model}")
#     generator = ContentGenerator(args.config)
    
#     try:
#         generator.initialize(args.model)
#         print("✅ Generator initialized successfully!")
        
#         if args.batch:
#             batch_mode(generator, args.batch)
#         else:
#             interactive_mode(generator)
            
#     except KeyboardInterrupt:
#         print("\n\n👋 Shutting down...")
#     except Exception as e:
#         print(f"❌ Fatal error: {e}")
#         return 1
#     finally:
#         # Cleanup
#         if hasattr(generator, 'model_loader'):
#             generator.model_loader.unload_model()
    
#     return 0

# if __name__ == "__main__":
#     sys.exit(main())



#!/usr/bin/env python3
"""
MLOps Content Generator - Main Entry Point
Updated to use Ensemble Generator for better results
"""

# import os
# import sys
# import argparse
# import logging
# import json
# from pathlib import Path
# from datetime import datetime

# # Add project root to path
# sys.path.insert(0, str(Path(__file__).parent))

# from src.models.ensemble_generator import EnsembleGenerator
# from src.monitoring.logger import AppLogger
# from src.utils.config_manager import ConfigManager
# from src.models.flan_t5_generator import FLANT5Generator


# def setup_environment():
#     """Setup environment and directories"""
#     directories = [
#         'models', 
#         'logs', 
#         'experiments', 
#         'models/registry', 
#         'data',
#         'cache',
#         'outputs'
#     ]
#     for directory in directories:
#         Path(directory).mkdir(parents=True, exist_ok=True)
#         print(f"✅ Created directory: {directory}")
    
#     # Create .env if not exists
#     if not Path('.env').exists():
#         if Path('.env.example').exists():
#             with open('.env.example', 'r') as source:
#                 with open('.env', 'w') as target:
#                     target.write(source.read())
#             print("✅ Created .env file from template")
#         else:
#             print("⚠️  .env.example not found, skipping...")
    
#     print("✅ Environment setup complete")

# def print_banner():
#     """Print welcome banner"""
#     banner = """
#     ╔══════════════════════════════════════════════════════════╗
#     ║     🚀 MLOPS CONTENT GENERATOR - ENSEMBLE EDITION       ║
#     ║                                                          ║
#     ║  Combining: FLAN-T5 + GPT-2 Medium + BART               ║
#     ║  For: Superior Content Generation                        ║
#     ╚══════════════════════════════════════════════════════════╝
#     """
#     print(banner)

# def interactive_mode(generator):
#     """Run in interactive mode with ensemble generator"""
    
#     print_banner()
#     print("\n" + "="*60)
#     print("🤖 INTERACTIVE MODE - ENSEMBLE GENERATOR")
#     print("="*60)
#     print("\n📊 Available Models in Ensemble:")
#     print("   • FLAN-T5      → Structure & Instruction Following")
#     print("   • GPT-2 Medium → Creative Writing & Fluency")
#     print("   • BART         → Refinement & Summarization")
#     print("="*60)
#     print("\nCommands:")
#     print("  /help     - Show this help")
#     print("  /info     - Show ensemble information")
#     print("  /save     - Save last generation to file")
#     print("  /templates- Show prompt templates")
#     print("  /quit     - Exit")
#     print("="*60)
    
#     last_result = None
    
#     while True:
#         print("\n" + "-"*40)
#         print("\n📝 Enter your product/prompt (or command):")
#         user_input = input(">>> ").strip()
        
#         if user_input.lower() == '/quit':
#             print("\n👋 Goodbye! Thanks for using Ensemble Generator!")
#             break
            
#         elif user_input.lower() == '/help':
#             print("\n📋 Available Commands:")
#             print("  /help     - Show this help")
#             print("  /info     - Show ensemble information")
#             print("  /save     - Save last generation to file")
#             print("  /templates- Show prompt templates")
#             print("  /quit     - Exit")
#             continue
            
#         elif user_input.lower() == '/info':
#             print("\nℹ️  Ensemble Generator Information:")
#             print("   Models Loaded: 3")
#             print("   • FLAN-T5-base (instruction understanding)")
#             print("   • GPT-2-medium (creative writing)")
#             print("   • BART-large (refinement)")
#             print(f"   Device: {generator.device}")
#             print("   Capabilities: Product descriptions, stories, emails, etc.")
#             continue
            
#         elif user_input.lower() == '/templates':
#             print("\n📋 Prompt Templates:")
#             print("\n1. Product Description:")
#             print('   "gaming laptop with RTX 3060, 16GB RAM"')
#             print("\n2. Story:")
#             print('   "Write a short story about a robot learning to paint"')
#             print("\n3. Email:")
#             print('   "professional follow-up email after job interview"')
#             print("\n4. Social Media:")
#             print('   "Instagram post about morning coffee"')
#             continue
            
#         elif user_input.lower() == '/save':
#             if last_result:
#                 filename = f"outputs/generation_{last_result['generation_id']}.json"
#                 with open(filename, 'w') as f:
#                     json.dump(last_result, f, indent=2)
#                 print(f"✅ Saved to {filename}")
#             else:
#                 print("⚠️  No generation to save yet")
#             continue
            
#         elif not user_input:
#             continue
        
#         # Get optional parameters
#         print("\n⚙️  Generation Parameters (press Enter to use defaults):")
        
#         try:
#             tone = input("Tone [professional/exciting/casual] (default: professional): ").strip()
#             if not tone:
#                 tone = "professional"
            
#             max_words = input("Max words (default: 100): ").strip()
#             max_words = int(max_words) if max_words else 100
            
#             features = input("Key features (comma-separated, optional): ").strip()
#             audience = input("Target audience (optional): ").strip()
            
#             print("\n⏳ Generating with ensemble (this may take 30-60 seconds)...")
#             print("   • FLAN-T5: Creating outline...")
#             print("   • GPT-2: Adding creativity...")
#             print("   • BART: Refining...")
            
#             # Generate content
#             result = generator.generate_product_description(
#                 product=user_input,
#                 features=features if features else None,
#                 target_audience=audience if audience else None,
#                 tone=tone,
#                 max_words=max_words
#             )
            
#             last_result = result
            
#             # Display result
#             print("\n" + "="*70)
#             print("✨ FINAL GENERATED CONTENT")
#             print("="*70)
#             print(result['generated_content'])
#             print("="*70)
#             print(f"\n📊 Generation Stats:")
#             print(f"   • Generation ID: {result['generation_id']}")
#             print(f"   • Models Used: {', '.join(result['metadata']['models_used'])}")
#             print(f"   • Final Length: {result['metadata']['final_length']} words")
#             print(f"   • Time: {result['metadata']['generation_time']} seconds")
            
#             # Ask for refinement
#             print("\n🔄 Would you like to:")
#             print("   1. Regenerate (different variation)")
#             print("   2. Make it shorter")
#             print("   3. Make it longer")
#             print("   4. Save and continue")
#             print("   5. Continue with new prompt")
            
#             choice = input("Choice (1-5): ").strip()
            
#             if choice == '1':
#                 print("\n🔄 Regenerating with same parameters...")
#                 result = generator.generate_product_description(
#                     product=user_input,
#                     features=features if features else None,
#                     target_audience=audience if audience else None,
#                     tone=tone,
#                     max_words=max_words
#                 )
#                 last_result = result
#                 print("\n" + "="*70)
#                 print(result['generated_content'])
#                 print("="*70)
                
#             elif choice == '2':
#                 shorter = max_words // 2
#                 print(f"\n📏 Creating shorter version ({shorter} words)...")
#                 # Use BART directly for summarization
#                 from transformers import pipeline
#                 summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
#                 summary = summarizer(result['generated_content'], 
#                                     max_length=shorter, 
#                                     min_length=shorter//2)[0]['summary_text']
#                 print("\n" + "="*70)
#                 print("📏 SHORTER VERSION:")
#                 print("="*70)
#                 print(summary)
                
#             elif choice == '3':
#                 longer = max_words * 2
#                 print(f"\n📏 Creating longer version ({longer} words)...")
#                 # Regenerate with more words
#                 result = generator.generate_product_description(
#                     product=user_input,
#                     features=features if features else None,
#                     target_audience=audience if audience else None,
#                     tone=tone,
#                     max_words=longer
#                 )
#                 last_result = result
#                 print("\n" + "="*70)
#                 print(result['generated_content'])
#                 print("="*70)
                
#             elif choice == '4':
#                 filename = f"outputs/{result['generation_id']}.txt"
#                 with open(filename, 'w') as f:
#                     f.write(result['generated_content'])
#                 print(f"✅ Saved to {filename}")
                
#         except KeyboardInterrupt:
#             print("\n\n⚠️  Generation interrupted")
#             continue
#         except Exception as e:
#             print(f"\n❌ Error: {e}")
#             import traceback
#             traceback.print_exc()

# def batch_mode(generator, input_file):
#     """Run in batch mode from file"""
#     print(f"📂 Processing batch from {input_file}")
    
#     if not Path(input_file).exists():
#         print(f"❌ File not found: {input_file}")
#         return
    
#     with open(input_file, 'r') as f:
#         lines = [line.strip() for line in f if line.strip()]
    
#     print(f"📝 Found {len(lines)} items to process")
    
#     results = []
#     for i, line in enumerate(lines, 1):
#         print(f"\n🔄 Processing {i}/{len(lines)}: {line[:50]}...")
        
#         # Parse line - can be simple product name or product|features|audience
#         parts = line.split('|')
#         product = parts[0].strip()
#         features = parts[1].strip() if len(parts) > 1 else None
#         audience = parts[2].strip() if len(parts) > 2 else None
        
#         result = generator.generate_product_description(
#             product=product,
#             features=features,
#             target_audience=audience,
#             max_words=100
#         )
#         results.append(result)
        
#         # Save individual result
#         output_file = f"outputs/batch_{i}_{result['generation_id']}.txt"
#         with open(output_file, 'w') as f:
#             f.write(result['generated_content'])
#         print(f"   ✅ Saved to {output_file}")
    
#     # Save all results
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     batch_file = f"outputs/batch_results_{timestamp}.json"
#     with open(batch_file, 'w') as f:
#         json.dump(results, f, indent=2)
    
#     print(f"\n✅ Batch processing complete!")
#     print(f"📊 Results saved to {batch_file}")
#     print(f"📈 Success rate: {sum(1 for r in results if r['status'] == 'success')}/{len(results)}")

# def web_api_mode():
#     """Start the FastAPI server"""
#     import uvicorn
#     print("🌐 Starting Web API server...")
#     print("   Press Ctrl+C to stop")
#     uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000, reload=True)

# def main():
#     """Main entry point"""
#     parser = argparse.ArgumentParser(description='MLOps Content Generator - Ensemble Edition')
#     parser.add_argument('--mode', type=str, choices=['interactive', 'batch', 'api', 'setup'],
#                        default='interactive', help='Run mode')
#     parser.add_argument('--input', type=str, help='Input file for batch mode')
#     parser.add_argument('--model', type=str, default='ensemble',
#                        help='Model to use (ensemble, flan, gpt2, bart)')
#     parser.add_argument('--config', type=str, default='config/config.yaml',
#                        help='Config file path')
    
#     args = parser.parse_args()
    
#     # Setup environment
#     print("🔧 Setting up environment...")
#     setup_environment()
    
#     if args.mode == 'setup':
#         print("✅ Setup complete!")
#         return
    
#     # Initialize generator
#     if args.mode == 'api':
#         web_api_mode()
#         return
    
#     print("\n" + "="*60)
#     print("🚀 Initializing Ensemble Generator...")
#     print("="*60)
#     print("📦 This will load 3 models (first time may take 5-10 minutes)")
#     print("   • FLAN-T5-base (250MB)")
#     print("   • GPT-2-medium (1.5GB)")
#     print("   • BART-large (1.6GB)")
#     print("="*60)
    
#     try:
#         generator = EnsembleGenerator()
        
#         if args.mode == 'batch':
#             if not args.input:
#                 print("❌ Please specify input file with --input")
#                 return
#             batch_mode(generator, args.input)
#         else:  # interactive mode
#             interactive_mode(generator)
            
#     except KeyboardInterrupt:
#         print("\n\n👋 Shutting down...")
#     except Exception as e:
#         print(f"\n❌ Fatal error: {e}")
#         import traceback
#         traceback.print_exc()
#         return 1
    
#     return 0

# if __name__ == "__main__":
#     sys.exit(main())




#!/usr/bin/env python3
"""
MLOps Content Generator - Main Entry Point
Updated with FLAN-T5 as primary generator (optimized for 16GB RAM laptop)
"""

import os
import sys
import argparse
import logging
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import generators
from src.models.flan_t5_generator import FLANT5Generator
from src.models.ensemble_generator import EnsembleGenerator
from src.monitoring.logger import AppLogger
from src.utils.config_manager import ConfigManager

def setup_environment():
    """Setup environment and directories"""
    directories = [
        'models', 
        'logs', 
        'experiments', 
        'models/registry', 
        'data',
        'cache',
        'outputs'
    ]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Create .env if not exists
    if not Path('.env').exists():
        if Path('.env.example').exists():
            with open('.env.example', 'r') as source:
                with open('.env', 'w') as target:
                    target.write(source.read())
            print("✅ Created .env file from template")
        else:
            print("⚠️  .env.example not found, skipping...")
    
    print("✅ Environment setup complete")

def print_banner():
    """Print welcome banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║     🚀 MLOPS CONTENT GENERATOR - FLAN-T5 EDITION        ║
    ║                                                          ║
    ║  Using: FLAN-T5-large (Optimized for 16GB RAM)          ║
    ║  For: Professional Content That Actually Follows        ║
    ║        Your Instructions!                                ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def interactive_mode(generator, model_type="flan-t5"):
    """Run in interactive mode with selected generator"""
    
    print_banner()
    print("\n" + "="*60)
    print(f"🤖 INTERACTIVE MODE - {model_type.upper()} GENERATOR")
    print("="*60)
    
    if model_type == "flan-t5":
        print("\n📊 Model Information:")
        print("   • FLAN-T5-large → Actually follows instructions!")
        print("   • Size: ~3-4GB RAM usage")
        print("   • Quality: Professional-grade output")
        print("   • Perfect for: Product descriptions, emails, stories")
    else:
        print("\n📊 Available Models in Ensemble:")
        print("   • FLAN-T5      → Structure & Instruction Following")
        print("   • GPT-2 Medium → Creative Writing & Fluency")
        print("   • BART         → Refinement & Summarization")
    
    print("="*60)
    print("\nCommands:")
    print("  /help     - Show this help")
    print("  /info     - Show generator information")
    print("  /save     - Save last generation to file")
    print("  /templates- Show prompt templates")
    print("  /switch   - Switch between FLAN-T5 and Ensemble")
    print("  /quit     - Exit")
    print("="*60)
    
    last_result = None
    
    while True:
        print("\n" + "-"*40)
        print("\n📝 Enter your prompt (or command):")
        user_input = input(">>> ").strip()
        
        if user_input.lower() == '/quit':
            print("\n👋 Goodbye! Thanks for using FLAN-T5 Generator!")
            break
            
        elif user_input.lower() == '/help':
            print("\n📋 Available Commands:")
            print("  /help     - Show this help")
            print("  /info     - Show generator information")
            print("  /save     - Save last generation to file")
            print("  /templates- Show prompt templates")
            print("  /switch   - Switch between FLAN-T5 and Ensemble")
            print("  /quit     - Exit")
            continue
            
        elif user_input.lower() == '/info':
            print("\nℹ️  Generator Information:")
            if model_type == "flan-t5":
                print("   • Model: FLAN-T5-large")
                print("   • Type: Instruction-tuned T5")
                print("   • RAM Usage: ~3-4GB")
                print("   • Strengths: Follows instructions perfectly")
                print("   • Best for: Product descriptions, emails, structured content")
            else:
                print("   • Models Loaded: 3")
                print("   • FLAN-T5-base (instruction understanding)")
                print("   • GPT-2-medium (creative writing)")
                print("   • BART-large (refinement)")
            print(f"   • Device: {generator.device if hasattr(generator, 'device') else 'CPU'}")
            continue
            
        elif user_input.lower() == '/templates':
            print("\n📋 PROVEN PROMPT TEMPLATES THAT WORK:")
            print("\n🎯 For Product Descriptions:")
            print('   • "Write a product description for a laptop with attractive design, WiFi, USB ports, affordable price, easy to use"')
            print('   • "Create a compelling description for a gaming laptop with RGB keyboard and RTX graphics"')
            print('   • "Write about a budget laptop perfect for students"')
            
            print("\n📧 For Emails:")
            print('   • "Write a professional follow-up email after a job interview"')
            print('   • "Draft a promotional email for a new laptop launch"')
            
            print("\n📱 For Social Media:")
            print('   • "Create an Instagram post about our new affordable laptop"')
            print('   • "Write a tweet announcing a laptop sale"')
            continue
            
        elif user_input.lower() == '/switch':
            print("\n🔄 Switching generator type...")
            if model_type == "flan-t5":
                print("Loading Ensemble Generator (may take a few minutes)...")
                new_generator = EnsembleGenerator()
                interactive_mode(new_generator, "ensemble")
            else:
                print("Loading FLAN-T5 Generator...")
                new_generator = FLANT5Generator("large")
                interactive_mode(new_generator, "flan-t5")
            return
            
        elif user_input.lower() == '/save':
            if last_result:
                filename = f"outputs/generation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w') as f:
                    if isinstance(last_result, dict):
                        f.write(last_result.get('generated_content', str(last_result)))
                    else:
                        f.write(str(last_result))
                print(f"✅ Saved to {filename}")
            else:
                print("⚠️  No generation to save yet")
            continue
            
        elif not user_input:
            continue
        
        # Get optional parameters
        print("\n⚙️  Generation Parameters (press Enter to use defaults):")
        
        try:
            max_words = input("Max words (default: 120): ").strip()
            max_words = int(max_words) if max_words else 120
            
            if model_type == "flan-t5":
                print("\n⏳ FLAN-T5 is generating (this actually follows your instructions!)...")
                
                # Use FLAN-T5's generate method
                if hasattr(generator, 'generate_product_description'):
                    result = generator.generate_product_description(
                        product=user_input,
                        max_words=max_words
                    )
                else:
                    result = generator.generate_from_prompt(user_input, max_words)
                
                last_result = result
                
                # Display result
                print("\n" + "="*70)
                print("✨ FLAN-T5 GENERATED CONTENT")
                print("="*70)
                print(result if isinstance(result, str) else result.get('generated_content', result))
                print("="*70)
                
            else:
                # Ensemble mode
                print("\n⏳ Generating with ensemble (this may take 30-60 seconds)...")
                print("   • FLAN-T5: Creating outline...")
                print("   • GPT-2: Adding creativity...")
                print("   • BART: Refining...")
                
                # Parse features if provided
                features = None
                if ',' in user_input:
                    parts = user_input.split(',', 1)
                    user_input = parts[0].strip()
                    features = parts[1].strip()
                
                result = generator.generate_product_description(
                    product=user_input,
                    features=features,
                    max_words=max_words
                )
                
                last_result = result
                
                # Display result
                print("\n" + "="*70)
                print("✨ ENSEMBLE GENERATED CONTENT")
                print("="*70)
                print(result['generated_content'])
                print("="*70)
                print(f"\n📊 Generation Stats:")
                print(f"   • Generation ID: {result['generation_id']}")
                print(f"   • Models Used: {', '.join(result['metadata']['models_used'])}")
                print(f"   • Final Length: {result['metadata']['final_length']} words")
                print(f"   • Time: {result['metadata']['generation_time']} seconds")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Generation interrupted")
            continue
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

def batch_mode(generator, input_file, model_type="flan-t5"):
    """Run in batch mode from file"""
    print(f"📂 Processing batch from {input_file}")
    
    if not Path(input_file).exists():
        print(f"❌ File not found: {input_file}")
        return
    
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    print(f"📝 Found {len(lines)} items to process")
    
    results = []
    for i, line in enumerate(lines, 1):
        print(f"\n🔄 Processing {i}/{len(lines)}: {line[:50]}...")
        
        if model_type == "flan-t5":
            # Simple processing for FLAN-T5
            result = generator.generate_from_prompt(line, max_words=120)
            results.append({"prompt": line, "content": result})
            
            # Save individual result
            output_file = f"outputs/batch_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(output_file, 'w') as f:
                f.write(result)
            print(f"   ✅ Saved to {output_file}")
        else:
            # Ensemble processing
            parts = line.split('|')
            product = parts[0].strip()
            features = parts[1].strip() if len(parts) > 1 else None
            
            result = generator.generate_product_description(
                product=product,
                features=features,
                max_words=100
            )
            results.append(result)
            
            # Save individual result
            output_file = f"outputs/batch_{i}_{result['generation_id']}.txt"
            with open(output_file, 'w') as f:
                f.write(result['generated_content'])
            print(f"   ✅ Saved to {output_file}")
    
    # Save all results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_file = f"outputs/batch_results_{timestamp}.json"
    with open(batch_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Batch processing complete!")
    print(f"📊 Results saved to {batch_file}")

def web_api_mode():
    """Start the FastAPI server"""
    import uvicorn
    print("🌐 Starting Web API server...")
    print("   Press Ctrl+C to stop")
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000, reload=True)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='MLOps Content Generator - FLAN-T5 Edition')
    parser.add_argument('--mode', type=str, choices=['interactive', 'batch', 'api', 'setup'],
                       default='interactive', help='Run mode')
    parser.add_argument('--input', type=str, help='Input file for batch mode')
    parser.add_argument('--model', type=str, choices=['flan-t5', 'ensemble'],
                       default='flan-t5', help='Model to use (flan-t5 recommended for 16GB RAM)')
    parser.add_argument('--config', type=str, default='config/config.yaml',
                       help='Config file path')
    
    args = parser.parse_args()
    
    # Setup environment
    print("🔧 Setting up environment...")
    setup_environment()
    
    if args.mode == 'setup':
        print("✅ Setup complete!")
        return
    
    # Initialize generator based on selection
    if args.mode == 'api':
        web_api_mode()
        return
    
    print("\n" + "="*60)
    print(f"🚀 Initializing {args.model.upper()} Generator...")
    print("="*60)
    
    try:
        if args.model == 'flan-t5':
            print("📦 Loading FLAN-T5-large (optimized for your 16GB RAM laptop)")
            print("   • Model size: ~3-4GB RAM")
            print("   • Quality: Professional-grade")
            print("   • This model ACTUALLY follows instructions!")
            generator = FLANT5Generator("large")  # "large" is perfect for 16GB RAM
        else:
            print("📦 Loading Ensemble Generator (3 models)")
            print("   • FLAN-T5-base (250MB)")
            print("   • GPT-2-medium (1.5GB)")
            print("   • BART-large (1.6GB)")
            print("   Total: ~3.5GB RAM")
            generator = EnsembleGenerator()
        
        if args.mode == 'batch':
            if not args.input:
                print("❌ Please specify input file with --input")
                return
            batch_mode(generator, args.input, args.model)
        else:  # interactive mode
            interactive_mode(generator, args.model)
            
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())