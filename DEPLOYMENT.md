# Deploy to LiveKit Cloud

This guide covers deploying your LiveKit Voice Agent to LiveKit Cloud using the LiveKit CLI.

## Prerequisites

- LiveKit Cloud account (sign up at https://cloud.livekit.io)
- LiveKit CLI installed (already installed via `brew install livekit`)
- Your agent code and Dockerfile ready

## Deployment Steps

### 1. Authenticate with LiveKit Cloud

First, authenticate your CLI with your LiveKit Cloud account:

```bash
lk cloud auth
```

This will open a browser window for you to log in and link your LiveKit Cloud project to the CLI.

### 2. Set Default Project (Optional)

If you have multiple projects, list them and set a default:

```bash
# List all projects
lk project list

# Set default project
lk project set-default "your-project-name"
```

### 3. Create Agent Configuration

Create a new agent configuration with LiveKit Cloud:

```bash
lk agent create --region us-west \
  --secrets OPENAI_API_KEY="your-openai-api-key"
```

This command:
- Registers your agent with LiveKit Cloud
- Creates a `livekit.toml` configuration file
- Assigns a unique agent ID
- Sets up secrets as environment variables

**Note**: The `--region` flag specifies where your agent will be deployed. Available regions include:
- `us-west` - US West Coast
- `us-east` - US East Coast
- `eu-central` - Europe Central
- `ap-southeast` - Asia Pacific

### 4. Deploy Your Agent

Deploy your agent to LiveKit Cloud:

```bash
lk agent deploy
```

This command:
1. **Uploads** your code to LiveKit Cloud build service
2. **Builds** a container image from your Dockerfile
3. **Deploys** the agent to your LiveKit Cloud project
4. **Automatically scales** based on demand

### 5. Monitor Deployment

Check your agent's status:

```bash
# View agent logs
lk agent logs

# Check agent status
lk agent list
```

You can also monitor your agent in the LiveKit Cloud dashboard at https://cloud.livekit.io

---

## Updating Your Agent

To deploy a new version of your agent:

```bash
lk agent deploy
```

LiveKit Cloud performs **rolling deployments**:
- New agent instances are deployed alongside existing ones
- New sessions are routed to new instances
- Old instances complete active sessions (up to 1 hour grace period)
- Zero downtime for users

---

## Managing Secrets

### Adding Secrets During Deployment

You can add or update secrets when deploying:

```bash
lk agent deploy --secrets OPENAI_API_KEY="new-key" NEW_SECRET="value"
```

### Using Secrets File

Create a `.env.secrets` file (add to `.gitignore`):
```
OPENAI_API_KEY=your-key
OTHER_SECRET=value
```

Deploy with secrets file:
```bash
lk agent deploy --secrets-file .env.secrets
```

### Mounting File Secrets

For sensitive files (like service account keys):

```bash
lk agent deploy --secret-mount ./credentials.json
```

---

## Verification

### Check Agent Connection

1. **LiveKit Cloud Dashboard**: Visit https://cloud.livekit.io and check the "Agents" section
2. **Agent should show as "Active"**
3. **View real-time logs** in the dashboard

### Test with Frontend

1. Connect a user to a room via your frontend
2. The agent should automatically join the room
3. Speak and verify the agent responds

### Monitor Logs

```bash
# Stream live logs
lk agent logs --follow

# View recent logs
lk agent logs --tail 100
```

---

## Troubleshooting

### Agent not deploying

**Check authentication:**
```bash
lk cloud auth
```

**Verify project is set:**
```bash
lk project list
lk project set-default "your-project"
```

### Agent crashes on startup

**Check logs:**
```bash
lk agent logs --tail 100
```

**Common issues:**
- Missing or invalid `OPENAI_API_KEY`
- Dockerfile errors
- Missing dependencies in `requirements.txt`

### Agent not connecting to rooms

**Verify credentials:**
- `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` are automatically provided by LiveKit Cloud
- You only need to provide application-specific secrets (like `OPENAI_API_KEY`)

### Multiple agent instances

This is **normal and expected**! LiveKit Cloud automatically:
- Scales agents based on demand
- Load balances across instances
- Ensures high availability

---

## Important Notes

### Automatic Credentials

When deploying to LiveKit Cloud, your agent automatically receives:
- `LIVEKIT_URL` - Your LiveKit server URL
- `LIVEKIT_API_KEY` - API credentials
- `LIVEKIT_API_SECRET` - API secret

**You don't need to set these manually!** They're injected automatically.

### What You Need to Provide

Only provide application-specific secrets:
- `OPENAI_API_KEY` - For OpenAI STT/LLM/TTS
- Any other API keys your agent needs

### Cost and Scaling

- LiveKit Cloud automatically scales your agents
- You're billed based on usage (agent runtime)
- Check your LiveKit Cloud dashboard for pricing details

---

## Quick Reference

```bash
# Authenticate
lk cloud auth

# Create agent
lk agent create --region us-west --secrets OPENAI_API_KEY="sk-..."

# Deploy agent
lk agent deploy

# View logs
lk agent logs --follow

# List agents
lk agent list

# Update secrets
lk agent deploy --secrets OPENAI_API_KEY="new-key"
```

---

## Next Steps

After deployment, your agent is live and will:
1. ✅ Automatically connect to your LiveKit Cloud project
2. ✅ Join rooms when users connect
3. ✅ Scale automatically based on demand
4. ✅ Handle multiple concurrent sessions

Your agent is now accessible 24/7 globally! 🎉
