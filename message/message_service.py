import smtplib
from email.mime.text import MIMEText
from email.header import Header

from message.api import MessageService

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


sender = '1219960386@qq.com'
authCode = 'lepsilgnjwbibabj'


class MessageServiceHandler:
    def sendMobileMessage(self, mobile, message):
        print("sendMobileMessage, mobile:" +mobile+", message: "+message)
        return True

    def sendEmailMessage(self, email, message):
        print("sendEmailMessage, email:" +email+", message: " +message)
        messageObj = MIMEText(message, "plain", 'utf-8')
        messageObj['From'] = sender
        messageObj['to'] = email
        messageObj['Subject'] = Header("Hello World")
        try:
            smtpObj = smtplib.SMTP('smtp.qq.com')
            smtpObj.login(sender, authCode)
            smtpObj.sendmail(sender, [email], messageObj.as_string())
        except smtplib.SMTPException as e:
            print(f'send mail fail: {e}')
        else:
            print('send mail success')
        return True


if __name__ == '__main__':
    handler = MessageServiceHandler()
    processor = MessageService.Processor(handler)
    transport = TSocket.TServerSocket('localhost', '9090')
    tfactory = TTransport.TFramedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    print('Python thrift server start!')
    server.serve()
    print('Python thrift server exit')
