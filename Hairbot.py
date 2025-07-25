import streamlit as st
from PIL import Image
import torch
import torchvision.transforms as transforms
import io
from datetime import datetime

# Custom CSS for enhanced styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main container with gradient background */
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #e0e6ed;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        min-height: 100vh;
    }
    
    /* Global backdrop blur effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(ellipse at top, rgba(120, 119, 198, 0.1) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    /* Enhanced buttons with glassmorphism */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 16px;
        padding: 14px 28px;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.5px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: none;
        box-shadow: 
            0 8px 32px rgba(102, 126, 234, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.6s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 
            0 12px 40px rgba(102, 126, 234, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(0) scale(0.98);
    }
    
    /* Glassmorphism input fields */
    .stSelectbox, .stTextInput, .stRadio, .stMultiselect {
        background: rgba(45, 55, 72, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 12px;
        padding: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }
    
    .stSelectbox:hover, .stTextInput:hover, .stRadio:hover, .stMultiselect:hover {
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 
            0 8px 32px rgba(102, 126, 234, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Enhanced file uploader */
    .stFileUploader {
        background: rgba(45, 55, 72, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 20px;
        border: 2px dashed rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stFileUploader:hover {
        border-color: rgba(102, 126, 234, 0.6);
        background: rgba(45, 55, 72, 0.8);
    }
    
    /* Animated expanders */
    .stExpander {
        background: rgba(37, 47, 63, 0.8);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        margin-bottom: 16px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        overflow: hidden;
    }
    
    .stExpander:hover {
        border-color: rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .stExpander .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        color: #e0e6ed;
        font-weight: 600;
        padding: 16px 20px;
        border-radius: 16px 16px 0 0;
    }
    
    /* Gradient headings with glow effect */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        text-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        margin-bottom: 20px;
    }
    
    .stMarkdown h1 {
        font-size: 2.5rem;
        line-height: 1.2;
    }
    
    .stMarkdown h2 {
        font-size: 2rem;
        line-height: 1.3;
    }
    
    .stMarkdown h3 {
        font-size: 1.5rem;
        line-height: 1.4;
    }
    
    /* Enhanced diagnosis box with animation */
    .diagnosis-box {
        background: linear-gradient(135deg, rgba(51, 65, 85, 0.9) 0%, rgba(71, 85, 105, 0.8) 100%);
        backdrop-filter: blur(20px);
        padding: 24px;
        border-radius: 20px;
        border-left: 6px solid #667eea;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .diagnosis-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
        background-size: 200% 100%;
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { background-position: -200% 0; }
        50% { background-position: 200% 0; }
    }
    
    .diagnosis-box:hover {
        transform: translateY(-4px);
        box-shadow: 
            0 25px 80px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    /* Modern warning box */
    .warning-box {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.9) 0%, rgba(220, 38, 38, 0.8) 100%);
        backdrop-filter: blur(10px);
        padding: 16px 20px;
        border-radius: 12px;
        color: #ffffff;
        margin-bottom: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(239, 68, 68, 0.3);
        font-weight: 500;
    }
    
    /* Animated progress bar */
    .stProgress .st-bo {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stProgress .st-bo::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: progressShine 2s ease-in-out infinite;
    }
    
    @keyframes progressShine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Subtle caption styling */
    .stCaption {
        color: #94a3b8;
        text-align: center;
        margin-top: 24px;
        font-size: 14px;
        font-weight: 400;
        opacity: 0.8;
    }
    
    /* Input field text colors */
    .stTextInput input, .stSelectbox select, .stRadio label, .stMultiselect div {
        color: #e0e6ed !important;
        background: transparent;
        border: none;
        font-weight: 500;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus {
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.3);
        outline: none;
    }
    
    /* Sidebar enhancements */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(15, 15, 35, 0.95) 0%, rgba(26, 26, 46, 0.9) 100%);
        backdrop-filter: blur(20px);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(45, 55, 72, 0.3);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }
    
    /* Floating animation for key elements */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .diagnosis-box {
        animation: float 6s ease-in-out infinite;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .stMarkdown h1 { font-size: 2rem; }
        .stMarkdown h2 { font-size: 1.5rem; }
        .stMarkdown h3 { font-size: 1.25rem; }
        .diagnosis-box { padding: 16px; }
        .stButton > button { padding: 12px 20px; }
    }
</style>
""", unsafe_allow_html=True)

# Title and header
st.title("✨ HairBot - Your Ultimate Hair Health Assistant")
st.markdown("An AI-powered tool to diagnose hair loss causes and recommend personalized treatments with precision.", unsafe_allow_html=True)

# Progress bar setup
sections = ["Basic Information", "Hair Loss History", "Medical History", "Hormonal/Reproductive", "Lifestyle & Diet", "Hair Care Routine", "Family History"]
completed_sections = 0
total_sections = len(sections)

# Symptom selection
symptom = st.selectbox(
    "Select a hair issue: 🧬",
    ["", "Dandruff", "Dry Hair", "Hair Fall", "Oily Scalp", "Itchy Scalp"],
    help="Choose the primary hair issue you're experiencing."
)

if symptom == "Hair Fall":
    # Basic Information
    with st.expander("👤 Basic Information", expanded=True):
        name = st.text_input("What is your name?", placeholder="Enter your name")
        age = st.text_input("What is your age?", placeholder="Enter your age (e.g., 30)")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], help="Select your gender")
        if name and age and gender:
            completed_sections += 1
        if not age.isdigit() and age:
            st.markdown("<div class='warning-box'>⚠️ Please enter a valid age (numbers only).</div>", unsafe_allow_html=True)

    # Hair Loss History
    with st.expander("🕒 Hair Loss History"):
        onset = st.selectbox("When did you first notice hair fall?", ["< 1 month ago", "1–3 months ago", "> 3 months ago"])
        speed = st.selectbox("Was the hair loss sudden or gradual?", ["Sudden", "Gradual"])
        pattern = st.selectbox("How is the hair falling?", ["All over scalp", "In patches", "Mainly hairline/crown"])
        if onset and speed and pattern:
            completed_sections += 1

    # Medical History
    with st.expander("🧬 Medical History"):
        conditions = st.multiselect("Do you have any of these conditions?", ["Thyroid problems", "Anemia", "Autoimmune diseases", "PCOS", "None"])
        meds = st.radio("Are you taking any medications regularly?", ["Yes", "No"])
        if conditions and meds:
            completed_sections += 1
        if "None" in conditions and len(conditions) > 1:
            st.markdown("<div class='warning-box'>⚠️ 'None' cannot be selected with other conditions.</div>", unsafe_allow_html=True)

    # Hormonal/Reproductive
    with st.expander("♀️ Hormonal/Reproductive (if applicable)"):
        hormonal_issues = st.multiselect("Have you experienced any of these?", ["Pregnancy/childbirth", "Irregular periods", "Menopausal symptoms", "Excess facial hair/acne", "None"])
        if hormonal_issues:
            completed_sections += 1
        if gender != "Female" and hormonal_issues and "None" not in hormonal_issues:
            st.markdown("<div class='warning-box'>⚠️ Hormonal issues are typically relevant for female patients. Please confirm.</div>", unsafe_allow_html=True)

    # Lifestyle & Diet
    with st.expander("🍽️ Lifestyle & Diet"):
        diet_type = st.selectbox("What is your diet type?", ["Non-vegetarian", "Vegetarian", "Vegan"], help="Select your dietary preference")
        diet_change = st.radio("Recent diet change or weight loss?", ["Yes", "No"])
        stress = st.selectbox("Rate your stress levels recently", ["Low", "Moderate", "High"])
        if diet_type and diet_change and stress:
            completed_sections += 1
        if stress == "High":
            st.markdown("<div class='warning-box'>⚠️ High stress can contribute to hair loss. Consider stress management techniques.</div>", unsafe_allow_html=True)
        if diet_type in ["Vegetarian", "Vegan"] and diet_change == "Yes":
            st.markdown("<div class='warning-box'>⚠️ Vegetarian/vegan diets with recent changes may lead to nutritional deficiencies. Ensure adequate protein, iron, and B12 intake.</div>", unsafe_allow_html=True)

    # Hair Care Routine
    with st.expander("🧴 Hair Care Routine"):
        tight_styles = st.radio("Do you wear tight hairstyles frequently?", ["Yes", "No"])
        heat_tools = st.selectbox("How often do you use heat or chemical treatments?", ["Frequently", "Occasionally", "Never"])
        scalp_issues = st.radio("Any recent scalp irritation, flaking, or itching?", ["Yes", "No"])
        water_quality = st.radio("Do you use hard water or chlorinated water (e.g., pool water, untreated tap water)?", ["Yes", "No"])
        if tight_styles and heat_tools and scalp_issues and water_quality:
            completed_sections += 1
        if tight_styles == "Yes":
            st.markdown("<div class='warning-box'>⚠️ Tight hairstyles may cause traction alopecia. Consider looser styles.</div>", unsafe_allow_html=True)
        if water_quality == "Yes":
            st.markdown("<div class='warning-box'>⚠️ Hard or chlorinated water may cause hair breakage or scalp irritation. Consider using a shower filter or clarifying shampoo.</div>", unsafe_allow_html=True)

    # Family History
    with st.expander("👪 Family History"):
        family_history = st.radio("Any family history of hair loss?", ["Yes", "No", "Not sure"])
        if family_history:
            completed_sections += 1

    # Progress bar
    progress = completed_sections / total_sections
    st.progress(progress)
    st.markdown(f"**Form Completion: {int(progress * 100)}%** ({completed_sections}/{total_sections} sections completed)", unsafe_allow_html=True)

    # Image Upload
    with st.expander("📸 Upload Hair Image for Norwood Stage Detection"):
        uploaded_file = st.file_uploader("Upload a clear photo of your hair/scalp", type=["jpg", "jpeg", "png"], help="Upload a high-quality image (max 5MB)")
        if uploaded_file:
            # Basic image validation
            img = Image.open(uploaded_file)
            if uploaded_file.size > 5 * 1024 * 1024:  # 5MB limit
                st.markdown("<div class='warning-box'>⚠️ Image size exceeds 5MB. Please upload a smaller file.</div>", unsafe_allow_html=True)
            else:
                st.image(img, caption="Uploaded Hair/Scalp Image", use_column_width=True)

    # Norwood treatment dictionary
    norwood_treatment = {
    "1": {
        "treatment": "No treatment needed, but 5% minoxidil or LLLT (red light therapy) can be used as prevention.",
        "reversible": True
    },
    "2": {
        "treatment": "5% minoxidil + 0.1% topical finasteride (morning and night). PRP or LLLT may enhance results.",
        "reversible": True
    },
    "3": {
        "treatment": "10% minoxidil + oral or topical finasteride. Microneedling twice a week + PRP or LLLT recommended.",
        "reversible": True
    },
    "3V": {
        "treatment": "10% minoxidil + oral finasteride. Focus on crown with PRP or red light therapy support.",
        "reversible": True
    },
    "4": {
        "treatment": "High-strength minoxidil (10%) + oral finasteride. Microneedling + PRP or LLLT advised.",
        "reversible": True
    },
    "5": {
        "treatment": "Hair transplant often necessary. PRP/LLLT may slow loss. Medication (finasteride, minoxidil) can maintain.",
        "reversible": True
    },
    "6": {
        "treatment": "Hair transplant is the most effective option. PRP and medication can help retain donor hair.",
        "reversible": False
    },
    "7": {
        "treatment": "Only viable solution: hair transplant. Maintain donor area with finasteride, PRP may help scalp health.",
        "reversible": False
    }
}


    def recommend_treatment(stage):
        stage_str = str(stage)
        if stage_str not in norwood_treatment:
            return "Unknown Norwood stage."

        data = norwood_treatment[stage_str]
        status = "🟢 **Reversible**" if data["reversible"] else "🔴 **Not Reversible** (Transplant Likely Needed)"

        return f"""
### 🧠 Detected Norwood Stage: **Stage {stage}**
**💊 Recommended Treatment:**  
{data['treatment']}

**{status}**
**Note**: This is a placeholder. Integrate an ML model for accurate Norwood stage detection.
"""

    if uploaded_file and uploaded_file.size <= 5 * 1024 * 1024:
        # Simulate prediction result
        norwood_stage = 4  # Replace with ML model output
        st.markdown(recommend_treatment(norwood_stage), unsafe_allow_html=True)

    # Diagnosis Summary
    with st.expander("📋 Diagnosis Summary", expanded=True):
       diagnosis = ""
       tests = []

    if not name or not age or not gender:
        st.markdown("<div class='warning-box'>⚠️ Please complete the Basic Information section for a diagnosis.</div>", unsafe_allow_html=True)

    if completed_sections < total_sections:
        st.markdown("<div class='warning-box'>⚠️ Please complete all sections for a comprehensive diagnosis.</div>", unsafe_allow_html=True)
    else:
        if stress == "High" and diet_change == "Yes":
            diagnosis += "- Hair fall may be due to **Telogen Effluvium** triggered by stress or recent dietary changes.\n"
            tests.append("Ferritin, Vitamin D, Zinc, Thyroid function (TSH, T3, T4)")

        if pattern == "In patches" and scalp_issues == "No":
            diagnosis += "- Patchy hair loss without scalp irritation suggests **Alopecia Areata**. Consult a dermatologist for autoimmune evaluation.\n"
            tests.append("Autoimmune markers (ANA, anti-thyroid antibodies)")

        if "Thyroid problems" in conditions:
            diagnosis += "- Possible contribution from **Thyroid Dysfunction**. Check TSH levels and manage appropriately.\n"
            tests.append("Thyroid function tests (TSH, T3, T4)")

        if "PCOS" in conditions or any(issue != "None" for issue in hormonal_issues):
            diagnosis += "- **Hormonal imbalances** (e.g., PCOS or pregnancy) may contribute to hair loss. Consultation with an endocrinologist is advised.\n"
            tests.append("Hormone panel (testosterone, DHEA-S, LH/FSH, prolactin)")

        if tight_styles == "Yes":
            diagnosis += "- Frequent tight hairstyles could cause **Traction Alopecia**. Switch to looser styles to prevent further damage.\n"
            tests.append("Trichoscopy (if hair loss persists)")

        if family_history == "Yes" and pattern == "Mainly hairline/crown":
            diagnosis += "- Pattern suggests **Androgenetic Alopecia** with family history. Consider treatments like minoxidil or finasteride.\n"
            tests.append("Hormone panel (especially for women if PCOS suspected)")

        if scalp_issues == "Yes":
            diagnosis += "- Scalp irritation or flaking may indicate **Seborrheic Dermatitis** or **Fungal Infection**. Consult a dermatologist.\n"
            tests.append("Fungal culture or KOH test")

        if water_quality == "Yes":
            diagnosis += "- Exposure to **hard/chlorinated water** may contribute to breakage or scalp issues. Use a shower filter or clarifying shampoo.\n"
            tests.append("Water quality test (for mineral or chlorine content)")

        if diet_type in ["Vegetarian", "Vegan"] and diet_change == "Yes":
            diagnosis += f"- Your **{diet_type.lower()} diet** and recent changes may lead to nutritional deficiencies. Ensure adequate protein, iron, and B12.\n"
            tests.append("Ferritin, Vitamin B12, Serum protein")

        if diagnosis:
            st.markdown("### 🧾 Diagnosis Summary")
            st.markdown(diagnosis)
            st.markdown("**Note**: Always consult a dermatologist to confirm the diagnosis and discuss treatment options.")

            if tests:
                st.markdown("### 🩺 Recommended Tests")
                st.markdown("\n".join(f"- {t}" for t in tests))
        else:
            st.info("No specific diagnosis pattern matched. Please provide more details or consult a dermatologist.")

        # Download Diagnosis Report
        if st.button("📥 Download Diagnosis Report"):
            report = f"""
# HairBot Diagnosis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Patient Information
- **Name**: {name or 'Not provided'}
- **Age**: {age or 'Not provided'}
- **Gender**: {gender or 'Not provided'}

## Hair Loss Details
- **Onset**: {onset or 'Not provided'}
- **Speed**: {speed or 'Not provided'}
- **Pattern**: {pattern or 'Not provided'}

## Medical and Lifestyle Factors
- **Conditions**: {', '.join(conditions) if conditions else 'Not provided'}
- **Medications**: {meds or 'Not provided'}
- **Hormonal Issues**: {', '.join(hormonal_issues) if hormonal_issues else 'Not provided'}
- **Diet Type**: {diet_type or 'Not provided'}
- **Diet Change/Weight Loss**: {diet_change or 'Not provided'}
- **Stress Level**: {stress or 'Not provided'}
- **Tight Hairstyles**: {tight_styles or 'Not provided'}
- **Heat/Chemical Treatments**: {heat_tools or 'Not provided'}
- **Scalp Issues**: {scalp_issues or 'Not provided'}
- **Water Quality (Hard/Chlorinated)**: {water_quality or 'Not provided'}
- **Family History**: {family_history or 'Not provided'}

## Diagnosis
{diagnosis or 'No specific diagnosis matched due to incomplete information.'}

## Recommended Tests
{', '.join(tests) if tests else 'None recommended due to incomplete information.'}

*Generated by HairBot. Consult a dermatologist for professional advice.*
"""
            b = io.BytesIO(report.encode())
            st.download_button(
                label="Download Report (TXT)",
                data=b,
                file_name=f"hairbot_report_{name or 'user'}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
            st.success("Report downloaded successfully!")

elif symptom:
    with st.expander("🔍 Suggested Action", expanded=True):
        if symptom == "Dandruff":
            st.write("For **Dandruff**, use shampoos with ketoconazole, zinc pyrithione, or salicylic acid. Avoid harsh shampoos and oily products.")
        elif symptom == "Dry Hair":
            st.write("For **Dry Hair**, apply hydrating masks, avoid frequent heat styling, and use leave-in conditioners with argan oil or shea butter.")
        elif symptom == "Oily Scalp":
            st.write("For **Oily Scalp**, wash regularly with a mild clarifying shampoo and avoid heavy conditioners on the scalp.")
        elif symptom == "Itchy Scalp":
            st.write("For **Itchy Scalp**, try anti-dandruff shampoos and avoid fragranced products. Tea tree oil shampoos can help.")
        else:
            st.write(f"For **{symptom}**, consult a dermatologist for personalized care.")

# Footer
st.markdown("---")
st.caption("🔬 Powered by HairBot | Created by Nitin and Jaykrishnan | Built with Streamlit")
