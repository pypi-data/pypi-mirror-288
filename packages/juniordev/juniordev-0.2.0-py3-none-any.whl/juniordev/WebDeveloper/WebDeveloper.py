from agency_swarm.agents import Agent
from .tools import ChangeLines, CheckCurrentDir,DirectoryNavigator,RunCommand,FileWriter,FileReader,ListDir

class WebDeveloper(Agent):
    def __init__(self):
        super().__init__(
            name="WebDeveloper",
            description="A versatile agent for WebDevCrafters capable of navigating directories, reading, writing, modifying files, and executing terminal commands.",
            instructions="./instructions.md",
            # files_folder="./files",
            # schemas_folder="./schemas",
            tools=[ChangeLines, CheckCurrentDir, DirectoryNavigator, RunCommand, FileWriter, FileReader, ListDir],
            # tools_folder="./tools"
        )
