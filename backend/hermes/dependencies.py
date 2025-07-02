from esmerald import Inject

from .agent import get_agent_client

dependencies = {"agent": Inject(get_agent_client)}
