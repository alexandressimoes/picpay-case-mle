# Desenvolvimento do Micro Serviço de Model Serving

#### Objetivo
O PicPay possui um serviço de PIX por WhatsApp onde o cliente envia um texto ou áudio para o
assistente de pagamentos do PicPay no WhatsApp solicitando uma operação bancária da seguinte
forma:
Faça um PIX de R$10,00 para o João amanhã
O assistente então interpreta essa mensagem e realiza a operação financeira solicitada.
O objetivo dessa etapa é construir um micro serviço que receba uma mensagem desse tipo e retorne
os dados que serão utilizados para dar continuidade na trasação, ex:
- OPERACAO: PIX
- VALOR: 10,00
- DESTINO: João
- DATA: amanhã

O serviço deve ser construído em Python, containerizado utilizando Docker e executável localmente.