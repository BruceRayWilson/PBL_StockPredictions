from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
import autogen

# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
# and OAI_CONFIG_LIST_sample

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")


# config_list_gpt4 = autogen.config_list_from_json(
#     "OAI_CONFIG_LIST",
#     filter_dict={
#         "model": ["gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
#     },
# )

llm_config = {"config_list": config_list, "seed": 42}


coder = autogen.AssistantAgent(
    name="Coder",  # the default assistant agent is capable of solving problems with code
    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
   name="User_proxy",
#    system_message="A human admin.",
#    code_execution_config={"last_n_messages": 3, "work_dir": "coding"},
   code_execution_config={"work_dir": "coding"},
#    human_input_mode="NEVER",
)

critic = autogen.AssistantAgent(
    name="Critic",
    system_message="""Critic. You are a helpful assistant highly skilled in evaluating the quality of a given visualization code by providing a score from 1 (bad) - 10 (good) while providing clear rationale. YOU MUST CONSIDER VISUALIZATION BEST PRACTICES for each evaluation. Specifically, you can carefully evaluate the code across the following dimensions
- bugs (bugs):  are there bugs, logic errors, syntax error or typos? Are there any reasons why the code may fail to compile? How should it be fixed? If ANY bug exists, the bug score MUST be less than 5.
- Data transformation (transformation): Is the data transformed appropriately for the visualization type? E.g., is the dataset appropriated filtered, aggregated, or grouped  if needed? If a date field is used, is the date field first converted to a date object etc?
- Goal compliance (compliance): how well the code meets the specified visualization goals?
- Visualization type (type): CONSIDERING BEST PRACTICES, is the visualization type appropriate for the data and intent? Is there a visualization type that would be more effective in conveying insights? If a different visualization type is more appropriate, the score MUST BE LESS THAN 5.
- Data encoding (encoding): Is the data encoded appropriately for the visualization type?
- aesthetics (aesthetics): Are the aesthetics of the visualization appropriate for the visualization type and the data?

YOU MUST PROVIDE A SCORE for each of the above dimensions.
{bugs: 0, transformation: 0, compliance: 0, type: 0, encoding: 0, aesthetics: 0}
Do not suggest code. 
Finally, based on the critique above, suggest a concrete list of actions that the coder should take to improve the code.
""",
    llm_config=llm_config,
)

groupchat = autogen.GroupChat(agents=[user_proxy, coder, critic], messages=[], max_round=20)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

message = """
Create a Python script that manages classes for stock market data and stock trading.
There are two options for running this script.
Option A: Run the script from the command line using CLI arguments.  
Create an add_args method to build the command line argument parser.  
Make every option a different argument.  
Do not lump them into a single arguments.
Option B: Run the script and use the menu.

Create a menu for the following options:
1. Stock Symbol Verification
Execute the code using
    import StockSymbolCollection
    csv_filename = 'train_base.csv'  # Use this exact filename.
    StockSymbolCollection.exec(csv_filename)
2. Stock Data Collection
Execute the code using
    import StockData
    # Define start and end times
    # Get the dates from the command line for both options.
    start_time = datetime(2023, 1, 1)
    end_time = datetime(2023, 10, 1)

    # Create an instance of StockData with a list of symbols
    symbols_list = ["AAPL", "MSFT", "GOOGL"] # Read from 'train.csv'

    # Execute the data retrieval for all symbols
    result = StockData.exec(symbols_list, start_time, end_time)
3. Stock Preprocessor
Execute the code using
    StockPreprocessor.exec()
4. LLM
4.1 LLM Training
4.2 LLM Prediction
Add docstrings.  
Type all method variables to help you understand what you are doing.  Type the return type.
Use classes for everything except the main methods.
Create everything else as necessary.
"""

user_proxy.initiate_chat(manager, message=message)
