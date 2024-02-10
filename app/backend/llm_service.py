from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import LlamaCpp

def get_llm(self, model_id="llama2_7b"):
	self.llm = LlamaCpp(
		#model_path="/Users/josi/Llama2_weights/llama-2-7b.Q4_K_M.gguf?download=true",
		model_path = "/Users/josi/Llama2_weights/llama-2-7b-chat.Q5_K_M.gguf",
		temperature=0.75,
		max_tokens=2048,
		top_p=1,
		# callback_manager=callback_manager,
		verbose=True,  # Verbose is required to pass to the callback manager
	)


"""
	common functionalities used across every agent
"""


class BaseAgent:
	def __init__(
		self,
		model_id,
	):
		self.history = []

		self.model_id = "/content/llama-2-7b-chat.Q4_K_M.gguf"

		self.llm = get_llm(model_id=self.model_id)

	def answer(self):
		raise("Son didn't implement this shit")

	def check_break_condition(self, human_message):
		if human_message == "exit":
			return 0
		else: 1

	def load_conversation(self, user, chat_id):
		pass


class ConversationAgent:
	def __init__(self, language, topic="everyday life"):

		super().__init__()

		self.language = language
		self.topic = topic
		self.system_prompt = self.get_system_prompt(language=self.language, topic=self.topic)


			# self.history.append({"system": self.system_prompt})
		print("Initialize Conversation Chain...")
		self.conversation = ConversationChain(
			prompt=self.system_prompt,
			llm=self.llm_conv, 
			verbose=True, 
			memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
			)
		print("Finished Initializing Chain")




	def get_system_prompt(self, language, topic):
		_template = "The following is a friendly conversation between a human and an AI. The AI answers precisely only talks in {}. No word is other than {}. The AI is enthusiastic about the topic '{}'. If the AI does not know the answer to a question, it truthfully says it does not know.".format(language, language, topic)

		template = _template + """

		Current conversation:
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
		response = self.conversation.predict(input=user_message)
		print(response)
		self.history.append({"USER": user_message, "ASSISTANT": response})




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

class MessageProcessor:
	def __init__(self):
		self.tmp = "HI bro"

	def process_message(self, user_message, chat_type, formality):
		tmp = "You just entered: "
		res = tmp + user_message + " with:" + chat_type + " + " + formality
		# return "You just entered: ".format(user_message)
		print(res)
		return res

class TranslatorAgent(BaseAgent):
	def __init__(self, language):
		super().__init__()

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


class GrammarAssistant(BaseAgent):
	def __init__(self, language):
		super().__init__()

		self.language = language
		self.system_prompt = self.get_system_prompt(language=self.language)
		
		self.chain = LLMChain(
			llm = self.llm,
			prompt = self.system_prompt
			)

	def get_system_prompt(self, language="english"):
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
		return response


class EndlessConversation(BaseAgent):
	def __init__(self, language, topic, conv_length):
		super().__init__()

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
