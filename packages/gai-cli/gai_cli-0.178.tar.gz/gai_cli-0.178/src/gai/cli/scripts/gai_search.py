from gai.cli._gai_cli.Tools import Tools
import os
from openai import OpenAI

os.environ["OPENAI_API_KEY"]=""
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"]=""
client=OpenAI(api_key=os.environ["OPENAI_API_KEY"])
from gai.ttt.client.completions import Completions
client=Completions.PatchOpenAI(client)

def search(search_term):
    from gai.cli._gai_cli.Tools import Tools
    tools=Tools(client)
    tools.do_gg(search_term)