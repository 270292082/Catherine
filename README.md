# Catherine
An AI-powered conversational agent designed to provide emotional support, active listening, and structured coping strategies. This project is not a replacement for professional therapy, but rather a supportive tool for reflection, journaling, and self-guided mental well-being practices.

### Features

- 🧠 Conversational Support – empathetic, context-aware dialogue

- 📓 Journaling Mode – structured prompts for self-reflection

- 🌙 Mindfulness Tools – grounding exercises, breathing techniques, positive affirmations

- 🔄 Memory System – recalls key facts and progress across sessions

- 🎛 Customizable Personality – adjustable tone (gentle, professional, casual, etc.)

- 🔐 Local-first – can run fully offline for privacy (depending on chosen model)

### Installation
#### Prerequisites

- Python 3.10+
- Echoes (tomwongs)
- Mem4ai (unclecode)
- Nextcord (for discord implementation)
- Good GPU for fast inference (adjust your AI model depending on the power you have available)

#### Steps

```
# Clone the repository
git clone https://github.com/270292082/Catherine
cd Catherine


# Create virtual environment
python -m venv venv
source venv/bin/activate   # on Linux/Mac
venv\Scripts\activate      # on Windowspython 

# Install dependencies
pip install -r requirements.txt
```
Once the program done you have to put the api key in 'core/api.py' (create the file)
``` core/api.py
key = "[YOUR_API_KEY]"
```

### Privacy & Security 

- By default, conversations are stored locally in data/sessions/.
- No external API calls unless explicitly configured.
- You may enable/disable memory as needed.

### Disclaimer

This project is not a substitute for professional mental health care.\
If you are experiencing severe distress or suicidal thoughts, please seek immediate help from a licensed professional or contact your local crisis hotline.