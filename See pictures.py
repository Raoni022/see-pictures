from PIL import Image
import numpy as np
import tensorflow as tf

# Carregar o modelo pré-treinado MobileNetV2
modelo = tf.keras.applications.MobileNetV2(weights='imagenet')

def preprocessar_imagem(caminho_imagem, tamanho=(224, 224)):
    """Carrega, redimensiona e pré-processa a imagem para o modelo."""
    try:
        imagem = Image.open(caminho_imagem).convert('RGB')
        imagem = imagem.resize(tamanho)
        imagem_array = np.array(imagem)
        imagem_array = tf.keras.applications.mobilenet_v2.preprocess_input(imagem_array)
        imagem_expandida = np.expand_dims(imagem_array, axis=0)
        return imagem_expandida
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {caminho_imagem}")
        return None
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return None

def analisar_imagem(caminho_imagem, top_n=5):
    """Identifica e analisa a imagem usando o modelo pré-treinado."""
    imagem_pre_processada = preprocessar_imagem(caminho_imagem)

    if imagem_pre_processada is not None:
        # Fazer a previsão
        previsoes = modelo.predict(imagem_pre_processada)

        # Decodificar as previsões para obter rótulos legíveis
        resultados = tf.keras.applications.mobilenet_v2.decode_predictions(previsoes, top=top_n)[0]

        print(f"Análise da imagem: {caminho_imagem}")
        for i, (imagem_net_id, descricao, probabilidade) in enumerate(resultados):
            print(f"{i+1}: {descricao} (Probabilidade: {probabilidade:.2f})")

if __name__ == "__main__":
    caminho_da_imagem = input("Digite o caminho da imagem que deseja analisar: ")
    analisar_imagem(caminho_da_imagem)