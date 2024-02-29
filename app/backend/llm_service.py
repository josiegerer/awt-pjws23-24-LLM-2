from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

def get_llm():
	llm = LlamaCpp(
		model_path = "./../../../llama_weights/llama-2-7b-chat.Q4_K_M.gguf",
		temperature=0.3,
		max_tokens=512,
		top_p=1,
		n_ctx = 1024,
		# callback_manager=callback_manager,
		verbose=True,  # Verbose is required to pass to the callback manager
		stop = ["Human", "AI Assistant", "Language Teacher", "Student", "Partner", "AI", "English Teacher", "Expert Partner", "Curious Partner"],
	)
	return llm

"""
	common functionalities used across every agent
"""


class ConversationAgent:
	def __init__(self, language, chat_history, formality, topic="everyday life"):

		#super().__init__()
		self.llm_conv = get_llm()
		self.language = language
		self.topic = topic
		self.formality = formality
		self.chat_history = chat_history
		self.system_prompt = self.get_system_prompt()
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


	def get_system_prompt(self):
		_template = "The following is a friendly conversation between a human and a language Partner. The AI answers precisely only talks in {} and uses {} language only. No word is other than {}. If the AI does not know the answer to a question, it truthfully says it does not know.".format(self.language, self.formality, self.language)
		_history_template = "\n current conversation:\n {}".format(self.chat_history)
		template = _template + _history_template + """

		{history} 
		Human: {input}
		Partner:"""

		system_prompt = PromptTemplate(input_variables=["history", "input"], template=template)
		return system_prompt


	def answer(self, user_message):
		print(self.chat_history)
		response = self.conversation.predict(input=user_message)
		print(response)
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
			conversation_agent = ConversationAgent("english", history, topic = "everyday life", formality = formality)
			model_answer = conversation_agent.answer(user_message)
		else:
			grammar_agent = GrammarAssistant("english", formality = formality)
			model_answer = grammar_agent.answer(user_message)

		return model_answer

class EvalProcessor:
	def __init__(self):
		print("time to eval")

	def eval_conversation(self, chat_type, formality, chat_history):
		result_list = chat_history.split("\\n")
		full_history = format_dialogue(result_list)

		evaluator = EvaluationAgent(formality, chat_type)
		model_answer = evaluator.evaluate(full_history)
		return model_answer

class EvaluationAgent:
	def __init__(self, formality, chat_type):
		self.formality = formality
		self.chat_type = chat_type

		if chat_type == "conversation":
			self.system_prompt = self.get_system_prompt_conv(formality=self.formality)
			print("#"*50)
		elif chat_type == "grammar":
			self.system_prompt = self.get_system_prompt_grammar(formality=self.formality)
		else:
			raise ValueError("CHAT TYPE NOT KNOWN")
		print(self.system_prompt)
		self.llm = get_llm()

		self.chain = LLMChain(
			llm = self.llm,
			prompt = self.system_prompt
			)

	def get_system_prompt_conv(self, formality):
		_template = """ You are a friendly english language teacher. Given a conversation history between a student and its teacher you evaluate the language of the student. 
		You give the student a grade between 0 and 10. 10 is the best grade and 0 ist the worst grade. You explain the student the decision of your grade, and you also give him
		examples why you choose that grade. Explain using examples from the student. The student should have use {} language"
		""".format(formality)

		template = _template + """

		Conversation History: 
		{history}

		English Teacher:"""

		system_prompt = PromptTemplate(input_variables=["history"], template=template)
		return system_prompt

	def get_system_prompt_grammar(self, formality):
		_template = """ You are a friendly english grammar and comprehension teacher. 
		Given english sentences from the student you only analyze and evaluate the english grammar and the semantic of the sentences. 
		You give the student a grade between 0 and 10. 10 is the best grade and 0 ist the worst grade. You explain the student the decision of your grade, and you also give him
		examples why you choose that grade. Explain using examples from the student. The student should have use {} language"
		""".format(formality)

		template = _template + """

		Conversation History: 
		{history}

		English Teacher:"""

		system_prompt = PromptTemplate(input_variables=["history"], template=template)
		return system_prompt

	def evaluate(self, full_history):
		response = self.chain.run(history=full_history)
		print(response)
		return response

class EndlessProcessor:
	def __init__(self, topic):
		self.topic = topic

	def process_message(self, formality, chat_history, user_message):
		result_list = chat_history.split("\\n")
		turn_indice = len(result_list) % 2
		full_history = format_dialogue(result_list)

		endless = EndlessConversation(formality, full_history, turn_indice, self.topic)
		model_answer = endless.answer(user_message)
		return model_answer

class EndlessConversation:
	def __init__(self, formality, chat_history, turn_indice, topic):
		self.formality = formality
		self.chat_history = chat_history
		self.turn_indice = turn_indice
		self.topic = topic
		
		if self.turn_indice == 1:
			self.system_prompt = self.get_system_prompt_1(formality=self.formality, topic=self.topic)
		elif self.turn_indice == 0:
			self.system_prompt = self.get_system_prompt_0(formality=self.formality, topic=self.topic)

		self.llm_conv = get_llm()
		self.conversation = ConversationChain(
			prompt=self.system_prompt,
			llm=self.llm_conv, 
			verbose=True, 
		)

	def get_system_prompt_1(self, formality, topic):
		_history_template = "\n Current Conversation:\n {}".format(self.chat_history)
		_template = """
		You are a friendly conversation partner. You are very knowledgable about the topic {}.
		You respond to your other conversation partner in a friendly and open-minded manner.
		You only make use of {} language.
		You do not hallucinate and if you do not know something, you do not say something factly false.
		""".format(topic, formality)

		template = _template + _history_template + """
		{history}

		Curious Partner: {input}
		Expert Partner: """

		system_prompt = PromptTemplate(input_variables=["history", "input"], template=template)

		return system_prompt

	def get_system_prompt_0(self, formality, topic):
		_history_template = "\n Current Conversation:\n {}".format(self.chat_history)
		_template = """
		You are a friendly conversation partner. You are very curious about the topic {}.
		You respond to your other conversation partner in a friendly and open-minded manner.
		You only make use of {} language.
		You do not hallucinate and if you do not know something, you do not say something factly false.
		""".format(topic, formality)

		template = _template + _history_template + """
		{history}

		Expert Partner: {input}
		Curious Partner: """

		system_prompt = PromptTemplate(input_variables=["history", "input"], template=template)

		return system_prompt

	def answer(self, user_message):
		response = self.conversation.predict(input=user_message)
		return response




class GrammarAssistant:
	def __init__(self, language, formality):
		#super().__init__()

		self.language = "english"
		self.formality = formality
		self.system_prompt = self.get_system_prompt(language=self.language)
		self.llm = get_llm()
		
		self.chain = LLMChain(
			llm = self.llm,
			prompt = self.system_prompt
			)

	def get_system_prompt(self, language="english"):
		_template = " You are a friendly language teacher for the language {} using {} style only. You nicely correct and analyse the grammar and semantical mistakes of the sentences provided by the student. You do not halucinate or interpret the text of the user.\
			    If a message does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer, please don't share false information. \
				If words in the provided message are grammatically correct still analyse the semantic meaning of the sentence and correct it if needed. Think about the correction and analysis step by step.".format(language,self.formality)

		template = _template + """

		Student: {message}
		Language Teacher:"""

		system_prompt = PromptTemplate(input_variables=["message"], template=template)
		return system_prompt

	def answer(self, user_message):
		message = "analyse and correct the following message: " + user_message
		response = self.chain.run(message=message)
		print(response)
		# self.history.append({"USER": user_message, "ASSISTANT": response})
		return response

