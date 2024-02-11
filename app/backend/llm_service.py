from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

def get_llm():
	print("HI")
	llm = LlamaCpp(
		model_path = "./../../../llama_weights/llama-2-7b-chat.Q4_K_M.gguf",
		temperature=0.3,
		max_tokens=512,
		top_p=1,
		n_ctx = 1024,
		# callback_manager=callback_manager,
		verbose=True,  # Verbose is required to pass to the callback manager
		stop = ["Human", "AI Assistant", "Language Teacher", "Student"],
	)
	print("PLEASE?")
	return llm

"""
	common functionalities used across every agent
"""


class ConversationAgent:
	def __init__(self, language, chat_history, topic="everyday life"):

		#super().__init__()
		self.llm_conv = get_llm()

		self.language = language
		self.topic = topic
		self.chat_history = chat_history
		self.system_prompt = self.get_system_prompt(language=self.language, topic=self.topic)
		#self.memory = ConversationBufferMemory(memory_key="history",chat_memory=chat_history) ##TO DO
		#error	"1 validation error for ConversationBufferMemory\nchat_memory\n instance of BaseChatMessageHistory expected (type=type_error.arbitrary_type; expected_arbitrary_type=BaseChatMessageHistory)"

		# self.history.append({"system": self.system_prompt})
		print("Initialize Conversation Chain...")
		self.conversation = ConversationChain(
			prompt=self.system_prompt,
			llm=self.llm_conv, 
			verbose=True, 
			#memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
			#memory=self.memory,
			#memory = self.chat_history
			)
		print("Finished Initializing Chain")


	def get_system_prompt(self, language, topic):
		_template = "The following is a friendly conversation between a human and an AI. The AI answers precisely only talks in {}. No word is other than {}. The AI is enthusiastic about the topic '{}'. If the AI does not know the answer to a question, it truthfully says it does not know.".format(language, language, topic)
		_history_template = "\n current conversation:\n {}".format(self.chat_history)
		template = _template + _history_template + """

		{history} 
		Human: {input}
		AI Assistant:"""

		system_prompt = PromptTemplate(input_variables=["history", "input"], template=template)
		return system_prompt

	"""
		Probably not needed to pre/post-process the message
	"""
	def process_message(self):
		pass

	def answer(self, user_message):
		print(self.chat_history)
		response = self.conversation.predict(input=user_message)
		#print(response)
		#self.history.append({"USER": user_message, "ASSISTANT": response})
		return response



	def retriever(self):
		pass


	# def talk(self): 
	# 	history = {}

	# 	while smth:
	# 		human = input("bla")
	# 		response = answer(self.llm)
	# 		history += {"human": human, "assistant": response}

	# 		smth = self.check_break_condition()

	# 	return history


def format_dialogue(dialogue_list):
	formatted_dialogue = ""
	for i in range(len(dialogue_list)):
		if i % 2 == 0:
			formatted_dialogue += f"Human: {dialogue_list[i]}\n"
		else:
			formatted_dialogue += f"AI:  {dialogue_list[i]}\n"
	return formatted_dialogue


class MessageProcessor:
	def __init__(self):
		self.tmp = "HI bro"

	def process_message(self, user_message, chat_type, formality, chat_history):
		tmp = "You just entered: "
		res = tmp + user_message + " with:" + chat_type + " + " + formality
		# return "You just entered: ".format(user_message)
		print(res)

		##chose prompt based on chat-type (grammar assistant, coversation) and formality (informal, formal) 
		##_template = " You are a friendly language teacher for the language {}. You translate that the text from {} to {} precisely. You do not halucinate or interpret the text of the user. The generated text must be in {}".format(dest_language, dest_language, source_language, source_language)
		## -> get_prompt anpassen

		result_list = chat_history.split("\\n")
		history = format_dialogue(result_list)
		#history = {"history": history}
			
		if chat_type == "conversation":
			conversation_agent = ConversationAgent("english", history, "everyday life")
			model_answer = conversation_agent.answer(user_message)
		else:
			grammar_agent = GrammarAssistant("english")
			model_answer = grammar_agent.answer(user_message)

		return model_answer

class TranslatorAgent:
	def __init__(self, language):
		#super().__init__()

		self.language = language
		self.system_prompt = self.get_system_prompt(language=self.language)
			
		self.chain = LLMChain(
			llm = self.llm,
			prompt = self.system_prompt
			)

	def get_system_prompt(self, language):
		_template = " You are a friendly language teacher for the language {}. You translate that the text from {} to {} precisely. You do not halucinate or interpret the text of the user. The generated text must be in {}".format(dest_language, dest_language, source_language, source_language)

		template = _template + """

		Human: {message}
		Language Teacher:"""

		system_prompt = PromptTemplate(input_variables=["message"], template=template)
		return system_prompt

	def answer(self, user_message):
		response = self.chain.run(input=user_message)
		print(response)
		self.history.append({"USER": user_message, "ASSISTANT": response})


class GrammarAssistant:
	def __init__(self, language="english"):
		#super().__init__()

		self.language = language
		self.system_prompt = self.get_system_prompt(language=self.language)
		self.llm = get_llm()
		
		self.chain = LLMChain(
			llm = self.llm,
			prompt = self.system_prompt
			)

	def get_system_prompt(self, language="english"):
		_template = " You are a friendly language teacher for the language {}. You nicely analyse and correct the sentences of the student. You do not halucinate or interpret the text of the user.".format(language)

		template = _template + """

		Student: {message}
		Language Teacher:"""

		system_prompt = PromptTemplate(input_variables=["message"], template=template)
		return system_prompt

	def answer(self, user_message):
		response = self.chain.run(input=user_message)
		print(response)
		# self.history.append({"USER": user_message, "ASSISTANT": response})
		return response


class EndlessConversation:
	def __init__(self, language, topic, conv_length):
		#super().__init__()

		self.language = language
		self.topic = topic
		self.conv_length = conv_length

		self.agent_1_system_prompt = self.get_system_prompt(language=self.language, topic=self.topic, agent="first")
		self.agent_2_system_prompt = self.get_system_prompt(language=self.language, topic=self.topic, agent="second")

		self.conversation = ConversationChain(
			prompt=self.system_prompt,
			llm=self.llm_conv, 
			verbose=True, 
			memory=ConversationBufferMemory(ai_prefix="User2", human_prefix="User1"),
			)

	def get_system_prompt(self, language="english", topic="normal things", mood=None):
		if mood is None:
			_template = "The following is a friendly conversation between User1 and User2 who are experts in the topic '{}'. User1 and User2 only speak in {}. They never, never use another language than {}. Each user answers precisely and talkative with each other. If any User does not know the answer to a question, it truthfully says it does not know.".format(topic, language, language)
		elif mood is not None:
			assert len(mood) == 2
			_template = "The following is a friendly conversation between User1 and User2 who are experts in the topic '{}'. User1 and User2 only speak in {}. They never, never use another language than {}. User1 tends to be {}, whereas User1 is {}. If any User does not know the answer to a question, it truthfully says it does not know.".format(topic, language, language, mood[0], mood[1])
		else:
			raise("The length of Mood is not equal to 2.")


		template = _template + """

		Current conversation:
		{history}
		User1: {input}
		User2:"""

		system_prompt = PromptTemplate(input_variables=["history", "input"], template=template)
		return system_prompt

	# def endless_conversatio(self):
	# 	for i in range(self.conv_length):
	# 		response
