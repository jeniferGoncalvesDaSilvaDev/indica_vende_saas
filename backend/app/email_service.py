
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional

def send_welcome_email(user_email: str, user_name: str) -> bool:
    """
    Envia email de boas-vindas para novo usuário
    """
    try:
        # Configurações do servidor SMTP (usando variáveis de ambiente)
        smtp_server = os.getenv("SMTP_SERVER", "smtp.smtp2go.com")
        smtp_port = int(os.getenv("SMTP_PORT", "2525"))
        sender_email = os.getenv("SENDER_EMAIL", "noreply@indicavende.com")
        sender_password = os.getenv("SENDER_PASSWORD", "kjcd5588J#")
        
        # Se não houver configuração de email, não envia (modo desenvolvimento)
        if not sender_email or not sender_password:
            print(f"⚠️ Email não configurado. Email que seria enviado para: {user_email}")
            return True
        
        # Criar mensagem
        message = MIMEMultipart("alternative")
        message["Subject"] = "Parabéns! Você criou uma conta na IndicaVende"
        message["From"] = sender_email
        message["To"] = user_email
        
        # Corpo do email em HTML
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                        <h1 style="color: white; margin: 0;">🚀 IndicaVende</h1>
                    </div>
                    
                    <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
                        <h2 style="color: #667eea;">Parabéns, {user_name}!</h2>
                        
                        <p>Você criou uma conta na plataforma <strong>IndicaVende</strong>! 🎉</p>
                        
                        <p>Estamos muito felizes em ter você conosco. Agora você pode:</p>
                        
                        <ul style="background: white; padding: 20px; border-left: 4px solid #667eea; border-radius: 5px;">
                            <li>✅ Gerenciar seus leads de forma eficiente</li>
                            <li>✅ Acompanhar suas vendas em tempo real</li>
                            <li>✅ Aumentar sua produtividade com nosso dashboard</li>
                        </ul>
                        
                        <p>Acesse agora mesmo e comece a transformar suas indicações em resultados!</p>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="https://indicavende.replit.app" 
                               style="background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                                Acessar Plataforma
                            </a>
                        </div>
                        
                        <p style="color: #666; font-size: 14px; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 20px;">
                            Se você tiver alguma dúvida, estamos aqui para ajudar!<br>
                            Equipe IndicaVende
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Versão em texto simples (fallback)
        text_content = f"""
        Parabéns, {user_name}!
        
        Você criou uma conta na plataforma IndicaVende! 🎉
        
        Estamos muito felizes em ter você conosco. Agora você pode:
        
        ✅ Gerenciar seus leads de forma eficiente
        ✅ Acompanhar suas vendas em tempo real
        ✅ Aumentar sua produtividade com nosso dashboard
        
        Acesse agora mesmo e comece a transformar suas indicações em resultados!
        
        Equipe IndicaVende
        """
        
        # Adicionar partes do email
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Enviar email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        print(f"✅ Email de boas-vindas enviado para: {user_email}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar email: {str(e)}")
        return False
