from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import os


def generateKeyPair():
    if not os.path.exists('./RSA_key'):
        os.mkdir('./RSA_key')
    # 生成一个新的 RSA 密钥对
    key = RSA.generate(2048)
    # 将私钥导出为 PEM 格式的字符串
    private_key_pem = key.export_key(format="PEM")
    # 将 PEM 格式的私钥写入到文件中
    with open("RSA_key/private_key.pem", "wb") as f:
        f.write(private_key_pem)
    # 从私钥中提取公钥
    public_key = key.publickey()
    public_key_pem = public_key.export_key(format="PEM")
    with open("RSA_key/public_key.pem", "wb") as f:
        f.write(public_key_pem)


# 给根节点签名
def sign(root):
    # 加载随机的公私钥
    generateKeyPair()
    # 加载私钥
    with open('RSA_key/private_key.pem', 'rb') as f:
        private_key = RSA.import_key(f.read())
    # 使用私钥对哈希值进行签名
    root = SHA256.new(root.encode())
    signer = PKCS1_v1_5.new(private_key)
    signature = signer.sign(root)
    return signature


# 验证根节点是否是正确的
def verifySign(root, sign, path):
    # 加载公钥
    with open(path, 'rb') as f:
        public_key = RSA.import_key(f.read())
    # 使用公钥验证签名
    verifier = PKCS1_v1_5.new(public_key)
    root = SHA256.new(root.encode())
    if verifier.verify(root, sign):
        print("签名验证成功，可以开始比对.")
    else:
        print("签名验证失败!!!")
    return verifier.verify(root, sign)
