# """
# Streamlit UI for MLOps Content Generator Demo
# Run with: streamlit run streamlit_app.py
# """

# import streamlit as st
# import requests
# import json
# import pandas as pd
# import plotly.graph_objects as go
# from datetime import datetime
# import time

# # Page config
# st.set_page_config(
#     page_title="MLOps Content Generator",
#     page_icon="🤖",
#     layout="wide"
# )

# # API endpoint (change if running elsewhere)
# API_URL = "http://localhost:8000"

# # Title
# st.title("🤖 MLOps Content Generator Demo")
# st.markdown("Production-ready content generation with MLOps best practices")

# # Sidebar
# with st.sidebar:
#     st.header("⚙️ Configuration")
    
#     # Model selection
#     model = st.selectbox(
#         "Select Model",
#         ["gpt2", "gpt2-medium", "microsoft/DialoGPT-medium", "EleutherAI/gpt-neo-125M"],
#         index=0
#     )
    
#     # Generation parameters
#     st.subheader("Generation Parameters")
#     temperature = st.slider("Temperature (creativity)", 0.1, 1.0, 0.7, 0.1)
#     max_words = st.slider("Max words per line", 10, 200, 50, 10)
#     num_lines = st.slider("Number of lines", 1, 10, 1, 1)
    
#     # System info
#     st.subheader("System Info")
#     try:
#         health = requests.get(f"{API_URL}/health").json()
#         st.success(f"✅ API Connected")
#         st.info(f"📊 Model: {health.get('model', 'Unknown')}")
#         st.info(f"💻 Device: {health.get('device', 'Unknown')}")
#     except:
#         st.error("❌ API Not Connected")
#         st.info("Run: uvicorn src.api.app:app --reload")

# # Main content area
# col1, col2 = st.columns([2, 1])

# with col1:
#     st.header("📝 Input")
    
#     # Prompt input
#     prompt = st.text_area(
#         "Enter your prompt:",
#         height=150,
#         placeholder="e.g., Write a product description for a smart water bottle..."
#     )
    
#     # Generate button
#     if st.button("🚀 Generate Content", type="primary", use_container_width=True):
#         if prompt:
#             with st.spinner("Generating content..."):
#                 try:
#                     # Call API
#                     start_time = time.time()
#                     response = requests.post(
#                         f"{API_URL}/generate",
#                         json={
#                             "prompt": prompt,
#                             "max_words": max_words,
#                             "num_lines": num_lines,
#                             "temperature": temperature
#                         }
#                     )
#                     end_time = time.time()
                    
#                     if response.status_code == 200:
#                         result = response.json()
                        
#                         # Store in session state
#                         st.session_state.last_result = result
#                         st.session_state.generation_time = end_time - start_time
#                         st.session_state.prompt = prompt
                        
#                         st.success("✅ Generation complete!")
#                     else:
#                         st.error(f"Error: {response.text}")
#                 except Exception as e:
#                     st.error(f"Connection error: {e}")
#         else:
#             st.warning("Please enter a prompt")

# with col2:
#     st.header("📊 Quick Stats")
    
#     if 'last_result' in st.session_state:
#         result = st.session_state.last_result
        
#         # Metrics cards
#         st.metric("Generation Time", f"{st.session_state.generation_time:.2f}s")
#         st.metric("Content Length", f"{len(result['generated_content'])} chars")
#         st.metric("Model Used", result['metadata']['model'])
#         st.metric("Generation ID", result['generation_id'][:8] + "...")
        
#         # Show timestamp
#         st.caption(f"Generated: {result['metadata']['timestamp']}")
#     else:
#         st.info("Generate content to see stats")

# # Results section
# st.header("✨ Generated Content")

# if 'last_result' in st.session_state:
#     result = st.session_state.last_result
    
#     # Display in a nice container
#     with st.container():
#         st.markdown("---")
        
#         # Show prompt
#         st.subheader("📌 Prompt")
#         st.info(st.session_state.prompt)
        
#         # Show generated content
#         st.subheader("📄 Generated Content")
        
#         # Format based on number of lines
#         if num_lines > 1:
#             lines = result['generated_content'].split('\n\n')
#             for i, line in enumerate(lines, 1):
#                 st.markdown(f"**Line {i}:**")
#                 st.write(line)
#                 if i < len(lines):
#                     st.markdown("---")
#         else:
#             st.write(result['generated_content'])
        
#         # Download button
#         st.download_button(
#             label="📥 Download as Text",
#             data=result['generated_content'],
#             file_name=f"generated_{result['generation_id']}.txt",
#             mime="text/plain"
#         )
# else:
#     st.info("👆 Enter a prompt and click Generate to see results here")

# # Advanced section with tabs
# st.header("🔬 Advanced Features")

# tab1, tab2, tab3, tab4 = st.tabs(["Batch Processing", "Model Comparison", "Metrics", "Logs"])

# with tab1:
#     st.subheader("Batch Generation")
    
#     batch_prompts = st.text_area(
#         "Enter multiple prompts (one per line):",
#         height=150,
#         placeholder="Write a tweet about AI\nCreate a Facebook post\nDraft an email subject line"
#     )
    
#     if st.button("📦 Process Batch", use_container_width=True):
#         if batch_prompts:
#             prompts = [p.strip() for p in batch_prompts.split('\n') if p.strip()]
            
#             with st.spinner(f"Processing {len(prompts)} prompts..."):
#                 try:
#                     response = requests.post(
#                         f"{API_URL}/batch-generate",
#                         json={
#                             "prompts": prompts,
#                             "max_words": max_words,
#                             "num_lines": num_lines,
#                             "temperature": temperature
#                         }
#                     )
                    
#                     if response.status_code == 200:
#                         results = response.json()
                        
#                         st.success(f"✅ Processed {results['successful']} prompts")
                        
#                         # Display results
#                         for i, res in enumerate(results['results']):
#                             with st.expander(f"Result {i+1}: {res['prompt'][:50]}..."):
#                                 st.write(res['generated_content'])
#                     else:
#                         st.error(f"Error: {response.text}")
#                 except Exception as e:
#                     st.error(f"Connection error: {e}")

# with tab2:
#     st.subheader("A/B Test: Compare Models")
    
#     test_prompt = st.text_input("Test prompt for comparison:", 
#                                 value="Write a short slogan for a tech company")
    
#     if st.button("🔄 Compare Models", use_container_width=True) and test_prompt:
#         models = ["gpt2", "gpt2-medium"]
#         results = []
        
#         for model_name in models:
#             with st.spinner(f"Testing {model_name}..."):
#                 try:
#                     # Switch model
#                     requests.post(f"{API_URL}/model/reload?model_name={model_name}")
                    
#                     # Generate
#                     response = requests.post(
#                         f"{API_URL}/generate",
#                         json={
#                             "prompt": test_prompt,
#                             "max_words": 30,
#                             "num_lines": 1,
#                             "temperature": 0.7
#                         }
#                     )
                    
#                     if response.status_code == 200:
#                         result = response.json()
#                         results.append({
#                             "model": model_name,
#                             "content": result['generated_content'],
#                             "time": result['metadata']['generation_time']
#                         })
#                 except Exception as e:
#                     st.error(f"Error with {model_name}: {e}")
        
#         # Display comparison
#         if results:
#             col1, col2 = st.columns(2)
#             for i, result in enumerate(results):
#                 with col1 if i == 0 else col2:
#                     st.markdown(f"**{result['model']}**")
#                     st.write(result['content'])
#                     st.caption(f"Time: {result['time']:.2f}s")

# with tab3:
#     st.subheader("System Metrics")
    
#     if st.button("🔄 Refresh Metrics"):
#         try:
#             metrics_response = requests.get(f"{API_URL}/metrics")
#             st.text(metrics_response.text[:1000] + "...")
#         except:
#             st.error("Could not fetch metrics")
    
#     # Sample metrics chart
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(
#         x=list(range(10)),
#         y=[2.3, 2.1, 1.9, 2.4, 2.2, 1.8, 2.0, 2.3, 2.1, 1.7],
#         mode='lines+markers',
#         name='Generation Time (s)'
#     ))
#     fig.update_layout(
#         title="Generation Time Trend (Last 10 requests)",
#         xaxis_title="Request",
#         yaxis_title="Time (seconds)"
#     )
#     st.plotly_chart(fig, use_container_width=True)

# with tab4:
#     st.subheader("Recent Logs")
    
#     try:
#         if Path("logs/app.log").exists():
#             with open("logs/app.log", "r") as f:
#                 logs = f.readlines()[-20:]  # Last 20 lines
#                 for log in logs:
#                     st.code(log.strip())
#         else:
#             st.info("No logs found. Run the app to generate logs.")
#     except Exception as e:
#         st.error(f"Error reading logs: {e}")

# # Footer
# st.markdown("---")
# st.markdown(
#     """
#     <div style='text-align: center'>
#         <p>🚀 MLOps Content Generator | Complete Production-Ready Demo</p>
#         <p style='color: gray; font-size: 0.8em;'>Built with FastAPI, Hugging Face, and MLOps best practices</p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )


"""
Streamlit UI for MLOps Content Generator - FLAN-T5 Integrated
Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import requests
import json
import time
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import FLAN-T5 generator
from src.models.flan_t5_generator import FLANT5Generator

# Page config
st.set_page_config(
    page_title="MLOps Content Generator",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'generator' not in st.session_state:
    st.session_state.generator = None
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'model_size' not in st.session_state:
    st.session_state.model_size = "large"
if 'generation_history' not in st.session_state:
    st.session_state.generation_history = []

def load_model(model_size):
    """Load FLAN-T5 model"""
    with st.spinner(f"🚀 Loading FLAN-T5-{model_size}... This may take 2-5 minutes on first run"):
        try:
            # Create progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Downloading model... (this happens only once)")
            progress_bar.progress(30)
            
            # Load the model
            st.session_state.generator = FLANT5Generator(model_size)
            
            progress_bar.progress(100)
            status_text.text("✅ Model loaded successfully!")
            time.sleep(1)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            st.session_state.model_loaded = True
            st.session_state.model_size = model_size
            return True
        except Exception as e:
            st.error(f"❌ Error loading model: {e}")
            return False

def generate_content(prompt, max_words, num_lines, temperature=0.7):
    """Generate content using FLAN-T5"""
    
    if not st.session_state.model_loaded or st.session_state.generator is None:
        return "⚠️ Please load a model first using the sidebar."
    
    try:
        # Create instruction based on parameters
        if num_lines > 1:
            instruction = f"""Write a {num_lines}-paragraph product description for: {prompt}

Requirements:
- Each paragraph approximately {max_words} words
- Professional and engaging tone
- Highlight key features and benefits
- Make it compelling and persuasive

Description:"""
        else:
            instruction = f"""Write a product description for: {prompt}

Requirements:
- Approximately {max_words} words
- Professional and engaging tone
- Highlight key features and benefits
- Make it compelling and persuasive

Description:"""
        
        # Show what we're sending to the model
        with st.expander("📤 View prompt sent to model"):
            st.text(instruction)
        
        # Generate
        start_time = time.time()
        result = st.session_state.generator.generate_from_prompt(instruction, max_words * num_lines)
        generation_time = time.time() - start_time
        
        # Add to history
        st.session_state.generation_history.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "prompt": prompt,
            "result": result,
            "time": f"{generation_time:.2f}s"
        })
        
        return result, generation_time
        
    except Exception as e:
        return f"❌ Generation error: {e}", 0

def main():
    # Title
    st.title("🤖 MLOps Content Generator")
    st.markdown("*Powered by FLAN-T5 - Actually follows your instructions!*")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        st.subheader("🎯 Model Selection")
        model_size = st.selectbox(
            "Select FLAN-T5 Size:",
            ["large (Recommended - 16GB RAM)", "base (Faster - 8GB RAM)"],
            index=0
        )
        
        # Extract size from selection
        size = model_size.split()[0]
        
        # Load model button
        if st.button("🚀 Load Model", use_container_width=True):
            success = load_model(size)
            if success:
                st.success(f"✅ FLAN-T5-{size} loaded!")
        
        # Model status
        st.subheader("📊 Model Status")
        if st.session_state.model_loaded:
            st.success(f"✅ Loaded: FLAN-T5-{st.session_state.model_size}")
            
            # Model info
            st.info(f"""
            **Model Info:**
            - RAM Usage: ~{4 if st.session_state.model_size == 'large' else 2}GB
            - Type: Instruction-tuned T5
            - Best for: Following instructions exactly
            """)
        else:
            st.warning("⚠️ No model loaded")
            st.info("Click 'Load Model' to start")
        
        # Generation parameters
        st.subheader("🎛️ Generation Parameters")
        temperature = st.slider("Temperature (creativity)", 0.1, 1.0, 0.7, 0.1)
        max_words = st.slider("Max words per section", 30, 200, 100, 10)
        num_lines = st.slider("Number of sections", 1, 5, 1, 1)
        
        # Clear history button
        if st.button("🗑️ Clear History"):
            st.session_state.generation_history = []
            st.success("History cleared!")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Input")
        
        # Prompt templates
        with st.expander("📋 PROVEN PROMPT TEMPLATES (Click to expand)"):
            st.markdown("""
            **Copy and paste these templates:**
            
            **Product Descriptions:**
            ```
            Write a product description for a laptop with:
            - Attractive aluminum design
            - Built-in WiFi and USB ports
            - Affordable price under $500
            - Easy to use for beginners
            - Good value for money
            ```
            
            **Gaming Laptop:**
            ```
            Write a description for a gaming laptop featuring:
            - RGB keyboard
            - High refresh rate display
            - Powerful cooling system
            - Dedicated graphics card
            ```
            
            **Student Laptop:**
            ```
            Create a description for a budget laptop perfect for students:
            - Lightweight and portable
            - Long battery life
            - Durable construction
            - Affordable price
            ```
            
            **Professional Laptop:**
            ```
            Write a professional laptop description targeting business users:
            - Sleek professional design
            - Security features
            - All-day battery
            - Powerful performance
            ```
            """)
        
        # Prompt input
        prompt = st.text_area(
            "Enter your prompt:",
            height=200,
            placeholder="Write a product description for a laptop with attractive design, WiFi, USB ports, affordable price...",
            disabled=not st.session_state.model_loaded
        )
        
        # Generate button
        col1_btn, col2_btn = st.columns(2)
        with col1_btn:
            generate_clicked = st.button(
                "🚀 Generate Content", 
                type="primary", 
                use_container_width=True,
                disabled=not st.session_state.model_loaded or not prompt
            )
        with col2_btn:
            if st.button("🔄 Clear Input", use_container_width=True):
                st.session_state.prompt = ""
                st.rerun()
    
    with col2:
        st.header("📊 Quick Stats")
        
        if st.session_state.model_loaded:
            st.metric("Model Status", "✅ Loaded")
            st.metric("Model Size", f"FLAN-T5-{st.session_state.model_size}")
            st.metric("RAM Usage", "~4GB" if st.session_state.model_size == 'large' else "~2GB")
        else:
            st.metric("Model Status", "❌ Not Loaded")
        
        if st.session_state.generation_history:
            last = st.session_state.generation_history[-1]
            st.metric("Last Generation", last['time'])
            st.metric("Total Generations", len(st.session_state.generation_history))
    
    # Generation results
    if generate_clicked and prompt:
        with st.spinner("🎨 FLAN-T5 is generating your content..."):
            result, gen_time = generate_content(prompt, max_words, num_lines, temperature)
            
            # Store in session state
            st.session_state.last_result = result
            st.session_state.last_prompt = prompt
            st.session_state.last_time = gen_time
    
    # Display results
    st.header("✨ Generated Content")
    
    if 'last_result' in st.session_state:
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📄 Formatted View", "🔍 Raw Text", "📊 Analysis"])
        
        with tab1:
            st.markdown("### 📌 Your Prompt")
            st.info(st.session_state.last_prompt)
            
            st.markdown("### 📄 Generated Content")
            
            # Format based on number of lines
            if num_lines > 1:
                paragraphs = st.session_state.last_result.split('\n\n')
                for i, para in enumerate(paragraphs, 1):
                    with st.container():
                        st.markdown(f"**Section {i}:**")
                        st.write(para)
                        if i < len(paragraphs):
                            st.markdown("---")
            else:
                st.write(st.session_state.last_result)
            
            # Download button
            st.download_button(
                label="📥 Download as Text",
                data=st.session_state.last_result,
                file_name=f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        with tab2:
            st.text(st.session_state.last_result)
            
            # Copy to clipboard button (using JavaScript)
            st.markdown(
                f"""
                <button onclick="navigator.clipboard.writeText(`{st.session_state.last_result}`)">
                📋 Copy to Clipboard
                </button>
                """,
                unsafe_allow_html=True
            )
        
        with tab3:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Word Count", len(st.session_state.last_result.split()))
            with col2:
                st.metric("Character Count", len(st.session_state.last_result))
            with col3:
                st.metric("Generation Time", f"{st.session_state.last_time:.2f}s")
            
            # Show sample stats
            words = st.session_state.last_result.split()
            if words:
                word_lengths = [len(w) for w in words]
                st.subheader("Word Length Distribution")
                chart_data = pd.DataFrame({
                    'Word Length': word_lengths
                })
                st.bar_chart(chart_data)
    
    else:
        st.info("👆 Enter a prompt and click Generate to see results here")
    
    # Generation history
    if st.session_state.generation_history:
        with st.expander("📜 Generation History"):
            history_df = pd.DataFrame(st.session_state.generation_history)
            st.dataframe(history_df, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🚀 Powered by FLAN-T5 - The model that actually follows instructions!</p>
            <p style='color: gray; font-size: 0.8em;'>
                Status: <span style='color: {}; font-weight: bold;'>{}</span> | 
                Model: <span style='color: {}; font-weight: bold;'>{}</span>
            </p>
        </div>
        """.format(
            "green" if st.session_state.model_loaded else "red",
            "Model Loaded" if st.session_state.model_loaded else "No Model Loaded",
            "green" if st.session_state.model_loaded else "gray",
            f"FLAN-T5-{st.session_state.model_size}" if st.session_state.model_loaded else "None"
        ),
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()