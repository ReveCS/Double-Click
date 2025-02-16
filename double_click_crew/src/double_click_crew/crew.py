from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai_tools import CSVSearchTool
from crewai.knowledge.source.excel_knowledge_source import ExcelKnowledgeSource
import os


# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class DoubleClickCrew():
	"""DoubleClickCrew crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# Get the directory where crew.py is located
	current_dir = os.path.dirname(__file__)

	# Construct the path to marketing_campaign.xlsx in the parent directory
	csv_path = os.path.abspath(os.path.join(current_dir, '../../../marketing_campaign.csv'))

	# Initialize tools or sources
	search_tool = CSVSearchTool(csv=csv_path)
	excel_source = ExcelKnowledgeSource(
    	file_paths=['marketing_campaign.xlsx']
	)
	
	"""
	@before_kickoff
	def before_kickoff_function(self, inputs):
		print(f"Before kickoff function with inputs: {inputs}")
		return inputs # You can return the inputs or modify them as needed

	@after_kickoff
	def after_kickoff_function(self, result):
		print(f"After `kickoff` function with result: {result}")
		return result # You can return the result or modify it as needed"""

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def data_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['data_analyst'],
			tools=[self.search_tool],
			knowledge_sources=[self.excel_source],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='outputs/most_amount_of_wine.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the DoubleClickCrew crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)	
