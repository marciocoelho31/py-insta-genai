import openai
from dotenv import load_dotenv
import os
import requests
from pydub import AudioSegment
from PIL import Image

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
        model = "gpt-4-turbo",
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
        model = "gpt-4-turbo",
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
        model = "gpt-4-turbo",
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

def openai_dalle_gerar_imagem(resolucao, resumo_para_imagem, nome_arquivo, openai, qtd_imagens = 1):
    print("Criando uma imagem utilizando a API do DALL-E...")

    prompt_user = f"Uma pintura ultra futurista, textless, 3d que retrate {resumo_para_imagem}"

    resposta = openai.images.generate(
        prompt = prompt_user,
        n = qtd_imagens,
        size = resolucao
    )

    return resposta.data

def ferramenta_download_imagem(nome_arquivo, imagem_gerada, qtd_imagens = 1):
  lista_nome_imagens = []
  try:
    for contador_imagens in range(0, qtd_imagens):
        caminho = imagem_gerada[contador_imagens].url
        imagem = requests.get(caminho)

        with open(f"{nome_arquivo}_{contador_imagens}.png", "wb") as arquivo_imagem:
            arquivo_imagem.write(imagem.content)

        lista_nome_imagens.append(f"{nome_arquivo}_{contador_imagens}.png")
    return lista_nome_imagens
  except:
    print("Ocorreu um erro!")
    return None

def ferramenta_transcrever_audio_em_partes(caminho_audio_podcast, nome_arquivo):
    print("Iniciando corte...")
    audio = AudioSegment.from_mp3(caminho_audio_podcast)

    dez_minutos = 10 * 60 * 1000
    
    contador_pedaco = 1
    arquivos_exportados = []

    while len(audio) > 0:
        pedaco = audio[:dez_minutos]
        nome_pedaco_audio = f"{nome_arquivo}_parte_{contador_pedaco}.mp3"
        pedaco.export(nome_pedaco_audio, format="mp3")
        arquivos_exportados.append(nome_pedaco_audio)
        audio = audio[dez_minutos:]
        contador_pedaco += 1

    return arquivos_exportados

def openai_whisper_transcrever_em_partes(caminho_audio, nome_arquivo, modelo_whisper, openai):
    print("Estou transcrevendo com o Whisper...")

    lista_arquivos_audio = ferramenta_transcrever_audio_em_partes(caminho_audio, nome_arquivo)

    lista_pedacos_de_audio = []

    for um_pedaco_de_audio in lista_arquivos_audio:
        audio = open(um_pedaco_de_audio, "rb")

        resposta = openai.audio.transcriptions.create(
            model = modelo_whisper,
            file = audio
        )

        transcricao = resposta.text
        lista_pedacos_de_audio.append(transcricao)

    transcricao = "".join(lista_pedacos_de_audio)

    with open(f"texto_completo_{nome_arquivo}.txt", "w", encoding="utf-8") as arquivo_texto:
        arquivo_texto.write(transcricao)

    return transcricao

def selecionar_imagem(lista_imagens_geradas):
    return lista_imagens_geradas[int(input("Qual imagem você deseja selecionar? Informe o número do sufixo da imagem gerada: "))]

def ferramenta_converter_png_para_jpg(caminho_imagem_escolhida, nome_arquivo):
    img_png = Image.open(caminho_imagem_escolhida)
    img_png.save(caminho_imagem_escolhida.split(".")[0] + ".jpg")

    return caminho_imagem_escolhida.split(".")[0] + ".jpg"

def main():
    load_dotenv()

    caminho_audio = "podcast/podcast-mc-full.mp3"
    nome_arquivo = "podcast-mc-full"
    url_podcast = ""

    api_key_openai = os.getenv("API_KEY_OPENAI")
    openai.api_key = api_key_openai

    modelo_whisper = "whisper-1"

    resolucao = "1024x1024"

    qtd_imagens = 4

    # transcricao_completa = openai_whisper_transcrever_em_partes(caminho_audio, nome_arquivo, modelo_whisper, openai)
    transcricao_completa = ferramenta_ler_arquivo("texto_completo_podcast-mc-full.txt")

    # resumo_instagram = openai_gpt_resumir_texto(str(transcricao_completa), nome_arquivo, openai)
    resumo_instagram  = ferramenta_ler_arquivo("resumo_instagram_podcast-mc-full.txt")

    # hashtags = openai_gpt_criar_hashtag(resumo_instagram, nome_arquivo, openai)
    hashtags = ferramenta_ler_arquivo("hashtags_podcast-mc-full.txt")

    # resumo_imagem_instagram = openai_gpt_gerar_texto_imagem(resumo_instagram, nome_arquivo, openai)
    resumo_imagem_instagram = ferramenta_ler_arquivo("resumo_instagram_podcast-mc-full.txt")

    imagem_gerada = openai_dalle_gerar_imagem(resolucao, resumo_instagram, nome_arquivo, openai, qtd_imagens)
    lista_imagens_geradas = ferramenta_download_imagem(nome_arquivo, imagem_gerada, qtd_imagens)

    caminho_imagem_escolhida = selecionar_imagem(lista_imagens_geradas)
    caminho_imagem_convertida = ferramenta_converter_png_para_jpg(caminho_imagem_escolhida, nome_arquivo)

if __name__=="__main__":
    main()
