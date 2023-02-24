# 循环右移操作
import struct


def _rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xffffffff


# delta的操作
def delta0(x):
    return _rotr(x, 7) ^ _rotr(x, 18) ^ (x >> 3)


def delta1(x):
    return _rotr(x, 17) ^ _rotr(x, 19) ^ (x >> 10)


# sigma的操作
def sigma0(x):
    return _rotr(x, 2) ^ _rotr(x, 13) ^ _rotr(x, 22)


def sigma1(x):
    return _rotr(x, 6) ^ _rotr(x, 11) ^ _rotr(x, 25)


class hash256:
    def __init__(self, message):
        if not isinstance(message, bytes):
            raise TypeError('Input must be a bytes')
        self.message = message
        self.W = []
        self.blocks = []
        self.hash_values = [
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
            0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        ]
        # 初始化小常数
        self.constants = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
            0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
            0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
            0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
            0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
            0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
            0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
            0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
            0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]

    def pad(self):
        # 计算消息长度，单位为字节
        message_length = len(self.message)
        # 添加填充,直到填充消息取64的余为56为止
        padded_message = self.message + b'\x80'
        while len(padded_message) % 64 != 56:
            padded_message += b'\x00'
        # 添加消息长度
        padded_message += message_length.to_bytes(8, byteorder='big', signed=True)
        # 划分成512位的块
        for i in range(0, len(padded_message), 64):
            block = padded_message[i:i + 64]
            self.blocks.append(block)

    def message_expanding(self):
        for block in self.blocks:
            w = [0] * 64

            for i in range(16):
                w[i] = int.from_bytes(block[i * 4:i * 4 + 4], byteorder='big', signed=True)
            for i in range(16, 64):
                w[i] = (delta1(w[i - 2]) + w[i - 7] + delta0(w[i - 15]) + w[i - 16]) & 0xffffffff
            self.W.append(w)

    def compression(self):
        for block in self.W:
            # 初始化工作变量
            a, b, c, d, e, f, g, h = self.hash_values
            # 循环64次
            for i in range(64):
                # 定义辅助变量和寄存器
                S1 = sigma1(e)
                ch = (e & f) ^ ((~e) & g)
                temp1 = (h + S1 + ch + self.constants[i] + block[i]) & 0xffffffff
                S0 = sigma0(a)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = (S0 + maj) & 0xffffffff
                # 更新寄存器
                h = g
                g = f
                f = e
                e = (d + temp1) & 0xffffffff
                d = c
                c = b
                b = a
                a = (temp1 + temp2) & 0xffffffff
            # 更新hash值
            self.hash_values[0] = (self.hash_values[0] + a) & 0xffffffff
            self.hash_values[1] = (self.hash_values[1] + b) & 0xffffffff
            self.hash_values[2] = (self.hash_values[2] + c) & 0xffffffff
            self.hash_values[3] = (self.hash_values[3] + d) & 0xffffffff
            self.hash_values[4] = (self.hash_values[4] + e) & 0xffffffff
            self.hash_values[5] = (self.hash_values[5] + f) & 0xffffffff
            self.hash_values[6] = (self.hash_values[6] + g) & 0xffffffff
            self.hash_values[7] = (self.hash_values[7] + h) & 0xffffffff

    def get_value(self):
        self.pad()
        self.message_expanding()
        self.compression()
        # 返回摘要
        return b''.join([x.to_bytes(4, byteorder='big') for x in self.hash_values]).hex()


if __name__ == '__main__':
    text = b'123456'
    hash256 = hash256(text)
    print(hash256.get_value())
