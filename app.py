import modules.audio_modules as am
import modules.text_modules as tm
import datetime
import streamlit as st
from dotenv import load_dotenv
import os


def clear_history():
    if 'history' in st.session_state:
        del st.session_state['history']

if __name__ == "__main__":

    st.write('# audioGPT by patrick🤖🎙️')
    st.write('\n\n\n\n')
    col1,col2 = st.columns(2)
    with col2:
        st.image('https://dallery.gallery/wp-content/uploads/2022/07/DALL%C2%B7E-prompt-resources-tools-inspiration-for-AI-art-585x775.jpg'
                 , width=325)
    with col1:
        st.write('Añade tu API Key de OpenAI y sube un archivo de audio para comenzar.')
        # cargar api key desde el archivo .env
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        # text_input para la api_key
        api_key = st.text_input('OpenAI API Key:', value = api_key ,type='password', on_change=clear_history)
        # guardar clave
        pass_col, get_col = st.columns(2)
        with pass_col:
            guardar_clave = st.checkbox('Guardar clave')
        with get_col:
            st.write('[Obtener una API Key](https://www.youtube.com/watch?v=VpcpHjeLZSs)')
        # estado del archivo
        st.session_state.is_file_charged = False
        # widget para subir archivo
        uploaded_file = st.file_uploader('Subir archivo', type=['m4a', 'mp3','mp4', 'mpeg', 'mpga', 'wav', 'webm'])
        # boton de añadir
        add_data_button = st.button('Añadir', on_click=clear_history)
        # si no ha apretado el boton de añadir pero el vector db del archivo si está cargado
    if not add_data_button:
            if  os.path.exists('db'):
                st.success('Ya existe un archivo en memoria. Añadir otro lo sobreescribirá.')
                st.session_state.is_file_charged = True
            
    st.divider()

        # si reescribes la clave
    if api_key:
            # cargar la clave en la variable de entorno
            os.environ['OPENAI_API_KEY'] = api_key
            # guardarla en el archivo .env
    if guardar_clave:
            with open('.env', 'w') as f:
                f.write(f'OPENAI_API_KEY={api_key}')

        # se sube un archivo
    if uploaded_file and add_data_button:
            with st.spinner('Procesando...'):
                
                bytes_data = uploaded_file.read()
                file_name = os.path.join('./', uploaded_file.name)
                with open(file_name, 'wb') as f:
                    f.write(bytes_data)

                # transcribir el archivo
                print("Transcribing document...")
                transcriber = am.OpenAITranscribeAudio(api_key=api_key)
                data = transcriber.transcribe_audio(file_path=file_name)
                text = data['text']
                # guardar la transcripcion
                with open('output/transcription.txt', 'w') as f:
                    f.write(text)
                st.session_state.transcribed_text = text
                #cargar el archivo
                print("Loading document...")
                loaded_data = tm.LoadDocument.load_document(file_path='output/transcription.txt', file_extension='.txt')
                # separar en chunks
                print("Chunking document...")
                chunks = tm.ChunkData.chunk_data(data=loaded_data)
                # instanciar embedding model
                print("Creating embedding model...")
                embedding_model = tm.OpenAIEmbeddings.create_embedding_model()
                # crear vector store, generar y guardar embeddings
                print("Creating vector store...")
                vector_store = tm.VectorStoreChroma.create_vector_store(chunks, embedding_model)
                # guardar el db en la sesion de Streamlit
                print("Saving vector store...")
                st.session_state.vs = vector_store
                st.success('Nuevo archivo cargado.')
                st.session_state.is_file_charged = True


    
    #rol del chatbot
    system_message = 'Tu rol es'

    # transcripción
    if st.session_state.is_file_charged:
        text = st.session_state.transcribed_text
        st.text_area('Transcripción: ', value=text, height=300)

        # obtener fecha y hora actual
        now = datetime.datetime.now()

        # boton de descargar transcripcion
        st.download_button(
        label="Descargar transcripción",
        data=text,
        file_name='transcripcion_'+ str(now) +'.txt',
        mime='text/plain')

        st.divider()

        # query del usuario
        query = st.text_area('Hacer una pregunta a la IA sobre el audio...', height=160)

        # boton de generar respuesta
        is_button_pressed = st.button('Generar respuesta')

        # si el usuario apretó generar respuesta
        if query and is_button_pressed:

            # si los datos del archivo no han sido cargados en la sesion de Streamlit
            if 'vs' not in st.session_state:

                # instanciar embedding model
                embedding_model = tm.OpenAIEmbeddings.create_embedding_model()
                # crear vector store, generar y guardar embeddings
                vector_store = tm.VectorStoreChroma.create_vector_store(chunks, embedding_model)
                # guardar el db en la sesion de Streamlit
                st.session_state.vs = vector_store

            # si los datos estan cargados
            if 'vs' in st.session_state:
                with st.spinner('Pensando...'):
                    
                    # recuperar vector store
                    vector_store = st.session_state.vs
                    # instanciar chatbot
                    print("Creating chatbot...")
                    chatbot = tm.OpenAIChat.create_chat_model(system_message=system_message)
                    # crear cadena de respuesta
                    print("Creating answer...")
                    answer = tm.SimpleQuestionAnswer.ask_and_get_answer(query=query, vector_store=vector_store, llm=chatbot, k=3)
                    print("Gathering sources...")
                    sources = vector_store.similarity_search(query)

                    st.text_area('Respuesta: ', value=answer, height=300)

                    with st.expander('Fuentes: '):
                            for source in sources:
                                st.write(source.page_content + '\n')

                    st.divider()

                    # si no hay historial, crearlo
                    if 'history' not in st.session_state:
                        st.session_state.history = ''

                    # pregunta actual
                    value = f'Pregunta: {query} \n\nRespuesta: {answer}'

                    st.session_state.history = f'{value} \n {"-" * 20} \n {st.session_state.history}'
                    h = st.session_state.history

                    # historial
                    with st.expander('Historial'):
                        st.text_area(label='Historial', value=h, key='history', height=400)

# para correr la app en terminal: streamlit run ./model.py