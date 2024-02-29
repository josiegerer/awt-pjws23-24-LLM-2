from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain, RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from constants import DB_FAISS_PATH, MODEL_PATH, MAX_TOKEN

DB_FAISS_PATH = DB_FAISS_PATH

def qa_prompt(formality):
	_template = "Retrieve words and information for the following text using {} language:\n".format(formality)
	prompt_template = _template + """
	{context}
	"""
	prompt = PromptTemplate(template=prompt_template,
                            input_variables=['context'])
	
	print(prompt)
	return prompt

def retrieval_qa(llm, prompt, vector_store):
	print(prompt)
	qa_chain = RetrievalQA.from_chain_type(llm=llm,
										#    chain_type='stuff',
										   retriever=vector_store.as_retriever(search_kwargs={'k': 3}),
										#    return_source_documents=True,
										   chain_type_kwargs={'prompt': prompt})
	print(qa_chain)
	return qa_chain


def qa_bot(qa_prompt):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2",
                                       model_kwargs={'device': 'cpu'})
    vector_store = FAISS.load_local(DB_FAISS_PATH, embeddings)
    llm = get_llm() 
    qa = retrieval_qa(llm, qa_prompt, vector_store)

    return qa

def get_llm():
	llm = LlamaCpp(
		model_path = MODEL_PATH,
		temperature=0.3,
		max_tokens=MAX_TOKEN,
		top_p=1,
		n_ctx=1024,
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
		# self.system_prompt = self.get_system_prompt()
		#self.memory = ConversationBufferMemory(memory_key="history",chat_memory=chat_history) ##TO DO
		#error	"1 validation error for ConversationBufferMemory\nchat_memory\n instance of BaseChatMessageHistory expected (type=type_error.arbitrary_type; expected_arbitrary_type=BaseChatMessageHistory)"

		# self.history.append({"system": self.system_prompt})


	def get_system_prompt(self):
		_template = "The following is a friendly conversation between a human and a language Partner. The AI answers precisely only talks in {} and uses {} language only. No word is other than {}. If the AI does not know the answer to a question, it truthfully says it does not know. Make use of the following words and wordings in your answer.".format(self.language, self.formality, self.language)
		_history_template = "\n Current Conversation:\n {}".format(self.chat_history)
		print(self.qa_prompt)
		template = _template + self.qa_prompt["result"] + _history_template + """

		{history} 
		Human: {input}
		Partner:"""

		self.system_prompt = PromptTemplate(input_variables=["history", "input"], template=template)
		print(self.system_prompt)
		# return system_prompt

	def get_qa_prompt(self, user_message):
		qa_prompt_template = qa_prompt(self.formality)
		print("FINAL HI")
		print(user_message)
		qa_bot_instance = qa_bot(qa_prompt_template)
		print(qa_bot_instance)
		# query = "Retrieve {} words and information for the following text:\n{}\n".format(self.formality, user_message)
		self.qa_prompt = qa_bot_instance({"query": user_message})

	def answer(self, user_message):
		print(self.chat_history)
		# GET QA ANSWER 
		# GET SYSTEM PROMPT AND APPLY QA RESULT
		# INIT CHAIN
		# PREDICT

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

		response = self.conversation.predict(input=user_message)
		print(response)
		#self.history.append({"USER": user_message, "ASSISTANT": response})
		return response

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
			print("DOING INIT")
			conversation_agent = ConversationAgent("english", history, topic = "everyday life", formality = formality)
			conversation_agent.get_qa_prompt(user_message)
			print("CREATED QA PROMPT")
			conversation_agent.get_system_prompt()
			print("CREATED System prompt")
			model_answer = conversation_agent.answer(user_message)
		else:
			grammar_agent = GrammarAssistant("english", formality = formality)
			grammar_agent.get_qa_prompt(user_message)
			grammar_agent.get_system_prompt()
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
		You are a conversation partner that is very knowledgable about the topic {}.
		You respond to your other conversation partner in a precise and simple manner without any exaggerations and only make use of {} language.
		You do not hallucinate and if you do not know the answer to something you truthfully say so.
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
		You are a conversation partner that is very knowledgable about the topic {}.
		You respond to your other conversation partner in a precise and simple manner without any exaggerations and only make use of {} language.
		You do not hallucinate and if you do not know the answer to something you truthfully say so.
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
		# self.system_prompt = self.get_system_prompt(language=self.language)
		self.llm = get_llm()
		
	
	def get_qa_prompt(self, user_message):
		qa_prompt_template = qa_prompt(self.formality)
		print("FINAL HI")
		print(user_message)
		qa_bot_instance = qa_bot(qa_prompt_template)
		print(qa_bot_instance)
		# query = "Retrieve {} words and information for the following text:\n{}\n".format(self.formality, user_message)
		self.qa_prompt = qa_bot_instance({"query": user_message})

	def get_system_prompt(self):
		_template = " You are a friendly language teacher for the language {} using {} style only. You nicely correct and analyse the grammar and semantical mistakes of the sentences provided by the student. You do not halucinate or interpret the text of the user.\
			    If a message does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer, please don't share false information. \
				If words in the provided message are grammatically correct still analyse the semantic meaning of the sentence and correct it if needed. Think about the correction and analysis step by step.".format(self.language, self.formality)

		template = _template + self.qa_prompt["result"] + """

		Student: {message}
		Language Teacher:"""

		self.system_prompt = PromptTemplate(input_variables=["message"], template=template)

	def answer(self, user_message):
		self.chain = LLMChain(
			llm = self.llm,
			prompt = self.system_prompt
			)
		print(self.system_prompt)
		message = "analyse and correct the following message: " + user_message
		response = self.chain.run(message=message)
		print(response)
		# self.history.append({"USER": user_message, "ASSISTANT": response})
		return response

