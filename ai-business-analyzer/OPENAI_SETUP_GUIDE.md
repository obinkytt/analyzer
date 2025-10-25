# 🔑 How to Get OpenAI API Key - Step by Step

## Step 1: Create OpenAI Account
1. **Go to**: https://platform.openai.com/
2. **Click**: "Sign up" (top right)
3. **Use**: Email or Google/Microsoft account
4. **Verify**: Your email address

## Step 2: Add Payment Method (Required)
⚠️ **Even for free credits**, you need to add a payment method:
1. **Go to**: https://platform.openai.com/account/billing
2. **Click**: "Add payment method"
3. **Add**: Credit/debit card or PayPal
4. **Set**: Monthly spending limit (e.g., $10)

## Step 3: Generate API Key
1. **Go to**: https://platform.openai.com/api-keys
2. **Click**: "Create new secret key"
3. **Name it**: "Business Analyzer App"
4. **Copy**: The key immediately (you can't see it again!)
5. **Store safely**: In password manager or secure note

## Step 4: Configure Your App

### Local Development
1. **Edit your `.env` file**:
```env
OPENAI_API_KEY=sk-your-actual-key-here
ANALYSIS_PROVIDER=openai
```

2. **Test the integration**:
```bash
python test_openai_integration.py
```

### Production Deployment
1. **Add environment variable** in your hosting platform:
   - **Render**: Environment Variables section
   - **Railway**: Variables tab
   - **Fly.io**: `fly secrets set OPENAI_API_KEY=sk-...`

## Step 5: Monitor Usage
1. **Dashboard**: https://platform.openai.com/usage
2. **Set alerts**: Get notified at 50%, 80% of limit
3. **Review monthly**: Check usage patterns

## Security Best Practices

### ✅ DO
- Store API key in environment variables
- Set monthly spending limits
- Use different keys for development/production
- Monitor usage regularly
- Rotate keys periodically

### ❌ DON'T
- Commit API keys to Git
- Share keys in chat/email
- Use same key across multiple projects
- Set unlimited spending
- Ignore usage alerts

## Troubleshooting

### "Invalid API Key" Error
1. Check the key starts with `sk-`
2. Ensure no extra spaces/characters
3. Verify key isn't expired
4. Check you're using the right key

### "Quota Exceeded" Error
1. Check your usage limits
2. Add more credits or raise limit
3. Wait for monthly reset
4. Consider optimizing prompts

### "Rate Limit" Error
1. Add delays between requests
2. Implement retry logic
3. Consider upgrading plan
4. Batch multiple requests

## Alternative Setup (If You Don't Want to Pay)

### Option 1: Use Heuristic Only
Your app already works great without AI!
```env
ANALYSIS_PROVIDER=heuristic
# No API key needed
```

### Option 2: Local Ollama (Free)
```env
ANALYSIS_PROVIDER=ollama
OLLAMA_MODEL=llama2
# Run Ollama locally for free
```

### Option 3: Freemium Model
- Free users get heuristic analysis
- Premium users get AI analysis
- Start free, upgrade when needed

## Next Steps
1. ✅ Get your API key
2. ✅ Configure environment variables
3. ✅ Test with small usage
4. ✅ Deploy your app
5. ✅ Monitor and optimize costs

**Your app is already amazing with heuristic analysis - AI just makes it even better!** 🚀