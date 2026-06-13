import asyncio
import sys
from pathlib import Path

# Add the fake_news_agent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent / 'fake_news_agent'))

# Now import api module directly
import api
root = api.root
resp = asyncio.run(root())
print(type(resp))
# If FileResponse, print filename
if hasattr(resp, 'path'):
    print('path:', resp.path)
if hasattr(resp, 'filename'):
    print('filename:', resp.filename)
else:
    print(resp)
