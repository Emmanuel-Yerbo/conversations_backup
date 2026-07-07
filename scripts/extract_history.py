import os
import json
import re
from datetime import datetime

# Path Configuration
USER_PROFILE = os.environ.get('USERPROFILE', 'C:\\Users\\LENOVO')
BRAIN_DIRS = [
    os.path.join(USER_PROFILE, '.gemini', 'antigravity', 'brain'),
    os.path.join(USER_PROFILE, '.gemini', 'antigravity-backup', 'brain'),
    os.path.join(USER_PROFILE, '.gemini', 'antigravity-ide', 'brain')
]
REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_DIR, 'data')
DETAIL_DIR = os.path.join(DATA_DIR, 'detail')
MEDIA_DEST_DIR = os.path.join(REPO_DIR, 'media')
TAKEOUT_DIR = os.path.join(REPO_DIR, 'takeout')

# Create target directories
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DETAIL_DIR, exist_ok=True)
os.makedirs(MEDIA_DEST_DIR, exist_ok=True)
os.makedirs(TAKEOUT_DIR, exist_ok=True)

# Known titles and summaries from prompt context
KNOWN_CONVERSATIONS = {
    "a80652a2-3f6f-407e-a81b-f67cdcbec7ad": {
        "title": "GeoAI Faculty Outreach Strategy",
        "summary": "Strategizing academic outreach for GeoAI research positions, aligning skills with faculty member profiles, and drafting high-impact cold emails."
    },
    "ad6d50a9-2e40-46d8-844c-61d07388fc96": {
        "title": "Finalizing GeoAI Research Pipeline",
        "summary": "Discussion and execution of a GeoAI research pipeline for precision agriculture and landscape classifications in West Africa."
    },
    "d33323d7-5bb0-4b15-88c6-c7417cb70a37": {
        "title": "Drafting Nunn Family Fellowship Application",
        "summary": "Auditing and humanizing a research proposal for the Nunn Family Fellowship and University of Ghana MPhil program using an adversarial AI pipeline."
    },
    "d3011edc-0e68-4460-85c5-8e57da2c2d6e": {
        "title": "Urban Geomorphology Implementation Framework",
        "summary": "Developing framework files and processing spatial statistics for urban geomorphology studies."
    },
    "caf87358-043e-4baf-94a7-670a55e7ed83": {
        "title": "Extracting Population Data for GIS",
        "summary": "Extracting population statistics and GIS shapefiles for integration with spatial analysis models."
    },
    "5703f06d-4e56-4f1f-b1ea-448fde4a937a": {
        "title": "Converting Literature To Word",
        "summary": "Converting literature reviews, citations, and documents into Microsoft Word format with consistent academic styling."
    },
    "a84c3bbd-98da-4b94-8165-29b18ab60865": {
        "title": "Web Development Asset Analysis",
        "summary": "Analyzing assets, structure, and code systems for geographical interactive web applications."
    },
    "51eed351-8f17-43e1-b404-f216f378b89e": {
        "title": "Term Paper Assignment Implementation",
        "summary": "Developing lesson plans, slide decks, and materials for physics and biology curriculum assignments."
    },
    "3dc196c6-417c-4087-b50e-9a5091cdf3f6": {
        "title": "Mapping Ghana Nighttime Lights",
        "summary": "Processing satellite nighttime light datasets to map development indicators and urban growth in Ghana."
    },
    "e6c389b1-859e-44c6-81f7-95fc5f49a888": {
        "title": "Esri Conference Abstract Development",
        "summary": "Drafting and refining a conference abstract for submission to the annual Esri conference."
    },
    "34caa434-b89a-4d0f-beb1-a0e500fa71b2": {
        "title": "Editing Project Documents",
        "summary": "Editing research statements, cover letters, and project writeups for pedestrian safety and geodjango blueprints."
    }
}

def clean_xml_tags(text):
    """Clean XML tags like <USER_REQUEST> from text and extract pure request if possible."""
    if not text:
        return ""
    
    # Try to extract content of USER_REQUEST first
    match = re.search(r'<USER_REQUEST>(.*?)</USER_REQUEST>', text, re.DOTALL | re.IGNORECASE)
    if match:
        text = match.group(1).strip()
    
    # Remove any other common tags
    text = re.sub(r'<ADDITIONAL_METADATA>.*?</ADDITIONAL_METADATA>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<USER_SETTINGS_CHANGE>.*?</USER_SETTINGS_CHANGE>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text) # Strip remaining tags
    return text.strip()

def sanitize_secrets(text):
    """Redact typical API keys and secrets from the conversation text to prevent security leaks."""
    if not text:
        return ""
    # Redact Groq API Keys (gsk_...)
    text = re.sub(r'gsk_[a-zA-Z0-9_-]{30,}', '[REDACTED_GROQ_API_KEY]', text)
    # Redact GCP API Keys (AIzaSy...)
    text = re.sub(r'AIzaSy[A-Za-z0-9_-]{30,}', '[REDACTED_GCP_API_KEY]', text)
    # Redact GCP API/Gemini Keys starting with AQ.
    text = re.sub(r'AQ\.[A-Za-z0-9_-]{30,}', '[REDACTED_GCP_TOKEN]', text)
    # Redact OpenAI API Keys (sk-...)
    text = re.sub(r'sk-[a-zA-Z0-9_-]{30,}', '[REDACTED_OPENAI_API_KEY]', text)
    return text

def infer_title_and_summary(uuid, first_user_input):
    """Get title and summary using known map, or infer from first user input."""
    if uuid in KNOWN_CONVERSATIONS:
        return KNOWN_CONVERSATIONS[uuid]["title"], KNOWN_CONVERSATIONS[uuid]["summary"]
    
    clean_input = clean_xml_tags(first_user_input)
    if not clean_input:
        return f"Conversation {uuid[:8]}", "No details available."
    
    # Extract first line or sentence as title
    lines = clean_input.split('\n')
    first_line = lines[0].strip()
    if len(first_line) > 60:
        title = first_line[:57] + "..."
    else:
        title = first_line
        
    # Remove characters that can break markdown headers
    title = re.sub(r'[#*`\[\]]', '', title).strip()
    if not title:
        title = f"Conversation {uuid[:8]}"
        
    # Use first few lines as summary
    summary = clean_input[:150].strip()
    if len(clean_input) > 150:
        summary += "..."
    summary = summary.replace('\n', ' ')
    
    return title, summary

def format_timestamp(ts_str):
    """Convert ISO timestamp to human readable format."""
    try:
        dt = datetime.strptime(ts_str.split('.')[0].replace('Z', ''), "%Y-%m-%dT%H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return ts_str

def parse_transcript(convo_id, file_path):
    """Parse transcript.jsonl or overview.txt into structured list of turns."""
    turns = []
    if not os.path.exists(file_path):
        return turns
        
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                source = data.get('source')
                msg_type = data.get('type')
                created_at = data.get('created_at', '')
                content = data.get('content', '')
                tool_calls = data.get('tool_calls', [])
                
                # Skip cleared steps with no content/tool calls
                if not content and not tool_calls:
                    continue
                
                # We care about User inputs and Model responses
                if source == "USER_EXPLICIT" and msg_type == "USER_INPUT":
                    turns.append({
                        "role": "user",
                        "time": created_at,
                        "content": sanitize_secrets(clean_xml_tags(content)),
                        "raw_content": sanitize_secrets(content)
                    })
                elif source == "MODEL" and msg_type == "PLANNER_RESPONSE":
                    formatted_tools = []
                    if tool_calls:
                        for call in tool_calls:
                            name = call.get('name')
                            args = call.get('args', {})
                            target = args.get('TargetFile') or args.get('AbsolutePath') or args.get('CommandLine') or args.get('Url') or args.get('query') or ''
                            formatted_tools.append({
                                "name": name,
                                "target": sanitize_secrets(target)
                            })
                    
                    turns.append({
                        "role": "assistant",
                        "time": created_at,
                        "content": sanitize_secrets(content or "[Response Cleared]"),
                        "tools": formatted_tools
                    })
            except Exception as e:
                # Skip invalid lines
                continue
                
    return turns

def generate_markdown(metadata, turns):
    """Generate beautiful Markdown document for a conversation."""
    md = []
    md.append(f"# 💬 {metadata['title']}")
    md.append(f"**Conversation ID:** `{metadata['id']}`  ")
    md.append(f"**Started:** {format_timestamp(metadata['created_at'])} | **Last Updated:** {format_timestamp(metadata['updated_at'])}  ")
    md.append(f"**Messages:** {metadata['message_count']} | **Model:** {metadata['model_name']}  ")
    md.append("\n---\n")
    
    if metadata['summary']:
        md.append(f"> **Summary:** {metadata['summary']}\n\n---\n")
        
    for turn in turns:
        role = turn['role']
        time_str = format_timestamp(turn['time'])
        content = turn['content']
        
        if role == 'user':
            md.append(f"### 👤 User — *{time_str}*\n")
            md.append(content)
            md.append("\n")
        else:
            md.append(f"### 🤖 Gemini/Antigravity — *{time_str}*\n")
            
            # Document tool calls if any
            if turn.get('tools'):
                md.append("<details><summary>🛠️ Tools Executed</summary>\n")
                for tool in turn['tools']:
                    md.append(f"- **`{tool['name']}`**: `{tool['target']}`\n")
                md.append("</details>\n")
                
            md.append(content)
            md.append("\n")
            
        md.append("\n---\n")
        
    return "\n".join(md)

def parse_takeout_json(takeout_path):
    """Parse Google Takeout MyActivity.json for Gemini Apps activity."""
    turns_by_convo = {}
    if not os.path.exists(takeout_path):
        return turns_by_convo
        
    print(f"Reading Google Takeout JSON: {takeout_path}...")
    with open(takeout_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                print("Error: Takeout JSON root is not a list")
                return turns_by_convo
                
            for item in data:
                header = item.get('header', '')
                if 'Gemini' not in header:
                    continue
                
                title = item.get('title', '')
                time_str = item.get('time', '')
                title_url = item.get('titleUrl', '')
                
                convo_id = "general_web_chat"
                if title_url:
                    match = re.search(r'/app/c/([a-zA-Z0-9_-]+)', title_url)
                    if match:
                        convo_id = match.group(1)
                        
                query = title.replace('Asked Gemini Apps:', '').strip()
                if not query:
                    continue
                    
                details = item.get('details', [])
                response = ""
                for detail in details:
                    name = detail.get('name', '')
                    if name:
                        response = name
                        break
                        
                if convo_id not in turns_by_convo:
                    turns_by_convo[convo_id] = []
                    
                turns_by_convo[convo_id].append({
                    "role": "user",
                    "time": time_str,
                    "content": sanitize_secrets(query),
                    "raw_content": sanitize_secrets(title)
                })
                
                if response:
                    turns_by_convo[convo_id].append({
                        "role": "assistant",
                        "time": time_str,
                        "content": sanitize_secrets(response),
                        "tools": []
                    })
        except Exception as e:
            print(f"Error parsing Takeout JSON: {e}")
            
    for convo_id in turns_by_convo:
        turns_by_convo[convo_id].sort(key=lambda x: x['time'])
        
    return turns_by_convo

def sync_conversations():
    """Main synchronization loop."""
    print("Scanning app data directories:")
    for d in BRAIN_DIRS:
        print(f"  - {d}")
        
    # Gather all conversation folders from all directories
    convo_map = {} # uuid -> list of target log paths
    
    for d in BRAIN_DIRS:
        if not os.path.exists(d):
            continue
        folders = [f for f in os.listdir(d) if os.path.isdir(os.path.join(d, f)) and len(f) == 36]
        for folder in folders:
            convo_path = os.path.join(d, folder)
            transcript_path = os.path.join(convo_path, '.system_generated', 'logs', 'transcript.jsonl')
            overview_path = os.path.join(convo_path, '.system_generated', 'logs', 'overview.txt')
            
            target_path = None
            if os.path.exists(transcript_path):
                target_path = transcript_path
            elif os.path.exists(overview_path):
                target_path = overview_path
                
            if target_path:
                if folder not in convo_map:
                    convo_map[folder] = []
                convo_map[folder].append(target_path)
                
    print(f"Found {len(convo_map)} unique conversation directories with logs.")
    
    convo_list = []
    
    for folder, paths in convo_map.items():
        # Parse turns for each path and keep the one with the most turns
        best_turns = []
        best_path = None
        for path in paths:
            turns = parse_transcript(folder, path)
            if len(turns) > len(best_turns):
                best_turns = turns
                best_path = path
                
        if not best_turns:
            continue
            
        # Get start/end timestamps
        created_at = best_turns[0]['time']
        updated_at = best_turns[-1]['time']
        
        # Get first non-empty user turn content to infer title
        first_input = ""
        for t in best_turns:
            if t['role'] == 'user' and t['content'].strip():
                first_input = t['content']
                break
        
        title, summary = infer_title_and_summary(folder, first_input)
        
        metadata = {
            "id": folder,
            "title": title,
            "summary": summary,
            "created_at": created_at,
            "updated_at": updated_at,
            "message_count": len(best_turns),
            "model_name": "Gemini 3.5 Flash / Claude Opus" # Fallback/generic
        }
        
        # Save individual JSON
        convo_json_path = os.path.join(DETAIL_DIR, f"{folder}.json")
        with open(convo_json_path, 'w', encoding='utf-8') as f:
            json.dump({"metadata": metadata, "turns": best_turns}, f, indent=2)
            
        # Generate and save Markdown
        md_content = generate_markdown(metadata, best_turns)
        convo_md_path = os.path.join(DETAIL_DIR, f"{folder}.md")
        with open(convo_md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        convo_list.append(metadata)
        print(f"  Processed: {title}")
        
    # Process Google Takeout data if available
    takeout_json_path = os.path.join(TAKEOUT_DIR, 'MyActivity.json')
    if os.path.exists(takeout_json_path):
        takeout_convos = parse_takeout_json(takeout_json_path)
        print(f"Found Google Takeout data. Processing {len(takeout_convos)} web conversations...")
        for convo_id, turns in takeout_convos.items():
            if not turns:
                continue
                
            created_at = turns[0]['time']
            updated_at = turns[-1]['time']
            
            first_input = ""
            for t in turns:
                if t['role'] == 'user' and t['content'].strip():
                    first_input = t['content']
                    break
                    
            title, summary = infer_title_and_summary(convo_id, first_input)
            
            metadata = {
                "id": f"web_{convo_id}",
                "title": f"[Web] {title}",
                "summary": f"(Google Takeout Web Chat) {summary}",
                "created_at": created_at,
                "updated_at": updated_at,
                "message_count": len(turns),
                "model_name": "Google Gemini Web"
            }
            
            # Save individual JSON
            convo_json_path = os.path.join(DETAIL_DIR, f"web_{convo_id}.json")
            with open(convo_json_path, 'w', encoding='utf-8') as f:
                json.dump({"metadata": metadata, "turns": turns}, f, indent=2)
                
            # Generate and save Markdown
            md_content = generate_markdown(metadata, turns)
            convo_md_path = os.path.join(DETAIL_DIR, f"web_{convo_id}.md")
            with open(convo_md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
                
            convo_list.append(metadata)
            print(f"  Processed web conversation: {title}")
            
    # Sort conversations by updated_at descending
    convo_list.sort(key=lambda x: x['updated_at'], reverse=True)
    
    # Save main conversations.json
    with open(os.path.join(DATA_DIR, 'conversations.json'), 'w', encoding='utf-8') as f:
        json.dump(convo_list, f, indent=2)
        
    # Generate README.md index
    generate_readme(convo_list)
    print("Sync complete!")

def generate_readme(conversations):
    """Generate main README.md index."""
    readme_path = os.path.join(REPO_DIR, 'README.md')
    md = [
        "# 📚 Gemini Conversation History Repository",
        "\nThis repository serves as a permanent backup, index, and searchable library of all conversations with Gemini/Antigravity.\n",
        "## 📊 Statistics",
        f"- **Total Conversations:** {len(conversations)}",
        f"- **Last Synced:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        "## 🔍 Interactive Dashboard",
        "To search and read conversations in a premium interface, open [dashboard/index.html](./dashboard/index.html) in any web browser.\n",
        "## 📁 Conversation Index\n",
        "| Title | Messages | Last Updated | File |",
        "| :--- | :---: | :---: | :--- |"
    ]
    
    for convo in conversations:
        link = f"./data/detail/{convo['id']}.md"
        updated = convo['updated_at'].split('T')[0]
        md.append(f"| **{convo['title']}** | {convo['message_count']} | {updated} | [Read Transcript]({link}) |")
        
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md))

if __name__ == "__main__":
    sync_conversations()
