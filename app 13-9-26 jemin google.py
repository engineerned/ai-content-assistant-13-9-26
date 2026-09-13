import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate tailored social media posts, captions, and hashtags in seconds.")

# Sidebar - API Key Configuration
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter your Groq API Key:", type="password")
    st.markdown("[Get a free Groq API key](https://console.groq.com/)")

# Inputs Form
st.subheader("Post Details")

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Instagram", "Facebook"])
    content_type = st.selectbox("Content Type", ["Educational", "Promotional", "Storytelling", "Announcement"])
with col2:
    tone = st.selectbox("Tone", ["Professional", "Casual", "Engaging", "Informative", "Humorous"])
    audience = st.text_input("Target Audience", placeholder="e.g., Tech founders, college students")

topic = st.text_area("Topic / Main Idea", placeholder="e.g., Why learning Python in 2026 is still worth it.")

# Generate Button Logic
if st.button("Generate Content", type="primary", use_container_width=True):
    if not api_key:
        st.error("Please provide a valid Groq API key in the sidebar.")
    elif not topic or not audience:
        st.warning("Please fill in both the Topic and Target Audience fields.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            # Construct Prompt
            prompt = f"""
            You are an expert social media copywriter.
            Create a complete post tailored for {platform}.
            
            Parameters:
            - Content Type: {content_type}
            - Topic: {topic}
            - Target Audience: {audience}
            - Tone: {tone}
            
            Instructions:
            1. Write a compelling post text formatted appropriately for {platform}.
            2. Provide an optional short image/video caption suggestion.
            3. Include 5-10 relevant, high-performing hashtags at the bottom.
            """
            
            with st.spinner("Generating post..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                
                output_text = response.choices[0].message.content
                
                st.success("Post generated!")
                st.markdown("---")
                st.markdown(output_text)
                
        except Exception as e:
            st.error(f"Error: {e}")
