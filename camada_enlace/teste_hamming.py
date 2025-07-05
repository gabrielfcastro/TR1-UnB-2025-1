# Codigo feito por Gabriel Francisco de Oliveira Castro de matricula 202066571
from correcao.hamming import Hamming

# --- Bloco de Teste ---
if __name__ == "__main__":
    detector_hamming = Hamming()
    dados_originais = [1, 0, 1, 1, 0, 1, 0]
    print(f"Dados originais: {dados_originais}")
    
    mensagem_transmitida = detector_hamming.transmitir(dados_originais)
    print(f"Mensagem transmitida: {mensagem_transmitida}")
    
    
    mensagem_com_erro = list(mensagem_transmitida)
    mensagem_com_erro[6] ^= 1 # Erro na posicao 7 (dado)
    
    print("\n--- Teste com Erro ---")
    print(f"Mensagem com erro: {mensagem_com_erro}")
    print(f"Verificação (com erro): {detector_hamming.verificar(mensagem_com_erro)}") # Deve ser False
    
    dados_recuperados = detector_hamming.corrigir(mensagem_com_erro)
    print(f"Dados recuperados: {dados_recuperados}")
    
    assert dados_recuperados == dados_originais
    print("\nSUCESSO! O código foi corrigido e os dados recuperados.")