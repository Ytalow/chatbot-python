import customtkinter

from dotenv import load_dotenv
from langchain import hub
from langchain_anthropic import ChatAnthropic
from langchain_voyageai import VoyageAIEmbeddings
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain.chains.combine_documents import create_stuff_documents_chain
from langsmith import traceable

# set the colors used on Tkinter
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.chat_history = []

        # set window configuration
        self.title("Bate-papo com IA com contexto")
        self.geometry(f"{1200}x{720}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2), weight=0)
        self.grid_rowconfigure((0), weight=1)

        # side menu with buttons
        self.options_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.options_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.options_frame.grid_rowconfigure(3, weight=1)

        self.convert_pdf_to_txt_button = customtkinter.CTkButton(
            self.options_frame,
            command=self.convert_pdf_to_txt_event,
            text="Converter PDF em txt",
        )
        self.convert_pdf_to_txt_button.grid(row=0, column=0, padx=20, pady=(60, 10))
        self.update_ai_context_button = customtkinter.CTkButton(
            self.options_frame,
            command=self.contextualize_from_docs_event,
            text="Atualizar contexto",
        )
        self.update_ai_context_button.grid(row=1, column=0, padx=20, pady=10)
        self.clear_history_button = customtkinter.CTkButton(
            self.options_frame,
            command=self.clear_history_event,
            text="Limpar histórico",
        )
        self.clear_history_button.grid(row=2, column=0, padx=20, pady=10)
        self.title_label = customtkinter.CTkLabel(
            self.options_frame,
            text="modelo utilizado:\n" + llm.model,
            font=customtkinter.CTkFont(size=20),
            anchor="w",
        )
        self.title_label.grid(row=7, column=0, padx=20, pady=(20, 10))

        # create an output textbox
        self.textbox = customtkinter.CTkTextbox(self, wrap="word")
        self.textbox.grid(
            row=0, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )
        # bind all the keys to nothing for the text to be selectable, but uneditable
        self.textbox.bind("<Key>", lambda e: "break")

        # create entry widget
        self.entry = customtkinter.CTkEntry(
            self, placeholder_text="Insira sua mensagem:"
        )
        self.entry.grid(
            row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew"
        )

        # create enter button
        self.enter_input_button = customtkinter.CTkButton(
            master=self,
            fg_color="transparent",
            border_width=2,
            text="Enter",
            command=self.enter_input_event,
        )
        self.enter_input_button.grid(
            row=1, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )

        self.bind("<Return>", self.enter_input_event)

        self.welcome_message = (
            "Chatbot: Bem vindo!\n" + "Dado o contexto, como posso te ajudar?"
        )
        self.textbox.insert("0.0", self.welcome_message)

    def loading_event(self):
        self.entry.delete("0", "end")
        self.entry.insert("0", "Carregando...")
        self.entry.update()
        self.entry.configure(state="disabled")

    def ready_event(self):
        self.entry.configure(state="normal")
        self.entry.delete("0", "end")

    def clear_history_event(self):
        self.textbox.delete("0.0", "end")
        chat_history.clear()
        self.textbox.insert("0.0", self.welcome_message)

    def convert_pdf_to_txt_event(self):
        exec(open("pdf_to_txt_converter.py").read())

    def enter_input_event(self, event=None):
        user_input = self.entry.get().strip()
        if user_input:
            self.textbox.insert("end", "\n\nVocê: \n" + user_input)
            self.loading_event()
            self.update()
            response = self.chatbot_prompt(user_input)
            self.ready_event()
            self.textbox.insert("end", "\n\nChatbot: \n" + response)

    def contextualize_from_docs_event(self):
        self.entry["text"] = "Carregando..."
        self.entry.configure(state="disabled")

        docs = TextLoader("./text.txt").load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        texts = text_splitter.split_documents(docs)
        self.retriever = FAISS.from_documents(
            texts, VoyageAIEmbeddings(model="voyage-law-2")
        ).as_retriever()

        self.history_aware_retriever = create_history_aware_retriever(
            llm, self.retriever, contextualize_q_prompt
        )
        self.rag_chain = create_retrieval_chain(
            self.history_aware_retriever, question_answer_chain
        )
        self.entry.configure(state="normal")
        self.entry.delete("0", "end")

    @traceable
    def chatbot_prompt(self, user_input: str):
        response = self.rag_chain.invoke(
            {"input": user_input, "chat_history": self.chat_history}
        )
        chat_history.extend([HumanMessage(content=user_input), response["answer"]])
        return response["answer"]


if __name__ == "__main__":

    # load environment variables
    load_dotenv()
    # another llm suggestions is claude-3-haiku-20240307
    llm = ChatAnthropic(model="claude-3-sonnet-20240229")
    prompt = hub.pull("rlm/rag-prompt")

    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Generate your response by following the steps below:
    1. Recursively break-down the question into smaller questions/directives if multiple\
    2. For each atomic question/directive:\
    select the most relevant information from the context given and conversation history\
    3. Generate a draft response using the selected information, \
    whose brevity/detail are tailored based on the specificity of the question\
    4. Remove duplicate content from the draft response\
    5. Generate your final response after adjusting it to increase accuracy and relevance\
    6. Now only show your final response! Do not provide any explanations or details, unless asked to.\
    {context}"""
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    chat_history = []

    app = App()
    app.contextualize_from_docs_event()
    app.mainloop()
