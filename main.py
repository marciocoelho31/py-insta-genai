import openai
from dotenv import load_dotenv
import os

def openai_whisper_transcrever(caminho_audio, nome_arquivo, modelo_whisper, openai):
    print("Estou transcrevendo com o Whisper...")

    audio = open(caminho_audio, "rb")

    resposta = openai.audio.transcriptions.create(
        model = modelo_whisper,
        file = audio
    )

    transcricao = resposta.text

    with open(f"texto_completo_{nome_arquivo}.txt", "w", encoding="utf-8") as arquivo_texto:
        arquivo_texto.write(transcricao)

    return transcricao

def openai_gpt_resumir_texto(transcricao_completa, nome_arquivo, openai):
    print("Resumindo com o gpt para um post do instagram ...")

    prompt_sistema = """
    Assuma que você é um músico independente de rock que costuma postar conteúdos em plataformas digitais para divulgar seu trabalho e que está construindo conteúdos em uma plataforma de áudio (podcast).

    Os textos produzidos devem levar em consideração uma peresona que consumirá os conteúdos gerados. Leve em consideração:

    - Seus seguidores são pessoas que gostam de rock nacional e de artistas novos e independentes, e que amam consumir conteúdos relacionados a música e curiosidades sobre os artistas e suas carreiras e obras musicais 
    - Você deve utilizar o gênero neutro na construção do seu texto
    - Os textos serão utilizados para convidar pessoas do instagram para consumirem seu conteúdo de áudio
    - O texto deve ser escrito em português do Brasil.

    """
    prompt_usuario = ". \nReescreva a transcrição acima para que possa ser postado como uma legenda do Instagram. Ela deve resumir o texto para chamada na rede social. Inclua hashtags"

    resposta = openai.chat.completions.create(
        model = "gpt-3.5-turbo-16k",
        messages = [
            {
                "role": "system",
                "content": prompt_sistema
            },
            {
                "role": "user",
                "content": transcricao_completa + prompt_usuario
            }
        ],
        temperature = 0.6
    )

    resumo_instagram = resposta.choices[0].message.content.strip()

    with open(f"resumo_instagram_{nome_arquivo}.txt", "w", encoding="utf-8") as arquivo_texto:
        arquivo_texto.write(resumo_instagram)

    return resumo_instagram

def ferramenta_ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, "rb") as arquivo:
            return arquivo.read()
    except IOError as e:
        print(f"Erro no carregamento do arquivo: {e}")

def openai_gpt_criar_hashtag(resumo_instagram, nome_arquivo, openai):
    print("Gerando as hashtags com a openai...")

def openai_gpt_criar_hashtag(resumo_instagram, nome_arquivo, openai):
    print("Gerando as hashtags com a open ai ... ")

    prompt_sistema = """
    Assuma que você é um músico independente de rock que costuma postar conteúdos em plataformas digitais para divulgar seu trabalho e que está construindo conteúdos em uma plataforma de áudio (podcast).

    Os textos produzidos devem levar em consideração uma persona que consumirá os conteúdos gerados. Leve em consideração:

    - Seus seguidores são pessoas que gostam de rock nacional e de artistas novos e independentes, e que amam consumir conteúdos relacionados a música e curiosidades sobre os artistas e suas carreiras e obras musicais
    - Você deve utilizar o gênero neutro na construção do seu texto
    - Os textos serão utilizados para convidar pessoas do instagram para consumirem seu conteúdo de áudio
    - O texto deve ser escrito em português do Brasil.
    - A saída deve conter 5 hashtags.

    """

    prompt_usuario =f'Aqui está um resumo de um texto "{resumo_instagram}". Por favor, gere 5 hashtags que sejam relevantes para este texto e que possam ser publicadas no Instagram.  Por favor, faça isso em português do Brasil '

    resposta = openai.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {
                "role": "system",
                "content": prompt_sistema
            },
            {
                "role": "user",
                "content": prompt_usuario
            }
        ],
        temperature = 0.6
    )

    hashtags = resposta.choices[0].message.content.strip()

    with open(f"hashtags_{nome_arquivo}.txt", "w", encoding="utf-8") as arquivo_texto:
        arquivo_texto.write(hashtags)

    return hashtags

def openai_gpt_gerar_texto_imagem(resumo_instagram, nome_arquivo, openai):
    print("Gerando a saída de texto para criação de imagens com o gpt...")

    prompt_sistema = """

    - A saída deve ser uma única, do tamanho de um tweet, que seja capaz de descrever o conteúdo do texto para que possa ser transcrito como uma imagem.
    - Não inclua hashtags

    """

    prompt_usuario =  f'Reescreva o texto a seguir, em uma frase, para descrever o texto abaixo em um tweet: {resumo_instagram}'    

    resposta = openai.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {
                "role": "system",
                "content": prompt_sistema
            },
            {
                "role": "user",
                "content": prompt_usuario
            }
        ],
        temperature = 0.6
    )

    texto_para_imagem = resposta.choices[0].message.content.strip()

    with open(f"texto_para_geracao_imagem_{nome_arquivo}.txt", "w", encoding="utf-8") as arquivo_texto:
        arquivo_texto.write(texto_para_imagem)

    return texto_para_imagem

def main():
    load_dotenv()

    caminho_audio = "podcast/podcast-podletras-mc-videbula.mp3"
    nome_arquivo = "podcast-podletras-mc-videbula.mp3"
    url_podcast = ""

    api_key_openai = os.getenv("API_KEY_OPENAI")
    openai.api_key = api_key_openai

    modelo_whisper = "whisper-1"

    # transcricao_completa = openai_whisper_transcrever(caminho_audio, nome_arquivo, modelo_whisper, openai)
    transcricao_completa = ferramenta_ler_arquivo("texto_completo_podcast-podletras-mc-videbula.mp3.txt")

    # resumo_instagram = openai_gpt_resumir_texto(transcricao_completa, nome_arquivo, openai)
    resumo_instagram  = ferramenta_ler_arquivo("resumo_instagram_podcast-podletras-mc-videbula.mp3.txt")

    # hashtags = openai_gpt_criar_hashtag(resumo_instagram, nome_arquivo, openai)
    hashtags = ferramenta_ler_arquivo("hashtags_podcast-podletras-mc-videbula.mp3.txt")

    resumo_imagem_instagram = openai_gpt_gerar_texto_imagem(resumo_instagram, nome_arquivo, openai)

if __name__=="__main__":
    main()
