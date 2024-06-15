from numpy import zeros
from copy import deepcopy
from functools import reduce
from binascii import unhexlify


class AES128():
    def __init__(self, key):
        self.key = key
        self.Key2Matrix()   #转矩阵
        self.Key_extension()    #密钥扩展

    # 转成矩阵
    def Plaintext2Matrix(self):
        self.P_Matrix = zeros((4, 4), dtype=int)
        plain_array = bytes.fromhex(self.plain)
        for x in range(16):
            self.P_Matrix[x % 4][x // 4] = plain_array[x]

        #print(self.P_Matrix)

    def Key2Matrix(self):
        self.K_Matrix = zeros((4, 44), dtype=int)  # 基础+10轮扩展
        key_array = bytes.fromhex(self.key)  # 将密钥转换为 16 字节字节数组
        for x in range(16):
            self.K_Matrix[x % 4][x // 4] = key_array[x]

        #print(self.K_Matrix)

    def Ciphertext2Matrix(self):
        self.C_Matrix = zeros((4, 4), dtype=int)
        for x in range(len(self.cipher) // 2):
            self.C_Matrix[x % 4][x // 4] = int(self.cipher[2 * x:2 * x + 2], 16)

        #print(self.C_Matrix)

    # 密钥扩展
    def Key_extension(self):  # 密钥扩展
        self.sbox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
                     0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
                     0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
                     0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
                     0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
                     0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
                     0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
                     0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
                     0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
                     0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
                     0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
                     0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
                     0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
                     0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
                     0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
                     0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb,
                     0x16, ]
        self.Rconj = [[0x01, 0x00, 0x00, 0x00], [0x02, 0x00, 0x00, 0x00], [0x04, 0x00, 0x00, 0x00],[0x08, 0x00, 0x00, 0x00], [0x10, 0x00, 0x00, 0x00],
                      [0x20, 0x00, 0x00, 0x00], [0x40, 0x00, 0x00, 0x00], [0x80, 0x00, 0x00, 0x00],[0x1B, 0x00, 0x00, 0x00], [0x36, 0x00, 0x00, 0x00]]

        for i in range(4,44):
            if i%4:     # W[i] = W[i-4] xor W[i-1]
                self.K_Matrix[:, i] = self.XOR(self.K_Matrix[:, i-4], self.K_Matrix[:, i-1])
            else:       # W[i] = W[i-4] xor T(W[i-1])
                temp = self.Byte_Cycle(self.K_Matrix[:, i-1], 1, 1)     # 字循环
                #print(temp)
                temp = self.Byte_Substitution(temp,1)   # S盒
                temp = self.XOR(temp, self.Rconj[i//4 -1])   #轮常量替换

                self.K_Matrix[:, i] = self.XOR(self.K_Matrix[:, i-4], temp)

    # 行/列位移 ,√
    def Byte_Cycle(self, cycle_element, direction, t=0):
        if direction:
            return list(map(lambda i:cycle_element[(i+t) % 4], range(4)))
        else:
            return list(map(lambda i: cycle_element[(i - t) % 4], range(4)))

    # 异或，√
    def XOR(self,elementx,elementy):
        return list(map(lambda i:elementx[i]^elementy[i], range(4)))

    # S盒
    def Byte_Substitution(self, Substitution_element, box_id):
        if box_id == 1:
            # print(Substitution_element[1],self.sbox[Substitution_element[1]])
            return list(map(lambda x:self.sbox[Substitution_element[x]], range(4)))
        else:
            return list(map(lambda x:self.invsbox[Substitution_element[x]], range(4)))

    # 加密
    def encrypto(self, plaintext):
        self.plain = plaintext
        self.Plaintext2Matrix()

        self.Column_mixed_matrix = [[0x02, 0x03, 0x01, 0x01],
                                      [0x01, 0x02, 0x03, 0x01],
                                      [0x01, 0x01, 0x02, 0x03],
                                      [0x03, 0x01, 0x01, 0x02]]

        self.Intermediate_Matrix = self.P_Matrix    # 保留明文
        self.AES_encrypto1_9()
        self.AES_encrypto10()

        return self.final_encryptohex()

    # 初始替换+1-9次循环
    def AES_encrypto1_9(self):
        # 初始变换
        self.Round_key_addition(0)
        # print(self.Intermediate_Matrix)

        for i in range(9):
            # 字节替换
            for j in range(4):
                self.Intermediate_Matrix[:, j] = self.Byte_Substitution(self.Intermediate_Matrix[:, j], 1)
            # 行位移
            for k in range(4):
                self.Intermediate_Matrix[k, :] = self.Byte_Cycle(self.Intermediate_Matrix[k, :], 1, k)
            # 列混合
            self.Column_mixing(1)
            # 轮密钥加
            self.Round_key_addition(i + 1)

    # 最后一次循环没有列混合
    def AES_encrypto10(self):
        # 字节替换
        for j in range(4):
            self.Intermediate_Matrix[:, j] = self.Byte_Substitution(self.Intermediate_Matrix[:, j], 1)  # 行位移
        # 行位移
        for k in range(4):
            self.Intermediate_Matrix[k, :] = self.Byte_Cycle(self.Intermediate_Matrix[k, :], 1, k)

        # 轮密钥加
        self.Round_key_addition(10)

    # 解密
    def decrypto(self, ciphertext):
        self.cipher = ciphertext
        self.Ciphertext2Matrix()

        self.invsbox =[0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
                        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
                        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
                        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
                        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
                        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
                        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
                        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
                        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
                        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
                        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
                        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
                        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
                        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
                        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
                        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D]
        self.Inverse_column_mixed_matrix = [[0x0e, 0x0b, 0x0d, 0x09],
                                                  [0x09, 0x0e, 0x0b, 0x0d],
                                                  [0x0d, 0x09, 0x0e, 0x0b],
                                                  [0x0b, 0x0d, 0x09, 0x0e]]

        self.Intermediate_Matrix = self.C_Matrix  # 保留密文
        self.AES_decrypto1_9()
        self.AES_decrypto10()

        return self.final_decryptostr()

    def AES_decrypto1_9(self):
        self.Round_key_addition(10)

        for i in range(9):
            # 行位移
            for k in range(4):
                self.Intermediate_Matrix[k, :] = self.Byte_Cycle(self.Intermediate_Matrix[k, :], 0, k)
            # 字节替换
            for j in range(4):
                self.Intermediate_Matrix[:, j] = self.Byte_Substitution(self.Intermediate_Matrix[:,j], 0)
            # 轮密钥加
            self.Round_key_addition(10 - i - 1)
            # 列混合
            self.Column_mixing(0)


    # 最后一次循环没有列混合
    def AES_decrypto10(self):
        # 行位移
        for k in range(4):
            self.Intermediate_Matrix[k, :] = self.Byte_Cycle(self.Intermediate_Matrix[k, :], 0, k)
        # 字节替换
        for j in range(4):
            self.Intermediate_Matrix[:, j] = self.Byte_Substitution(self.Intermediate_Matrix[:, j], 0)

        # 轮密钥加
        self.Round_key_addition(0)

    #轮密钥加
    def Round_key_addition(self, rounds):
        temp = deepcopy(self.Intermediate_Matrix)
        for i in range(4):
            self.Intermediate_Matrix[:, i] = self.XOR(temp[:,i], self.K_Matrix[:,4*rounds+i])
            # print("temp:",temp[:,i],"K_Matrix:",self.K_Matrix[:,4*rounds+i],"xor=",self.Intermediate_Matrix[:, i])

    # 列混合
    def Column_mixing(self, inverse):
        temp = deepcopy(self.Intermediate_Matrix)

        if inverse:
            for i in range(4):
                for j in range(4):
                    self.Intermediate_Matrix[i][j] = self.Ques_element(temp[:, j], self.Column_mixed_matrix[i])
        else:
            for i in range(4):
                for j in range(4):
                    self.Intermediate_Matrix[i][j] = self.Ques_element(temp[:, j], self.Inverse_column_mixed_matrix[i])

    # 域上乘法
    def Ques_element(self, element0, element1):  # 求下标为（x,y）的单个矩阵元素
        temp = list(map(lambda x, y: self.Multiplication_over_field(x, y), element0, element1))
        return reduce(lambda x, y: x ^ y, temp)

    def Xtime(self, x):   # 为域上乘法提供基础
        if x // 128:
            return ((x * 2) ^ (0x1b)) % 256
        else:
            return (x * 2) % 256

    def Multiplication_over_field(self, x, y):  # 域上乘法
        Xtime_weight = [x]  # 对于x的权的列表并初始化

        result = 0
        for i in range(8):
            Xtime_weight.append(self.Xtime(Xtime_weight[i]))

        for j in range(8):
            if bin(y)[2:].rjust(8, '0')[j] == '1':
                result = result ^ Xtime_weight[7 - j]
        return result

    # 输出
    def final_encryptohex(self):
        result = []

        for i in range(4):  # 第i列连起来
            result.append("".join((list(map(lambda x: hex(x)[2:].rjust(2, '0'), self.Intermediate_Matrix[:, i])))))
        result = "".join(result)

        return result

    def final_decryptostr(self):
        temp = []

        for i in range(4):
            temp.append("".join((list(map(lambda x: hex(x)[2:].rjust(2, '0'), self.Intermediate_Matrix[:, i])))))
        temp = "".join(temp)

        result = unhexlify(temp.encode('utf-8'))
        return result


if __name__ == '__main__':
    #key = '2b7e151628aed2a6abf7158809cf4f3c'
    #plaintext = '3243f6a8885a308d313198a2e0370734'
    key = 'A7F6AFAD026442664786F03AD93C93C9'
    plaintext = '61636C95370B87B0E98914027138C711'

    aes = AES128(key)
    enc = aes.encrypto(plaintext)
    print(enc.encode('utf-8'))
    dec = aes.decrypto(enc)
    dec_hex = ''.join(f'{byte:02X}' for byte in dec)
    print(dec_hex)